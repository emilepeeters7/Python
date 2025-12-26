import sqlite3
import os
import configuration


class Database:
    def __init__(self):
        # Ensure the folder exists
        os.makedirs(os.path.dirname(configuration.DATABASE_PATH), exist_ok=True)

        # Connect to the database
        self.conn = sqlite3.connect(configuration.DATABASE_PATH)
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.create_tables()

    def execute(self, sql, params=None):
        if params is None:
            return self.cursor.execute(sql)
        else:
            return self.cursor.execute(sql, params)

    def commit(self):
        self.conn.commit()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS brommers (
                id INTEGER PRIMARY KEY,
                merk TEXT NOT NULL,
                model TEXT NOT NULL,
                productiedatum TEXT NOT NULL,
                prijs REAL NOT NULL,
                vinnummer TEXT NOT NULL UNIQUE
            )
        """)
        self.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = Database()
    print("Database and tables are created")
