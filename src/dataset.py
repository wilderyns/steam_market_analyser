import pandas
import zipfile, io, os
from .features import Features
def load_dataset(file_path: str):
    try:
        csv = pandas.read_csv(file_path)
        print(f"Dataset loaded successfully with {len(csv)} records and {len(csv.columns)} columns.")
        return csv
    except Exception as e:
        return e

def export_results(dataframe, file_path: str):
    try:
        dataframe.to_csv(file_path, index=False)
        print(f"Results exported successfully to {file_path}")
    except Exception as e:
        print(f"Error exporting results: {e}")

def fetch_dataset(features: Features):
    if not features.has_requests:
        return
    else:
        import requests

        # Download from curl -L -o ~/Downloads/steam-games-dataset.zip\
        # https://www.kaggle.com/api/v1/datasets/download/fronkongames/steam-games-dataset with curl
        # Download to data/downloads and then unzip to data/steam_market_data.csv
        url = "https://www.kaggle.com/api/v1/datasets/download/fronkongames/steam-games-dataset"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    z.extractall("data/")
                
                os.remove("data/games.json")
                os.rename("data/games.csv", "data/steam_market_data.csv")
                
                print("Dataset fetched and extracted successfully.")
            else:
                print(f"Failed to fetch dataset. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching dataset: {e}")
    pass

