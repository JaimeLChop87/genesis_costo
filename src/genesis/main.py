import sys
import os
from PyQt6.QtWidgets import QApplication
from genesis.data.database import DatabaseMaestro
from genesis.ui.main_window import MainWindow


def main():
    
    app = QApplication(sys.argv)
    cargar_estilos(app)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec())
    
def cargar_estilos(app):
    path = "src/genesis/ui/resources/styles.qss"
    if os.path.exists(path):
        with open(path, "r") as f:
            app.setStyleSheet(f.read())

if __name__ == "__main__":
    main()
    
