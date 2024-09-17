# Registro_de_Egresos
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import simpledialog
import BD_Login
from tkinter import messagebox as msg
from tips_app import Tooltip
from datetime import datetime
from tkinter import Label
from PIL import ImageGrab


class registro_egresos(tk.Toplevel):
	def __init__(self, master = None):
		super().__init__(master)
		# Creamos una ventana
		self.title("Registro de Egresos")
		self.geometry("660x620")

		# Posicionamos la ventana a la mitad de pantalla
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla/2)-660/2)
		posicion_largo = int((largo_pantalla/2)-620/2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))
		self.config(bg = 'mint cream')

		self.model = BD_Login.modelo(self)

		# Ventanas secundarias
		self.frame_0 = tk.LabelFrame(self,text = "Registro de compras", font = ("Lucida Console", 12), fg = 'navy', bg = 'lightyellow')
		self.frame_0.grid(columnspan = 6, column = 0, row = 0, padx = 10, pady = 5)
		self.frame_1 = tk.LabelFrame(self,text = "Registro del día", font = ("Lucida Console", 12), fg = 'Blue4', bg = 'azure')
		self.frame_1.grid(columnspan = 6, column = 0, row = 1, padx = 10)

		#self.frame_2 = tk.LabelFrame(self, text = "IMPRESIÓN DE EGRESO", font = ("Verdana",12))
		#self.frame_2.grid(columnspan = 8, column = 0, row = 0, padx = 10)

		# Varibales
		self.var_estatus = tk.IntVar(self, name = 'status', value = '1')
		self.comb_concepto = tk.StringVar()
		self.tex_precio = tk.StringVar()
		self.tex_monto_total = tk.StringVar()
		self.ent_monto_total = tk.Entry(self.frame_0, font = 12, width = 12, textvariable = self.tex_monto_total)
		self.tex_comprobante = tk.Label(self.frame_1, bg = 'white', width = 10, 
								font = ("Arial bold", 10), bd = 1, relief = 'solid')
		self.numero_comprobante = 1
		fecha_actual = datetime.now()
		fecha = fecha_actual.strftime("%d/%m/%Y")		
		
		# Llamamos a las funciones
		self.crear_widgets()
		self.deshabilita_controles()
		self.mostrar_conceptos()
		self.actualizar_fecha()
		self.mostrar_egresos(fecha)
		self.insertar_ultimo_comprobante()
		self.mostrar_ventas_tabla(fecha)
		
	def crear_widgets(self):


		#------------------ TEXTO (LABELS) ----------------------- #

		tk.Label(self.frame_0, text = "Concepto: ", font = ("Rockwell", 12), bg = 'lightyellow').grid(column = 0, row = 1, sticky = 'W')

		tk.Label(self.frame_0, text = "Precio:             $", font =  ("Rockwell", 12), bg = 'lightyellow').grid(column = 0, row = 2, sticky = 'W')

		tk.Label(self.frame_0, text = "Total:               $", font = ("Rockwell", 12), bg = 'lightyellow').grid(column = 0, row = 4, sticky = 'W')

		tk.Label(self.frame_0,text = "Cantidad: ", font =  ("Rockwell", 12), bg = 'lightyellow').grid(column = 0, row = 3, sticky = "W")
		self.cantidad = tk.Spinbox(self.frame_0, width = 4, from_ = 1, to = 300, command = self.calcular_monto_total)
		self.cantidad.bind("<<Modified>>", self.calcular_monto_total())
		self.cantidad.bind("<FocusOut>", lambda event: self.calcular_monto_total())
		self.cantidad.grid(column = 1, row = 3, padx = 5, pady  = 15, sticky = "W")

		tk.Label(self.frame_0, text = "Fecha Actual:", font = ("Lucida Console",10), bg = 'lightyellow').grid(column = 3, pady  = 5, padx = 2,  row  = 0, sticky = "E")
		self.fecha_tex = tk.Text(self.frame_0, height = 1, width = 12)
		self.fecha_tex.grid(column = 4, row = 0, padx = 5, sticky = "W")
		self.fecha_tex.bind('<FocusIn>', self.modo_lectura)



		# ----------------------------- BOTONES ----------------------------- #
		
		self.btn_borrar = tk.Button(self.frame_0, text = "Borrar", width = 10, command = self.limpia_controles)
		self.btn_borrar.grid(column = 1, row = 5, pady = 15, padx = 18, sticky = "E")

		self.btn_nuevo = tk.Button(self.frame_0, text = "Nuevo", width = 10, command = self.usuario_nuevo)
		self.btn_nuevo.grid(column = 2, row = 5, pady = 15, padx = 6, sticky = "W")

		self.btn_registrar = tk.Button(self.frame_0, text = "Registrar", width = 10, command = self.guardar_datos)
		self.btn_registrar.grid(column = 3, row = 5, pady = 15, padx = 10)

		self.btn_salir = tk.Button(self, text = "Regresar", width = 10, command = self.master.mostrar_menu_Principal)
		self.btn_salir.place(x = 15, y = 25)

		self.btn_cancelar = tk.Button(self.frame_0, text = "Cancelar", width = 10, command = self.cancelar)
		self.btn_cancelar.grid(column = 4, row = 5, pady = 15, padx = 5, sticky = "W")

		tk.Label(self.frame_1, text = " ").grid(column = 1, row = 0, padx = 5, pady = 5, sticky = 'W')

		self.btn_editar = tk.Button(self.frame_1, text = "Editar", width = 10, command = self.usuario_editar)
		self.btn_editar.place(x = 315, y = 260)

		self.btn_guardar = tk.Button(self.frame_1, text = "Guardar", width = 10, command = self.usuario_guardar)
		self.btn_guardar.grid(column = 3, row = 2, pady = 5, padx = 10, sticky = "E")		

		self.btn_Imprimir = tk.Button(self.frame_1, text = "Imprimir", width = 10, command = self.imprimir_datos)
		self.btn_Imprimir.grid(column = 4, row = 2, pady = 5, padx = 10, sticky = "W")

		self.btn_registro_completo = tk.Button(self.frame_1, text = "Ver registro completo", width = 20, command = self.master.abrir_tabla_egresos)
		self.btn_registro_completo.grid(column = 0, row = 2, padx = 5, pady = 5, sticky = 'W')


		# --------------------------- COMBO BOX ----------------------------- #
		self.ent_concepto = ttk.Combobox(self.frame_0, width=28, textvariable= self.comb_concepto)
		self.ent_concepto.grid(column = 1, row = 1, padx = 5, pady = 15, sticky = 'W')
		self.ent_concepto.bind("<FocusIn>", self.actualizar_conceptos)

		# ---------------------------- RADIO BUTTON ------------------------- #
		self.rbt_compras = tk.Radiobutton(self.frame_0,text = "Compras ", bg = 'lightyellow', variable = self.var_estatus,  value = 1, command = self.servicios_activa)
		self.rbt_compras.grid(column = 3, row = 2, padx  = 10, sticky = "E")
		self.rbt_servicios = tk.Radiobutton(self.frame_0,text = "Servicios ", bg = 'lightyellow', variable = self.var_estatus, value = 0, command = self.compras_activa)
		self.rbt_servicios.grid(column = 3, row = 3, padx = 10, sticky = "E")

		# ------------------------------ TEXTBOX ---------------------------- #
		
		#self.tex_monto_total = tk.StringVar()
		#self.ent_monto_total = tk.Entry(self.frame_0, font = 12, width = 12, textvariable = self.tex_monto_total)
		self.ent_monto_total.bind('<FocusIn>', self.modo_lectura)
		self.ent_monto_total.grid(column = 1, row = 4, padx = 5, sticky = 'W')
		Tooltip(self.ent_monto_total, "Se rellena automáticamente \n (precio * cantidad)")

		#self.tex_precio = tk.StringVar()		
		self.tex_precio.trace("w", lambda *args: self.calcular_monto_total())
		self.ent_precio = tk.Entry(self.frame_0, font = 12, width = 12, textvariable = self.tex_precio)
		self.ent_precio.bind("<Key>", self.validar)
		self.ent_precio.grid(column = 1, row = 2, padx = 5, pady = 15, sticky = 'W')

		tk.Label(self.frame_1, text = "    Total de egresos: $", bg = 'azure', font =  ("Rockwell", 12)).grid(column = 0, row = 0, sticky = "E")
		#self.ent_egreso_total = tk.Entry(self.frame_1, font = 12, width = 12, textvariable = self.tex_egreso_total)
		#self.ent_egreso_total.bind("<<KeyRelease>>", self.formato_moneda(self.ent_egreso_total))
		self.tex_egreso_total = tk.StringVar(self.frame_1)
		self.ent_egreso_total = tk.Entry(self.frame_1, font = 12, width = 12, textvariable = self.tex_egreso_total)
		self.ent_egreso_total.bind('<FocusIn>', self.modo_lectura)
		self.ent_egreso_total.bind('<FocusOut>',  lambda event: self.formato_moneda(self.ent_egreso_total))
		self.ent_egreso_total.grid(column = 1, row = 0, pady = 8, sticky = "E")
		Tooltip(self.ent_egreso_total, "Egresos de este día")

		tk.Label(self.frame_1, text = "# Comprobante: ", font =  ("Rockwell", 10), bg = 'azure').grid(column = 3, row = 0, sticky = "E")
		#self.tex_comprobante = tk.Label(self.frame_1, text = '0000', bg = 'white', width = 10, font = ("Arial bold", 10), bd = 1, relief = 'solid')
		self.tex_comprobante.grid(column = 4, row = 0, pady = 5, sticky = 'W')
		#self.ent_comprobante = tk.Entry(self.frame_1, font = 12, width = 12, textvariable = self.tex_comprobante)
		#self.ent_comprobante.grid(column = 4, row = 0, padx = 7, pady = 15, sticky = 'W')

		# ------------------------------ TREEVIEW ----------------------------- #
		#  TABLA REGISTRADA EN LA BASE DE DATOS 
		self.frame_tabla = tk.Frame(self.frame_1)
		self.frame_tabla.grid(columnspan = 5, row = 1, sticky = "W", padx = 10, pady = 5)
		self.style = ttk.Style()
		self.style.configure("Treeview.Heading", font = ("Arial bold", 8))
		self.tabla = ttk.Treeview(self.frame_tabla, height = 8)
		#self.tabla.tag_configure("Treeview.Heading", font=("Arial bold", 12))
		self.tabla.grid(column = 0, row = 0, padx = 10)
		ladox = tk.Scrollbar(self.frame_tabla, orient = tk.HORIZONTAL, command = self.tabla.xview)
		ladox.grid(column = 0, row = 1, sticky = "ew")
		ladoy = tk.Scrollbar(self.frame_tabla, orient = tk.VERTICAL, command = self.tabla.yview)
		ladoy.grid(column = 1, row = 0, sticky = "ns")

		self.tabla['columns'] = ('ID', 'COMPROBANTE', 'FECHA', 'CONCEPTO', 'CATEGORIA', 'CANTIDAD', 'PRECIO_UNITARIO', 'PRECIO_FINAL')
		
		self.tabla.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('ID', minwidth = 5, width = 5, anchor = 'center')
		self.tabla.column('COMPROBANTE', minwidth = 70, width = 70, anchor = 'center', stretch = True)
		self.tabla.column('FECHA', minwidth = 70, width = 70, anchor = 'center')
		self.tabla.column('CONCEPTO', minwidth = 80, width = 120, anchor = 'center', stretch = True)
		self.tabla.column('CATEGORIA', minwidth = 80, width = 90, anchor = 'center', stretch = True)
		self.tabla.column('CANTIDAD', minwidth = 60, width = 70, anchor = 'center')
		self.tabla.column('PRECIO_UNITARIO', minwidth = 50, width = 70, anchor = 'center')
		self.tabla.column('PRECIO_FINAL', minwidth = 80, width = 80, anchor = 'center')


		self.tabla.heading('#0', text = "\n", anchor = 'center')
		self.tabla.heading('ID', text = 'ID', anchor = 'center')
		self.tabla.heading('COMPROBANTE', text = 'COMPROBANTE', anchor = 'center')
		self.tabla.heading('FECHA', text = 'FECHA', anchor = 'center')
		self.tabla.heading('CONCEPTO', text = 'CONCEPTO', anchor = 'center')
		self.tabla.heading('CATEGORIA', text = 'CATEGORÍA', anchor = 'center')
		self.tabla.heading('CANTIDAD', text = 'CANTIDAD', anchor = 'center')
		self.tabla.heading('PRECIO_UNITARIO', text = '  PRECIO\nUNITARIO', anchor = 'center')
		self.tabla.heading('PRECIO_FINAL', text = 'PRECIO FINAL', anchor = 'center')

	# -------------- CREAR FUNCIONES --------------------- #
	def guardar_datos(self):
		if (self.validacion_controles() == False):
			return
		else:
			concepto = self.comb_concepto.get()
			precio_unitario = self.tex_precio.get()
			cantidad_producto = self.cantidad.get()
			precio_final = self.tex_monto_total.get()
			egreso_total = self.tex_egreso_total.get()
			comprobante = self.tex_comprobante.cget('text')
			fecha = self.fecha_tex.get("1.0", "end-1c")
			#fecha = 1234

			if self.var_estatus.get() == 1:
				categoria = "Compras"
			else:
				categoria = "Servicios"

			precio_final = self.convertir_formato_numero(precio_final)

			self.model.inserta_pagos(comprobante, fecha, concepto, categoria, cantidad_producto, precio_unitario, precio_final)
			#self.model.inserta_ingreso_total(ingreso_total)
			#self.deshabilita_controles()
			# Visualizamos los datos en el grid
			self.mostrar_conceptos()
			self.mostrar_egresos(fecha)
			self.generar_comprobante()
			self.deshabilita_controles()
			self.tabla.delete(*self.tabla.get_children())
			self.mostrar_ventas_tabla(fecha)
			# Preparamos la pantalla para la siguiente operación

	def mostrar_ventas_tabla(self, fecha):
		for dato in self.model.muestra_compras(fecha):
			self.tabla.insert('', 0, text = '', value = dato)

	def mostrar_conceptos(self):
	    conceptos = self.model.obtener_conceptos_egresos()
  
	    if len(conceptos) > 0:
	        # Actualizar el contenido del combobox de conceptos
	        self.ent_concepto['values'] = conceptos

	def actualizar_conceptos(self, event):
		conceptos = self.model.obtener_conceptos_egresos()
  
		if len(conceptos) > 0:
	        # Actualizar el contenido del combobox de conceptos
			self.ent_concepto['values'] = conceptos

	def mostrar_egresos(self, fecha):
		total_egresos = self.model.obtener_egresos(fecha)
		self.ent_egreso_total.delete(0, 'end')
		self.ent_egreso_total.insert(0, "{:,.2f}".format(total_egresos))

	def validar(self, event):
		if event.keysym != "BackSpace" and event.char not in "0123456789,.":
			return "break"

	def formato_moneda(self, entry):
		try:
			num = float(entry.get().replace(",", ""))
			num_formateado = "{:,.2f}".format(num)
			entry.delete(0, tk.END)
			entry.insert(0, num_formateado)

		except ValueError:
			pass
		self.ent_egreso_total.configure(state="normal")

	def calcular_monto_total(self):
		self.ent_monto_total.configure(state="normal")
		try:
			monto = float(self.tex_precio.get().replace(",", ""))
			cantidad = int(self.cantidad.get())
			total = monto * cantidad
			self.ent_monto_total.delete(0, tk.END)
			self.ent_monto_total.insert(0, "{:,.2f}".format(total))
			self.ent_monto_total.configure(state="disabled")
		except ValueError:
			pass

	def convertir_formato_numero(self, numero_str):
		# Reemplazar comas por nada y puntos por punto decimal
		numero_limpio = numero_str.replace(",", "").replace(".", ".")
        
		try:
			numero_convertido = float(numero_limpio)
			return numero_convertido
		except ValueError:
			return None

	def compras_activa(self):
		self.cantidad.delete(0, tk.END)
		self.cantidad.insert(0, '1')
		self.cantidad.config(state = "disabled")
		self.calcular_monto_total()

	def servicios_activa(self):
		self.cantidad.config(state = "normal")

	def modo_lectura(self, event):
		event.widget.config(state = 'disabled')

	def generar_comprobante(self):
		comprobante_texto = self.tex_comprobante.cget('text')  # Obtener el valor actual del Label como cadena
		comprobante_numero = int(comprobante_texto)  # Convertir la cadena a un número entero
		comprobante_numero += 1  # Incrementar el número
		nuevo_comprobante_texto = "{:04d}".format(comprobante_numero)  # Formatear como cadena con ceros a la izquierda
		self.tex_comprobante.config(text=nuevo_comprobante_texto) 

	def validacion_controles(self):
		if self.ent_concepto.get() == '':
			msg.showerror("Error", "Ingresa un concepto, por favor")
			return False
		elif self.ent_precio.get() == '' or self.ent_precio.get() == '0':
			msg.showerror("Error", "Ingresa el precio, por favor")
			return False
		elif self.cantidad.get() == '' or self.cantidad.get() == '0':
			msg.showerror("Error", "Ingresa una cantidad válidad, por favor")
			return False

	def deshabilita_controles(self):
		self.ent_concepto.configure(state = 'disabled')
		self.ent_precio.configure(state = 'disabled')
		self.ent_monto_total.configure(state = 'disabled')
		self.cantidad.configure(state = 'disabled')
		self.rbt_compras.configure(state = 'disabled')
		self.rbt_servicios.configure(state = 'disabled')

		self.btn_nuevo.configure(state = 'normal')
		self.btn_editar.configure(state = 'normal')
		self.btn_Imprimir.configure(state = 'normal')
		self.btn_registrar.configure(state = 'disabled')
		self.btn_borrar.configure(state = 'disabled')
		self.btn_guardar.configure(state = 'disabled')

	def habilita_controles(self):
		self.ent_concepto.configure(state = 'normal')
		self.ent_precio.configure(state = 'normal')
		self.ent_monto_total.configure(state = 'normal')
		self.cantidad.configure(state = 'normal')
		if self.var_estatus.get() == 1:
			self.cantidad.configure(state = 'normal')
		else:
			self.cantidad.config(state = 'disabled')

		self.rbt_compras.configure(state = 'normal')
		self.rbt_servicios.configure(state = 'normal')

		self.btn_nuevo.configure(state = 'disabled')
		self.btn_editar.configure(state = 'disabled')
		self.btn_Imprimir.configure(state = 'disabled')
		self.btn_registrar.configure(state = 'normal')
		self.btn_borrar.configure(state = 'normal')
		self.btn_guardar.configure(state = 'disabled')
		concepto = self.ent_concepto.get()
		self.ent_concepto.delete(0, 'end')
		self.ent_concepto.insert(0, '')

	def limpia_controles(self):
		concepto = self.ent_concepto.get()
		self.ent_precio.delete(0, 'end')
		self.cantidad.delete(0, 'end')
		self.cantidad.insert(0, '1')
		self.ent_monto_total.delete(0, 'end')
		self.ent_concepto.delete(0, 'end')
		self.ent_concepto.insert(0, concepto)

	def usuario_nuevo(self):
		self.habilita_controles()
		self.limpia_controles()

	def insertar_ultimo_comprobante(self):
		get_comprobante = self.model.cargar_ultimo_comprobante()
		comprobante_texto = "{:04d}".format(get_comprobante)
		self.tex_comprobante.config(text=comprobante_texto)

	def usuario_editar(self):
		if self.tabla.focus() == '':
			msg.showerror("Error", "Selecciona un usuario de la tabla, por favor")
			return

		self.habilita_controles()

		self.item_seleccionado = self.tabla.item(self.tabla.selection())
		t_comprobante = self.item_seleccionado['values'][1]
		self.tex_comprobante.config(text = "{:04d}".format(t_comprobante))
		self.ent_concepto.insert(0, self.item_seleccionado['values'][3])

		if self.item_seleccionado['values'][4] == 'Servicios':
			self.rbt_compras.deselect()
			self.rbt_servicios.select()
			self.cantidad.config(state = 'disabled')
		else:
			self.rbt_compras.select()
			self.rbt_servicios.deselect()
		self.cantidad.delete(0, 'end')
		self.cantidad.insert(0, self.item_seleccionado['values'][5])
		self.ent_precio.insert(0, self.item_seleccionado['values'][6])
		self.id_egreso = self.item_seleccionado['values'][0]
		self.btn_guardar.config(state = 'normal')
		self.btn_registrar.config(state = 'disabled')

	def usuario_guardar(self):
		if (self.validacion_controles() == False):
			return


		# Actualizar la base de datos con los datos modificados
		concepto = self.comb_concepto.get()
		precio_unitario = self.tex_precio.get()
		cantidad_producto = self.cantidad.get()
		precio_final = self.tex_monto_total.get()
		#egreso_total = self.tex_egreso_total.get()
		comprobante = self.tex_comprobante.cget('text')
		fecha = self.fecha_tex.get("1.0", "end-1c")
		#id_egresos = self.id_egreso
		#fecha = 1234

		if self.var_estatus.get() == 1:
			categoria = "Compras"
		else:
			categoria = "Servicios"

		precio_final = self.convertir_formato_numero(precio_final)

		self.model.actualizar_egresos(self.id_egreso, comprobante, fecha, concepto, categoria, cantidad_producto, precio_unitario, precio_final)
		
		# Visualizamos los datos en la tabla
		self.tabla.delete(*self.tabla.get_children())
		self.mostrar_ventas_tabla(fecha)
		# Preparamos la pantalla para la siguiente operación
		self.limpia_controles()
		self.deshabilita_controles()
		self.insertar_ultimo_comprobante()
		self.mostrar_egresos(datetime.now().strftime("%d/%m/%Y"))






# ----------------------------- Funciones para imprimir los datos ------------------------- #
	def imprimir_datos(self):
		if self.tabla.focus() == '':
			msg.showerror("Error", "Selecciona un usuario de la tabla, por favor")
			return

		self.btn_editar.configure(state = 'disabled')
		self.btn_Imprimir.configure(state = 'disabled')
		self.btn_cancelar.configure(state = 'disabled')
		self.btn_registro_completo.configure(state = 'disabled')
		self.item_seleccionado = self.tabla.item(self.tabla.selection())
		id_egreso = self.item_seleccionado['values'][0]
		t_comprobante = self.item_seleccionado['values'][1]
		comprobante = "{:04d}".format(t_comprobante)
		fecha = self.item_seleccionado['values'][2]
		concepto =  self.item_seleccionado['values'][3]
		categoria = self.item_seleccionado['values'][4] 

		cantidad = self.item_seleccionado['values'][5]
		precio = self.item_seleccionado['values'][6]
		precio_final = self.item_seleccionado['values'][7]

		self.frame_2 = tk.LabelFrame(self, text="Registro de Egresos", font = ("Lucida Console",12))
		self.frame_2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
		self.frame_2.config(borderwidth=2, relief="solid")

	    # Configuración del tipo de letra
		font = ("Courier New Bold", 11)
		font2 = ("Courier New", 11)

	    # Creación de las etiquetas y su ubicación en el grid
		Label(self.frame_2, text="\n\n\n\n\n\n\n\n             COMPROBANTE:", font=font).grid(row=1, column=0, sticky= 'e')
		Label(self.frame_2, text="             FECHA:", font=font).grid(row=2, column=0, sticky='e')
		Label(self.frame_2, text="             CONCEPTO:", font=font).grid(row=4, column=0, sticky='e')
		Label(self.frame_2, text="             CATEGORÍA:", font=font).grid(row=3, column=0, sticky='e')
		Label(self.frame_2, text="             CANTIDAD:", font=font).grid(row=5, column=0, sticky='e')
		Label(self.frame_2, text="             PRECIO UNITARIO:", font=font).grid(row=6, column=0, sticky='e')
		Label(self.frame_2, text="             PRECIO FINAL:\n\n\n\n\n\n\n\n\n", font=font).grid(row=7, column=0, sticky='e')
	    
		# Agregar las etiquetas para las firmas
		#Label(self.frame_2, text="      Firma del que entrega\n\n", font=font).grid(row=9, column=0, sticky='W')
		label = Label(self, text="  _______________________________", font=font)
		label.place(x = 180, y = 410)
		#Label(self.frame_2, text="      Firma del cliente     \n\n", font=font).grid(row=9, column = 1, sticky = 'W')
		#Label(self.frame_2, text="   _______________________     ", font=font).grid(row=8, column=1, sticky='E')

		# Creación de las etiquetas y su ubicación en el grid
		#Label(self.frame_2, text="ID:\n", font=font).grid(row=0, column=0, sticky=W)
		Label(self.frame_2, text = "\n\n\n\n\n\n\n\n" + comprobante, font=font2).grid(row=1, column=1, sticky='W')
		Label(self.frame_2, text = fecha, font=font2).grid(row=2, column=1, sticky='W')
		Label(self.frame_2, text = concepto, font=font2).grid(row=4, column=1, sticky='W')
		Label(self.frame_2, text = categoria, font=font2).grid(row=3, column=1, sticky='W')
		Label(self.frame_2, text = cantidad, font=font2).grid(row=5, column=1, sticky='W')
		Label(self.frame_2, text = precio, font=font2).grid(row=6, column=1, sticky='W')
		Label(self.frame_2, text = precio_final + "                     \n\n\n\n\n\n\n\n\n", font=font2).grid(row=7, column=1, sticky='W')

		# Crear la caja de texto
		# Función para cambiar el foco al Label al hacer clic en él
		def on_label_click(event):
		    self.frame_2.focus()

		# Vincular la función al evento <Button-1> (clic del botón izquierdo del ratón)
		self.frame_2.bind("<Button-1>", on_label_click)

		razon = tk.Entry(self.frame_2, borderwidth=0, highlightthickness=0, background = 'gray94', width = 40, fg = 'blue')
		razon.config(justify = 'center')
		razon.place(x = 60, y  = 95)
		motivo = tk.Entry(self, borderwidth=0, highlightthickness=0, background = 'gray94', width = 40, fg = 'blue')
		motivo.config(justify = 'center')
		motivo.place(x = 140, y = 430)

		# Agregar el texto de fondo
		razon.insert(0, "INGRESA TÍTULO O MOTIVO AQUÍ")
		motivo.insert(0, "INGRESA MOTIVO O TITULAR")

		# Función para borrar el texto de fondo al hacer clic en la caja de texto
		def on_entry_click(event):
		    if razon.get() == "INGRESA TÍTULO O MOTIVO AQUÍ":
		        razon.delete(0, 'end')
		        razon.config(fg = 'black', font = ("Courier New Bold", 12))
		def motivo_click(event):
		    if motivo.get() == "INGRESA MOTIVO O TITULAR":
		        motivo.delete(0, 'end')
		        motivo.config(fg = 'black', font = ("Courier New Bold", 12))



		# Vincular la función al evento <Button-1> (clic del botón izquierdo del ratón)
		razon.bind("<Button-1>", on_entry_click)
		motivo.bind("<Button-1>", motivo_click)

		#Cerrar ventana:
		def cerrar_frame(event):
		    self.frame_2.destroy()
		    motivo.destroy()
		    label.destroy()
		    self.btn_editar.configure(state = 'normal')
		    self.btn_Imprimir.configure(state = 'normal')
		    self.btn_cancelar.configure(state = 'normal')
		    self.btn_registro_completo.configure(state = 'normal')


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
		    imagen = ImageGrab.grab((x+ 125, y + 10, x + w - 30, y + h -125 ))

		    # Guardar la imagen en un archivo
		    imagen.save(f"Egreso #{comprobante}-{id_egreso}.png")
		    msg.showinfo("Éxito", f"El comprobante se ha guardado con el nombre:\n                   Egreso #{comprobante}-{id_egreso}")

		btn_imprimir_datos = tk.Button(self.frame_2, text = "Guardar")
		btn_imprimir_datos.bind("<Button-1>", imprimir_labelframe)
		btn_imprimir_datos.place(x = 220, y = 400)


		# ------------------------ Agregar íconos ------------------------ #
	def actualizar_fecha(self):
		now = datetime.now()
		formatted_date = now.strftime("%d/%m/%Y")
		self.fecha_tex.delete("1.0", tk.END)  # Limpiar el contenido actual
		self.fecha_tex.insert(tk.END, formatted_date)
		self.after(1000, self.actualizar_fecha)

	def cancelar(self):
		self.deshabilita_controles()
		self.limpia_controles()


		'''
		self.calendario = DateEntry(self, locale='es_MX', date_pattern='dd/mm/yyyy',
                       background='orange', foreground='black', bordercolor='green',
                       normalbackground='white', normalforeground='black',
                       weekendbackground='white', weekendforeground='red',
                       headersbackground='lightgreen', headersforeground='black')
		self.calendario.place(x = 580, y = 5)
'''


if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	app = registro_egresos(root)
	app.mainloop()