import sqlite3
from typing import List, Dict, Any, Optional

class ORM:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    # Database/Table Management
    def create_table(self, table_name: str, schema: str) -> None:
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
        self.conn.commit()

    def drop_table(self, table_name: str) -> None:
        self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()

    # Schema Management
    def add_column(self, table_name: str, column_name: str, data_type: str) -> None:
        self.cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type}")
        self.conn.commit()

    def remove_column(self, table_name: str, column_name: str) -> None:
        self.cur.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in self.cur.fetchall() if col[1] != column_name]
        
        temp_table = f"{table_name}_new"
        self.cur.execute(f"CREATE TABLE {temp_table} AS SELECT {', '.join(columns)} FROM {table_name}")
        
        self.drop_table(table_name)
        self.cur.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
        self.conn.commit()

    def change_column_type(self, table_name: str, column_name: str, new_type: str) -> None:
        self.cur.execute(f"PRAGMA table_info({table_name})")
        cols = self.cur.fetchall()
        new_cols = [f"{col[1]} {new_type}" if col[1] == column_name else f"{col[1]} {col[2]}" for col in cols]
        
        temp_table = f"{table_name}_new"
        self.create_table(temp_table, ", ".join(new_cols))
        self.cur.execute(f"INSERT INTO {temp_table} SELECT * FROM {table_name}")
        self.drop_table(table_name)
        self.cur.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
        self.conn.commit()

    def close(self) -> None:
        self.cur.close()
        self.conn.close()

