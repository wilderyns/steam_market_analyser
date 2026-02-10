import io
import os
from pathlib import Path
import zipfile
import csv
from app.models.appstate import AppState
from app.models.dataset_nolib import DatasetNoLib
from app.models.dataset_pandas import DatasetPandas


def init_dataset(state: AppState, console=None):
    if not check_data_on_disk(state.dataset_path):
        state.dataset = None
        state.last_results = None
        return False
    
    if state.features.has_pandas:
        try:
            state.dataset = load_pandas(state.dataset_path)
            state.last_results = state.dataset
            return True
        except Exception:
            state.dataset = None
            state.last_results = None
            return False
    else:
        try:
            state.dataset = load_nolib(state.dataset_path)
            state.last_results = state.dataset
            return True
        except Exception:
            state.dataset = None
            state.last_results = None
            return False
    
def load_pandas(path: Path) -> DatasetPandas:
    import pandas
    dataframe = pandas.read_csv(path)
    return DatasetPandas(dataframe)

def load_nolib(path: Path) -> DatasetNoLib:
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        raise ValueError("Dataset CSV is empty.")
    columns = rows[0]
    data_rows = rows[1:]
    return DatasetNoLib(columns, data_rows)

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
