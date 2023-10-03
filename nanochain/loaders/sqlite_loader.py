import sqlite_utils

class SQLiteLoader:
    def __init__(self, db_path):
        """
        Initialize the SQLiteLoader with a path to the SQLite database.
        
        Args:
        - db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.db = sqlite_utils.Database(db_path)
    
    def get_tables(self):
        """
        Fetch all table names from the SQLite database.
        
        Returns:
        - List of table names.
        """
        return self.db.table_names()
    
    def fetch_table_data(self, table_name, limit=None):
        """
        Fetch data from a specific table.
        
        Args:
        - table_name (str): Name of the table to fetch data from.
        - limit (int, optional): Limit the number of rows fetched. If None, fetch all rows.
        
        Returns:
        - List of dictionaries with table data.
        """
        table = self.db[table_name]
        return list(table.rows_where(limit=limit))
