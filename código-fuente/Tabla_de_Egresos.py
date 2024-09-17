# Tabla_de_Egresos
import tkinter as tk
import BD_Login
from tkinter import ttk, filedialog
from datetime import datetime
import BD_Login
from openpyxl import Workbook
import tips_app as Tooltip

class tabla_egresos(tk.Toplevel):
	def __init__(self, master = None):
		super().__init__(master)
		# Creamos una ventana
		self.title("Tabla de egresos")
		self.geometry("720x620")

		self.model = BD_Login.modelo(self)

		# Posicionamos la ventana a la mitad de pantalla
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla/2)-720/2)
		posicion_largo = int((largo_pantalla/2)-620/2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))
		self.config(bg = 'mint cream')

		# Ventanas secundarias
		self.frame_0 = tk.LabelFrame(self)
		self.frame_0.grid(columnspan = 5, column = 0, row = 0, padx = 10, pady = 5)
		self.frame_1 = tk.LabelFrame(self, bg = 'lightyellow')
		self.frame_1.grid(columnspan = 5, column = 0, row = 2, padx = 10)

		# Llamamos a las funciones
		self.crear_widgets()
		self.mostrar_ventas_tabla()
		self.egresos_totales()
		self.actualizar_fecha()



	def crear_widgets(self):

		# -------------------------   LABELS   --------------------------#
		self.titulo = tk.Label(self, text = "REGISTRO DE EGRESOS", font = ("Arial Black", 10), bg = 'mint cream')
		self.titulo.grid(column = 0, row = 1)

		tk.Label(self.frame_0, text = "                           ").grid(column = 3, row = 0, padx = 10)
		tk.Label(self.frame_0, text = "                           ").grid(column = 4, row = 0, padx = 10)
		tk.Label(self.frame_0, text = "                                  ").grid(column = 5, row = 0, padx = 10)
		tk.Label(self.frame_0, text = "Fecha: ", font = ("Arial bold",10)).place(x = 510, y = 17)
		self.fecha_tex = tk.Text(self.frame_0, height = 1, width = 14)
		self.fecha_tex.bind('<FocusIn>', self.modo_lectura)
		self.fecha_tex.bind('<FocusOut>', self.modo_lectura)
		self.fecha_tex.grid(column = 6, row = 0, padx = 15, sticky = "E")


		# ------------------------ BOTONONES --------------------------- #
		self.exportar = tk.Button(self.frame_0, text="Exportar", command = self.exportar_a_excel)
		self.exportar.grid(column = 2, row = 0, ipadx = 10, padx = 5, pady = 15, sticky = "W")

		self.menuPrincipal = tk.Button(self.frame_0, text="Menú Principal", font=("Arial", 11), command = self.master.mostrar_menu_Principal)
		#self.menuPrincipal = tk.Button(self.frame_0, text="Menú Principal")
		self.menuPrincipal.grid(column = 0, row = 0, ipadx = 10, padx = 5, pady = 15, sticky = "W")
		# ------------------------------ TEXT BOX ----------------------------- #
		tk.Label(self.frame_1, text = "Total de egresos: $", font = ("Rockwell", 12), bg = 'lightyellow').place(x = 20, y = 0)
		tex_total_egresos = tk.StringVar()
		self.ent_total_egresos = tk.Entry(self.frame_1, width = 14, textvariable = tex_total_egresos)
		self.ent_total_egresos.bind('<FocusIn>', self.modo_lectura)
		self.ent_total_egresos.bind('<FocusOut>', self.modo_escritura)
		self.ent_total_egresos.config(font = ("Courier New Bold", 12))
		self.ent_total_egresos.place(x = 165, y = 4)


		tk.Label(self.frame_1, text = "").grid(column = 0, row = 0)

		self.tex_buscar = tk.StringVar()
		self.ent_buscar = tk.Entry(self, width = 20, font = ("Arial", 9), textvariable = self.tex_buscar)
		self.ent_buscar.insert(0, "Buscar")
		self.ent_buscar.config(fg = 'gray')
		self.ent_buscar.bind('<KeyRelease>', self.buscar)
		self.ent_buscar.bind('<FocusIn>', self.click_entry)
		self.ent_buscar.bind('<FocusOut>', self.no_click_entry)
		self.ent_buscar.place(x = 510, y = 110)

		# ------------------------------ TREEVIEW ----------------------------- #
		#  TABLA REGISTRADA EN LA BASE DE DATOS DE LA TRANSACCIÓN POR PERSONA
		#self.frame_tabla = tk.Frame(self.frame_1)
		#self.frame_tabla.grid(columnspan = 6, row = 1, sticky = "W", padx = 10, pady = 5)
		self.tabla = ttk.Treeview(self.frame_1, height = 18)
		self.tabla.grid(column = 0, row = 2, padx = 10, pady = 15)
		ladox = tk.Scrollbar(self.frame_1, orient = tk.HORIZONTAL, command = self.tabla.xview)
		ladox.grid(column = 0, row = 3, sticky = "ew")
		ladoy = tk.Scrollbar(self.frame_1, orient = tk.VERTICAL, command = self.tabla.yview)
		ladoy.grid(column = 1, row = 2, pady = 15, sticky = "ns")

		self.tabla['columns'] = ('FOLIO', 'FECHA', 'CATEGORÍA', 'CONCEPTO', 'CANTIDAD', 'PRECIO UNITARIO', 'PRECIO FINAL')
		
		self.tabla.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('FOLIO', minwidth = 70, width = 70, anchor = 'center')
		self.tabla.column('FECHA', minwidth = 70, width = 70, anchor = 'center')
		self.tabla.column('CATEGORÍA', minwidth = 70, width = 90, anchor = 'center')
		self.tabla.column('CONCEPTO', minwidth = 80, width = 120, anchor = 'center', stretch = True)
		self.tabla.column('CANTIDAD', minwidth = 60, width = 90, anchor = 'center', stretch = True)
		self.tabla.column('PRECIO UNITARIO', minwidth = 60, width = 90, anchor = 'center')
		self.tabla.column('PRECIO FINAL', minwidth = 80, width = 80, anchor = 'center')

		self.tabla.heading('#0', anchor = 'center')
		self.tabla.heading('FOLIO', text = 'FOLIO', anchor = 'center')
		self.tabla.heading('FECHA', text = 'FECHA', anchor = 'center')
		self.tabla.heading('CATEGORÍA', text = 'CATEGORÍA', anchor = 'center')
		self.tabla.heading('CONCEPTO', text = 'CONCEPTO', anchor = 'center')
		self.tabla.heading('CANTIDAD', text = 'CANTIDAD', anchor = 'center')
		self.tabla.heading('PRECIO UNITARIO', text = 'PRECIO UNITARIO', anchor = 'center')
		self.tabla.heading('PRECIO FINAL', text = 'PRECIO FINAL', anchor = 'center')

	def mostrar_ventas_tabla(self):
		for dato in self.model.muestra_todos_egresos():
			self.tabla.insert('', 0, text = '', value = dato)

	def egresos_totales(self):
		egreso_total = self.model.obtener_egresos_totales()
		self.ent_total_egresos.delete(0, 'end')
		if egreso_total is not None:
		    self.ent_total_egresos.insert(0, "{:,.2f}".format(egreso_total))
		else:
			self.ent_total_egresos.insert(0, '')

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

	def actualizar_fecha(self):
		now = datetime.now()
		formatted_date = now.strftime("%d/%m/%Y")
		self.fecha_tex.delete("1.0", tk.END)  # Limpiar el contenido actual
		self.fecha_tex.insert(tk.END, formatted_date)

	def modo_lectura(self, event):
		event.widget.config(state = 'disabled')

	def modo_escritura(self, event):
		event.widget.config(state = 'normal')

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

	def buscar_en_tabla(self, tabla, valor):
	    for item in tabla.get_children():
	        if valor in tabla.item(item, 'values'):
	            return item
	    return None

	def buscar(self, event):
	    valor = self.ent_buscar.get()
	    if not valor:
	    	self.tabla.delete(*self.tabla.get_children())
	    	self.mostrar_ventas_tabla()

	    else:
	        for item in self.tabla.get_children():
	        	values = [str(v) for v in self.tabla.item(item, 'values')]
	        	if any(valor.lower() in v.lower() or valor in v for v in values):
			        self.tabla.reattach(item, '', 'end')
	        	else:
			        self.tabla.detach(item)
	    self.egresos_totales()



if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	app = tabla_egresos(root)
	app.mainloop()