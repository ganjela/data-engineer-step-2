import requests

def extract_opensea_collections(api_key, chain = "ethereum"):
    url = "https://api.opensea.io/api/v2/collections"
    params = {"chain": chain}

    headers = {
        "Accept": "application/json",
        "X-API-KEY": api_key
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


