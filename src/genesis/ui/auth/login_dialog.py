from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout,QMessageBox
from PyQt6.QtCore import Qt

from genesis.data.database import DatabaseMaestro


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_maestro = DatabaseMaestro()
        self.init_ui_login()
        


    def init_ui_login(self):
        # parametros generales venata login
        self.setObjectName("LoginCard")
        self.setWindowTitle("Acceso - Génesis")
        self.setFixedSize(400, 400)        
        
        # frame_Layout principal
        self.layout_login = QVBoxLayout(self)
        self.layout_login.setObjectName("LoginLayout")
        self.layout_login.setContentsMargins(20, 20, 20, 20)
        self.layout_login.setSpacing(10)

        # --- SECCIÓN: USUARIO ---
        self.lbl_user = QLabel("Usuario Email")
        self.lbl_user.setObjectName("LoginLabel")
        
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("ejemplo@Nikia.com")
        self.input_user.setObjectName("LoginInput")

        # --- SECCIÓN: CONTRASEÑA ---
        self.lbl_pass = QLabel("Contraseña")
        self.lbl_pass.setObjectName("LoginLabel")
        
        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("**********")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setObjectName("LoginInput")
        
        # permite hacer entrada con ENTER
        self.input_pass.returnPressed.connect(self.procesar_login)

        # --- BOTONES Y ENLACES ---
        self.btn_acceder = QPushButton("INICIAR SESIÓN")
        self.btn_acceder.setObjectName("BtnAcceder")
        self.btn_acceder.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_acceder.clicked.connect(self.procesar_login) # Conexión funcional

        self.lbl_tiene_cuenta = QLabel("¿No tienes una cuenta? Regístrate")
        self.lbl_tiene_cuenta.setObjectName("LoginLabel")
        self.lbl_tiene_cuenta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_crear_cuenta = QLabel("Crear Cuenta")
        self.lbl_crear_cuenta.setObjectName("NavButton")
        self.lbl_crear_cuenta.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lbl_crear_cuenta.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- AGREGAR AL LAYOUT ---
        self.layout_login.addWidget(self.lbl_user)
        self.layout_login.addWidget(self.input_user)
        self.layout_login.addSpacing(8)
        self.layout_login.addWidget(self.lbl_pass)
        self.layout_login.addWidget(self.input_pass)
        self.layout_login.addSpacing(16)
        self.layout_login.addWidget(self.btn_acceder)
        self.layout_login.addStretch() # Empuja todo hacia arriba
        self.layout_login.addWidget(self.lbl_tiene_cuenta)
        self.layout_login.addWidget(self.lbl_crear_cuenta)



    def procesar_login(self):
        # 0.datos de entrada usuario
        usuario = self.input_user.text()
        password = self.input_pass.text()
        
        # 1. Validacion campos vacios
        if not usuario or not password:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, completa todos los campos.")
            return
        
        # Bloqueo de boton evitar simultaneadad clicks
        self.btn_acceder.setEnabled(False)
        self.btn_acceder.setText("Verificando...")
        
        
        # 2. verificacion credenciales en DB
        try:
            if self.db_maestro.verify_user_credentials(usuario, password):
                print(f"Acceso concedido para {usuario}")
                self.accept()
            else:
                QMessageBox.critical(self, "Error de Acceso", "Usuario o contraseña incorrectos.")
                print("Error de acceso")
                self.input_pass.clear()
                self.input_pass.setFocus()
        finally:
            # Rehabilitar boton
            self.btn_acceder.setEnabled(True)
            self.btn_acceder.setText("INICIAR SESIÓN")