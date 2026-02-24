from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt

from genesis.ui.modules.maestro_crisol.maestro_controller import TipoCostoController


class GenericEditDialog(QDialog):
    def __init__(self, parent=None, title="Editar Registro", fields=None):
        """
        :param fields: Diccionario con la estructura {'nombre_campo': 'valor_actual'}
        """
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedWidth(380)
        self.setObjectName("EditDialog")
        self.inputs = {}
        self.init_ui_dialogs(fields)

    def init_ui_dialogs(self, fields):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Crear dinámicamente los campos según el diccionario recibido
        for label_text, value in fields.items():
            label = QLabel(f"{label_text}:")
            label.setObjectName("LabelForm")
            
            line_edit = QLineEdit(str(value))
            line_edit.setObjectName("InputForm")
            
            self.inputs[label_text] = line_edit
            
            main_layout.addWidget(label)
            main_layout.addWidget(line_edit)

        # Botones
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Actualizar")
        self.btn_save.setObjectName("BtnGuardar")
                
        self.btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_cancel)
        main_layout.addLayout(btn_layout)

        # Conexiones
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.validate_and_accept)
        
    def validate_and_accept(self):
        # Validación básica: que ningún campo esté vacío
        for name, input_field in self.inputs.items():
            if not input_field.text().strip():
                QMessageBox.warning(self, "Error", f"El campo '{name}' es obligatorio.")
                return
        self.accept()

    def get_values(self):
        """Devuelve un diccionario con los nuevos valores ingresados."""
        return {name: input_field.text().strip() for name, input_field in self.inputs.items()}


class EditarPlantillaMaestroDialog(QDialog):
    def __init__(self, parent, cod, desc, nivel_id, tipo_costo_id, opciones_tipo_costo):
            super().__init__(parent)
            self.setWindowTitle("Editar Plantilla Maestro")
            self.setFixedWidth(400)
            self.setObjectName("EditDialog")
            
            # Guardamos los IDs actuales y las opciones
            self.nivel_id_actual = nivel_id
            self.tipo_costo_id_actual = tipo_costo_id
            self.opciones_tipo_costo = opciones_tipo_costo # Lista de tuplas [(id, nombre), ...]

            self.init_ui(cod, desc)

    def init_ui(self, cod, desc):
            layout = QVBoxLayout(self)
            layout.setSpacing(15)
            layout.setContentsMargins(20, 20, 20, 20)

            # --- Campo Código ---
            layout.addWidget(QLabel("Código:", self))
            self.txt_codigo = QLineEdit(str(cod))
            self.txt_codigo.setObjectName("InputForm")
            layout.addWidget(self.txt_codigo)

            # --- Campo Descripción ---
            layout.addWidget(QLabel("Descripción:", self))
            self.txt_descripcion = QLineEdit(str(desc))
            self.txt_descripcion.setObjectName("InputForm")
            layout.addWidget(self.txt_descripcion)

            # --- ComboBox Nivel ---
            layout.addWidget(QLabel("Nivel:", self))
            self.combo_nivel = QComboBox()
            self.combo_nivel.setObjectName("InputForm")
            niveles = [
                ("Nivel - 1", 1), ("Nivel - 2", 2), ("Nivel - 3", 3),
                ("Nivel - 4", 4), ("Nivel - 5", 5)
            ]
            for texto, valor in niveles:
                self.combo_nivel.addItem(texto, valor)
            
            # Posicionar en el nivel actual
            self.combo_nivel.setCurrentIndex(self.combo_nivel.findData(self.nivel_id_actual))
            layout.addWidget(self.combo_nivel)

            # --- ComboBox Tipo Costo ---
            layout.addWidget(QLabel("Tipo Costo:", self))
            self.combo_tipo_costo = QComboBox()
            self.combo_tipo_costo.setObjectName("InputForm")
            
            for id_tc, nombre_tc in self.opciones_tipo_costo:
                self.combo_tipo_costo.addItem(nombre_tc, id_tc)
                
            # Posicionar en el tipo de costo actual
            self.combo_tipo_costo.setCurrentIndex(self.combo_tipo_costo.findData(self.tipo_costo_id_actual))
            layout.addWidget(self.combo_tipo_costo)

            # --- Botones de Acción ---
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(0, 10, 0, 0)

            self.btn_actualizar = QPushButton("Actualizar")
            self.btn_actualizar.setObjectName("BtnGuardar")
            self.btn_actualizar.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_actualizar.clicked.connect(self.validate_and_accept)

            self.btn_cancelar = QPushButton("Cancelar")
            self.btn_cancelar.setObjectName("BtnCancelar") # Si tienes estilo para cancelar
            self.btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_cancelar.clicked.connect(self.reject)

            btn_layout.addWidget(self.btn_actualizar)
            btn_layout.addWidget(self.btn_cancelar)
            layout.addLayout(btn_layout)

    def validate_and_accept(self):
        if not self.txt_codigo.text().strip() or not self.txt_descripcion.text().strip():
            QMessageBox.warning(self, "Campos Requeridos", "Por favor completa el código y la descripción.")
            return
        self.accept()

    def get_datos(self):
        """Retorna los valores finales para el controlador."""
        return {
            "codigo": self.txt_codigo.text().strip().upper(),
            "descripcion": self.txt_descripcion.text().strip().upper(),
            "nivel": self.combo_nivel.currentData(),
            "tipo_costo": self.combo_tipo_costo.currentData()
            }

class EditarEstructuraMeasroPlantilla(QDialog):
    def __init__(self, parent, patron_n1, patron_n2, patron_n3, patron_n4, patron_n5):
            super().__init__(parent)
            self.setWindowTitle("Editar Patron de Estructura Maestro")
            self.setFixedWidth(400)
            self.setObjectName("EditDialog")