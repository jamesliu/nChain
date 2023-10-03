import sqlite3
import os

# Determine the path for test.db based on the current file's location
current_file_path = os.path.dirname(os.path.abspath(__file__))
test_db_path = os.path.join(current_file_path, '..', 'tests', 'resources', 'test.db')

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect(test_db_path)
cursor = conn.cursor()

# Create a sample table
cursor.execute('''CREATE TABLE sample(id INTEGER PRIMARY KEY, name TEXT)''')

# Insert sample data
sample_data = [('John',), ('Jane',)]
cursor.executemany('INSERT INTO sample(name) VALUES (?)', sample_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
