from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LoginCard")
        self.setWindowTitle("Acceso - Génesis")
        self.setFixedSize(400, 300)
        self.init_ui_login()

    def init_ui_login(self):
        # Layout principal
        self.layout_login = QVBoxLayout(self)
        self.layout_login.setObjectName("LoginLayout")

        # --- SECCIÓN: USUARIO ---
        self.lbl_user = QLabel("Usuario Email")
        self.lbl_user.setObjectName("LoginLabel")
        
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("User")
        self.input_user.setObjectName("LoginInput")

        # --- SECCIÓN: CONTRASEÑA ---
        self.lbl_pass = QLabel("Key Contraseña")
        self.lbl_pass.setObjectName("LoginLabel")
        
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("**********")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setObjectName("LoginInput")

        # --- BOTONES Y ENLACES ---
        self.btn_acceder = QPushButton("Iniciar Sesión")
        self.btn_acceder.setObjectName("BtnAcceder")
        self.btn_acceder.clicked.connect(self.procesar_login) # Conexión funcional

        self.lbl_tiene_cuenta = QLabel("¿No tienes una cuenta?")
        self.lbl_tiene_cuenta.setObjectName("LoginLabel")
        self.lbl_tiene_cuenta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_crear_cuenta = QLabel("Crear Cuenta")
        self.lbl_crear_cuenta.setObjectName("NavButton")
        self.lbl_crear_cuenta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- AGREGAR AL LAYOUT ---
        self.layout_login.addWidget(self.lbl_user)
        self.layout_login.addWidget(self.input_user)
        self.layout_login.addSpacing(4)
        self.layout_login.addWidget(self.lbl_pass)
        self.layout_login.addWidget(self.input_pass)
        self.layout_login.addSpacing(4)
        self.layout_login.addWidget(self.btn_acceder)
        self.layout_login.addSpacing(4)
        #self.layout_login.addStretch() # Empuja todo hacia arriba
        self.layout_login.addWidget(self.lbl_crear_cuenta)
        self.layout_login.addSpacing(4)


    def procesar_login(self):
        # Aquí validas los datos
        usuario = self.input_user.text()
        password = self.input_pass.text()

        if usuario == "admin" and password == "1234":
            print("Credenciales correctas")
            self.accept()  # Cierra el diálogo y devuelve '1'
        else:
            print("Error de acceso")
            self.input_pass.clear()