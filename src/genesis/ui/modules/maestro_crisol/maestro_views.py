from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, QFrame, QHeaderView,
                             QMessageBox, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication

from genesis.ui.modules.maestro_crisol.maestro_controller import TipoCostoController

class TipoCostoView(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = TipoCostoController()
        self.init_ui()
        self.cargar_datos()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.init_form_card()
        self.init_line_divider()
        self.init_table_registros()
        
        layout.addWidget(self.form_card)
        layout.addWidget(self.linea_divisora)
        layout.addWidget(self.tabla)

    def init_table_registros (self):
        """ Inicializa la tabla de registros."""
                # --- TABLA DE REGISTROS ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setObjectName("TablaRegistros")
        self.tabla.setHorizontalHeaderLabels(["edit","Código","Descripcion Tipo Costo"])
    # --- PERMITIR SELECCIÓN Y COPIADO ---
        # Permite seleccionar celdas individuales o filas completas
        self.tabla.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Selecciona filas completas
        self.tabla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # 2. Política de Foco (CAMBIO CLAVE)
        # Cambia NoFocus por StrongFocus o elimina la línea
        self.tabla.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tabla.setTabKeyNavigation(True)
        
        # configuracion de ancho de columnas específicas
        header = self.tabla.horizontalHeader()
        
        self.tabla.setColumnWidth(0, 50)   
        self.tabla.setColumnWidth(1, 80) 
        self.tabla.setColumnWidth(2, 200) 
        
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        # Estética
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setShowGrid(False)  

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
        # 1. obtener datos del formulario y limpiar espacios
        cod = self.txt_codigo.text().strip()
        desc = self.txt_descripcion.text().strip()
        # 2. validar campos obligatorios
        if not cod or not desc:
            print("Ambos campos son obligatorios.")
            QMessageBox.warning(self, "Campos Requeridos", 
                            "Por favor, complete tanto el código como la descripción.")
            return
        # 3. bloquear botón para evitar múltiples clics
        self.sender().setEnabled(False)
        self.sender().setText("Guardando...")
        
        # 4. guardar en la base de datos a través del controlador
        try:
            exito, mensaje = self.controller.guardar_tipo_costo(cod, desc)
            if exito:
                # Limpiar campos y refrescar tabla
                self.txt_codigo.clear()
                self.txt_descripcion.clear()
                self.cargar_datos()
                QMessageBox.information(self, "Éxito", mensaje)
            else:
                QMessageBox.critical(self, "Error de Validación", mensaje)
                
        except Exception as e:
            # Error técnico no controlado
            QMessageBox.critical(self, "Error del Sistema", f"Ocurrió un error inesperado: {str(e)}")
        
        finally:
            # 5. Siempre rehabilitar el botón al terminar el proceso
            self.sender().setEnabled(True)
            self.sender().setText("Guardar")

    def cargar_datos(self):
        registros = self.controller.obtener_todos()
        self.tabla.setRowCount(len(registros))
        
        for row_idx, ( cod, desc) in enumerate(registros):
            # 1. Item ID (con ceros a la izquierda)
            #item_id = QTableWidgetItem(str(id_db).zfill(4))
            #item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 2. Item Descripción (Mayúsculas para mantener el estilo de la imagen)
            item_desc = QTableWidgetItem(desc.upper())
            
            # 3. Item Id Custom (Código + Icono)
            item_custom = QTableWidgetItem(cod.upper())
            item_custom.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # icono herramienta edisión (solo visual, sin funcionalidad en esta etapa)
            icono_custom = QPushButton("⚙️")
            icono_custom.setCursor(Qt.CursorShape.PointingHandCursor)
            icono_custom.setToolTip("Editar este registro")
            icono_custom.setStyleSheet("background: transparent; border: none; font-size: 14px;")
            
            icono_custom.clicked.connect(lambda checked, c=cod, d=desc: self.abrir_editor( c, d))
            # Asignar a la tabla
            # self.tabla.setItem(row_idx, 0, item_id)
            self.tabla.setItem(row_idx, 2, item_desc)
            self.tabla.setItem(row_idx, 1, item_custom)
            self.tabla.setCellWidget(row_idx, 0, icono_custom)

    def keyPressEvent(self, event):
        """Captura el evento de presionar teclas (Ctrl+C)."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_C:
            self.copiar_al_portapapeles()
        else:
            super().keyPressEvent(event)

    def copiar_al_portapapeles(self):
        """Copia las filas seleccionadas al portapapeles en formato texto."""
        seleccion = self.tabla.selectedItems()
        if not seleccion:
            return

        # Agrupamos por filas para mantener el formato de tabla
        filas_datos = {}
        for item in seleccion:
            row = item.row()
            col = item.column()
            if row not in filas_datos:
                filas_datos[row] = {}
            filas_datos[row][col] = item.text()

        # Construimos el string final (separado por tabulaciones para Excel/Sheets)
        lineas = []
        for r in sorted(filas_datos.keys()):
            # Solo tomamos columnas 1 y 2 (Código y Descripción), ignoramos el botón de la col 0
            columnas = [filas_datos[r].get(c, "") for c in range(1, 3)]
            lineas.append("\t".join(columnas))

        texto_final = "\n".join(lineas)
        
        # Enviamos al portapapeles del sistema
        QGuiApplication.clipboard().setText(texto_final)

    def abrir_editor(self, cod_actual, desc_actual):
        """Abre un diálogo para editar código y descripción."""
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Editar Tipo de Costo")
        dialogo.setFixedWidth(350)
        
        layout_edit = QVBoxLayout(dialogo)
        layout_edit.setSpacing(10)

        # Campos de entrada
        lbl_cod = QLabel("Código:")
        input_cod = QLineEdit(cod_actual)
        input_cod.setMaxLength(4)
        input_cod.setObjectName("InputForm")
        
        lbl_desc = QLabel("Descripción:")
        input_desc = QLineEdit(desc_actual)
        input_desc.setMaxLength(40)
        input_desc.setObjectName("InputForm")

        # Botones de acción
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("Actualizar")
        btn_guardar.setObjectName("BtnGuardar")
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        # Para que herede tus estilos
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setCursor(Qt.CursorShape.PointingHandCursor)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)

        layout_edit.addWidget(lbl_cod)
        layout_edit.addWidget(input_cod)
        layout_edit.addWidget(lbl_desc)
        layout_edit.addWidget(input_desc)
        layout_edit.addLayout(btn_layout)

        # Lógica de botones
        btn_cancelar.clicked.connect(dialogo.reject)

        def procesar_actualizacion():
            # Aquí va la lógica para llamar a tu controlador
            nuevo_cod = input_cod.text().strip()
            nueva_desc = input_desc.text().strip()
            
            if nuevo_cod and nueva_desc:
                # Nota: Aquí deberías pasar también el ID si lo tienes disponible
                # exito, mensaje = self.controller.actualizar_tipo_costo(cod_actual, nuevo_cod, nueva_desc)
                print(f"Enviando actualización: {nuevo_cod} - {nueva_desc}")
                dialogo.accept() # Cierra el diálogo con éxito
                self.cargar_datos() # Refresca la tabla
            else:
                QMessageBox.warning(dialogo, "Error", "Los campos no pueden estar vacíos.")

        btn_guardar.clicked.connect(procesar_actualizacion)

        # --- LÍNEA CLAVE QUE FALTABA ---
        dialogo.exec() 