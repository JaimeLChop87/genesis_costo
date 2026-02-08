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
                    "INSERT INTO tipocosto (cod_tipo_costo, descripcion_tipo_costo) VALUES (?, ?)",
                    (cod.upper().strip(), descripcion.upper().strip())
                )
                conn.commit()
                return True, "Registro guardado exitosamente."
        except sqlite3.IntegrityError:
            return False, "El código o la descripción ya existen."
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

    def obtener_tipocosto(self):
        """Consulta todos los registros para llenar la tabla."""
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id_tipo_costo, cod_tipo_costo, descripcion_tipo_costo FROM tipocosto ORDER BY id_tipo_costo DESC")
                return cursor.fetchall()
        except Exception:
            return []
    
    def actualizar_tipo_costo(self, id_registro, nuevo_cod, nueva_desc):
        """Actualiza un registro validando restricciones UNIQUE."""
        try:
            with self.db_manager.get_connection() as conn:
                conn.execute('''
                    UPDATE tipocosto 
                    SET cod_tipo_costo = ?, descripcion_tipo_costo = ?
                    WHERE id_tipo_costo = ?
                ''', (nuevo_cod.upper(), nueva_desc.upper(), id_registro))
                conn.commit()
                return True, "Registro actualizado correctamente."
        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                return False, "Error: El código o la descripción ya existen en otro registro."
            return False, f"Error de integridad: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

