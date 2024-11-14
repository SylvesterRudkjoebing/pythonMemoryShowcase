import sqlite3
import pandas as pd

class MemoryDB:
    def __init__(self, db_filename="memoryDB.db"):
        """
        Connects to a SQLite database file.
        If the database doesn't exist, it will be created.
        
        :param db_filename: Name of the SQLite database file (default is 'MemoryDB.db')
        """
        self.db_filename = db_filename
        self.conn = sqlite3.connect(self.db_filename)  # Connect to the SQLite database file
        print(f"Connected to SQLite database '{self.db_filename}'.")

    def load_csv(self, file_path):
        """
        Loads a CSV file into a Pandas DataFrame.
        
        :param file_path: Path to the CSV file
        :return: Pandas DataFrame
        """
        return pd.read_csv(file_path)

    def insert_dataframe(self, df, table_name, if_exists='replace'):
        """
        Inserts a DataFrame into a SQLite table.
        
        :param df: DataFrame to insert
        :param table_name: Name of the target table in SQLite
        :param if_exists: Behavior when the table exists ('fail', 'replace', 'append')
        """
        df.to_sql(table_name, self.conn, if_exists=if_exists, index=False)
        print(f"Data inserted into table '{table_name}' successfully.")

    def table_exists(self, table_name):
        """
        Checks if a table exists in the SQLite database.
        
        :param table_name: The name of the table to check
        :return: True if the table exists, False otherwise
        """
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        result = self.conn.execute(query).fetchone()
        return result is not None

    def seedMemories(self):
        """
        Loads data from specified CSV files and inserts them as tables
        in the SQLite database, only if the table does not already exist.
        """
        file_paths = ['data/small/events.csv', 'data/small/people.csv', 'data/small/participations.csv']

        for file_path in file_paths:
            # Extract the base name (e.g., 'events', 'people', or 'participations') without the path or file extension
            table_name = file_path.split('/')[-1].replace('.csv', '')

            # Check if the table already exists in the database
            if not self.table_exists(table_name):
                print(f"Table '{table_name}' does not exist. Inserting data...")
                # Load CSV into DataFrame and insert into the SQLite table
                df = self.load_csv(file_path)
                self.insert_dataframe(df, table_name)
            else:
                print(f"Table '{table_name}' already exists. Skipping data insertion.")

        print("Seeding completed.")

    def query(self, query):
        """
        Executes a SQL query and returns the results as a DataFrame.
        
        :param query: SQL query string
        :return: DataFrame containing query results
        """
        return pd.read_sql(query, self.conn)

    def close(self):
        """Closes the connection to the SQLite database."""
        self.conn.close()
        print(f"Connection to '{self.db_filename}' closed.")
