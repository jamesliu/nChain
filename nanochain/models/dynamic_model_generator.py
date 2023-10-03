import sqlite_utils
from pydantic import BaseModel, create_model
from typing import Type

class DynamicModelGenerator:
    def __init__(self, db_path: str):
        """
        Initialize the DynamicModelGenerator with a path to the SQLite database.

        :param db_path: Path to the SQLite database file.
        """
        self.db = sqlite_utils.Database(db_path)
    
    # TODO: Figure out how to dynamically create a Pydantic model
    def generate_model(self, table_name: str) -> Type[BaseModel]:
        """
        Dynamically generate a Pydantic model based on the structure (schema) of an SQLite table.

        :param table_name: Name of the SQLite table for which the model needs to be generated.
        :return: Dynamically generated Pydantic model class for the specified table.
        """
        table = self.db[table_name]
        columns = {col.name: col.type for col in table.columns}

        # Creating Pydantic fields based on SQLite table columns
        fields = {col: (typ, None) for col, typ in columns.items()}
        
        # FAILED to Dynamically creating the Pydantic model using the fields
        # DynamicModel = create_model(table_name, **fields)

        # Defining and returning model inside a function to ensure a fresh namespace
        # FAILED
        # TODO: Figure out how to dynamically create a Pydantic model
        def create_dynamic_model():
            return create_model(table_name, **fields)
    
        return create_dynamic_model()

