# src/manage_db.py

import sqlite3
from datetime import datetime

class database:
    def __init__(self, database_name="screen_time.db") -> None:
        """
        Initializes the Database class and creates a connection to the SQLite database.

        Args:
            database_name (str): The name of the database file. Defaults to "screen_time.db".

        This constructor also creates a table for the current date if it doesn't already exist.
        """
        self.database_name = database_name
        self.table_name = datetime.today().strftime("%Y-%m-%d")
        self.create_connection()
        self.create_table()

    def create_connection(self):
        """
        Create a database connection.

        Raises:
            Exception: If there is an error connecting to the database.
        """
        try:
            self.con = sqlite3.connect(self.database_name)
            self.cur = self.con.cursor()
        except sqlite3.Error as e:
            raise Exception(f"Error connecting to database: {e}")

    def create_table(self):
        """
        Create a table for the current date if it doesn't exist.

        Raises:
            Exception: If there is an error creating the table.
        """
        try:
            self.cur.execute(f"""
                CREATE TABLE IF NOT EXISTS "{self.table_name}" (
                    name TEXT NOT NULL,
                    time INTEGER NOT NULL
                )
            """)
        except sqlite3.Error as e:
            raise Exception(f"Error creating table: {e}")

    def check_if_day_change(self):
        """
        Check if the day has changed and create a new table if necessary.

        This method updates the table name to the current date and creates a new table 
        for the current date if it has changed since the last check.
        """
        current_date = datetime.today().strftime("%Y-%m-%d")
        if current_date != self.table_name:
            self.table_name = current_date
            self.create_table()

    def update_table(self, name: str):
        """
        Update the time for a given name or insert a new record.

        Args:
            name (str): The name of the user or application to update.

        This method checks if the day has changed, then updates the time for the specified 
        name if it exists, or inserts a new record with a time of 1 if it does not.
        """
        self.check_if_day_change()
        try:
            self.cur.execute(f"SELECT time FROM \"{self.table_name}\" WHERE name = ?", (name,))
            row = self.cur.fetchone()

            if row:
                new_time = row[0] + 1
                self.cur.execute(f"UPDATE \"{self.table_name}\" SET time = ? WHERE name = ?", (new_time, name))
            else:
                self.cur.execute(f"INSERT INTO \"{self.table_name}\" (name, time) VALUES (?, ?)", (name, 1))

            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error updating table: {e}")
            self.con.rollback()

    def return_data(self) -> dict:
        """
        Return all data from the current table.

        Returns:
            dict: A dictionary containing the names and their corresponding screen time 
            for the current date.

        Raises:
            Exception: If there is an error retrieving data from the database.
        """
        output = {}
        try:
            tables = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            for table in tables:
                results = self.cur.execute(f"SELECT name, time FROM \"{table[0]}\"").fetchall()
                output[table[0]] = {name: time for name, time in results}
        except sqlite3.Error as e:
            raise Exception(f"Error retrieving data: {e}")
        return output

    def __del__(self):
        """
        Close the database connection.

        This method ensures that the database connection is properly closed when the 
        Database object is deleted.
        
        Raises:
            Exception: If there is an error closing the database connection.
        """
        try:
            if self.cur:
                self.cur.close()
            if self.con:
                self.con.close()
        except sqlite3.Error as e:
            raise Exception(f"Error closing database connection: {e}")
