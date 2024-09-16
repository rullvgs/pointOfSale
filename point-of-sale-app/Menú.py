# Ventana del menú principal
import tkinter as tk
from tkinter import ttk
from Registro_de_ventas import abrir_registro_ventas

def abrir_menu():
	#------------- Functions ------------- #
	def ent_click(event):
		if ent_buscar.get() == 'Buscar':
			ent_buscar.delete(0, 'end')
			ent_buscar.insert(0, '')
			ent_buscar.config(fg = 'black')

	def ent_no_click(event):
		if ent_buscar.get() == '':
			ent_buscar.insert(0, 'Buscar')
			ent_buscar.config(fg = 'gray')

	def click_registro_ventas():
		
		abrir_registro_ventas()

	def click_registro_egresos():
		from Registro_de_Egresos import abrir_registro_egresos
		abrir_registro_egresos()

	def click_documentos():
		from Documentación import abrir_documentos
		abrir_documentos()

	def click_perfil():
		from Perfil import abrir_perfil
		abrir_perfil()


	# Creamos una ventana
	ventana = tk.Tk()
	ventana.title("Menú Principal")
	ventana.geometry("580x640")
	# Posicionamos a la ventana a la mitad de nuestra pantalla
	ancho_pantalla = ventana.winfo_screenwidth()
	largo_pantalla = ventana.winfo_screenheight()
	posicion_ancho = int((ancho_pantalla/2)-580/2)
	posicion_largo = int((largo_pantalla/2)-640/2)
	ventana.geometry("+{}+{}".format(posicion_ancho,posicion_largo))

	# ----------------------- LABEL --------------------- #
	


	# -------------------------- BOTONES ------------------------- #
	btn_venta = tk.Button(ventana, text = "Registro de ventas", width = 18, font = ("Arial Bold", 12), command = click_registro_ventas)
	btn_venta.place(x = 185, y = 90)

	btn_egreso = tk.Button(ventana, text = "Registro de egresos", width = 18, font = ("Arial Bold", 12), command = click_registro_egresos)
	btn_egreso.place(x = 185, y = 180)

	btn_documento = tk.Button(ventana, text = "Documentos", width = 18, font = ('Arial Bold', 12), command = click_documentos)
	btn_documento.place(x = 185, y = 270)

	btn_perfil = tk.Button(ventana, text = "Perfil", font = ("Arial", 10), fg = 'Black', command = click_perfil)
	btn_perfil.place(x = 515, y = 10)

	# ---------------------------- TextBox ------------------------ #
	buscar = tk.StringVar()
	ent_buscar = tk.Entry(ventana, width = 16, font = 1, textvariable = buscar)
	ent_buscar.insert(0, 'Buscar')
	ent_buscar.config(fg = 'gray')
	ent_buscar.bind('<FocusIn>', ent_click)
	ent_buscar.bind('<FocusOut>', ent_no_click)
	ent_buscar.place(x = 400, y = 350)



	#Cerramos y destruimos la ventana
	ventana.mainloop()

abrir_menu()