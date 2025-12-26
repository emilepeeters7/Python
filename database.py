import sqlite3
import os
import configuration


class Database:
    def __init__(self):
        os.makedirs(os.path.dirname(configuration.DATABASE_PATH), exist_ok=True)

        self.conn = sqlite3.connect(configuration.DATABASE_PATH)
        self.cursor = self.conn.cursor()

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
        dummy_brommers = [
            ("Piaggio", "Vespa Primavera", "2021-03-15", 2800.00, "VIN0001"),
            ("Yamaha", "Aerox", "2020-07-10", 2500.50, "VIN0002"),
            ("Honda", "PCX125", "2019-05-22", 2700.75, "VIN0003"),
            ("KTM", "Duke 125", "2022-01-18", 3200.00, "VIN0004"),
        ]
        
        for merk, model, productiedatum, prijs, vinnummer in dummy_brommers:
            try:
                self.cursor.execute(
                    "INSERT INTO brommers (merk, model, productiedatum, prijs, vinnummer) VALUES (?, ?, ?, ?, ?)",
                    (merk, model, productiedatum, prijs, vinnummer)
                )
            except sqlite3.IntegrityError:
                # Als het VIN al bestaat, sla over
                continue
            
        self.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = Database()
    print("Database and tables are created")
