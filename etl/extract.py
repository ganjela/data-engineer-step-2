import requests
from typing import Dict, Any

def extract_opensea_collections(api_key: str, chain: str = "ethereum") -> Dict[str, Any]:
    url: str = "https://api.opensea.io/api/v2/collections"
    params: Dict[str, str] = {"chain": chain}

    headers: Dict[str, str] = {
        "Accept": "application/json",
        "X-API-KEY": api_key
    }

    response: requests.Response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")



