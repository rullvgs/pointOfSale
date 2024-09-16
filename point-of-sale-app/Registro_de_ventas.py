import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import simpledialog
from tooltip import Tooltip

def abrir_registro_ventas():
	# Creamos una ventana
	ventana = tk.Tk()
	ventana.title("Registro de ventas")
	ventana.geometry("500x520")

	# Posicionamos la ventana a la mitad de pantalla
	ancho_pantalla = ventana.winfo_screenwidth()
	largo_pantalla = ventana.winfo_screenheight()
	posicion_ancho = int((ancho_pantalla/2)-500/2)
	posicion_largo = int((largo_pantalla/2)-520/2)
	ventana.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

	# ------------ FRAME SECUNDARIOS ---------------- #
	frame_supconceptos = tk.Frame(ventana, width=250, height=260)
	frame_supconceptos.place(x=0, y=230)
	#------------- Functions ------------- #
	'''
	def ent_click(event):
		if ent_buscar.get() == 'Buscar':
			ent_buscar.delete(0, 'end')
			ent_buscar.insert(0, '')
			ent_buscar.config(fg = 'black')

	def ent_no_click(event):
		if ent_buscar.get() == '':
			ent_buscar.insert(0, 'Buscar')
			ent_buscar.config(fg = 'gray')
	'''
	ent_subconceptos = []
	tex_subconceptos = []
	ent_monto_subconceptos = []
	monto_subconceptos = []

	def agregar_subconcepto():
	    subconcepto = simpledialog.askstring("Subconcepto", "Ingresa el nombre del subconcepto:")
	    if subconcepto:
	        tex_subconcepto = tk.StringVar(value=subconcepto)
	        ent_subconcepto = tk.Entry(frame_supconceptos, font=12, width=10, textvariable=tex_subconcepto, state="readonly")
	        ent_subconcepto.bind("<Double-Button-1>", lambda event: ent_subconcepto.config(state="normal"))
	        ent_subconcepto.bind("<FocusOut>", lambda event: ent_subconcepto.config(state="readonly"))
	        ent_subconcepto.place(x=40, y=25 + len(ent_subconceptos) * 25)
	        tex_subconceptos.append(tex_subconcepto)
	        ent_subconceptos.append(ent_subconcepto)

	        monto_subconcepto = tk.StringVar()
	        ent_monto_subconcepto = tk.Entry(frame_supconceptos, font=12, width=10, textvariable=monto_subconcepto)
	        ent_monto_subconcepto.insert(0, '')
	        ent_monto_subconcepto.place(x=136, y=25 + len(ent_monto_subconceptos) * 25)
	        monto_subconceptos.append(monto_subconcepto)
	        ent_monto_subconceptos.append(ent_monto_subconcepto)



	#------------------ TEXTO (LABELS) ----------------------- #
	equipo = tk.Label(ventana, text = "Equipo: ", font = ("Arial bold", 12))
	equipo.place(x = 72, y = 50)

	persona = tk.Label(ventana, text = "Persona:", font =  ("Arial bold", 12))
	persona.place(x =62, y = 100)

	concepto = tk.Label(ventana, text = "Concepto: ", font = ("Arial bold", 12))
	concepto.place(x = 51, y = 150)

	subconceptos = tk.Label(ventana, text = "Subconceptos: ", font = ("Arial bold", 12))
	subconceptos.place(x = 15, y = 200)

	importe_p = tk.Label(ventana, text = "Importe: ", font = ("Arial", 12))
	importe_p.place(x = 350, y = 200)

	importe_team = tk.Label(ventana, text = "Importe total del equipo: ", font = ("Arial", 12))
	importe_team.place(x = 300, y = 290)


	# -------------------------------- COMBOBOX ----------------------------------------
	comb_equipo_var = tk.StringVar()
	ent_comb_equipo = ttk.Combobox(ventana, width=18, textvariable= comb_equipo_var)
	ent_comb_equipo.place(x = 142, y = 52)
	ent_comb_equipo.configure(values=("Nombre EQUIPO ","EQUIPO Nombre", "EQUIPO2 Nombre 2"))
	ent_comb_equipo.current(0)

	comb_persona_var = tk.StringVar()
	ent_comb_persona = ttk.Combobox(ventana, width=18, textvariable= comb_persona_var)
	ent_comb_persona.place(x = 142, y = 102)
	ent_comb_persona.configure(values=("Nombre Apellido ","Apellido Nombre", "Apellido2 Nombre 2"))
	ent_comb_persona.current(0)

	comb_concepto_var = tk.StringVar()
	ent_comb_concepto = ttk.Combobox(ventana, width=18, textvariable= comb_concepto_var)
	ent_comb_concepto.place(x = 142, y = 152)
	ent_comb_concepto.configure(values=("CONCEPTO 1","CONCEPTO2", "CONCEPTO3"))
	ent_comb_concepto.current(0)

	# ---------------- CAJAS DE TEXTO (textBox) ------------------------ #
	tex_importe_p = tk.StringVar()
	ent_importe_p = tk.Entry(ventana, font = 12, width = 14, textvariable = tex_importe_p)
	ent_importe_p.place(x = 320, y = 230)

	tex_sub_equipo = tk.StringVar()
	ent_sub_equipo = tk.Entry(ventana, font = 12, width = 14, textvariable = tex_sub_equipo)
	ent_sub_equipo.place(x = 320, y = 320)

	tex_subconcepto1 = tk.StringVar(value = "DEUDA")
	ent_subconceto1 = tk.Entry(frame_supconceptos, font = 12, width = 10, textvariable = tex_subconcepto1, state="readonly")
	ent_subconceto1.bind("<Double-Button-1>", lambda event: ent_subconceto1.config(state = "normal"))
	ent_subconceto1.bind("<FocusOut>", lambda event: ent_subconceto1.config(state = "readonly"))
	ent_subconceto1.place(x = 40, y = 0)
	tooltip = Tooltip(ent_subconceto1, "Haz doble clic para editar")

	monto_subconcepto1 = tk.StringVar()
	ent_monto_subconcepto1 = tk.Entry(frame_supconceptos, font = 12, width = 10, textvariable = monto_subconcepto1)
	ent_monto_subconcepto1.insert(0, '')
	ent_monto_subconcepto1.place(x = 136, y = 0)

	'''buscar = tk.StringVar()
	ent_buscar = tk.Entry(ventana, width = 16, font = 1, textvariable = buscar)
	ent_buscar.insert(0, 'Buscar')
	ent_buscar.config(fg = 'gray')
	ent_buscar.bind('<FocusIn>', ent_click)
	ent_buscar.bind('<FocusOut>', ent_no_click)
	ent_buscar.place(x = 490, y = 5)
	'''
	# -------------------------- BOTONES -------------------------- #
	btn_imprimir = tk.Button(ventana, text = "Imprimir", width = 10)
	btn_imprimir.place(x = 300, y = 484)

	btn_guardar = tk.Button(ventana, text = "Guardar", width = 10)
	btn_guardar.place(x = 400, y = 484)

	btn_mas_equipo = tk.Button(ventana, text = "+", width = 2, pady=-9)
	btn_mas_equipo.place(x = 275, y = 50)

	btn_mas_persona = tk.Button(ventana, text = "+", width = 2, pady=-9)
	btn_mas_persona.place(x = 275, y = 100)

	btn_mas_concepto = tk.Button(ventana, text = "+", width = 2, pady=-9)
	btn_mas_concepto.place(x = 275, y = 150)

	btn_mas_subconcepto = tk.Button(ventana, text = "+", width = 2, pady=-9, comman = agregar_subconcepto)
	btn_mas_subconcepto.place(x = 142, y = 199)

	# ------------------------ Agregar íconos ------------------------ #

	calendario = DateEntry(ventana, locale='es_MX', date_pattern='dd/mm/yyyy',
	                       background='orange', foreground='black', bordercolor='green',
	                       normalbackground='white', normalforeground='black',
	                       weekendbackground='white', weekendforeground='red',
	                       headersbackground='lightgreen', headersforeground='black')
	calendario.place(x = 380, y = 5)










	# ---------- EJECUTAR VENTANA PRINCIPAL ----------------- # 

	ventana.mainloop()