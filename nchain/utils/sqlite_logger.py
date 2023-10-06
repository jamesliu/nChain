import logging
import sqlite3
import json
from nchain import user_dir

def logs_db_path():
    return user_dir() / "logs.db"

def _human_readable_size(size: int) -> str:
    """Convert a size in bytes to a human-readable format."""
    # Define the units and their respective byte sizes
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    unit_index = 0

    # Loop to find the appropriate unit for the size
    while size > 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    # Format the size to 2 decimal places and append the unit
    return "{:.2f} {}".format(size, units[unit_index])

def logs_db_size(db_path):
    return _human_readable_size(db_path.stat().st_size)


#logger=setup_logging()

class SQLiteHandler(logging.Handler):
    """Custom logging handler that writes logs to an SQLite database."""
    
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path
        self._initialize_db()
        
    def _initialize_db(self):
        """Ensure the logs table exists in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create logs table if not exists
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            event TEXT NOT NULL,
            message TEXT NOT NULL,
            level TEXT NOT NULL,
            other_data TEXT
        )
        ''')
        
        # Commit and close the connection
        conn.commit()
        conn.close()
        
    def emit(self, record):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Prepare structured log data
        timestamp = record.created
        event = record.name
        message = record.getMessage()
        level = record.levelname
        other_data = json.dumps(record.__dict__)
        
        # Insert log entry into the logs table
        cursor.execute('''
        INSERT INTO logs (timestamp, event, message, level, other_data)
        VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, event, message, level, other_data))
        
        # Commit and close the connection
        conn.commit()
        conn.close()

# The SQLiteHandler now includes the method _initialize_db to ensure the logs table exists in the database.
# You can now use this updated class in your main script to handle logging to the SQLite database.


if __name__ == '__main__':
    # Configure logging to use the SQLiteHandler
    logging.basicConfig(level=logging.INFO)  # Log all events from INFO level and above
    logger = logging.getLogger("nanoLLM")
    logger.addHandler(SQLiteHandler())
    
    # Test the logging configuration
    logger.info("Logging system initialized", extra={"event": "system_init"})
    
    "Logging configuration set up and test log entry created."
    
    # Fetch the latest log entries from the SQLite database
    # Connect to the SQLite database
    conn = sqlite3.connect(str(logs_db_path()))
    cursor = conn.cursor()
    
    # Fetch the last 5 log entries
    cursor.execute('''
    SELECT timestamp, event, message, level, other_data 
    FROM logs 
    ORDER BY id DESC 
    LIMIT 5
    ''')
    log_entries = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    print(json.dumps(log_entries))

def setup_logger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("nanoLLM")
    logger.addHandler(SQLiteHandler(str(logs_db_path())))
    #Avoid propagating the log messages to the root logger to prevent duplicate messages such as console output.
    logger.propagate = False
    return logger
logger = setup_logger()

