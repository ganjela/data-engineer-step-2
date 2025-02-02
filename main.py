from etl import extract_opensea_collections, transform_collections
from utils import save_raw_data
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

def run_etl_pipeline(api_key: str) -> None:

    raw_data = extract_opensea_collections(api_key, chain="ethereum")

    save_raw_data(raw_data, 'data_lake/ethereum_collections_raw.json')
    
    transformed_data = transform_collections(raw_data)

    print(transformed_data)    

if __name__ == "__main__":
    api_key = os.getenv("OPENSEA_API_KEY")
    run_etl_pipeline(api_key)