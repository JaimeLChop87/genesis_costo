from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, QFrame, QHeaderView,
                             QMessageBox, QDialog, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication

from genesis.ui.modules.maestro_crisol.maestro_controller import TipoCostoController
from genesis.ui.modules.maestro_crisol.maestro_views_edit import GenericEditDialog

class GeneralWidget():
    def __init__(self):
        self.init_line_divider()
        
    def init_line_divider(self):
        """Crea un divisor de línea horizontal."""
        self.linea_divisora = QFrame()
        self.linea_divisora.setFrameShape(QFrame.Shape.HLine) 
        self.linea_divisora.setFrameShadow(QFrame.Shadow.Sunken) 
        self.linea_divisora.setObjectName("SeparadorHorizontal")   

class TipoCostoView(QWidget, GeneralWidget):
    def __init__(self):
        super().__init__()
        self.controller = TipoCostoController()
        self.init_ui_tipocosto()
        self.cargar_datos()

    def init_ui_tipocosto(self):
        layout = QVBoxLayout(self)
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
        self.tabla.setColumnWidth(2, 300) 
        
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
        registros = self.controller.obtener_tipocosto()
        self.tabla.setRowCount(len(registros))
        
        for row_idx, ( id_db, cod, desc) in enumerate(registros):            
            # 1. Item Descripción (Mayúsculas para mantener el estilo de la imagen)
            item_desc = QTableWidgetItem(desc.upper())
            # 2. Item Id Custom (Código + Icono)
            item_custom = QTableWidgetItem(cod.upper())
            item_custom.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 3. icono herramienta edisión
            icono_custom = QPushButton("⚙️")
            icono_custom.setCursor(Qt.CursorShape.PointingHandCursor)
            icono_custom.setToolTip("Editar este registro")
            icono_custom.setStyleSheet("background: transparent; border: none; font-size: 14px;")
            icono_custom.clicked.connect(lambda checked, i=id_db, c=cod, d=desc: self.abrir_editor(i, c, d))
            
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

    def abrir_editor(self, id_db, cod_actual, desc_actual):
        """Abre un diálogo para editar código y descripción."""
        # 1. Definimos qué campos queremos editar en este contexto
        campos = {
            "Código": cod_actual,
            "Descripción": desc_actual
        }

        # 2. Instanciamos el diálogo genérico
        dialogo = GenericEditDialog(self, title="Editar Tipo de Costo", fields=campos)

        # 3. Si el usuario presiona "Actualizar"
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            nuevos_datos = dialogo.get_values()
            
            # 4. Extraemos los valores por nombre de campo
            nuevo_cod = nuevos_datos["Código"]
            nueva_desc = nuevos_datos["Descripción"]

            # 5. Llamamos al controlador
            exito, mensaje = self.controller.actualizar_tipo_costo(id_db, nuevo_cod, nueva_desc)
            
            if exito:
                # Opcional: mostrar mensaje de éxito
                # QMessageBox.information(self, "Éxito", mensaje)
                self.cargar_datos() # Refrescar la tabla para ver los cambios
            else:
                # Mostrar el error (por ejemplo, si el código ya existe)
                QMessageBox.critical(self, "Error de Actualización", mensaje)

class PlantillaMaestraViews(QWidget, GeneralWidget):
    # constructor
    def __init__(self):
        super().__init__()
        self.controller = TipoCostoController()
        self.init_ui_plantilla_maestro()
        self.init_line_divider()
        self.init_table_resgistroplanillamaestro()
    
    def init_ui_plantilla_maestro(self):
        layout = QVBoxLayout(self)
        
        self.init_form_card_plantillaMaestro()
        self.init_line_divider()
        self.init_table_resgistroplanillamaestro()
        
        layout.addWidget(self.form_card)
        layout.addWidget(self.linea_divisora)
        layout.addWidget(self.tabla)
        
        layout.addStretch()
        
    def init_form_card_plantillaMaestro(self):
        """Inicializa el formulario para generar plantilla maestra."""
        # 1.0 --- FORMULARIO - almacenar platilla maestra ---
            # 1.1 frame del formulario
        self.form_card = QFrame()
        self.form_card.setObjectName("FormCard") 
        form_layout = QVBoxLayout(self.form_card)
            # 1.2 campos del formulario descripción tipo costo
        self.txt_descripcion_form = QLabel('Descripción plantilla maestra')
        self.txt_descripcion_form.setObjectName("LabelForm")
        self.txt_descripcion = QLineEdit()
        self.txt_descripcion.setPlaceholderText("Ejemplo: Costos Directos Proyecto")
        self.txt_descripcion.setObjectName("InputForm")
        self.txt_descripcion.setFixedWidth(400)
        self.txt_descripcion.setMaxLength(40)
            # 1.3 campo del formulario código tipo costo
        self.txt_codigo_form = QLabel('Código plantilla maestra')
        self.txt_codigo_form.setObjectName("LabelForm")
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("01-CDP")
        self.txt_codigo.setObjectName("InputForm")
        self.txt_codigo.setFixedWidth(80)
        self.txt_codigo.setMaxLength(8)

        self.combobox_nivel_estructura()

        #self.combobox_nivelplantila.setObjectName("list_box")
        self.combobox_tipocosto()  
        
            # 1.6 botón guardar
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setObjectName("BtnGuardar")
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.setFixedWidth(100)
        btn_guardar.clicked.connect(self.handle_guardar_platillamaestro)

        form_layout.addWidget(self.txt_descripcion_form)
        form_layout.addWidget(self.txt_descripcion)
        form_layout.addWidget(self.txt_codigo_form)
        form_layout.addWidget(self.txt_codigo)
        form_layout.addWidget(self.txt_nivel)
        form_layout.addWidget(self.combobox_nivelplantila)
        form_layout.addWidget(self.txt_tipo_costo)
        form_layout.addWidget(self.combobox_tipo_costo)
        form_layout.addWidget(btn_guardar, alignment=Qt.AlignmentFlag.AlignLeft)  
    
    def combobox_tipocosto(self):
            # 1.5 selccion niveles jerarquia agrupadores de la palntilla maestra
        self.txt_tipo_costo = QLabel('Tipo Costo')
        self.txt_tipo_costo.setObjectName("LabelForm")
        self.combobox_tipo_costo=QComboBox()
        
        self.combobox_tipo_costo.clear()
        self.combobox_tipo_costo.addItem("Seleccione un tipo...", None)
        
        try:
            if not hasattr(self, 'tipo_costo_controller'):
                self.tipo_costo_controller = TipoCostoController()

            tipo_costos = self.tipo_costo_controller.obtener_tipocosto()

            if not tipo_costos:
                return

            opciones = [f"{tc[2]} - {tc[1]}" for tc in tipo_costos]
            
            # 3. Bloquear señales para evitar disparar eventos innecesarios durante la carga
            self.combobox_tipo_costo.blockSignals(True)
            self.combobox_tipo_costo.addItems(opciones)
            self.combobox_tipo_costo.blockSignals(False)
            
            self.combobox_tipo_costo.setFixedWidth(200)
            
            return self.combobox_tipo_costo
            
        except Exception as e:
            print(f"Error al cargar tipos de costo: {e}")
                
    def combobox_nivel_estructura(self):   
            # 1.4 selccion niveles jerarquia agrupadores de la palntilla maestra
        self.txt_nivel = QLabel('Niveles - Jerarquias')
        self.txt_nivel.setObjectName("LabelForm")
        self.combobox_nivelplantila=QComboBox()
        #self.combobox_nivelplantila.setObjectName("list_box")
        self.combobox_nivelplantila.addItems(['Nivel - 1',
                                              'Nivel - 2',
                                              'Nivel - 3',
                                              'Nivel - 4',
                                              'Nivel - 5'])     
        self.combobox_nivelplantila.setFixedWidth(150)
        return self.combobox_nivelplantila

    def init_table_resgistroplanillamaestro (self):
        """ Inicializa la tabla resultado busqueda todos las plantillas maestros."""
                # --- TABLA DE REGISTROS ---
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setObjectName("TablaRegistros")
        self.tabla.setHorizontalHeaderLabels(["edit","Código","Descripcion PlanillaMaestro","Nivel","Tipo costo"])
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
        self.tabla.setColumnWidth(2, 300) 
        self.tabla.setColumnWidth(3, 100)
        self.tabla.setColumnWidth(4, 100)
        
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        # Estética
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setShowGrid(False)
        
    def handle_guardar_platillamaestro (self):
        cod = self.txt_codigo.text().strip()
        desc = self.txt_descripcion.text().strip()
        nivel = self.combobox_nivelplantila.currentData()
        t_costo = self.combobox_tipo_costo.currentData()
        
        print(f"{cod}-{desc}\n-{nivel}\n-{t_costo}")
        