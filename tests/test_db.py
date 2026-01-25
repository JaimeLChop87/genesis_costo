import unittest
import os
from src.genesis.data.database import DatabaseMaestro

class TestDatabasePath(unittest.TestCase):
    def test_database_creation(self):
        """ prueba que la base de datos se crea en la ruta esperada """
        db = DatabaseMaestro()
        # Verificacion que el archivo se crea donde esperamos
        self.assertTrue(os.path.exists(db.db_path))
        self.assertIn("BBDD", db.db_path)

if __name__ == "__main__":
    unittest.main()