from PyQt6.QtWidgets import (QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, QFrame, QHeaderView,
                             QMessageBox, QDialog, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication

from genesis.ui.modules.maestro_crisol.maestro_controller import TipoCostoController , PlantillaMaestroController, EstructuraMaestroController
from genesis.ui.modules.maestro_crisol.maestro_controller import comun
from genesis.ui.modules.maestro_crisol.maestro_views_edit import GenericEditDialog, EditarPlantillaMaestroDialog

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
                comun.tipos_actualizados.emit()
            else:
                # Mostrar el error (por ejemplo, si el código ya existe)
                QMessageBox.critical(self, "Error de Actualización", mensaje)

class PlantillaMaestraViews(QWidget, GeneralWidget):
    def __init__(self):
        super().__init__()
        self.controller = PlantillaMaestroController()
        self.init_ui_plantilla_maestro()
        self.cargar_datos_plantillamaestro()
        
        comun.tipos_actualizados.connect(self.cargar_datos_plantillamaestro)
    
    def init_ui_plantilla_maestro(self):
        layout = QVBoxLayout(self)
        
        self.init_form_card_plantillaMaestro()
        self.init_line_divider()
        self.init_table_resgistroplanillamaestro()
        
        layout.addWidget(self.form_card)
        layout.addWidget(self.linea_divisora)
        layout.addWidget(self.tablaplanilla)
        
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
            # 1 selccion niveles jerarquia agrupadores de la palntilla maestra
        self.txt_tipo_costo = QLabel('Tipo Costo')
        self.txt_tipo_costo.setObjectName("LabelForm")
        self.combobox_tipo_costo=QComboBox()
        
        self.combobox_tipo_costo.clear()
        self.combobox_tipo_costo.addItem("Seleccione un tipo...", None)
        
        try:
            tipo_costos = self.controller.obtener_tipocosto()
            if not tipo_costos: return

            self.combobox_tipo_costo.clear()
            self.combobox_tipo_costo.addItem("Seleccione un tipo...", None)

            for tc in tipo_costos:
                # tc[0] es el ID, tc[1] descripción, tc[2] código
                label = f"{tc[2]} - {tc[1]}"
                id_real = tc[0] 
                # IMPORTANTE: addItem(texto, data)
                self.combobox_tipo_costo.addItem(label, id_real) 
                
            self.combobox_tipo_costo.setFixedWidth(200)
            return self.combobox_tipo_costo
        except Exception as e:
            print(f"Error: {e}")
                
    def combobox_nivel_estructura(self):   
            # 1.4 selccion niveles jerarquia agrupadores de la palntilla maestra
        self.txt_nivel = QLabel('Niveles - Jerarquias')
        self.combobox_nivelplantila = QComboBox()
        
        niveles = [
            ("Nivel - 1", 1),
            ("Nivel - 2", 2),
            ("Nivel - 3", 3),
            ("Nivel - 4", 4),
            ("Nivel - 5", 5)
        ]
        
        for texto, valor in niveles:
            self.combobox_nivelplantila.addItem(texto, valor)
            
        self.combobox_nivelplantila.setFixedWidth(150)
        return self.combobox_nivelplantila

    def init_table_resgistroplanillamaestro(self):
        """ Inicializa la tabla resultado busqueda todos las plantillas maestros."""
                # --- TABLA DE REGISTROS ---
        self.tablaplanilla = QTableWidget()
        self.tablaplanilla.setColumnCount(5)
        self.tablaplanilla.setObjectName("TablaRegistros")
        self.tablaplanilla.setHorizontalHeaderLabels(["edit","Código","Descripcion PlanillaMaestro","Nivel","Tipo costo"])
    # --- PERMITIR SELECCIÓN Y COPIADO ---
        # Permite seleccionar celdas individuales o filas completas
        self.tablaplanilla.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        self.tablaplanilla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows) # Selecciona filas completas
        self.tablaplanilla.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # 2. Política de Foco (CAMBIO CLAVE)
        # Cambia NoFocus por StrongFocus o elimina la línea
        self.tablaplanilla.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tablaplanilla.setTabKeyNavigation(True)
        
        # configuracion de ancho de columnas específicas
        header = self.tablaplanilla.horizontalHeader()
        
        self.tablaplanilla.setColumnWidth(0, 50)   
        self.tablaplanilla.setColumnWidth(1, 80) 
        self.tablaplanilla.setColumnWidth(2, 300) 
        self.tablaplanilla.setColumnWidth(3, 100)
        self.tablaplanilla.setColumnWidth(4, 100)
        
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        # Estética
        self.tablaplanilla.verticalHeader().setVisible(False)
        self.tablaplanilla.setShowGrid(False)
        
    def handle_guardar_platillamaestro(self):
        cod = self.txt_codigo.text().strip().upper()
        nom = self.txt_descripcion.text().strip().upper()
        nivel = self.combobox_nivelplantila.currentData()
        tipo_costo = self.combobox_tipo_costo.currentData()

        try:
            exito, mensaje = self.controller.guardar_plantilla_maestro(nom, cod, tipo_costo, nivel)
            if exito:
                # Limpiar campos y refrescar tabla
                self.txt_codigo.clear()
                self.txt_descripcion.clear()
                self.cargar_datos_plantillamaestro()
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
    
        
        print(f"{cod}-{nom}\n-{nivel}\n-{tipo_costo}")
 
    def cargar_datos_plantillamaestro(self):
        """consulta y carga registros en pantalla de los maestros creados"""
        registros = self.controller.obtener_plantilla_maestro()
        self.tablaplanilla.setRowCount(len(registros))
    
        # Añadimos 'id_pk' para recibir el primer valor (id_plantilla_maestro)
        for row_idx, (id_db, desc, cod, nivel, tipo_costo) in enumerate(registros):            
            # 1. Item Descripción
            item_desc = QTableWidgetItem(str(desc).upper())
            
            # 2. Item Código
            item_custom = QTableWidgetItem(str(cod).upper())
            item_custom.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            print(nivel, type(nivel))
            
            # Convertir a string nivel y tipo_costo por si vienen como int de la DB
            nivel=self.controller.encontrar_nivel_id_db(nivel)
            item_nivel = QTableWidgetItem(str(nivel))
            item_nivel.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            print(nivel, type(nivel))

            tipo_costo = self.controller.encontrar_tipocosto_id_db(tipo_costo)
            item_tipo_costo = QTableWidgetItem(str(tipo_costo))
            item_tipo_costo.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # 3. Icono edición
            icono_custom = QPushButton("⚙️")
            icono_custom.setCursor(Qt.CursorShape.PointingHandCursor)
            icono_custom.setToolTip("Editar registro")
            icono_custom.setStyleSheet("background: transparent; border: none; font-size: 14px;")
            icono_custom.clicked.connect(lambda checked, i=id_db, c=cod, d=desc, n=nivel, tc=tipo_costo: self.abrir_editor_plantillamaestro(i, c, d,n,tc))            

            
            # Asignar a la tabla
            self.tablaplanilla.setCellWidget(row_idx, 0, icono_custom)
            self.tablaplanilla.setItem(row_idx, 1, item_custom)
            self.tablaplanilla.setItem(row_idx, 2, item_desc)
            self.tablaplanilla.setItem(row_idx, 3, item_nivel)
            self.tablaplanilla.setItem(row_idx, 4, item_tipo_costo)

    def abrir_editor_plantillamaestro(self, id_db, cod_actual, desc_actual, nivel_actual, t_costo_actual):
    # 1. Obtener los IDs reales para posicionar los ComboBox correctamente
        # (Suponiendo que tus métodos del controlador devuelven el ID numérico)
        id_nivel = self.controller.encontrar_iddb_nivel(nivel_actual)
        id_t_costo = self.controller.encontrar_iddb_t_costo(t_costo_actual)

        # 2. Obtener lista de Tipos de Costo para llenar el combo
        tipos_db = self.controller.obtener_tipocosto()
        # Mapeamos a [(ID, "Código - Descripción"), ...]
        opciones_tc = [(tc[0], f"{tc[2]} - {tc[1]}") for tc in tipos_db]

        # 3. Lanzar el diálogo específico
        dialogo = EditarPlantillaMaestroDialog(
            self, cod_actual, desc_actual, id_nivel, id_t_costo, opciones_tc
        )

        if dialogo.exec() == QDialog.DialogCode.Accepted:
            v = dialogo.get_datos()
            
            # 4. Enviar al controlador
            exito, mensaje = self.controller.actualizar_plantilla_maestro(
                id_db, v["codigo"], v["descripcion"], v["nivel"], v["tipo_costo"]
            )

            if exito:
                self.cargar_datos_plantillamaestro()
                comun.tipos_actualizados.emit()
            else:
                QMessageBox.critical(self, "Error", mensaje)     

class EstructuraMaestroViews(QWidget, GeneralWidget):
    def __init__(self):
        super().__init__()
        self.controller = EstructuraMaestroController()
        self.controller_plantilla = PlantillaMaestroController()

        self.init_ui_estructuraMaestro()
    
    def init_ui_estructuraMaestro(self):
        """Inicializa la interfaz para parametrizar estructura maestro."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) # Mantener todo arriba

        
        # Botón para mostrar/ocultar (Toggle)
        self.btn_ocultar_formulario()
        
        self.init_form_card_estructuraMaestro()
        self.init_line_divider()
        self.setup_combobox_plantilla()
        # Añadimos en orden
        layout.addWidget(self.btn_toggle_form, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.txt_label_pmaestro)
        layout.addWidget(self.combobox_pmaestro)
        layout.addWidget(self.form_card)
        layout.addWidget(self.linea_divisora)

        layout.addStretch()
    
    def init_form_card_estructuraMaestro(self):
        """Inicializa el formulario para parametrizar estructura maestro."""
        self.form_card = QFrame()
        self.form_card.setObjectName("FormCard") 
        self.form_card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)   
        self.form_layout = QVBoxLayout(self.form_card)

        # 1. PRIMERO: Creamos el contenedor y el layout de niveles
        # Así, cuando setup_patron_nivel se ejecute, el atributo ya existe.
        self.container_niveles = QWidget()
        self.layout_niveles = QHBoxLayout(self.container_niveles)
        
        btn_guardar = QPushButton("Almacenar Patrón")
        btn_guardar.setObjectName("BtnGuardar")
        btn_guardar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_guardar.setFixedWidth(120)
        
        label_info = QLabel(f'Ingrese patrón de código para cada nivel. d=digitos 0-9 w=letra (. -)=separadores.\nEjemplo: Patrón: "dd"="01" | Patrón: "d-wdd"="1-C22"')
        label_info.setObjectName("LabelInform")

        # 3. TERCERO: Añadimos todo al layout en el orden visual deseado
        self.form_layout.addWidget(self.container_niveles)
        self.form_layout.addWidget(label_info)
        self.form_layout.addWidget(btn_guardar, alignment=Qt.AlignmentFlag.AlignLeft)
        
    def setup_combobox_plantilla(self):
        """Crea y llena el combobox."""
        self.txt_label_pmaestro = QLabel('Plantilla Maestra:')
        self.txt_label_pmaestro.setObjectName("LabelForm")
        
        self.combobox_pmaestro = QComboBox()
        self.combobox_pmaestro.setFixedWidth(320)
        
        # Conectamos la señal
        self.combobox_pmaestro.currentIndexChanged.connect(self.setup_patron_nivel)
        
        try:
            plantillas = self.controller_plantilla.obtener_plantilla_maestro()
            self.combobox_pmaestro.addItem("Seleccione una plantilla...", None)
            
            for p in plantillas:
                self.combobox_pmaestro.addItem(str(p[1]), p[0])  
        except Exception as e:
            print(f"Error al cargar plantillas: {e}")
        
        # Ahora sí puede ejecutarse sin error
        self.setup_patron_nivel()
        
    def setup_patron_nivel(self):
        """muestra caja edicion segun el nivel, el usuario 
        ingresa el patrón de código en cada nivel
        Ejemplo: Nivel 1 - Patrón: 'dd'
        Nivel 2 - Patrón: 'dd-dd'
        Nivel 3 - Patrón: 'dd-dd-wdd'"""
        # 1. Limpiar inputs anteriores antes de generar nuevos
        while self.layout_niveles.count():
            child = self.layout_niveles.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                # Si el hijo es un layout (como tu layoutv), hay que vaciarlo también
                self.limpiar_layout_recursivo(child.layout())

        # 2. Validar selección del ComboBox
        nombre_p = self.combobox_pmaestro.currentText()
        id_p = self.combobox_pmaestro.currentData()

        if id_p is None or nombre_p == "Seleccione una plantilla...":
            return

        # 3. Obtener nivel con manejo de errores
        resultado_nivel = self.controller.encontrar_nivel_jerarquia_palntilla_maestro(name_plantilla=nombre_p)

        # Validar que el resultado sea un número y no el string "Error" o None
        try:
            num_niveles = int(resultado_nivel)
        except (ValueError, TypeError):
            print(f"Error: El nivel devuelto no es válido: {resultado_nivel}")
            return

        # 4. Generar la interfaz dinámica
        for i in range(num_niveles):
            layout_v = QVBoxLayout()
            layout_v.setAlignment(Qt.AlignmentFlag.AlignLeft)
            
            label = QLabel(f'Nivel {i + 1}:')
            label.setObjectName("LabelForm")
            
            input_patron = QLineEdit()
            input_patron.setPlaceholderText("dd-dd")
            input_patron.setObjectName("InputForm")
            input_patron.setFixedWidth(60)
            
            layout_v.addWidget(label)
            layout_v.addWidget(input_patron)
            
            self.layout_niveles.addLayout(layout_v)
            
        self.layout_niveles.addStretch(1)

    def limpiar_layout_recursivo(self, layout):
        """Función auxiliar para borrar layouts anidados."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            else:
                self.limpiar_layout_recursivo(item.layout())

    def btn_ocultar_formulario(self):
        """Oculta o muestra el formulario de configuración de patrones."""
        self.btn_toggle_form = QPushButton(" 🔽 Ocultar Configuración de Patrones")
        self.btn_toggle_form.setCheckable(True)
        self.btn_toggle_form.setObjectName("BtnToggleHeader") 
        self.btn_toggle_form.clicked.connect(self.toggle_formulario)

    def toggle_formulario(self):
            # Si el botón está chequeado, ocultamos. Si no, mostramos.
            is_visible = self.form_card.isVisible()
            
            # Invertimos la visibilidad
            self.form_card.setVisible(not is_visible)
            
            # Cambiamos el texto y el icono (opcional) para feedback visual
            if not is_visible:
                self.btn_toggle_form.setText(" 🔽 Ocultar Configuración de Patrones")
            else:
                self.btn_toggle_form.setText(" ▶️ Mostrar Configuración de Patrones")
        