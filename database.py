import sqlite3

class Database:
    def __init__(self, db_name="storage_system.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self._initialize_tables()

    def _initialize_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                file_id TEXT PRIMARY KEY,
                file_hash TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                owner TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def authenticate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None

    def add_metadata(self, file_id, file_hash, file_name, file_type, file_size, owner):
        try:
            self.cursor.execute("""
                INSERT INTO metadata (file_id, file_hash, file_name, file_type, file_size, owner)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (file_id, file_hash, file_name, file_type, file_size, owner))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_metadata(self, file_id):
        self.cursor.execute("SELECT * FROM metadata WHERE file_id = ?", (file_id,))
        result = self.cursor.fetchone()
        if result:
            return {
                "file_id": result[0],
                "file_hash": result[1],
                "file_name": result[2],
                "file_type": result[3],
                "file_size": result[4],
                "owner": result[5]
            }
        return None

    def delete_metadata(self, file_id):
        self.cursor.execute("DELETE FROM metadata WHERE file_id = ?", (file_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0
