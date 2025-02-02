import json
import os
from typing import Dict, Any, Optional

def save_raw_data(data: Dict[str, Any], file_path: str) -> None:
    """
    Saves the given data to a file at the given path.

    This function ensures that the parent directory of the file path exists, 
    and then writes the data to the file in JSON format.
    """

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4) 

def read_raw_data(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Reads data from a file at the given path and returns it as a dictionary.

    If the file does not exist, this function returns None.
    """

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    with open(file_path, 'r') as f:
        return json.load(f)