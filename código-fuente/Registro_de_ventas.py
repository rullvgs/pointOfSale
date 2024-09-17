# Registro de ventas
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import simpledialog
import BD_Login
from tips_app import Tooltip
from datetime import datetime
from tkcalendar import Calendar
from tkinter import messagebox as msg
from tkinter import Label
from PIL import ImageGrab

class registro_ventas(tk.Toplevel):
	def __init__(self, master = None):
		super().__init__(master)
		# Creamos una ventana
		self.title("Registro de ventas")
		self.geometry("850x640")

		# Posicionamos la ventana a la mitad de pantalla
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla/2)-850/2)
		posicion_largo = int((largo_pantalla/2)-640/2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))
		self.config(bg = 'mint cream')

		self.model = BD_Login.modelo(self)

		# Ventanas secundarias
		self.frame_0 = tk.LabelFrame(self,text = "Registro de ventas", font = ("Arial blod", 14),fg = 'navy', bg = 'lightyellow')
		self.frame_0.grid(columnspan = 6, column = 0, row = 0, padx = 10, pady = 5)
		self.frame_1 = tk.LabelFrame(self,text = "Registro del día", font = ("Arial blod", 14), fg = 'navy', bg = 'lightyellow')
		self.frame_1.grid(columnspan = 6, column = 0, row = 1, padx = 10)

		# Variables
		self.tex_monto_total = tk.StringVar()
		self.ent_monto_total = tk.Entry(self.frame_0,  width = 18, textvariable = self.tex_monto_total)
		self.int_folio = tk.Label(self.frame_1, bg = 'white', width = 10, 
								font = ("Arial bold", 10), bd = 1, relief = 'solid')
		self.btn_registrar = tk.Button(self.frame_0, text = "Registrar", width = 10, command = self.guardar_datos)
		fecha_actual = datetime.now()
		fecha = fecha_actual.strftime("%d/%m/%Y")

		# Llamamos a las funciones		
		self.crear_widgets()
		self.actualizar_fecha()
		self.deshabilita_controles()
		self.actualizar_ingresos()
		self.insertar_ultimo_comprobante()
		self.mostrar_ventas_tabla(fecha)

	def crear_widgets(self):

		#------------------ TEXTO (LABELS) ----------------------- #
		self.importe_team = tk.Label(self.frame_0, text = "             Importe total del integrante:  $",bg = 'lightyellow', font = ("Rockwell", 12))
		self.importe_team.grid(column = 2, row = 2, sticky = 'W')

		self.equipo = tk.Label(self.frame_0, text = "             Importe total del equipo:        $", bg = 'lightyellow', font = ("Rockwell", 12))
		self.equipo.grid(column = 2, row = 3, sticky = 'W')

		self.persona = tk.Label(self.frame_1, text = "                   Folio:", font =  ("Rockwell", 12), bg = 'lightyellow')
		self.persona.grid(column = 0, row = 0, sticky = 'W')


		tk.Label(self.frame_0, text="   Cantidad:", font=("Rockwell", 12), bg = 'lightyellow').grid(column=1, row=5, sticky="W")
		self.cantidad = tk.Spinbox(self.frame_0, width=4, from_=1, to=100, command = self.calcular_monto_total)
		self.validar_spinbox_cmd = self.register(self.validar_spinbox)
		self.cantidad.config(validate="key", validatecommand=(self.validar_spinbox_cmd, "%P", "%d"))
		self.cantidad.bind("<<Modified>>", self.calcular_monto_total)
		self.cantidad.bind("<FocusOut>", lambda event: self.calcular_monto_total())
		self.cantidad.grid(column=1, row=5, padx=5, pady=15)

		tk.Label(self.frame_0, text = "Fecha Actual:", font = ("Lucida Console",10), bg = 'lightyellow').grid(column = 2, pady  = 5, padx = 8,  row  = 0, sticky = "E")
		#self.fecha_tex = tk.StringVar()
		#self.calendario = Calendar(self, selectmode="day", year=2023, month=8, day=4)
		#self.calendario.place(y = 2, x = 450)

		self.fecha_tex = tk.Text(self.frame_0, height = 1, width = 14)
		self.fecha_tex.grid(column = 3, row = 0, sticky = "W")
		self.fecha_tex.bind('<FocusIn>', self.modo_lectura)



		# ----------------------------- BOTONES ----------------------------- #
		
		self.btn_borrar = tk.Button(self.frame_0, text = "Borrar", width = 10, command = self.limpia_controles)
		self.btn_borrar.place(x = 425, y = 253)

		self.btn_nuevo = tk.Button(self.frame_0, text = "Nuevo", width = 10, command = self.usuario_nuevo, state = 'disabled')
		self.btn_nuevo.place(x = 520, y = 253)		

		
		#btn_registrar.bind('<Button-1>', self.mostrar_monto_total_integrante)
		self.btn_registrar.place(x = 615, y = 253)

		#btn_cancelar = tk.Button(self.frame_0, text = "Cancelar", width = 10, command = self.master.mostrar_menu_Principal)
		self.btn_salir = tk.Button(self, text = "Regresar", width = 10, command = self.master.mostrar_menu_Principal)
		self.btn_salir.place(x = 20, y = 30)

		self.btn_cancelar = tk.Button(self.frame_0, text = "Cancelar", width = 10, command = self.cancelar)
		self.btn_cancelar.place(x = 710, y = 253)

		self.btn_guardar = tk.Button(self.frame_1, text = "Guardar", width = 10, command = self.usuario_guardar)
		self.btn_guardar.place(x = 520, y = 1)

		tk.Label(self.frame_1, text = " ").grid(column = 1, row = 0, padx = 5, pady = 5, sticky = 'W')

		self.btn_editar = tk.Button(self.frame_1, text = "Editar", width = 10, command = self.usuario_editar)
		self.btn_editar.place(x = 615, y = 1)

		#btn_guardar = tk.Button(self.frame_1, text = "Guardar", width = 10)
		#btn_guardar.place(x = 615, y = 1)

		self.btn_Imprimir = tk.Button(self.frame_1, text = "Imprimir", width = 10, command = self.imprimir_datos)
		self.btn_Imprimir.place(x = 710, y = 1)

		self.btn_registro_completo = tk.Button(self.frame_1, text = "Ver registro general", width = 20, command = self.master.abrir_tabla_ventas)
		self.btn_registro_completo.grid(column = 0, row = 2, padx = 5, pady = 5, sticky = 'W')


		# --------------------------- COMBO BOX ----------------------------- #
		tk.Label(self.frame_0, text = "Equipo: ", font = ("Rockwell", 12), bg = 'lightyellow').grid(column = 0, row = 1, sticky = 'W')
		self.comb_equipo_var = tk.StringVar()
		self.ent_comb_equipo = ttk.Combobox(self.frame_0, width=28, textvariable=self.comb_equipo_var, values = self.model.obtener_equipos())
		self.ent_comb_equipo['values'] = self.model.obtener_equipos()
		self.ent_comb_equipo.bind("<<ComboboxSelected>>", self.equipo_combobox)
		self.ent_comb_equipo.bind("<FocusIn>", self.equipo_combobox)
		self.ent_comb_equipo.bind("<<KeyRelease>>", self.actualizar_combobox_integrante)
		self.ent_comb_equipo.grid(column=1, row=1, padx=15, pady=15, sticky='W')

		persona = tk.Label(self.frame_0, text = "Correspondiente a:", font =  ("Rockwell", 12), bg = 'lightyellow')
		persona.grid(column = 0, row = 2, sticky = 'W')
		self.comb_persona_var = tk.StringVar()
		self.ent_comb_persona = ttk.Combobox(self.frame_0, width=28, textvariable = self.comb_persona_var)
		self.ent_comb_persona.bind("<KeyRelease>", self.actualizar_combobox_integrante)
		self.ent_comb_persona.bind('<<ComboboxSelected>>', self.mostrar_monto_total_integrante)
		self.ent_comb_persona.grid(column = 1, row = 2, padx = 15, pady = 15, sticky = 'W')

		self.concepto = tk.Label(self.frame_0, text = "Concepto: ", font = ("Rockwell", 12), bg = 'lightyellow')
		self.concepto.grid(column = 0, row = 3, sticky = 'W')
		self.comb_concepto_var = tk.StringVar()
		self.ent_comb_concepto = ttk.Combobox(self.frame_0, width=28, textvariable=self.comb_concepto_var, values = self.model.obtener_conceptos())
		self.ent_comb_concepto['values'] = self.model.obtener_conceptos()
		self.ent_comb_concepto.bind("<<ComboboxSelected>>", self.actualizar_combobox_concepto)
		self.ent_comb_concepto.bind("<KeyRelease>", self.actualizar_combobox_concepto)
		self.ent_comb_concepto.grid(column = 1, row = 3, padx = 15, pady = 15, sticky = 'W')

		self.subconceptos = tk.Label(self.frame_0, text = "Subconcepto: ", font = ("Rockwell", 12), bg = 'lightyellow')
		self.subconceptos.grid(column = 0, row = 4, sticky = 'W')
		self.comb_sub_concepto_var = tk.StringVar()
		self.ent_sub_comb_concepto = ttk.Combobox(self.frame_0, width=28, textvariable = self.comb_sub_concepto_var)
		self.ent_sub_comb_concepto.bind("<KeyRelease>", self.actualizar_combobox_subconcepto)
		self.ent_sub_comb_concepto.grid(column = 1, row = 4, padx = 15, pady = 15, sticky = 'W')

		# ------------------------------ TEXTBOX ---------------------------- #
		self.importe_p = tk.Label(self.frame_0, text = "Monto:  $                               ", font = ("Rockwell", 12), bg = 'lightyellow')
		self.importe_p.grid(column = 0, row = 5, sticky = 'W')
		self.tex_monto = tk.StringVar()
		self.tex_monto.trace("w", lambda *args: self.calcular_monto_total())
		self.ent_monto = tk.Entry(self.frame_0, width = 17, textvariable = self.tex_monto)
		self.ent_monto.bind("<FocusOut>", lambda event: self.formato_moneda(self.ent_monto))
		self.ent_monto.bind("<Key>", self.validar)
		self.ent_monto.grid(column = 0, row = 5, padx = 15, pady = 15, sticky = 'E')
		Tooltip(self.ent_monto, "Costo unitario \n Ingresa solo números")

		tk.Label(self.frame_0, text = "             Monto total:                                $", font = ("Rockwell", 12), bg = 'lightyellow').grid(column = 2, row = 1, sticky = "w")
		self.ent_monto_total.bind("<FocusOut>", lambda event: self.formato_moneda(self.ent_monto_total))
		self.ent_monto_total.bind("<FocusIn>", self.modo_lectura)
		self.ent_monto_total.grid(column = 3, row = 1, padx = 5)
		Tooltip(self.ent_monto_total, "Se rellena automáticamente \n (Monto * Cantidad)")

		self.tex_importe_persona = tk.StringVar()
		self.ent_importe_persona = tk.Entry(self.frame_0, font = 12, width = 12, textvariable = self.tex_importe_persona)
		self.ent_importe_persona.bind('<FocusOut>', lambda event: self.formato_moneda(self.ent_importe_persona))
		self.ent_importe_persona.bind('<FocusIn>', self.modo_lectura)
		self.ent_importe_persona.grid(column = 3, row = 2,padx = 5, pady = 15, sticky = 'W')
		Tooltip(self.ent_importe_persona, "Se rellena automáticamente \n (Monto total de la persona de este día)")

		self.tex_importe_equipo = tk.StringVar()
		self.ent_importe_equipo = tk.Entry(self.frame_0, font = 12, width = 12, textvariable = self.tex_importe_equipo)
		self.ent_importe_equipo.bind('<FocusIn>', self.modo_lectura)
		self.ent_importe_equipo.bind('<FocusOut>', lambda event: self.formato_moneda(self.ent_importe_equipo))
		self.ent_importe_equipo.grid(column = 3, row = 3,padx = 5, pady = 15, sticky = 'W')
		Tooltip(self.ent_importe_equipo, "Se rellena automáticamente \n (Importe total de los integrantes del \n equipo seleccionado)")

		#self.int_folio = tk.StringVar()
		#self.ent_folio = tk.Entry(self.frame_0, text = "0001", font = 12, width = 12, textvariable = self.int_folio)
		#self.ent_folio.grid(column = 3, row = 4, padx = 5, pady = 15, sticky = 'W')
		#tk.Label(self.frame_1, text = "# Comprobante: ", font =  ("Rockwell", 10)).grid(column = 3, row = 0, sticky = "E")
		self.int_folio.grid(column = 0, row = 0, padx = 5, pady = 15, sticky = 'E')

		tk.Label(self.frame_1, text = "Total de ingresos:  $", font =  ("Rockwell", 12), bg = 'lightyellow').grid(column = 4, row = 2, sticky = "E")
		self.int_ingreso_total = tk.StringVar()
		self.ent_ingreso_total = tk.Entry(self.frame_1, font = 12, width = 12, textvariable = self.int_ingreso_total)
		self.ent_ingreso_total.bind('<FocusIn>', self.modo_lectura)
		self.ent_ingreso_total.bind('<FocusOut>', lambda event: self.formato_moneda(self.ent_ingreso_total))
		self.ent_ingreso_total.grid(column = 5, row = 2, padx = 5, pady = 15, sticky = 'W')
		Tooltip(self.ent_ingreso_total, "Ingreso total del día \n (Suma del importe total del \n de día los equipos)")

		# ------------------------------ TREEVIEW ----------------------------- #
		#  TABLA REGISTRADA EN LA BASE DE DATOS DE LA TRANSACCIÓN POR PERSONA
		self.frame_tabla = tk.Frame(self.frame_1)
		self.frame_tabla.grid(columnspan = 6, row = 1, sticky = "W", padx = 10, pady = 5)
		self.tabla = ttk.Treeview(self.frame_tabla, height = 7)
		self.tabla.grid(column = 0, row = 0, padx = 10)
		ladox = tk.Scrollbar(self.frame_tabla, orient = tk.HORIZONTAL, command = self.tabla.xview)
		ladox.grid(column = 0, row = 1, sticky = "ew")
		ladoy = tk.Scrollbar(self.frame_tabla, orient = tk.VERTICAL, command = self.tabla.yview)
		ladoy.grid(column = 1, row = 0, sticky = "ns")

		self.tabla['columns'] = ('ID', 'FECHA', 'FOLIO', 'NOMBRE DEL INTEGRANTE', 'CONCEPTO', 'SUBCONCEPTO', 'CANTIDAD', 'MONTO', 'TOTAL')
		
		self.tabla.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('ID', minwidth = 5, width = 5, anchor = 'center')
		self.tabla.column('FECHA', minwidth = 60, width = 60, anchor = 'center')
		self.tabla.column('FOLIO', minwidth = 50, width = 50, anchor = 'center')
		self.tabla.column('NOMBRE DEL INTEGRANTE', minwidth = 180, width = 200, anchor = 'center', stretch = True)
		self.tabla.column('CONCEPTO', minwidth = 80, width = 120, anchor = 'center', stretch = True)
		self.tabla.column('SUBCONCEPTO', minwidth = 60, width = 120, anchor = 'center', stretch = True)
		self.tabla.column('CANTIDAD', minwidth = 60, width = 60, anchor = 'center')
		self.tabla.column('MONTO', minwidth = 60, width = 80, anchor = 'center')
		self.tabla.column('TOTAL', minwidth = 80, width = 80, anchor = 'center')

		self.tabla.heading('#0', anchor = 'center')
		self.tabla.column('ID', minwidth = 5, width = 5, anchor = 'center')
		self.tabla.heading('FECHA', text = 'FECHA', anchor = 'center')
		self.tabla.heading('FOLIO', text = 'FOLIO', anchor = 'center')
		self.tabla.heading('NOMBRE DEL INTEGRANTE', text = 'NOMBRE DEL INTEGRANTE', anchor = 'center')
		self.tabla.heading('CONCEPTO', text = 'CONCEPTO', anchor = 'center')
		self.tabla.heading('SUBCONCEPTO', text = 'SUBCONCEPTO', anchor = 'center')
		self.tabla.heading('CANTIDAD', text = 'CANTIDAD', anchor = 'center')
		self.tabla.heading('MONTO', text = 'MONTO', anchor = 'center')
		self.tabla.heading('TOTAL', text = 'TOTAL', anchor = 'center')

	def guardar_datos(self):

		if (self.validacion_controles() == False):
			return
		else:
			nombre_equipo = self.comb_equipo_var.get()
			nombre_integrante = self.comb_persona_var.get()
			conceptos = self.comb_concepto_var.get()
			subconcepto = self.comb_sub_concepto_var.get()
			cantidad_producto = self.cantidad.get()
			monto = self.tex_monto.get()
			monto_total = self.tex_monto_total.get() 
			ingreso_total = self.int_ingreso_total.get()
			importe_total_integrante = self.tex_importe_persona.get()
			importe_total_equipo = self.tex_importe_equipo.get()
			folio = self.int_folio.cget('text')
			fecha = self.fecha_tex.get("1.0", "end-1c")
			precio_final = self.convertir_formato_numero(monto_total)
			monto = self.convertir_formato_numero(monto)
			total_integrante = self.convertir_formato_numero(importe_total_integrante)
			total_equipo = self.convertir_formato_numero(importe_total_equipo)

			# Insertar o actualizar los datos en las tablas correspondientes
			self.model.insertar_equipo_venta(nombre_equipo)
			self.ent_comb_equipo['values'] = self.model.obtener_equipos()
			resultado = self.model.inserta_integrante_venta(nombre_integrante, nombre_equipo)
			if resultado:
			    # El integrante se registró correctamente
			    self.model.inserta_concepto_venta(conceptos)
			    self.ent_comb_concepto['values'] = self.model.obtener_conceptos()
			    self.model.inserta_subconcepto_venta(subconcepto, conceptos)
			    self.model.inserta_compras_venta(folio, fecha, nombre_integrante, conceptos, subconcepto, cantidad_producto, monto, precio_final)
			    #self.model.inserta_ingreso_total(ingreso_total)
			    self.mostrar_monto_total_integrante(None)
			    self.deshabilita_controles()
			    self.mostrar_monto_equipo()
			    self.actualizar_ingresos()
			    self.equipo_combobox(None)
			    self.generar_comprobante()
			    # Visualizamos los datos en el grid
			    self.tabla.delete(*self.tabla.get_children())
			    self.mostrar_ventas_tabla(fecha)
			else:
				pass
			self.limpia_controles()
			
	def equipo_combobox(self, event):
		self.actualizar_combobox(None)
		self.mostrar_monto_equipo()

	def actualizar_combobox(self, event):
		equipo_seleccionado = self.comb_equipo_var.get()
		integrantes = self.model.obtener_usuarios(equipo_seleccionado)
  
		if len(integrantes) > 0:
            # Actualizar el contenido del combobox de integrantes
			self.ent_comb_persona['values'] = integrantes
	 
	def actualizar_combobox_concepto(self, event):
	    self.concepto_seleccionado = self.comb_concepto_var.get()
	    subconceptoos = self.model.obtener_subconceptos(self.concepto_seleccionado)

	    if len(subconceptoos) > 0:
	        # Actualizar el contenido del combobox
	        self.ent_sub_comb_concepto['values'] = subconceptoos
	        self.ent_sub_comb_concepto.set(subconceptoos[0])

	def actualizar_combobox_subconcepto(self, event):
	    concepto_seleccionado = self.comb_concepto_var.get()

	    if concepto_seleccionado:
	        subconcepto_ingresado = self.comb_sub_concepto_var.get().lower()
	        subconceptos_coincidentes = [subconcepto for subconcepto in self.model.obtener_subconceptos(concepto_seleccionado) if subconcepto.lower().startswith(subconcepto_ingresado)]
	        self.ent_sub_comb_concepto['values'] = subconceptos_coincidentes
	    else:
	        self.ent_sub_comb_concepto['values'] = ()

	def actualizar_combobox_integrante(self, event):
		equipo_seleccionado = self.comb_equipo_var.get()
		if equipo_seleccionado:
			integrante_ingresado = self.comb_persona_var.get().lower()
			integrantes_coincidentes = [integrante for integrante in self.model.obtener_usuarios(equipo_seleccionado) if integrante.lower().startswith(integrante_ingresado)]
			self.ent_comb_persona['values'] = integrantes_coincidentes
		else:
			self.ent_comb_persona['values'] = ()

	def actualizar_ingresos(self):
		fecha = fecha = self.fecha_tex.get("1.0", "end-1c")
		ingreso = self.model.buscar_ingreso_total(fecha)
		self.ent_ingreso_total.delete(0, 'end')
		if ingreso is not None:
		    self.ent_ingreso_total.insert(0, "{:,.2f}".format(ingreso))
		else:
		    pass

	def validar(self, event):
		if event.keysym != "BackSpace" and event.char not in "0123456789,.":
			return "break"

	def validar_spinbox(self, value, action):
		return value == "" or value.isdigit()
	
	def formato_moneda(self, entry):
		try:
			num = float(entry.get().replace(",", ""))
			num_formateado = "{:,.2f}".format(num)
			entry.delete(0, tk.END)
			entry.insert(0, num_formateado)

		except ValueError:
			pass
		self.ent_importe_persona.configure(state = "normal")
		self.ent_importe_equipo.configure(state = 'normal')
		self.ent_ingreso_total.configure(state = 'normal')

	def convertir_formato_numero(self, numero_str):
		# Reemplazar comas por nada y puntos por punto decimal
		numero_limpio = numero_str.replace(",", "").replace(".", ".")
        
		try:
			numero_convertido = float(numero_limpio)
			return numero_convertido
		except ValueError:
			return None

	def calcular_monto_total(self):
		self.ent_monto_total.configure(state="normal")
		try:
			monto = float(self.ent_monto.get().replace(",", ""))
			cantidad = int(self.cantidad.get())
			total = monto * cantidad
			self.ent_monto_total.delete(0, tk.END)
			self.ent_monto_total.insert(0, "{:,.2f}".format(total))
		except ValueError:
			pass

	def modo_lectura(self, event):
		event.widget.config(state = 'disabled')

	def generar_comprobante(self):
		folio_texto = self.int_folio.cget('text')  # Obtener el valor actual del Label como cadena
		folio_numero = int(folio_texto)  # Convertir la cadena a un número entero
		folio_numero += 1  # Incrementar el número
		nuevo_folio_texto = "{:04d}".format(folio_numero)  # Formatear como cadena con ceros a la izquierda
		self.int_folio.config(text=nuevo_folio_texto) 

	def insertar_ultimo_comprobante(self):
		get_comprobante = self.model.cargar_ultimo_folio()
		comprobante_texto = "{:04d}".format(get_comprobante)
		self.int_folio.config(text=comprobante_texto)

	def mostrar_ventas_tabla(self, fecha):
		for dato in self.model.muestra_ventas(fecha):
			self.tabla.insert('', 0, text = '', value = dato)


	def mostrar_monto_total_integrante(self, event):
		fecha = self.fecha_tex.get("1.0", "end-1c")
		integrante = self.comb_persona_var.get()
		dato_importe = self.model.sum_monto_integrante(fecha, integrante)
		self.ent_importe_persona.delete(0, 'end')
		if dato_importe is not None:
		    self.ent_importe_persona.insert(0, "{:,.2f}".format(dato_importe))
		else:
		    pass
		self.tex_importe_persona.set(dato_importe)

	def mostrar_monto_equipo(self):
		fecha = self.fecha_tex.get("1.0", "end-1c")
		equipo = self.comb_equipo_var.get()
		monto_equipo = self.model.importe_total_equipo(fecha, equipo)
		self.ent_importe_equipo.delete(0, 'end')
		if monto_equipo is not None:
		    self.ent_importe_equipo.insert(0, "{:,.2f}".format(monto_equipo))
		else:
		    pass

		self.tex_importe_equipo.set(monto_equipo)

	def validacion_controles(self):
		if self.ent_comb_equipo.get() == '':
			msg.showerror("Error", "Ingresa el equipo, por favor")
			return False
		elif self.ent_comb_persona.get() == '':
			msg.showerror("Error", "Ingresa el nombre de quien corresponda, por favor")
			return False
		elif self.ent_comb_concepto.get() == '':
			msg.showerror("Error", "Ingresa un concepto, por favor")
			return False
		elif self.ent_sub_comb_concepto.get() == '':
			msg.showerror("Error", "Ingresa un subconcepto, por favor")
			return False
		elif self.ent_monto.get() == '':
			msg.showerror("Error", "Ingresa el monto, por favor")
			return False

	def habilita_controles(self):
		self.ent_comb_equipo.configure(state = 'normal')
		self.ent_comb_persona.configure(state = 'normal')
		self.ent_comb_concepto.configure(state = 'normal')
		self.ent_sub_comb_concepto.configure(state = 'normal')
		self.ent_monto.configure(state = 'normal')
		self.cantidad.configure(state = 'normal')

		self.btn_nuevo.configure(state = 'disabled')
		self.btn_editar.configure(state = 'disabled')
		self.btn_Imprimir.configure(state = 'disabled')
		self.btn_registrar.configure(state = 'normal')
		self.btn_borrar.configure(state = 'normal')

	def deshabilita_controles(self):
		self.ent_comb_equipo.configure(state = 'disabled')
		self.ent_comb_persona.configure(state = 'disabled')
		self.ent_comb_concepto.configure(state = 'disabled')
		self.ent_sub_comb_concepto.configure(state = 'disabled')
		self.ent_monto.configure(state = 'disabled')
		self.cantidad.configure(state = 'disabled')

		self.btn_nuevo.configure(state = 'normal')
		self.btn_editar.configure(state = 'normal')
		self.btn_Imprimir.configure(state = 'normal')
		self.btn_registrar.configure(state = 'disabled')
		self.btn_borrar.configure(state = 'disabled')
		self.btn_guardar.config(state = 'disabled')
		#self.btn_Imprimir.configure(state = 'disabled')

	def limpia_controles(self):
		equipo = self.ent_comb_equipo.get()
		persona = self.ent_comb_persona.get()
		self.ent_comb_equipo.delete(0, 'end')
		self.ent_comb_persona.delete(0, 'end')
		self.ent_comb_equipo.insert(0, equipo)
		self.ent_comb_persona.insert(0, persona)

		self.ent_comb_concepto.delete(0, 'end')
		self.ent_sub_comb_concepto.delete(0, 'end')
		self.ent_monto.delete(0, 'end')
		self.ent_monto_total.delete(0, 'end')
		#self.ent_importe_persona.delete(0, 'end')
		#self.ent_importe_equipo.delete(0, 'end')

	def usuario_nuevo(self):
		self.habilita_controles()
		self.limpia_controles()	


	def usuario_editar(self):
		if self.tabla.focus() == '':
			msg.showerror("Error", "Selecciona un usuario de la tabla, por favor")
			return

		self.habilita_controles()

		self.item_seleccionado = self.tabla.item(self.tabla.selection())
		folio = self.item_seleccionado['values'][2]
		self.int_folio.config(text = "{:04d}".format(folio))
		#self.int_folio.config(text = self.item_seleccionado['values'][1])

		equipo = self.model.cargar_equipo(self.item_seleccionado['values'][3])
		self.ent_comb_equipo.delete(0, 'end')
		self.ent_comb_equipo.insert(0, equipo)

		self.ent_comb_persona.delete(0, 'end')
		self.ent_comb_persona.insert(0, self.item_seleccionado['values'][3])
		self.ent_comb_concepto.delete(0, 'end')
		self.ent_comb_concepto.insert(0, self.item_seleccionado['values'][4])
		self.ent_sub_comb_concepto.delete(0, 'end')
		self.ent_sub_comb_concepto.insert(0, self.item_seleccionado['values'][5])

		self.cantidad.delete(0, 'end')
		self.cantidad.insert(0, self.item_seleccionado['values'][6])

		self.ent_monto.delete(0, 'end')
		self.ent_monto.insert(0, self.item_seleccionado['values'][7])

		self.ent_monto_total.delete(0, 'end')
		self.ent_monto_total.insert(0, self.item_seleccionado['values'][8])

		self.id_compra = self.item_seleccionado['values'][0]
		self.btn_guardar.config(state = 'normal')
		self.btn_registrar.config(state = 'disabled')

	def usuario_guardar(self):
		if (self.validacion_controles() == False):
			return


		# Actualizar la base de datos con los datos modificados
		nombre_equipo = self.comb_equipo_var.get()
		nombre_integrante = self.comb_persona_var.get()
		conceptos = self.comb_concepto_var.get()
		subconcepto = self.comb_sub_concepto_var.get()
		cantidad_producto = self.cantidad.get()
		monto = self.tex_monto.get()
		monto_total = self.tex_monto_total.get() 
		folio = self.int_folio.cget('text')
		fecha = self.fecha_tex.get("1.0", "end-1c")
		precio_final = self.convertir_formato_numero(monto_total)
		monto = self.convertir_formato_numero(monto)
		#total_integrante = self.convertir_formato_numero(importe_total_integrante)
		#total_equipo = self.convertir_formato_numero(importe_total_equipo)


		self.model.actualizar_ventas(self.id_compra, fecha, folio, nombre_integrante, conceptos, subconcepto, cantidad_producto, monto, precio_final)
		
		# Visualizamos los datos en la tabla
		self.tabla.delete(*self.tabla.get_children())
		self.mostrar_ventas_tabla(fecha)
		# Preparamos la pantalla para la siguiente operación
		self.limpia_controles()
		self.deshabilita_controles()
		self.insertar_ultimo_comprobante()
		self.actualizar_ingresos()
		self.mostrar_monto_total_integrante(None)
		self.mostrar_monto_equipo()

	def imprimir_datos(self):
		if self.tabla.focus() == '':
			msg.showerror("Error", "Selecciona un usuario de la tabla, por favor")
			return

		self.btn_editar.configure(state = 'disabled')
		self.btn_Imprimir.configure(state = 'disabled')
		self.btn_cancelar.configure(state = 'disabled')
		self.btn_registro_completo.configure(state = 'disabled')
		self.item_seleccionado = self.tabla.item(self.tabla.selection())

		fecha = self.item_seleccionado['values'][1]
		folio_int = self.item_seleccionado['values'][2]
		folio = "{:04d}".format(folio_int)
		#self.int_folio.config(text = self.item_seleccionado['values'][1])

		equipo = self.model.cargar_equipo(self.item_seleccionado['values'][3])

		persona = self.item_seleccionado['values'][3]
		concepto = self.item_seleccionado['values'][4]
		subconcepto = self.item_seleccionado['values'][5]
		cantidad = self.item_seleccionado['values'][6]

		monto = self.item_seleccionado['values'][7]
		monto_total = self.item_seleccionado['values'][8]

		self.id_compra = self.item_seleccionado['values'][0]

		self.frame_2 = tk.LabelFrame(self, text="Registro de Egresos", font = ("Lucida Console",12))
		self.frame_2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		self.frame_2.config(borderwidth=2, relief="solid")

	    # Configuración del tipo de letra
		font = ("Courier New Bold", 11)
		font2 = ("Courier New", 11)

	    # Creación de las etiquetas y su ubicación en el grid
		Label(self.frame_2, text="\n\n\n\n\n\n\n\n             CLIENTE:", font=font).grid(row=1, column=0, sticky= 'e')
		Label(self.frame_2, text="             EQUIPO:", font=font).grid(row=2, column=0, sticky= 'e')
		Label(self.frame_2, text="             FOLIO:", font=font).grid(row=3, column=0, sticky= 'e')
		Label(self.frame_2, text="             FECHA:", font=font).grid(row=4, column=0, sticky='e')
		Label(self.frame_2, text="             CONCEPTO:", font=font).grid(row=5, column=0, sticky='e')
		Label(self.frame_2, text="             SUBCONCEPTO:", font=font).grid(row=6, column=0, sticky='e')
		Label(self.frame_2, text="             CANTIDAD:", font=font).grid(row=7, column=0, sticky='e')
		Label(self.frame_2, text="             PRECIO UNITARIO:", font=font).grid(row=8, column=0, sticky='e')
		Label(self.frame_2, text="             PRECIO FINAL:\n\n\n\n\n\n\n\n\n", font=font).grid(row=9, column=0, sticky='e')
	    
		# Agregar las etiquetas para las firmas
		#Label(self.frame_2, text="      Firma del que entrega\n\n", font=font).grid(row=9, column=0, sticky='W')
		label = Label(self, text=" _____________________", font=font)
		label.place(x = 210, y = 440)
		#Label(self.frame_2, text="      Firma del cliente     \n\n", font=font).grid(row=9, column = 1, sticky = 'W')
		#Label(self.frame_2, text="   _______________________     ", font=font).grid(row=8, column=1, sticky='E')
		label2 = Label(self, text=" _____________________", font=font)
		label2.place(x = 450, y = 440)
		# Creación de las etiquetas y su ubicación en el grid
		#Label(self.frame_2, text="ID:\n", font=font).grid(row=0, column=0, sticky=W)
		Label(self.frame_2, text = "\n\n\n\n\n\n\n\n" + persona, font=font2).grid(row=1, column=1, sticky='W')
		Label(self.frame_2, text = equipo, font=font2).grid(row=2, column=1, sticky='W')
		Label(self.frame_2, text = folio, font=font2).grid(row=3, column=1, sticky='W')
		Label(self.frame_2, text = fecha, font=font2).grid(row=4, column=1, sticky='W')
		Label(self.frame_2, text = concepto, font=font2).grid(row=5, column=1, sticky='W')
		Label(self.frame_2, text = subconcepto, font=font2).grid(row=6, column=1, sticky='W')
		Label(self.frame_2, text = cantidad, font=font2).grid(row=7, column=1, sticky='W')
		Label(self.frame_2, text = monto, font=font2).grid(row=8, column=1, sticky='W')
		Label(self.frame_2, text = monto_total + "                     \n\n\n\n\n\n\n\n\n", font=font2).grid(row=9, column=1, sticky='W')

		# Crear la caja de texto
		# Función para cambiar el foco al Label al hacer clic en él
		def on_label_click(event):
		    self.frame_2.focus()

		# Vincular la función al evento <Button-1> (clic del botón izquierdo del ratón)
		self.frame_2.bind("<Button-1>", on_label_click)

		razon = tk.Entry(self.frame_2, borderwidth=0, highlightthickness=0, background = 'gray94', width = 30, fg = 'blue')
		razon.config(justify = 'center')
		razon.place(x = 143, y  = 113)
		motivo = tk.Entry(self, borderwidth=0, highlightthickness=0, background = 'gray94', width = 30, fg = 'blue')
		motivo.config(justify = 'center')
		motivo.place(x = 210, y = 460)

		motivo2 = tk.Entry(self, borderwidth=0, highlightthickness=0, background = 'gray94', width = 30, fg = 'blue')
		motivo2.config(justify = 'center')
		motivo2.place(x = 450, y = 460)

		# Agregar el texto de fondo
		razon.insert(0, "INGRESA TÍTULO O MOTIVO AQUÍ")
		motivo.insert(0, "INGRESA MOTIVO O TITULAR")
		motivo2.insert(0, "INGRESA MOTIVO O TITULAR")

		# Función para borrar el texto de fondo al hacer clic en la caja de texto
		def on_entry_click(event):
		    if razon.get() == "INGRESA TÍTULO O MOTIVO AQUÍ":
		        razon.delete(0, 'end')
		        razon.config(fg = 'black', font = ("Courier New Bold", 10))
		def motivo_click(event):
		    if motivo.get() == "INGRESA MOTIVO O TITULAR":
		        motivo.delete(0, 'end')
		        motivo.config(fg = 'black', font = ("Courier New Bold", 8))

		def motivo2_click(event):
		    if motivo2.get() == "INGRESA MOTIVO O TITULAR":
		        motivo2.delete(0, 'end')
		        motivo2.config(fg = 'black', font = ("Courier New Bold", 8))



		# Vincular la función al evento <Button-1> (clic del botón izquierdo del ratón)
		razon.bind("<Button-1>", on_entry_click)
		motivo.bind("<Button-1>", motivo_click)
		motivo2.bind("<Button-1>", motivo2_click)

		#Cerrar ventana:
		def cerrar_frame(event):
		    self.frame_2.destroy()
		    motivo.destroy()
		    label.destroy()
		    self.btn_editar.configure(state = 'normal')
		    self.btn_Imprimir.configure(state = 'normal')
		    self.btn_cancelar.configure(state = 'normal')
		    self.btn_registro_completo.configure(state = 'normal')
		    motivo2.destroy()
		    label2.destroy()


		# Crear el botón Cerrar
		btn_cerrar = tk.Button(self.frame_2, text = "Cerrar", width = 8)
		btn_cerrar.bind("<Button-1>", cerrar_frame)
		btn_cerrar.place(x = 10, y = 0)
		
		def imprimir_labelframe( event):
		    # Obtener las coordenadas del LabelFrame en la pantalla
		    x = self.frame_2.winfo_rootx() + 100
		    y = self.frame_2.winfo_rooty() + 100
		    w = self.frame_2.winfo_width() + 100
		    h = self.frame_2.winfo_height() + 100

		    # Tomar una captura de pantalla del LabelFrame
		    imagen = ImageGrab.grab((x + 65, y + 10, x + w + 50, y + h -100 ))

		    # Guardar la imagen en un archivo
		    imagen.save(f"Egreso #{folio}-{self.id_compra}.png")
		    msg.showinfo("Éxito", f"El comprobante se ha guardado con el nombre:\n                   Egreso #{folio}-{self.id_compra}")

		btn_imprimir_datos = tk.Button(self.frame_2, text = "Guardar")
		btn_imprimir_datos.bind("<Button-1>", imprimir_labelframe)
		btn_imprimir_datos.place(x = 220, y = 440)

	def cancelar(self):
		self.deshabilita_controles()
		self.limpia_controles()


	# ------------------------ Agregar íconos ------------------------ #

	def actualizar_fecha(self):
		now = datetime.now()
		formatted_date = now.strftime("%d/%m/%Y")
		self.fecha_tex.delete("1.0", tk.END)  # Limpiar el contenido actual
		self.fecha_tex.insert(tk.END, formatted_date)
		#self.after(1000, self.actualizar_fecha)

'''
		
		self.calendario = DateEntry(self.frame_0, locale='es_MX', date_pattern='dd/mm/yyyy',
                       background='orange', foreground='black', bordercolor='green',
                       normalbackground='white', normalforeground='black',
                       weekendbackground='white', weekendforeground='red',
                       headersbackground='lightgreen', headersforeground='black')
		self.calendario.grid(column = 3, row = 0, padx = 5, pady = 5, sticky = 'E')'''




if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	app = registro_ventas(root)
	app.mainloop()