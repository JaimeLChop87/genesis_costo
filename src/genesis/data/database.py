import sqlite3
import os

class DatabaseMaestro:
    def __init__(self):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
        self.db_dir = os.path.join(project_root, "BBDD")
        self.db_path = os.path.join(self.db_dir, "maestro.db")
        os.makedirs(self.db_dir, exist_ok=True)
        self.create_table_user()
        
    def get_connection(self):
        """Retorna una conexión configurada."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Error crítico al conectar con la base de datos: {e}")
            return None

    def create_table_user(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    rol TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            
database = DatabaseMaestro()
