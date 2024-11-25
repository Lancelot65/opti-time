# src/manage_db.py

import sqlite3
from datetime import datetime

class database:
    def __init__(self, database_name = "screen_time.db") -> None:
        self.con = sqlite3.connect(database_name)
        self.cur = self.con.cursor()
        self.table_name = datetime.today().strftime("%Y-%m-%d")
        
        self.create_table()
         
    def create_table(self):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS \"{self.table_name}\" ( \
                           name TEXT NOT NULL, \
                           time INTEGER NOT NULL \
                           )")
    
    def check_if_day_change(self):
        if datetime.today().strftime("%Y-%m-%d") != self.table_name:
            self.table_name = datetime.today().strftime("%Y-%m-%d")
            self.create_table()
        
    def update_table(self, name : str):
        self.check_if_day_change()
        self.cur.execute(f"SELECT time FROM \"{self.table_name}\" WHERE name = ?", (name,))
        row = self.cur.fetchone()

        if row:
            print(row[0])
            new_time = row[0] + 1
            self.cur.execute(f"UPDATE \"{self.table_name}\" SET time = ? WHERE name = ?", (new_time, name))
        else:
            self.cur.execute(f"INSERT INTO \"{self.table_name}\" (name, time) VALUES (?, ?)", (name, 1))

        self.con.commit()
    
    def return_data(self):
        TABLES = self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        output = {}
        for table in TABLES:
            resultats = self.cur.execute(f"SELECT name, time FROM \"{table[0]}\"").fetchall()
            output[table[0]] = {nom: time for nom, time in resultats}
        return output

    def __del__(self):
        self.cur.close()
        self.con.close()