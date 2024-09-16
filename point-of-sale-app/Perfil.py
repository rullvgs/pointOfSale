# Perfil
import tkinter as tk
from tkinter import ttk

def abrir_perfil():
	# Aquí se crea la ventana
	ventana = tk.Tk()
	ventana.title("Perfil")
	ventana.geometry("680x620")

	# Aquí se posiciona la ventana a la mitad de la pantalla
	ancho_pantalla = ventana.winfo_screenwidth()
	largo_pantalla = ventana.winfo_screenheight()
	posicion_ancho = int((ancho_pantalla/2)-780/2)
	posicion_largo = int((largo_pantalla/2)-620/2)
	ventana.geometry("+{}+{}".format(posicion_ancho, posicion_largo))



	# Aquí se abre la ventana
	ventana.mainloop()