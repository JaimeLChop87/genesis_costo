import sqlite3
from genesis.data.database import DatabaseMaestro

class TipoCostoController:
    def __init__(self):
        self.db_manager = DatabaseMaestro()

    def guardar_tipo_costo(self, cod, descripcion):
        """Valida e inserta un nuevo registro."""
        if not cod or not descripcion:
            return False, "Ambos campos son obligatorios."
        
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO tipocosto (cod, descripcion) VALUES (?, ?)",
                    (cod.upper().strip(), descripcion.upper().strip())
                )
                conn.commit()
                return True, "Registro guardado exitosamente."
        except sqlite3.IntegrityError:
            return False, "El código o la descripción ya existen."
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def obtener_todos(self):
        """Consulta todos los registros para llenar la tabla."""
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, cod, descripcion FROM tipocosto ORDER BY id DESC")
                return cursor.fetchall()
        except Exception:
            return []