# importacion de modulos PyQt6

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QStackedWidget, QScrollArea, QTabBar)
from PyQt6.QtCore import Qt, QSize, QEvent
from PyQt6.QtGui import QPixmap, QIcon


class DashboardView(QMainWindow):
    def __init__(self, user_data=None):
        super().__init__()
        # asignar datos usuario
        self.user_data = user_data or {"nombre": "Usuario", "email": "Usuario@nikia.com"}
        # configuracion ventana dashboard
        self.setWindowTitle("Génesis - Dashboard Maestro")
        self.setMinimumSize(1100, 800)
        # Inicializar UI
        self.init_ui()
        # iniciar con sidebar oculto del menu herramienta principal
        self.sidebar.hide()
        # instalar event filter para capturar eventos globales ocultar sidebar
        self.work_space.installEventFilter(self)
        self.central_widget.installEventFilter(self)

    def init_ui(self):
        # Widget Central o Main y Layout Base
        self.central_widget = QWidget()
        self.central_widget.setObjectName("MainDashboard")
        self.setCentralWidget(self.central_widget)
        # aplicar estilos icons
        self.setWindowIcon(QIcon("src/genesis/ui/resources/icons/favicon.ico"))
        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.init_header_body()
        self.init_menu_main_tools()
        self.init_work_area()
        
    def init_header_body(self):
        """Inicializa el header logo y tarjeta de usuario, opciones especiales y área de trabajo"""
        # --- 0. HEADER (Logo, Accesos, Usuario) ---
        self.header_frame = QFrame()
        self.header_frame.setObjectName("HeaderFrameDashBoard")
        self.header_frame.setFixedHeight(70)
        header_layout = QHBoxLayout(self.header_frame)
        # 0.1 IZQUIERDO : Logo
        logo = QLabel()
        logo.setPixmap(QPixmap("src/genesis/ui/resources/images/Logo_Nikia_app.png").scaled(
            100, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        # 0.1.1 Accesos Rápidos (Botón Home para volver)
        self.btn_back_main = QPushButton()
        self.btn_back_main.setIcon(QIcon("src/genesis/ui/resources/icons/Main_w.png"))
        self.btn_back_main.setObjectName("BtnQuickAccess")
        self.btn_back_main.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_back_main.setToolTip("volver al inicio")
        # 0.1.2 Tarjeta de Usuario
        self.user_card = QFrame()
        self.user_card.setObjectName("UserCard")
        user_layout = QHBoxLayout(self.user_card)
        # 0.1.2 imagen de avatar tarjeta de usuario
        avatar = QLabel()
        avatar.setFixedSize(40, 40)
        avatar.setObjectName("UserAvatar") # Estilizar como círculo en QSS
        # 0.1.3 información usuario tarjeta
        user_info = QVBoxLayout()
        lbl_name = QLabel(self.user_data["nombre"])
        lbl_name.setObjectName("Userinfocard")
        lbl_email = QLabel(self.user_data["email"])
        lbl_email.setObjectName("Userinfocard")
        user_info.addWidget(lbl_name)
        user_info.addWidget(lbl_email)
        user_info.setSpacing(0)
            # agregar al layout tarjeta usuario
        user_layout.addWidget(avatar)
        user_layout.addLayout(user_info)
            # agregar elementos al header
        header_layout.addWidget(logo)
        header_layout.addSpacing(20)
        header_layout.addWidget(self.btn_back_main)
            #agregar espacio flexible
        header_layout.addStretch()
            # agregar tarjeta usuario al header
        header_layout.addWidget(self.user_card)

    def init_menu_main_tools(self):
        """Inicializa el menú horizontal de herramientas y el área de trabajo"""
        # --- 1. MENÚ HORIZONTAL (Herramientas) ---
        # 1.1 frame menú superior principal
        self.top_menu = QFrame()
        self.top_menu.setObjectName("NavButtonDashboard")
        self.top_menu.setFixedHeight(50)
        top_layout = QHBoxLayout(self.top_menu)
            # empujar los botones a la derecha
        top_layout.addStretch()   
        # 1.2 botones de herramientas principales
            # lista de opciones
        opciones = ["Maestro-Crisol", "Genesis_costo", "Rendimientos", "Gestor Recursos", "Informes", "Revit","Ayuda"]
            # crear botones dinámicamente
        for item in opciones:
            btn = QPushButton(item)
            btn.setObjectName("NavButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, i=item: self.update_sidebar(i))
            top_layout.addWidget(btn)

    def init_sidebar(self):
        """Inicializa el sidebar (menú lateral)"""
        # 1.0 area Sidebar Vertical mosrar menu opciones herramienta seleccionada
        self.sidebar = QFrame()
        self.sidebar.setObjectName("SidebarFrame")
        self.sidebar.setFixedWidth(220)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    def init_work_area(self):
        """Inicializa el área de trabajo con sidebar y espacio de contenido"""
        # --- 2. ÁREA DE TRABAJO (Sidebar + Contenido) ---
        
        self.body_container = QWidget()
        body_layout = QHBoxLayout(self.body_container)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        #2.1 inicializar sidebar
        self.init_sidebar()
        
        
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.tabs_manager = QTabBar()
        self.tabs_manager.setObjectName("ActiveTabsBar")
        self.tabs_manager.setTabsClosable(True) # Habilita el icono de cierre (X)
        self.tabs_manager.setMovable(True)
        
        # Conectar señales
        self.tabs_manager.tabBarClicked.connect(self.handler_switch_window)
        self.tabs_manager.tabCloseRequested.connect(self.handler_close_window)

        # 2.2 Stacked Widget (Donde viven las ventanas)
        self.work_space = QStackedWidget()
        
        self.content_layout.addWidget(self.tabs_manager)
        self.content_layout.addWidget(self.work_space)

        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.content_container, stretch=1)



        # 1.1 Botón Toggle (Colapsar Header)
        self.btn_toggle = QPushButton("▲")
        self.btn_toggle.setObjectName("BtnToggleHeader")
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.setFixedSize(25, 25)
        self.btn_toggle.clicked.connect(self.handler_toggle_header)
        
        
        # Agregar niveles al layout principal
        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addWidget(self.btn_toggle, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.top_menu)
        self.main_layout.addWidget(self.body_container)

    def handler_toggle_header(self):
        """ colapsa o expande el header al clickear el botón """
        if self.header_frame.height() > 0:
            self.header_frame.setFixedHeight(0)
            self.btn_toggle.setText("▼")
        else:
            self.header_frame.setFixedHeight(70)
            self.btn_toggle.setText("▲")

    def update_sidebar(self, tool_name):
        """Limpia, genera botones y MUESTRA el sidebar """
        # 1. Limpiar sidebar actual
        while self.sidebar_layout.count():
                item = self.sidebar_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                
        # 2. Definir opciones (tu lógica actual)
        if tool_name == "Maestro-Crisol":
            opciones = [ "Tipos Costo","Plantilla Maestra","Detalle Estructura", "Actvidad Item","Recusos Insumos","Ayuda Maestro"]
        elif tool_name == "Genesis_costo":
            opciones = ["Modelo ADN Salarial", "Roles Funciones Colaboradores", "Componente Detalle Recurso APU","Recusos Insumos Compuestos APU","Costos Matriz Periodo" ,"Ayuda Genesis Costo"]
        elif tool_name == "Rendimientos":
            opciones = ["Analisis Rendimiento", "Planilla Programacion", "Proyeccion Analisis Predictivo","Comparativos", "Ayuda Rendimientos"]
        elif tool_name == "Gestor Recursos":
            opciones = ["Gestor Recurso Equipos", "Gestor Recursos Insumos", "Gestor Recurso Humano","Comparativos", "Ayuda Logística"]

        else:
            opciones = [] # Si no hay opciones, lo ocultamos

        # 3. Lógica de visibilidad
        if opciones:
            for opt in opciones:
                btn = QPushButton(opt)
                btn.setObjectName("SidebarButton")
                btn.setToolTip(opt)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda checked, name=opt: self.open_new_window(name))
                self.sidebar_layout.addWidget(btn)
            
            self.sidebar.show() # Muestra el sidebar cuando hay contenido
        else:
            self.sidebar.hide() # Lo oculta si se selecciona algo sin submenú

    def open_new_window(self, window_title):
        """Crea la ventana, la añade al stack y la enlista en las pestañas"""
        
        # 1. Verificar si ya está abierta
        for i in range(self.tabs_manager.count()):
            if self.tabs_manager.tabText(i) == window_title:
                self.tabs_manager.setCurrentIndex(i)
                self.work_space.setCurrentIndex(i)
                return

        # 2. Crear el contenido de la ventana
        # Ejemplo: if window_title == "Tipos Costo": new_widget = VentanaCostos()
        new_window_widget = QWidget() 
        layout = QVBoxLayout(new_window_widget)
        layout.addWidget(QLabel(f"Contenido de: {window_title}")) 
        
        # 3. Registrar en el sistema
        idx = self.work_space.addWidget(new_window_widget)
        self.tabs_manager.addTab(window_title)
        
        # 4. Activar
        self.tabs_manager.setCurrentIndex(idx)
        self.work_space.setCurrentIndex(idx)

    def handler_switch_window(self, index):
        """Cambia la ventana visible al clickear la pestaña"""
        self.work_space.setCurrentIndex(index)

    def handler_close_window(self, index):
        """Cierra la ventana y la elimina de la lista"""
        widget = self.work_space.widget(index)
        self.work_space.removeWidget(widget)
        self.tabs_manager.removeTab(index)
        widget.deleteLater()

    def eventFilter(self, obj, event):
        # Detectamos el clic del mouse (MouseButtonPress)
        if event.type() == QEvent.Type.MouseButtonPress:
            # Si el sidebar está visible y el clic NO fue dentro del sidebar
            if self.sidebar.isVisible():
                # Verificamos si el widget clickeado es el sidebar o hijo del sidebar
                if not self.sidebar.geometry().contains(self.mapFromGlobal(event.globalPosition().toPoint())):
                    self.sidebar.hide()
        
        # Continuar con el comportamiento normal del evento
        return super().eventFilter(obj, event)