import sqlite3, configparser, os

class Database:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        config_path = os.path.join(base_dir, "settings.ini")
        if not os.path.exists(config_path):
            raise FileNotFoundError("settings.ini niet gevonden. Kopieer settings_example.ini naar settings.ini")

        config = configparser.ConfigParser()
        config.read(config_path)

        if "database" not in config:
            raise KeyError("Sectie [database] ontbreekt in settings.ini")

        db_path = os.path.join(base_dir, config["database"]["path"])

        os.makedirs(os.path.dirname(db_path), exist_ok=True)


        self.conn = sqlite3.connect(db_path)
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
                vinnummer TEXT NOT NULL UNIQUE
            )
        """)
        self.conn.commit()

    def execute(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor
    
    def close(self):
        self.conn.close()