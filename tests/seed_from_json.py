import json
import sqlite3
import os
import sys

from src.genesis.data.database import DatabaseMaestro


def cargar_desde_json():
    db = DatabaseMaestro()
    raiz_proyecto = "C:\\Users\\jaime\\Nikia\\Aplicativo_escritorio\\app_maestro\\app_maestro"
    # Usamos ruta absoluta para el JSON para evitar errores de terminal
    ruta_json = os.path.join(raiz_proyecto, "tests", "users_seed.json")
    
    try:
        with open(ruta_json, 'r') as f:
            usuarios = json.load(f)
            
        conn = db.get_connection()
        cursor = conn.cursor()
        
        for u in usuarios:
            try:
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, rol)
                    VALUES (?, ?, ?, ?)
                """, (u['username'], u['email'], u['password_hash'], u['rol']))
            except sqlite3.IntegrityError:
                print(f"Aviso: El usuario '{u['username']}' ya existe en la base de datos.")
                
        conn.commit()
        conn.close()
        print("🚀 ¡Carga masiva completada con éxito!")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo JSON en: {ruta_json}")

if __name__ == "__main__":
    cargar_desde_json()