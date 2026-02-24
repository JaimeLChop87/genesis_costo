import sqlite3
from PyQt6.QtCore import QObject, pyqtSignal
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

class PlantillaMaestroController(TipoCostoController):

    def __init__(self):
        self.db_manager = DatabaseMaestro()
    
    def guardar_plantilla_maestro(self, nom, cod, tipo_costo, nivel):
        """ valida la informacion en formulario inserta nuevo registro"""

        if not cod or not nom or tipo_costo is None or nivel is None:
            return False, "Todos los campos son obligatorios."

        # 2. Validación de límites (evita que el error salte recién en la DB)
        if len(nom) > 100:
            return False, "La descripción es demasiado larga (máx 100)."
        if len(cod) > 5:
            return False, "El código es demasiado largo (máx 5)."
        # 3. Validación de tipos
        try:
            nivel = int(nivel)
            tipo_costo = int(tipo_costo)
        except (ValueError, TypeError):
            return False, "Los valores de nivel y tipo de costo deben ser numéricos."

        try:
            # Usamos el administrador de conexión para asegurar que se cierre
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                query = '''
                    INSERT INTO plantillamaestro (
                        descripcion_plantilla_maestro, 
                        cod_plantilla_maestro, 
                        nivel_jerarquia, 
                        id_tipo_costo
                    ) VALUES (?, ?, ?, ?)
                '''
                cursor.execute(query, (nom.upper(), cod, nivel, tipo_costo))
                conn.commit()
                return True, "Registro guardado exitosamente."

        except sqlite3.IntegrityError as e:
            # Error específico si el código o descripción ya existen (por el UNIQUE)
            return False, "Error de duplicidad: El código o la descripción ya están registrados."
        except Exception as e:
            return False, f"Error en la base de datos: {str(e)}"
    
    def obtener_plantilla_maestro(self):
        """Consulta todos los registros para llenar la tabla muestra plantilla amestro."""
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id_plantilla_maestro, descripcion_plantilla_maestro, cod_plantilla_maestro, nivel_jerarquia, id_tipo_costo FROM plantillamaestro ORDER BY descripcion_plantilla_maestro DESC")
                return cursor.fetchall()
        except Exception:
            return []
    
    def encontrar_nivel_id_db(self, id_db):
        """Consulta el registro equivalente id_db en tabla"""
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT cod_nivel FROM nivelestructuramaestro WHERE id_nivel_estr = ?"
                cursor.execute(query, (id_db,))
                
                resultado = cursor.fetchone() 
                
                # Si encontró algo, devuelve el primer elemento de la tupla, 
                # de lo contrario devuelve un texto por defecto.
                return resultado[0]
                
        except Exception as e:
            print(f"Error consultando nivel: {e}")
            return "Error"     

    def encontrar_iddb_nivel(self, cod_nivel):
        """Consulta el registro equivalente id_db en tabla"""
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT id_nivel_estr FROM nivelestructuramaestro WHERE cod_nivel = ?"
                cursor.execute(query, (cod_nivel,))
                
                resultado = cursor.fetchone() 
                
                # Si encontró algo, devuelve el primer elemento de la tupla, 
                # de lo contrario devuelve un texto por defecto.
                return resultado[0]
                
        except Exception as e:
            print(f"Error consultando nivel: {e}")
            return "Error"

    def encontrar_iddb_t_costo(self, t_costo):
        """Consulta el registro equivalente id_db en tabla"""
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT id_tipo_costo FROM tipocosto WHERE cod_tipo_costo = ?"
                cursor.execute(query, (t_costo,))
                
                resultado = cursor.fetchone() 
                
                # Si encontró algo, devuelve el primer elemento de la tupla, 
                # de lo contrario devuelve un texto por defecto.
                return resultado[0]
                
        except Exception as e:
            print(f"Error consultando nivel: {e}")
            return "Error"  
    
    def encontrar_tipocosto_id_db(self, id_db):
        """Consulta el registro equivalente id_db en tabla"""
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT cod_tipo_costo FROM tipocosto WHERE id_tipo_costo = ?"
                cursor.execute(query, (id_db,))
                
                resultado = cursor.fetchone() 
                
                # Si encontró algo, devuelve el primer elemento de la tupla, 
                # de lo contrario devuelve un texto por defecto.
                return resultado[0]
                
        except Exception as e:
            print(f"Error consultando nivel: {e}")
            return "Error"  

    def actualizar_plantilla_maestro(self, id_registro, nuevo_cod, nueva_desc, nuevo_nivel,nuevo_t_costo):
        """Actualiza un registro validando restricciones UNIQUE tb_plantillamaestro."""
        try:
            with self.db_manager.get_connection() as conn:
                conn.execute('''
                    UPDATE plantillamaestro 
                    SET cod_plantilla_maestro = ?, descripcion_plantilla_maestro = ?, nivel_jerarquia = ?, id_tipo_costo = ?
                    WHERE id_plantilla_maestro = ?
                ''', (nuevo_cod.upper(), nueva_desc.upper(), nuevo_nivel, nuevo_t_costo, id_registro), )
                conn.commit()
                return True, "Registro actualizado correctamente."
        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                return False, "Error: El código o la descripción ya existen en otro registro."
            return False, f"Error de integridad: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"

class EstructuraMaestroController(PlantillaMaestroController):
    
    def __init__(self):
        self.db_manager = DatabaseMaestro()

    def encontrar_nivel_jerarquia_palntilla_maestro(self, name_plantilla):
        """Consulta el registro equivalente id_db en tabla"""
        try:
            with sqlite3.connect(self.db_manager.db_path) as conn:
                cursor = conn.cursor()
                query = "SELECT nivel_jerarquia FROM plantillamaestro WHERE descripcion_plantilla_maestro = ?"
                cursor.execute(query, (name_plantilla,))
                
                resultado = cursor.fetchone() 
                
                # Si encontró algo, devuelve el primer elemento de la tupla, 
                # de lo contrario devuelve un texto por defecto.
                return resultado[0]
                
        except Exception as e:
            print(f"Error consultando nivel: {e}")
            return "Error"
                



class Comunicador(QObject):
    # Definimos la señal que avisa que los Tipos de Costo cambiaron
    tipos_actualizados = pyqtSignal()

# Instancia única para toda la aplicación
comun = Comunicador()