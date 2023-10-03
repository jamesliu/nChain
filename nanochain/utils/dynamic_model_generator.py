from pydantic import BaseModel, create_model
import sqlite_utils

def generate_pydantic_models_from_db(db_path):
    """Generate Pydantic models dynamically based on an SQLite database."""
    db = sqlite_utils.Database(db_path)
    models = {}

    for table_name in db.table_names():
        table = db[table_name]
        columns = table.columns
        fields = {col.name: (col.type, None) for col in columns}
        model = create_model(table_name.capitalize(), **fields)
        models[table_name] = model

    return models
