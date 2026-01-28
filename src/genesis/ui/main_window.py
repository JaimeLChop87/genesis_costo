from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QStackedWidget, QDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QMovie, QIcon

from genesis.ui.auth.login_dialog import LoginDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Génesis - Sistema Maestro")
        self.setMinimumSize(1000, 700)
        
        # Widget Central
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        self.setWindowIcon(QIcon("src/genesis/ui/resources/icons/favicon.ico"))
        self.setCentralWidget(self.main_widget)
        self.layout_principal = QVBoxLayout(self.main_widget)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        self.imagen_fondo()

        self.setup_header()
        self.setup_content_area()
        
        
    def imagen_fondo(self):
        return self.main_widget.setStyleSheet("""
        #MainWidget {
        border-image: url("src/genesis/ui/resources/images/ImagenFondoMainWindows(2).png") 0 0 0 0 stretch stretch;
        background-repeat: no-repeat;
        background-position: center;
            }
        """)
        
    def setup_header(self):
        header = QFrame()
        header.setObjectName("HeaderFrame")
        header.setFixedHeight(100)
        layout = QHBoxLayout(header)

        # Logo
        logo = QLabel()
        pixmap = QPixmap("src/genesis/ui/resources/images/Logo_Nikia_app.png")
        logo.setPixmap(pixmap.scaled(120, 50, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(logo)

        layout.addStretch()

        # Menú
        for item in ["Nosotros", "Soluciones", "Productos"]:
            btn = QPushButton(item)
            btn.setObjectName("NavButton")
            layout.addWidget(btn)

        # Botón Acción
        btn_free = QPushButton("Iniciar Sesión")
        btn_free.setObjectName("BtnPremium")
        btn_free.clicked.connect(self.login_user)
        layout.addWidget(btn_free)
        
        self.layout_principal.addWidget(header)

    def setup_content_area(self):
        # QStackedWidget para cambiar entre el video y el login
        self.content_stack = QStackedWidget()
        
        # --- Pantalla de Inicio (Multimedia) ---
        self.promo_widget = QLabel()
        self.promo_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        """
        # Ejemplo: Cargar un GIF de fondo
        self.movie = QMovie("src/genesis/ui/resources/images/presentacion.gif")
        self.promo_widget.setMovie(self.movie)
        self.movie.start()
        """
        
        self.content_stack.addWidget(self.promo_widget)
        self.layout_principal.addWidget(self.content_stack)
        
    def login_user(self):
        # 1. Instanciamos el diálogo pasando 'self' (MainWindow) como padre
        ventana_login = LoginDialog(self)
        
        # 2. Ejecutamos el diálogo. 
        # El código se detiene aquí hasta que el diálogo se cierre.
        resultado = ventana_login.exec()
        
        # 3. Verificamos qué pasó
        if resultado == QDialog.DialogCode.Accepted:
            # Si el usuario puso bien sus datos y se ejecutó self.accept()
            print("El usuario ha iniciado sesión correctamente.")
        else:
            # Si el usuario cerró el diálogo sin loguearse
            print("Login cancelado o fallido.")