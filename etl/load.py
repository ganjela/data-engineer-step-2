from etl.orm import ORM
from typing import List, Dict, Any

def load_collections(transformed_data: List[Dict[str, Any]]) -> None:
    orm = ORM('database/opensea.db')
    
    table_name = 'ethereum_collections'
    schema = '''
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collection TEXT,
        name TEXT,
        description TEXT,
        image_url TEXT,
        owner TEXT,
        twitter_username TEXT,
        contracts TEXT,
        owner_collection_count INTEGER
    '''
    
    orm.create_table(table_name, schema)
        
    orm.close()