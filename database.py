import sqlite3, configparser, os

class Database:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("settings.ini")
        db_path = config["database"]["path"]

        # Maak map data/ aan indien nodig
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        # Verbind met database
        self.conn = sqlite3.connect(db_path)

        # Maak tabel aan
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS brommers (
                id INTEGER PRIMARY KEY,
                merk TEXT NOT NULL,
                model TEXT NOT NULL,
                productiedatum TEXT NOT NULL,
                prijs REAL NOT NULL,
                vinnummer TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor
