import sqlite3
import os
import hashlib

class DatabaseMaestro:
    def __init__(self):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # ruta base datos
        project_root = os.path.abspath(os.path.join(current_dir, "..", "..", ".."))
        self.db_dir = os.path.join(project_root, "BBDD")
        self.db_path = os.path.join(self.db_dir, "maestro.db")
        
        # asegurar existencia carpeta BBDD
        os.makedirs(self.db_dir, exist_ok=True)
        
        # crear tabla usuario si no existe
        self.create_table_user()
        self.create_table_tipocosto()
        
    def get_connection(self):
        
        """Retorna una conexión configurada."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Error crítico de DB: {e}")
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
    
    def hash_password(self, password):
        """Genera un hash SHA-256 para la contraseña"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
                      
    def verify_user_credentials(self, username, password_hash):
        """Verifica si las credenciales del usuario son correctas.
        recibe contraseña text plana y la hashea internamente."""
        
               # conexion con la base de datos
        conn = self.get_connection()
        if conn is None:
                return False
            
        try:
            # hash de la contraseña
            password_hash = self.hash_password(password_hash)
            # consulta SQL
            cursor = conn.cursor()
            # consulta parametrizada para evitar SQL injection ?
            query = "SELECT 1 FROM users WHERE username = ? AND password_hash = ?"
            cursor.execute(query, (username.strip(), password_hash))
            # Obtenemos el resultado consultado
            user = cursor.fetchone()
            # Cerramos el cursor
            cursor.close()
            # Retornamos la comparación lógica directamente
            return user is not None

        except Exception as e:
            print(f"Error en la consulta de verificacion: {e}")
            return False
        finally:
            # Nos aseguramos de cerrar la conexión SIEMPRE
            conn.close()

    def register_user(self, username, email, password, rol):
            """Método utilitario para insertar usuarios con la contraseña ya cifrada."""
            try:
                with self.get_connection() as conn:
                    hash_p = self.hash_password(password)
                    conn.execute('''
                        INSERT INTO users (username, email, password_hash, rol)
                        VALUES (?, ?, ?, ?)
                    ''', (username.strip(), email.strip(), hash_p, rol))
                    conn.commit()
                    return True
            except sqlite3.IntegrityError:
                print("El usuario o email ya existe.")
                return False

    def create_table_tipocosto(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tipocosto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion_tipo_costo TEXT NOT NULL UNIQUE CHECK(length(descripcion_tipo_costo) <= 50),
                    cod_tipo_costo TEXT NOT NULL UNIQUE CHECK(length(cod_tipo_costo) <= 4),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')


Pruebadb = DatabaseMaestro()
Pruebadb.register_user("jaime", "admin@nikia.com", "12345", "admin")