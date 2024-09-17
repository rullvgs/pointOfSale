# Tabla_de_ingresos.py
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime
import BD_Login
from openpyxl import Workbook

class tabla_ventas(tk.Toplevel):
	def __init__(self, master = None):
		super().__init__(master)
		# Creamos una ventana
		self.title("Tabla de ventas")
		self.geometry("860x620")

		self.model = BD_Login.modelo(self)

		# Posicionamos la ventana a la mitad de pantalla
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla/2)-850/2)
		posicion_largo = int((largo_pantalla/2)-620/2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))
		self.config(bg = 'mint cream')

		# Ventanas secundarias
		self.frame_0 = tk.LabelFrame(self)
		self.frame_0.grid(columnspan = 6, column = 0, row = 0, padx = 10, pady = 5)
		self.frame_1 = tk.LabelFrame(self,  bg = 'lightyellow')
		self.frame_1.grid(columnspan = 6, column = 0, row = 1, padx = 10)
		#self.frame_2 = tk.LabelFrame(self)
		#self.frame_2.grid(columnspan = 6, column = 2, row = 2, padx = 15)

		# Variables globales
		fecha_actual = datetime.now()
		self.fecha = fecha_actual.strftime("%d/%m/%Y")
		self.team_listbox = ttk.Combobox(self.frame_1)
		self.seleccion = tk.Label(self.frame_1, text = "Selecciona un equipo:", font = ("Arial bold", 8))
		self.llave = 1

		# Llamamos a las funciones
		self.crear_widgets()
		self.mostrar_ventas_tabla()
		self.actualizar_fecha()
		self.actualizar_ingresos()
		#self.mostrar_tabla_integrante()
		#self.mostrar_por_equipo()
		#self.mostrar_ventas_tabla_por_fecha(fecha)

	def crear_widgets(self):

		# -------------------------   LABELS   --------------------------#
		self.titulo = tk.Label(self.frame_1, text = "REGISTRO DE INGRESOS", font = ("Arial Black", 10), bg = 'lightyellow')
		self.titulo.place(x = 10, y = 0)

		tk.Label(self.frame_1, text = "                                    ", bg = 'lightyellow').grid(column = 2, row = 0, padx = 10)
		tk.Label(self.frame_0, text = "                                                 ").grid(column = 2, row = 0, padx = 10)
		tk.Label(self.frame_0, text = "                           ").grid(column = 4, row = 0, padx = 10)
		tk.Label(self.frame_0, text = "                                ").grid(column = 5, row = 0, padx = 10)
		tk.Label(self.frame_0, text = "                                                 ").grid(column = 6, row = 0, padx = 10)
		tk.Label(self.frame_0, text = "                                                Fecha:", font = ("Arial bold",10)).grid(column = 5, row = 0, padx = 10)

		self.fecha_tex = tk.Text(self.frame_0, height = 1, width = 14)
		self.fecha_tex.bind('<FocusIn>', self.modo_lectura)
		self.fecha_tex.grid(column = 6, row = 0, padx = 15, sticky = "W")

		# ------------------------ BOTONONES --------------------------- #

		self.exportar = tk.Button(self.frame_0, text="Exportar", font=("Arial", 11), command = self.exportar_a_excel)
		self.exportar.grid(column = 2, row = 0, padx = 5, pady = 15, sticky = "W")
		Tooltip = (self.exportar, "Se guarda en un archivo exel \n (Solo se guardan los datos mostrados en la tabla)")



		self.menuPrincipal = tk.Button(self.frame_0, text="Menú Principal", font=("Arial", 11), command = self.master.mostrar_menu_Principal)
		#self.menuPrincipal = tk.Button(self.frame_0, text="Menú Principal", font=("Arial", 11))
		self.menuPrincipal.grid(column = 0, row = 0, padx = 5, pady = 15, sticky = "W")

		tk.Label(self.frame_1, text = "Ver por: ", font = ("Arial bold", 10), fg = 'Blue4', bg = 'lightyellow').place(x = 280, y = 1)
		self.btn_filtro = tk.Button(self.frame_1, text = "Equipos", width = 8, command = self.mostrar_por_equipo)
		self.btn_filtro.place(x = 460, y = 0)

		self.btn_editar = tk.Button(self.frame_1, text = "Integrantes", command = self.mostrar_tabla_integrante)
		self.btn_editar.place(x = 540, y = 0)

		self.gen_reporte = tk.Button(self.frame_1, text="Registro General", command = self.mostrar_registro_general)
		self.gen_reporte.place(x = 350, y = 0)

		# ------------------------------ TEXT BOX ----------------------------- #

		def check_entry(entry, size):
		    text = entry.get()
		    if len(text) > size or not text.isdigit():
		        entry.delete(0, tk.END)
		        entry.insert(0, text[:-1])
		    elif len(text) == size:
		        entry.tk_focusNext().focus()
		'''
		dia_entry = tk.Entry(self.frame_2, width=2)
		dia_entry.grid(column = 6, row = 1)
		dia_entry.bind("<KeyRelease>", lambda e: check_entry(dia_entry, 2))

		slash_label = tk.Label(self.frame_2, text="/")
		slash_label.grid(column = 7, row = 1)

		mes_entry = tk.Entry(self.frame_2, width=2)
		mes_entry.grid(column = 8, row = 1)
		mes_entry.bind("<KeyRelease>", lambda e: check_entry(mes_entry, 2))

		slash_label = tk.Label(self.frame_2, text="/")
		slash_label.grid(column = 9, row = 1)

		año_entry = tk.Entry(self.frame_2, width=5)
		año_entry.grid(column = 10, row = 1)
		año_entry.bind("<KeyRelease>", lambda e: check_entry(año_entry, 4))
		'''

		tk.Label(self.frame_1, text = "Total de ingresos:  $", font = ("Rockwell", 12), bg = 'lightyellow').grid(column = 0, row = 1, pady = 10, sticky = "E")
		tex_total_ingresos = tk.StringVar()
		self.ent_total_ingresos = tk.Entry(self.frame_1, width = 14, textvariable = tex_total_ingresos, font = 10)
		self.ent_total_ingresos.bind('<FocusIn>', self.modo_lectura)
		self.ent_total_ingresos.bind('<FocusOut>', self.modo_escritura)
		self.ent_total_ingresos.grid(column = 1, row = 1, sticky = "W")

		self.tex_buscar = tk.StringVar()
		self.ent_buscar = tk.Entry(self, width = 20, font = ("Arial", 10), textvariable = self.tex_buscar)
		self.ent_buscar.insert(0, "Buscar")
		self.ent_buscar.config(fg = 'gray')
		self.ent_buscar.bind('<KeyRelease>', self.buscar)
		self.ent_buscar.bind('<FocusIn>', self.click_entry)
		self.ent_buscar.bind('<FocusOut>', self.no_click_entry)
		self.ent_buscar.place(x = 480, y = 140)

		# ------------------------------ TREEVIEW ----------------------------- #
		#  TABLA REGISTRADA EN LA BASE DE DATOS DE LA TRANSACCIÓN POR PERSONA
		self.frame_tabla = tk.Frame(self.frame_1)
		self.frame_tabla.grid(columnspan = 6, row = 2, sticky = "W", padx = 10, pady = 5)
		self.tabla = ttk.Treeview(self.frame_tabla, height = 18)
		self.tabla.grid(column = 0, row = 0, padx = 10, pady = 16)
		self.ladox = tk.Scrollbar(self.frame_tabla, orient = tk.HORIZONTAL, command = self.tabla.xview)
		self.ladox.grid(column = 0, row = 1, sticky = "ew")
		self.ladoy = tk.Scrollbar(self.frame_tabla, orient = tk.VERTICAL, command = self.tabla.yview)
		self.ladoy.grid(column = 1, row = 0, pady = 15, sticky = "ns")

		self.tabla['columns'] = ('N°', 'FECHA', 'EQUIPO', 'MONTO TOTAL DEL EQUIPO', 'INTEGRANTE', 'IMPORTE TOTAL DEL INTEGRANTE')
		
		self.tabla.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('N°', minwidth = 30, width = 30, anchor = 'center')
		self.tabla.column('FECHA', minwidth = 70, width = 70, anchor = 'center')
		self.tabla.column('EQUIPO', minwidth = 100, width = 160, anchor = 'center', stretch = True)	
		self.tabla.column('MONTO TOTAL DEL EQUIPO', minwidth = 80, width = 80, anchor = 'center', stretch = True)
		self.tabla.column('INTEGRANTE', minwidth = 100, width = 160, anchor = 'center', stretch = True)
		self.tabla.column('IMPORTE TOTAL DEL INTEGRANTE', minwidth = 80, width = 80, anchor = 'center')
		

		self.tabla.heading('#0', anchor = 'center')
		self.tabla.heading('N°', text = 'N°', anchor = 'center')
		self.tabla.heading('FECHA', text = 'FECHA', anchor = 'center')		
		self.tabla.heading('EQUIPO', text = 'EQUIPO', anchor = 'center')
		self.tabla.heading('MONTO TOTAL DEL EQUIPO', text = 'MONTO TOTAL DEL EQUIPO', anchor = 'center')
		self.tabla.heading('INTEGRANTE', text = 'INTEGRANTE', anchor = 'center')
		self.tabla.heading('IMPORTE TOTAL DEL INTEGRANTE', text = 'IMPORTE TOTAL DEL INTEGRANTE', anchor = 'center')
	
	def mostrar_registro_general(self):
		self.ent_buscar.destroy()
		self.frame_1.destroy()
		self.frame_1 = tk.LabelFrame(self, bg = 'lightyellow')
		self.frame_1.grid(columnspan = 6, column = 0, row = 1, padx = 10)

		self.team_listbox = ttk.Combobox(self.frame_1)
		self.seleccion = tk.Label(self.frame_1, text = "Selecciona un equipo:", font = ("Arial bold", 10), bg = 'lightyellow')

		self.tex_buscar = tk.StringVar()
		self.ent_buscar = tk.Entry(self, width = 20, font = ("Arial", 10), textvariable = self.tex_buscar)
		self.ent_buscar.insert(0, "Buscar")
		self.ent_buscar.config(fg = 'gray')
		self.ent_buscar.bind('<KeyRelease>', self.buscar)
		self.ent_buscar.bind('<FocusIn>', self.click_entry)
		self.ent_buscar.bind('<FocusOut>', self.no_click_entry)
		self.ent_buscar.place(x = 480, y = 140)

		tk.Label(self.frame_1, text = "Ver por: ", font = ("Arial bold", 10), fg = 'Blue4', bg = 'lightyellow').place(x = 280, y = 1)
		self.btn_filtro = tk.Button(self.frame_1, text = "Equipos", width = 8, command = self.mostrar_por_equipo)
		self.btn_filtro.place(x = 460, y = 0)

		self.btn_editar = tk.Button(self.frame_1, text = "Integrantes", command = self.mostrar_tabla_integrante)
		self.btn_editar.place(x = 540, y = 0)

		self.gen_reporte = tk.Button(self.frame_1, text="Registro General", command = self.mostrar_registro_general)
		self.gen_reporte.place(x = 350, y = 0)
		self.geometry("860x620")
		self.titulo = tk.Label(self.frame_1, text = "REGISTRO DE INGRESOS", font = ("Arial Black", 10), bg = 'lightyellow')
		self.titulo.place(x = 10, y = 0)

		tk.Label(self.frame_1, text = "",bg = 'lightyellow').grid(column = 6, row = 0, padx = 10)

		tk.Label(self.frame_1, text = "Total de ingresos:  $", font = ("Rockwell", 12), bg = 'lightyellow').grid(column = 0, row = 1, pady = 10, sticky = "E")
		tex_total_ingresos = tk.StringVar()
		self.ent_total_ingresos = tk.Entry(self.frame_1, width = 14, textvariable = tex_total_ingresos, font = 10)
		self.ent_total_ingresos.bind('<FocusIn>', self.modo_lectura)
		self.ent_total_ingresos.bind('<FocusOut>', self.modo_escritura)
		self.ent_total_ingresos.grid(column = 1, row = 1, sticky = "W")
		self.actualizar_ingresos()

		self.llave = 1
		self.tabla.destroy()
		self.ladox.destroy()
		self.ladoy.destroy()
		self.team_listbox.destroy()
		self.seleccion.destroy()
		# ------------------------------ TREEVIEW ----------------------------- #
		#  TABLA REGISTRADA EN LA BASE DE DATOS DE LA TRANSACCIÓN POR PERSONA
		self.frame_tabla = tk.Frame(self.frame_1)
		self.frame_tabla.grid(columnspan = 6, column = 0, row = 2, sticky = "W", padx = 10, pady = 5)
		self.tabla = ttk.Treeview(self.frame_tabla, height = 18)
		self.tabla.grid(column = 0, row = 0, padx = 10, pady = 16)
		self.ladox = tk.Scrollbar(self.frame_tabla, orient = tk.HORIZONTAL, command = self.tabla.xview)
		self.ladox.grid(column = 0, row = 1, sticky = "ew")
		self.ladoy = tk.Scrollbar(self.frame_tabla, orient = tk.VERTICAL, command = self.tabla.yview)
		self.ladoy.grid(column = 1, row = 0, pady = 15, sticky = "ns")

		self.tabla['columns'] = ('N°', 'FECHA', 'EQUIPO', 'MONTO TOTAL DEL EQUIPO', 'INTEGRANTE', 'IMPORTE TOTAL DEL INTEGRANTE')
		
		self.tabla.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('N°', minwidth = 30, width = 30, anchor = 'center')
		self.tabla.column('FECHA', minwidth = 70, width = 70, anchor = 'center')
		self.tabla.column('EQUIPO', minwidth = 100, width = 160, anchor = 'center', stretch = True)	
		self.tabla.column('MONTO TOTAL DEL EQUIPO', minwidth = 80, width = 80, anchor = 'center', stretch = True)
		self.tabla.column('INTEGRANTE', minwidth = 100, width = 160, anchor = 'center', stretch = True)
		self.tabla.column('IMPORTE TOTAL DEL INTEGRANTE', minwidth = 80, width = 80, anchor = 'center')
		

		self.tabla.heading('#0', anchor = 'center')
		self.tabla.heading('N°', text = 'N°', anchor = 'center')
		self.tabla.heading('FECHA', text = 'FECHA', anchor = 'center')		
		self.tabla.heading('EQUIPO', text = 'EQUIPO', anchor = 'center')
		self.tabla.heading('MONTO TOTAL DEL EQUIPO', text = 'MONTO TOTAL DEL EQUIPO', anchor = 'center')
		self.tabla.heading('INTEGRANTE', text = 'INTEGRANTE', anchor = 'center')
		self.tabla.heading('IMPORTE TOTAL DEL INTEGRANTE', text = 'IMPORTE TOTAL DEL INTEGRANTE', anchor = 'center')
		self.mostrar_ventas_tabla()

	def mostrar_ventas_tabla_por_fecha(self, fecha):

		equipo_anterior = None
		numero_fila = 1
		for dato in self.model.obtener_datos_por_fecha(fecha):
		    if dato[2] != equipo_anterior:
		        self.tabla.insert('', 'end', text = '', value = (numero_fila, dato[0], dato[1], dato[2], dato[3], dato[4]))
		        equipo_anterior = dato[2]
		    else:
		        self.tabla.insert('', 'end', text = '', value = (numero_fila, dato[0], dato[1], '', dato[3], dato[4]))
		    numero_fila += 1

		'''equipo_anterior = None
		numero_fila = 1
		for dato in self.model.obtener_datos_por_fecha(fecha):
		    if dato[2] != equipo_anterior:
		        self.tabla.insert('', 'end', text = '', value = (numero_fila, dato[0], dato[1], dato[2], dato[3], dato[4]))
		        equipo_anterior = dato[2]
		    else:
		        self.tabla.insert('', 'end', text = '', value = (numero_fila, dato[0], dato[1], '', dato[3], dato[4]))
		    numero_fila += 1

		'''

	def mostrar_ventas_tabla(self):
		equipo_anterior = None
		numero_fila = 1
		for dato in self.model.obtener_datos():
		    if dato[2] != equipo_anterior:
		        self.tabla.insert('', 'end', text = '', value = (numero_fila, dato[0], dato[1], dato[2], dato[3], dato[4]))
		        equipo_anterior = dato[2]
		    else:
		        self.tabla.insert('', 'end', text = '', value = (numero_fila, dato[0], dato[1], '', dato[3], dato[4]))
		    numero_fila += 1

	def buscar_en_tabla(self, tabla, valor):
	    for item in tabla.get_children():
	        if valor in tabla.item(item, 'values'):
	            return item
	    return None

	def buscar(self, event):
	    valor = self.ent_buscar.get()
	    if not valor:
	    	self.tabla.delete(*self.tabla.get_children())
	    	if self.llave == 1:
	    		# Visualizamos los datos nuevamente
	    		self.mostrar_ventas_tabla()
	    	elif self.llave == 2:
	    		contador = 1
	    		for dato in self.model.muestra_ventas_sin_fecha():
				    self.tabla.insert('', 'end', text=str(contador), values=dato)
				    contador += 1
	    	elif self.llave == 3:
	    		self.compras_integrantes(None)

	    else:
	        for item in self.tabla.get_children():
	        	values = [str(v) for v in self.tabla.item(item, 'values')]
	        	if any(valor.lower() in v.lower() or valor in v for v in values):
			        self.tabla.reattach(item, '', 'end')
	        	else:
			        self.tabla.detach(item)

	def click_entry(self, event):
		if self.ent_buscar.get() == 'Buscar':
			self.ent_buscar.delete(0, tk.END)
			self.ent_buscar.insert(0, '')
			self.ent_buscar.config(fg = 'black')

	def no_click_entry(self, event):
		if self.ent_buscar.get() == '':
			self.ent_buscar.delete(0, tk.END)
			self.ent_buscar.insert(0, 'Buscar')
			self.ent_buscar.config(fg = 'gray')

	def actualizar_ingresos(self):
		ingreso = self.model.ingresos_totales()
		self.ent_total_ingresos.delete(0, 'end')
		if ingreso is not None:
		    self.ent_total_ingresos.insert(0, "{:,.2f}".format(ingreso))
		else:
		    pass

	def modo_lectura(self, event):
		event.widget.config(state = 'disabled')

	def modo_escritura(self, event):
		event.widget.config(state = 'normal')

	def mostrar_tabla_integrante(self):
		self.actualizar_ingresos()
		self.geometry("890x620")
		self.ladox.destroy()
		self.ladoy.destroy()
		self.team_listbox.destroy()
		self.seleccion.destroy()
		# ------------------------------ TREEVIEW ----------------------------- #
		#  TABLA REGISTRADA EN LA BASE DE DATOS DE LA TRANSACCIÓN POR PERSONA
		self.llave = 2
		self.tabla.destroy()
		self.frame_tabla = tk.Frame(self.frame_1)
		self.frame_tabla.grid(columnspan = 6, row = 2, sticky = "W", padx = 10, pady = 5)
		self.tabla = ttk.Treeview(self.frame_tabla, height = 18)
		self.tabla.grid(column = 0, row = 0, padx = 10)
		self.ladox = tk.Scrollbar(self.frame_tabla, orient = tk.HORIZONTAL, command = self.tabla.xview)
		self.ladox.grid(column = 0, row = 1, sticky = "ew")
		self.ladoy = tk.Scrollbar(self.frame_tabla, orient = tk.VERTICAL, command = self.tabla.yview)
		self.ladoy.grid(column = 1, row = 0, sticky = "ns")

		self.tabla['columns'] = ('', 'FECHA', 'FOLIO', 'NOMBRE DEL INTEGRANTE', 'CONCEPTO', 'SUBCONCEPTO', 'CANTIDAD', 'MONTO', 'TOTAL')		
		self.tabla.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('', minwidth = 0, width = 0, anchor = 'center')
		#self.tabla.column('ID', minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('FECHA', minwidth = 65, width = 65, anchor = 'center')
		self.tabla.column('FOLIO', minwidth = 50, width = 50, anchor = 'center')
		self.tabla.column('NOMBRE DEL INTEGRANTE', minwidth = 180, width = 200, anchor = 'center', stretch = True)
		self.tabla.column('CONCEPTO', minwidth = 80, width = 120, anchor = 'center', stretch = True)
		self.tabla.column('SUBCONCEPTO', minwidth = 60, width = 120, anchor = 'center', stretch = True)
		self.tabla.column('CANTIDAD', minwidth = 60, width = 60, anchor = 'center')
		self.tabla.column('MONTO', minwidth = 60, width = 80, anchor = 'center')
		self.tabla.column('TOTAL', minwidth = 80, width = 80, anchor = 'center')

		self.tabla.heading('#0', anchor = 'center')
		self.tabla.heading('', text = 'N°', anchor = 'center')
		#self.tabla.heading('ID', anchor = 'center')
		self.tabla.heading('FECHA', text = 'FECHA', anchor = 'center')
		self.tabla.heading('FOLIO', text = 'FOLIO', anchor = 'center')
		self.tabla.heading('NOMBRE DEL INTEGRANTE', text = 'NOMBRE DEL INTEGRANTE', anchor = 'center')
		self.tabla.heading('CONCEPTO', text = 'CONCEPTO', anchor = 'center')
		self.tabla.heading('SUBCONCEPTO', text = 'SUBCONCEPTO', anchor = 'center')
		self.tabla.heading('CANTIDAD', text = 'CANTIDAD', anchor = 'center')
		self.tabla.heading('MONTO', text = 'MONTO \n UNITARIO', anchor = 'center')
		self.tabla.heading('TOTAL', text = 'TOTAL', anchor = 'center')

		self.tabla.delete(*self.tabla.get_children())
		contador = 1
		for dato in self.model.muestra_ventas_sin_fecha():
		    self.tabla.insert('', 'end', text=str(contador), values=dato)
		    contador += 1

	def mostrar_por_equipo(self):
		self.actualizar_ingresos()
		self.geometry("890x620")
		self.llave = 3
		self.tabla.destroy()
		self.ladox.destroy()
		self.ladoy.destroy()
		self.frame_tabla = tk.Frame(self.frame_1)
		self.frame_tabla.grid(columnspan = 6, row = 2, sticky = "W", padx = 10, pady = 5)
		self.tabla = ttk.Treeview(self.frame_tabla, height = 18)
		self.tabla.grid(column = 0, row = 0, padx = 10)
		self.ladox = tk.Scrollbar(self.frame_tabla, orient = tk.HORIZONTAL, command = self.tabla.xview)
		self.ladox.grid(column = 0, row = 1, sticky = "ew")
		self.ladoy = tk.Scrollbar(self.frame_tabla, orient = tk.VERTICAL, command = self.tabla.yview)
		self.ladoy.grid(column = 1, row = 0, sticky = "ns")

		self.tabla['columns'] = ('', 'FECHA', 'FOLIO', 'NOMBRE DEL INTEGRANTE', 'CONCEPTO', 'SUBCONCEPTO', 'CANTIDAD', 'MONTO', 'TOTAL')		
		self.tabla.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('', minwidth = 0, width = 0, anchor = 'center')
		#self.tabla.column('ID', minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('FECHA', minwidth = 65, width = 65, anchor = 'center')
		self.tabla.column('FOLIO', minwidth = 50, width = 50, anchor = 'center')
		self.tabla.column('NOMBRE DEL INTEGRANTE', minwidth = 180, width = 200, anchor = 'center', stretch = True)
		self.tabla.column('CONCEPTO', minwidth = 80, width = 120, anchor = 'center', stretch = True)
		self.tabla.column('SUBCONCEPTO', minwidth = 60, width = 120, anchor = 'center', stretch = True)
		self.tabla.column('CANTIDAD', minwidth = 60, width = 60, anchor = 'center')
		self.tabla.column('MONTO', minwidth = 60, width = 80, anchor = 'center')
		self.tabla.column('TOTAL', minwidth = 80, width = 80, anchor = 'center')

		self.tabla.heading('#0', anchor = 'center')
		self.tabla.heading('', text = 'N°', anchor = 'center')
		#self.tabla.heading('ID', anchor = 'center')
		self.tabla.heading('FECHA', text = 'FECHA', anchor = 'center')
		self.tabla.heading('FOLIO', text = 'FOLIO', anchor = 'center')
		self.tabla.heading('NOMBRE DEL INTEGRANTE', text = 'NOMBRE DEL INTEGRANTE', anchor = 'center')
		self.tabla.heading('CONCEPTO', text = 'CONCEPTO', anchor = 'center')
		self.tabla.heading('SUBCONCEPTO', text = 'SUBCONCEPTO', anchor = 'center')
		self.tabla.heading('CANTIDAD', text = 'CANTIDAD', anchor = 'center')
		self.tabla.heading('MONTO', text = 'MONTO \n UNITARIO', anchor = 'center')
		self.tabla.heading('TOTAL', text = 'TOTAL', anchor = 'center')

		nombre_equipo = self.model.obtener_equipos()
		self.team_listbox = ttk.Combobox(self.frame_1)
		self.seleccion = tk.Label(self.frame_1, text = "Selecciona un equipo:", font = ("Arial bold", 10), bg = 'lightyellow')
		self.seleccion.grid(column = 2, row = 1, sticky = "E")
		self.team_listbox.config(values = nombre_equipo)
		self.team_listbox.grid(column = 3, row = 1)
		self.team_listbox.bind("<<ComboboxSelected>>", self.compras_integrantes)

	def compras_integrantes(self, event):
		equipo = self.team_listbox.get()
		self.tabla.delete(*self.tabla.get_children())
		contador = 1
		for dato in self.model.muestra_compras_integrantes(equipo):
		    self.tabla.insert('', 'end', text=str(contador), values=dato)
		    contador += 1




		# ------------------------ Agregar íconos ------------------------ #

	def actualizar_fecha(self):
		now = datetime.now()
		formatted_date = now.strftime("%d/%m/%Y")
		self.fecha_tex.delete("1.0", tk.END)  # Limpiar el contenido actual
		self.fecha_tex.insert(tk.END, formatted_date)

	def exportar_a_excel(self):
	    archivo_excel = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")])

	    if archivo_excel:
	        wb = Workbook()
	        ws = wb.active

	        # Escribir encabezados de columna
	        encabezados = [self.tabla.heading(column)["text"] for column in self.tabla["columns"]]
	        ws.append(encabezados)

	        # Escribir datos de las filas
	        for fila in self.tabla.get_children():
	            valores = [self.tabla.item(fila, "values")[indice] for indice in range(len(encabezados))]
	            ws.append(valores)

	    wb.save(archivo_excel)
	    wb.close()



		

if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	app = tabla_ventas(root)
	app.mainloop()

