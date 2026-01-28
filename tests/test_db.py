import unittest
import os
from src.genesis.data.database import DatabaseMaestro
import sqlite3
import os

class TestDatabasePath(unittest.TestCase):
    def test_database_creation(self):
        """ prueba que la base de datos se crea en la ruta esperada """
        db = DatabaseMaestro()
        # Verificacion que el archivo se crea donde esperamos
        self.assertTrue(os.path.exists(db.db_path))
        self.assertIn("BBDD", db.db_path)




def consultar_usuarios():
    # Buscamos la ruta de la base de datos (subiendo un nivel desde tests/)
    base_dir = "C:\\Users\\jaime\\Nikia\\Aplicativo_escritorio\\app_maestro\\app_maestro\\BBDD"
    db_path = os.path.join(base_dir,"maestro.db")
    
    if not os.path.exists(db_path):
        print(f"Error: No se encontró el archivo de base de datos en: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Consultamos todos los campos que nos interesan
        cursor.execute("SELECT id, username, email, rol, password_hash FROM users")
        usuarios = cursor.fetchall()
        
        if not usuarios:
            print("La base de datos está conectada pero la tabla 'users' está vacía.")
        else:
            print("\n" + "="*80)
            print(f"{'ID':<4} | {'USUARIO':<15} | {'EMAIL':<20} | {'ROL':<12}")
            print("-" * 80)
            for u in usuarios:
                print(f"{u[0]:<4} | {u[1]:<15} | {u[2]:<20} | {u[3]:<12}")
            print("="*80)
            print(f"Total: {len(usuarios)} usuarios encontrados.\n")

    except sqlite3.Error as e:
        print(f"Error de SQLite: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    consultar_usuarios()    
    