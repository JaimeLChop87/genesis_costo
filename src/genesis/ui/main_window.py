from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QStackedWidget, QDialog)

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QMovie, QIcon

from genesis.ui.auth.login_dialog import LoginDialog
from genesis.ui.dashboard.dashboard_view import DashboardView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # configuracion ventana principal
        self.setWindowTitle("Génesis - Sistema Maestro")
        self.setMinimumSize(1000, 700)
        
        # establecer estado sesion
        self.is_logged_in = False
        
        # Inicializar UI
        self.init_ui()
                
    def init_ui(self):
        """ inicializa componentes visuales interfaz grafica """
        # Widget principal
        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        self.setCentralWidget(self.main_widget)
        
        # aplicar estilos icons
        self.setWindowIcon(QIcon("src/genesis/ui/resources/icons/favicon.ico"))
        
        # layaot principal
        self.layout_principal = QVBoxLayout(self.main_widget)
        self.layout_principal.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.setSpacing(0)
        
        # cargar secciones UI               
        self.setup_header()
        self.setup_content_area()             
        self.imagen_fondo()    
     
    def imagen_fondo(self):
        return self.main_widget.setStyleSheet("""
        #MainWidget {
        border-image: url("src/genesis/ui/resources/images/ImagenFondoMainWindows(2).png") 0 0 0 0 stretch stretch;
        background-repeat: no-repeat;
        background-position: center;
            }
        """)
        
    def setup_header(self):
        """ Configura el encabezado con logo y menú de navegación """
        # 0. CONTENEDOR : caja contenedora header
        header = QFrame()
        header.setObjectName("HeaderFrame")
        header.setFixedHeight(80)
            # parametro layout horizontal y margen
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # 1. IZQUIERDO : Logo con escala dinamica
        logo = QLabel()
            # cargar imagen logo
        pixmap = QPixmap("src/genesis/ui/resources/images/Logo_Nikia_app.png")
            # verificar carga correcta
        if not pixmap.isNull():
            logo.setPixmap(pixmap.scaled(120, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(logo)                                                                                                  

        # Espaciador flexible espacio vacio
        layout.addStretch()

        # 2. CENTRO :  Menú inicial navegacion
        self.menu_buttons = []
        opciones_menu = ["Nosotros", "Soluciones", "Productos", "prueba"]
        
        for item in opciones_menu:
            btn = QPushButton(item)
            btn.setObjectName("NavButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            layout.addWidget(btn)
            self.menu_buttons.append(btn)
            
        # Espaciador flexible espacio vacio
        layout.addStretch()

        # 3. DERECHO: Botón Acción iniciar sesión / ingreso
        self.btn_auth = QPushButton("Iniciar Sesión")
        self.btn_auth.setObjectName("BtnPremium")
        self.btn_auth.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_auth.clicked.connect(self.handle_auth_click)
        layout.addWidget(self.btn_auth)
        
        # 4. Agregar header al layout principal
        self.layout_principal.addWidget(header)

    def handle_auth_click(self):
        """Lógica inteligente: si no está logueado, pide login. Si sí, entra a la app."""
        
        if not self.is_logged_in:
            self.show_login_dialog()
        else:
            self.enter_application()

    def show_login_dialog(self):
        dialog = LoginDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.is_logged_in = True
            self.update_ui_post_login()
    
    def update_ui_post_login(self):
        """Cambia visualmente el botón y el estado de la UI"""
        self.btn_auth.setText("Ingresar Aplicación")
        self.btn_auth.setProperty("logged", "true") # Cambia el color vía CSS
        self.btn_auth.style().unpolish(self.btn_auth) # Refresca el estilo
        self.btn_auth.style().polish(self.btn_auth)
        print("UI actualizada: Sesión activa.")

    def enter_application(self):
        print("Cambiando a Dashboard...")
        
        # 1. Crear instancia del Dashboard
        # Pasamos datos (puedes traerlos de tu LoginDialog si los guardas)
        self.dashboard = DashboardView(user_data={
            "nombre": "Jaime", 
            "email": "admin@nikia.com"
        })
        
        # 2. Conectar el botón de regreso (opcional)
        self.dashboard.btn_back_main.clicked.connect(self.regresar_a_inicio)
        
        # 3. Mostrar Dashboard y ocultar esta ventana
        self.dashboard.show()
        self.hide()

    def regresar_a_inicio(self):
        self.dashboard.close()
        self.show()
        
    def setup_content_area(self):
        # QStackedWidget para cambiar entre el video y el login
        self.content_stack = QStackedWidget()
        
        # --- Pantalla de Inicio (Multimedia) ---
        self.promo_widget = QLabel()
        self.promo_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
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