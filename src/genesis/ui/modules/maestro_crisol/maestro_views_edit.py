from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
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
