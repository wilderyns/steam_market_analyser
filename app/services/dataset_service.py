import io
import os
from pathlib import Path
import zipfile
import csv 
from app.models.appstate import AppState
from app.models.dataset_nolib import DatasetNoLib
from app.models.dataset_pandas import DatasetPandas

def read_csv(path: Path):
    print(f"Attempting to read CSV at {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        raise ValueError("Dataset CSV is empty.")


    
    # Row 0 has the column header
    columns = rows[0]
    
    #Row 1 onwards are fully of quality data
    data_rows = rows[1:]

    # The dataset I downloaded here is broken, with the Discount and DLC count columns not being seperated, becoming "DiscountDLC Count".
    # Let's identify a mismatch between header and data columns, see if that's the reason for the mismatch, and fix it
    if "DiscountDLC count" in columns and data_rows:
        if len(data_rows[0]) == len(columns) + 1:
            i = columns.index("DiscountDLC count")
            columns = columns[:i] + ["Discount", "DLC count"] + columns[i + 1:]

    return columns, data_rows

def init_dataset(state: AppState, console=None):
    if not check_data_on_disk(state.dataset_path):
        print("Apparently data doesn't exist?")
        state.dataset = None
        state.last_results = None
        return False
    
    if state.features.has_pandas:
        try:
            state.dataset = load_pandas(state.dataset_path)
            state.last_results = state.dataset
            return True
        except Exception as e:
            print(f"Pandas load failed: {e}")

    try:
        state.dataset = load_nolib(state.dataset_path)
        state.last_results = state.dataset
        return True
    except Exception as e:
        print(f"Nolib load failed: {e}")
        state.dataset = None
        state.last_results = None
        return False
    
def load_pandas(path: Path) -> DatasetPandas:
    import pandas
    columns, rows = read_csv(path)
    dataframe = pandas.DataFrame(rows, columns=columns)
    return DatasetPandas(dataframe)

def load_nolib(path: Path) -> DatasetNoLib:
    columns, rows = read_csv(path)
    return DatasetNoLib(columns, rows)

def check_data_on_disk(path: Path):
    return path.exists() and path.is_file()

def attempt_data_download(state: AppState, dest_path=None):
    if not state.features.has_requests:
        raise RuntimeError("Requests library not installed; cannot fetch dataset automatically.")

    if not state.dataset_url:
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
