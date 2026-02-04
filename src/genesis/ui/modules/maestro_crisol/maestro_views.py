from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, QFrame, QHeaderView)
from PyQt6.QtCore import Qt

from genesis.ui.modules.maestro_crisol.maestro_controller import TipoCostoController

class TipoCostoView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = TipoCostoController()
        self.init_ui()
        self.cargar_datos() # Llenar tabla al iniciar
        
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.init_form_card()
        self.init_line_divider()
        
        
        
        
                # --- TABLA DE REGISTROS ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Id Código", "Tipo Costo", "Acción"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.form_card)
        layout.addWidget(self.linea_divisora)
        layout.addWidget(self.tabla)

        
        
    def init_form_card(self):
        """Inicializa el formulario para agregar tipo costo."""
        # 1.0 --- FORMULARIO - almacenar tipo costo ---
            # 1.1 frame del formulario
        self.form_card = QFrame()
        self.form_card.setObjectName("FormCard") 
        form_layout = QVBoxLayout(self.form_card)
            # 1.2 campos del formulario descripción tipo costo
        self.txt_descripcion_form = QLabel('Descripción tipo costo')
        self.txt_descripcion_form.setObjectName("LabelForm")
        self.txt_descripcion = QLineEdit()
        self.txt_descripcion.setPlaceholderText("Ejemplo: COSTO FIJO")
        self.txt_descripcion.setObjectName("InputForm")
        self.txt_descripcion.setFixedWidth(300)
        self.txt_descripcion.setMaxLength(40)
            # 1.3 campo del formulario código tipo costo
        self.txt_codigo_form = QLabel('Código tipo costo')
        self.txt_codigo_form.setObjectName("LabelForm")
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("CF")
        self.txt_codigo.setObjectName("InputForm")
        self.txt_codigo.setFixedWidth(80)
        self.txt_codigo.setMaxLength(4)
            # 1.4 botón guardar
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setObjectName("BtnGuardar")
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.setFixedWidth(100)
        btn_guardar.clicked.connect(self.handle_guardar)

        form_layout.addWidget(self.txt_descripcion_form)
        form_layout.addWidget(self.txt_descripcion)
        form_layout.addWidget(self.txt_codigo_form)
        form_layout.addWidget(self.txt_codigo)
        form_layout.addWidget(btn_guardar, alignment=Qt.AlignmentFlag.AlignLeft)

    def init_line_divider(self):
        """Crea un divisor de línea horizontal."""
        self.linea_divisora = QFrame()
        self.linea_divisora.setFrameShape(QFrame.Shape.HLine) 
        self.linea_divisora.setFrameShadow(QFrame.Shadow.Sunken) 
        self.linea_divisora.setObjectName("SeparadorHorizontal")


    def handle_guardar(self):
        cod = self.txt_codigo.text()
        desc = self.txt_descripcion.text()
        
        exito, mensaje = self.controller.guardar_tipo_costo(cod, desc)
        if exito:
            self.txt_codigo.clear()
            self.txt_descripcion.clear()
            self.cargar_datos()
        # Aquí podrías disparar un QMessageBox con el mensaje

    def cargar_datos(self):
        registros = self.controller.obtener_todos()
        self.tabla.setRowCount(len(registros))
        for row_idx, (id_db, cod, desc) in enumerate(registros):
            self.tabla.setItem(row_idx, 0, QTableWidgetItem(str(id_db).zfill(4)))
            self.tabla.setItem(row_idx, 1, QTableWidgetItem(desc))
            self.tabla.setItem(row_idx, 2, QTableWidgetItem(f"{cod} ⚙️"))