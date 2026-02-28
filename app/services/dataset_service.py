import io
import os
from pathlib import Path
import zipfile
import csv 
from app.models.appstate import AppState
from app.models.dataset import Dataset
from app.models.dataset_nolib import DatasetNoLib
from app.models.dataset_pandas import DatasetPandas

def read_csv(path: Path):
    """
    Read CSV at specified path and return the column headers and the rows of data
    Implements 2 fixes to the dataset, splitting the Discounts and DLC column names
    And dedupes the dataset - removes multiple Name entries
    
    Args:
        path (Path): The path to the csv file
        
    Returns:
        tuple: (columns[str], data_rows[str]) with column headers and rows of data
    """
    
    print(f"Attempting to read CSV at {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        raise ValueError("Dataset CSV is empty.")

    # Row 0 has the column header
    columns = rows[0]
    
    #Row 1 onwards are fully of data
    data_rows = rows[1:]

    # The dataset I downloaded here is broken, with the Discount and DLC count columns not being seperated, becoming "DiscountDLC Count".
    # Let's identify a mismatch between header and data columns, see if that's the reason for the mismatch, and fix it
    if "DiscountDLC count" in columns and data_rows:
        if len(data_rows[0]) == len(columns) + 1:
            i = columns.index("DiscountDLC count")
            columns = columns[:i] + ["Discount", "DLC count"] + columns[i + 1:]

    # The dataset contains some weird duplicate rows with the same game and all its statistics but different AppIDs. 
    # Let's just remove the duplicates for now.
    # TODO: Handle this properly, maybe prompt the user about what they'd like to do?
    
    if "Name" in columns:
        name_index = columns.index("Name")
        seen_names: set[str] = set()
        deduped_rows: list[list[str]] = []

        for row in data_rows:
            if name_index >= len(row):
                deduped_rows.append(row)
                continue

            game_name = str(row[name_index]).strip()
            if not game_name:
                deduped_rows.append(row)
                continue

            if game_name in seen_names:
                continue

            seen_names.add(game_name)
            deduped_rows.append(row)

        data_rows = deduped_rows

    return columns, data_rows

def init_dataset(state: AppState):
    """
    Check csv at dataset_path exists, then use load_pandas() or load_nolib() as appropriate 
    
    Args:
        state (AppState): Application state, used for dataset_path and to store dataset
        
    Returns:
        bool: True if successful, False otherwise
        
    Exceptions:
        Pandas load failed
        Nolib load failed
    """
    
    if not check_data_on_disk(state.dataset_path):
        print("Apparently data doesn't exist?")
        state.dataset = None
        state.base_dataset = None
        state.last_results = None
        return False
    
    columns, rows = read_csv(state.dataset_path)
    
    if state.features.has_pandas:
        try:
            state.dataset = factory_create_dataset(state, rows, columns, backend="pandas")
            state.base_dataset = state.dataset
            state.last_results = state.dataset
            state.transformations_applied = False
            state.transform_filter_note = None
            state.columns.load_columns(state.dataset.columns())
            return True
        except Exception as e:
            print(f"Pandas load failed: {e}")

    try:
        state.dataset = factory_create_dataset(state, rows, columns, backend="nolib")
        state.base_dataset = state.dataset
        state.columns.load_columns(state.dataset.columns())
        state.last_results = state.dataset
        state.transformations_applied = False
        state.transform_filter_note = None
        return True
    except Exception as e:
        print(f"Nolib load failed: {e}")
        state.dataset = None
        state.base_dataset = None
        state.last_results = None
        return False
    
def factory_create_dataset(
    state: AppState,
    rows: list[list],
    columns: list[str],
    backend: str | None = None,
) -> Dataset:
    """
    Create a dataset instance using the active backend or an explicit override.
    
    Args: 
        state (AppState): app state used to detect optional feature availability
        rows (list[list]): data rows
        columns (list[str]): a list of column headers
        backend (str | None): optional backend override ("pandas" or "nolib")
    
    Returns:
        Dataset: DatasetPandas or DatasetNoLib depending on selected backend

    """
    copied_rows = [list(row) for row in rows]

    selected_backend = backend
    if selected_backend is None:
        selected_backend = "pandas" if state.features.has_pandas else "nolib"

    if selected_backend == "pandas":
        import pandas
        df = pandas.DataFrame(copied_rows, columns=columns)
        return DatasetPandas(df)
    if selected_backend == "nolib":
        return DatasetNoLib(columns, copied_rows)

    raise ValueError(f"Unknown backend: {selected_backend}")
    
def check_data_on_disk(path: Path):
    """
    Simply check a passed path exists
    
    Args:
        path (Path): Dataset path
        
    Returns:
        bool: True if file exists, otherwise false
    """
    return path.exists() and path.is_file()

def attempt_data_download(state: AppState, dest_path=None):
    """
    Download from dataset URL as defined in state.dataset_url, unzip, delete .json copy, move and rename .csv into data directory
    
    Args:
        state (AppSate): Application state used for state.dataset_path, state.dataset_url
        dest_path (str): Override path to save downloaded files
        #TODO: How about a URL override too?
        
    Returns:
        None. #TODO: Make this return success or not
        
    Exceptions:
        #TODO: make a variation using the standard library
        RuntimeError: if requests is not installed 
        RuntimeError: if both state.dataset_url and dest_path arg are unset
        PermissionError: On 401 or 403 of trying to download the dataset
        RuntimeError: On 200 error
        RunetimeError: If zip file extraction fails for whatever reason
        RunetimeError: If csv file can't be found after extraction    
    """
    
    if not state.features.has_requests:
        raise RuntimeError("Requests library not installed; cannot fetch dataset automatically.")

    if not state.dataset_url and dest_path is None:
        raise RuntimeError("Dataset URL unset, cannot fetch the dataset if I don't know where it lives.")
    
    import requests 

    dest = dest_path if dest_path is not None else state.dataset_path

    dest.parent.mkdir(parents=True, exist_ok=True)

    resp = requests.get(state.dataset_url, timeout=60)

    if resp.status_code in (401, 403):
        raise PermissionError(
            f"Kaggle download blocked (HTTP {resp.status_code}). "
        )

    if resp.status_code != 200:
        raise RuntimeError(f"Failed to fetch dataset (HTTP {resp.status_code}).")

    try:
        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            z.extractall(dest.parent)
    except zipfile.BadZipFile as e:
        raise RuntimeError(
            "Download not a zip. Might need to sign in with Kaggle"
        ) from e

    extracted_csv = dest.parent / "games.csv"
    extracted_json = dest.parent / "games.json"

    if extracted_json.exists():
        extracted_json.unlink()

    if not extracted_csv.exists():
        raise RuntimeError("Expected games.csv after extraction but didn't find it.")

    # Move into place
    if dest.exists():
        dest.unlink()
        
    os.rename(str(extracted_csv), str(dest))

def populate_columns(state: AppState, headers: list[str]):
    """
    Populate our available columns of the selected columns model in state
    
    Args:
        state (AppState)
        headers (list[str]): Passes in column headers
        
    Returns:
        None
    """
    state.columns.available_columns = headers
