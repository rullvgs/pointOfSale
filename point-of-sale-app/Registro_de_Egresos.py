# Ventana de registro de egresos
import tkinter as tk 
from tkinter import ttk 

def abrir_registro_egresos():
	# Aquí se crea la ventana
	ventana = tk.Tk()
	ventana.title("Registro de Egresos")
	ventana.geometry("920x680")

	# Posicionamos a la ventana a mitad de la pantalla
	ancho_pantalla = ventana.winfo_screenwidth()
	largo_pantalla = ventana.winfo_screenheight()
	posicion_ancho = int((ancho_pantalla/2)-920/2)
	posicion_largo = int((largo_pantalla/2)-680/2)
	ventana.geometry("+{}+{}".format(posicion_ancho, posicion_largo))


	# Aquí se abrimos la ventana
	ventana.mainloop()	