import sqlite3
from typing import List, Dict, Any, Optional

class ORM:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    # Table Management
    def create_table(self, table_name: str, schema: str) -> None:
        """
        Creates a new table in the database if it does not exist.
        """

        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
        self.conn.commit()

    def drop_table(self, table_name: str) -> None:
        """
        Drops a table from the database if it exists.
        """

        self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()

    # Schema Management
    def add_column(self, table_name: str, column_name: str, data_type: str) -> None:
        """
        Adds a new column to a table in the database if it does not exist.
        """

        self.cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type}")
        self.conn.commit()

    def remove_column(self, table_name: str, column_name: str) -> None:
        """
        Removes a column from a table in the database if it exists.

        This operation is potentially slow as it involves creating a new table
        and copying all the data over.
        """

        self.cur.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in self.cur.fetchall() if col[1] != column_name]
        
        temp_table = f"{table_name}_new"
        self.cur.execute(f"CREATE TABLE {temp_table} AS SELECT {', '.join(columns)} FROM {table_name}")
        
        self.drop_table(table_name)
        self.cur.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
        self.conn.commit()

    def change_column_type(self, table_name: str, column_name: str, new_type: str) -> None:
        """
        Changes the type of a column in a table in the database.

        This operation is potentially slow as it involves creating a new table
        and copying all the data over.
        """

        self.cur.execute(f"PRAGMA table_info({table_name})")
        cols = self.cur.fetchall()
        new_cols = [f"{col[1]} {new_type}" if col[1] == column_name else f"{col[1]} {col[2]}" for col in cols]
        
        temp_table = f"{table_name}_new"
        self.create_table(temp_table, ", ".join(new_cols))
        self.cur.execute(f"INSERT INTO {temp_table} SELECT * FROM {table_name}")
        self.drop_table(table_name)
        self.cur.execute(f"ALTER TABLE {temp_table} RENAME TO {table_name}")
        self.conn.commit()

    # Data Operations
    def insert(self, table_name: str, data: List[Dict[str, Any]] | Dict[str, Any]) -> None:
        """Insert single or multiple rows."""

        if isinstance(data, dict):
            data = [data]
        
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['?'] * len(data[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        self.cur.executemany(query, [tuple(row.values()) for row in data])
        self.conn.commit()

    def select(
        self,
        table_name: str,
        columns: str = "*",
        where: Optional[str] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
        distinct: bool = False
    ) -> List[Any]:
        """
        Executes a SELECT query against the database.
        """

        query = ["SELECT"]
        if distinct:
            query.append("DISTINCT")
        query.append(f"{columns} FROM {table_name}")
        
        if where:
            query.append(f"WHERE {where}")
        if order_by:
            query.append(f"ORDER BY {order_by}")
        if limit:
            query.append(f"LIMIT {limit}")
            
        self.cur.execute(' '.join(query))
        return self.cur.fetchall()

    def update(self, table_name: str, set_values: str, where: str) -> None:
        """
        Updates records in a specified table based on the given conditions.
        """

        query = f"UPDATE {table_name} SET {set_values} WHERE {where}"
        self.cur.execute(query)
        self.conn.commit()

    def delete(self, table_name: str, where: str) -> None:
        """Deletes records from a specified table based on the given conditions."""

        query = f"DELETE FROM {table_name} WHERE {where}"
        self.cur.execute(query)
        self.conn.commit()

    # Filtering
    def filter(
        self,
        table_name: str,
        conditions: Dict[str, Any],
        operator: str = "AND",
        case_sensitive: bool = True
    ) -> List[Any]:
        """
        Filters records from a specified table based on the given conditions.
        """

        where_clauses = []
        params = []
        
        for col, val in conditions.items():
            if isinstance(val, list):
                placeholders = ', '.join(['?'] * len(val))
                where_clauses.append(f"{col} IN ({placeholders})")
                params.extend(val)
            elif '%' in str(val):
                op = "LIKE" if case_sensitive else "ILIKE"
                where_clauses.append(f"{col} {op} ?")
                params.append(val)
            else:
                where_clauses.append(f"{col} = ?")
                params.append(val)
                
        where = f" {operator} ".join(where_clauses)
        return self.cur.execute(f"SELECT * FROM {table_name} WHERE {where}", params).fetchall()

    def close(self) -> None:
        self.cur.close()
        self.conn.close()