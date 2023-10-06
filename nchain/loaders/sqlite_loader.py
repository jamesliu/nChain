import sqlite_utils
from typing import List, Type
from pydantic import BaseModel
from nchain.models.generic_model import GenericModel

class SQLiteLoader:
    def __init__(self, db_path: str):
        """
        Initialize the SQLiteLoader with a path to the SQLite database.

        :param db_path: Path to the SQLite database file.
        """
        self.db = sqlite_utils.Database(db_path)

    def get_table_names(self) -> List[str]:
        """
        Retrieve the names of all tables in the SQLite database.

        :return: List of table names.
        """
        return self.db.table_names()

    def fetch_all_data(self, table_name: str) -> List[Type[BaseModel]]:
        """
        Fetch all rows of data from the specified table and structure them using a Pydantic model.
        
        :param table_name: Name of the SQLite table from which data needs to be fetched.
        :return: List of Pydantic model instances representing rows of data from the specified table.
        """
        data = self.db[table_name].rows
        return [GenericModel(**row) for row in data]