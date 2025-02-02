import pandas as pd
import json
from typing import Dict, Any

def transform_collections(raw_data: Dict[str, Any]) -> pd.DataFrame:
    
    collections = raw_data.get("collections", [])
    
    if not collections:
        raise ValueError("No collections found in the provided OpenSea data.")

    df = pd.DataFrame(collections)

    df.replace({"": None}, inplace=True)  

    for col in ["collection", "name", "owner"]:
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
    
    required_fields = ["collection", "name", "owner"]

    df.dropna(subset=required_fields, inplace=True)

    df_transformed = df[[
        "collection", 
        "name", 
        "description", 
        "image_url", 
        "owner", 
        "twitter_username", 
        "contracts"
    ]].copy()

    df_transformed["contracts"] = df_transformed["contracts"].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

    owner_counts = df_transformed.groupby("owner").size().reset_index(name="owner_collection_count")

    df_transformed = df_transformed.merge(owner_counts, on="owner", how="left")

    return df_transformed

