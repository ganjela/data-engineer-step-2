from typing import List, Dict, Any, Union
from .orm import ORM
import pandas as pd
import sqlite3
import os

def load_collections(transformed_data: Union[pd.DataFrame, List[Dict[str, Any]]]) -> None:
    """
    Load transformed collection data into the SQLite database.

    This function takes a DataFrame or a list of dictionaries containing
    collection data and stores it into the 'ethereum_collections' table
    in the SQLite database located at 'database/opensea.db'.
    """

    orm = ORM('database/opensea.db')
    table_name = 'ethereum_collections'
    
    
    try:
        schema = '''
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            collection TEXT NOT NULL,
            name TEXT,
            description TEXT,
            image_url TEXT,
            owner TEXT,
            twitter_username TEXT,
            contracts TEXT,
            owner_collection_count INTEGER
        '''
        orm.create_table(table_name, schema)

        if isinstance(transformed_data, pd.DataFrame):
            transformed_data = transformed_data.to_dict(orient='records')
        
        if transformed_data:
            orm.insert(table_name, transformed_data)
            
            inserted = orm.select(table_name, columns="COUNT(*)", where="owner IS NOT NULL")
            print(f"Successfully inserted {inserted[0][0]} records")
            
            try:
                orm.add_column(table_name, "instagram_username", "text")
            except sqlite3.OperationalError:
                pass 
            
            invalid_owners = orm.filter(table_name, 
                conditions={"owner": ["0x%", "null"]},
                operator="OR",
                case_sensitive=False
            )
            if invalid_owners:
                print(f"Warning: Found {len(invalid_owners)} collections with invalid owner addresses")
                
    except sqlite3.Error as e:
        print(f"Database error occurred: {str(e)}")
        orm.conn.rollback()
        
    finally:
        orm.close()

if __name__ == "__main__":
    sample_data = [{
        "collection": "TestCollection",
        "name": "TestItem",
        "description": "Sample collection",
        "image_url": "https://example.com/image.jpg",
        "owner": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "twitter_username": "@testuser",
        "contracts": '["0x1234567890abcdef"]',
        "owner_collection_count": 5
    }]
    
    load_collections(sample_data)