# Menu_Principal
import tkinter as tk
from tkinter import ttk
from Registro_de_ventas import registro_ventas
from Registro_de_Egresos import registro_egresos
from Tabla_de_Ingresos import tabla_ventas
from Tabla_de_Egresos import tabla_egresos
from Perfil_Usuario import perfil
import tkinter.font as Font
from tkinter import messagebox as msg
from PIL import Image, ImageTk

class menu_Principal(tk.Toplevel):
    def __init__(self, master=None, usuario_logeado = None):
        super().__init__(master)
        self.title("Menú Principal")
        self.geometry("580x640")
        # Posicionamos a la ventana a la mitad de nuestra pantalla
        ancho_pantalla = self.winfo_screenwidth()
        largo_pantalla = self.winfo_screenheight()
        posicion_ancho = int((ancho_pantalla / 2) - 580 / 2)
        posicion_largo = int((largo_pantalla / 2) - 640 / 2)
        self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))


        # Recibimos al usuario:
        self.usuario_logeado = usuario_logeado

        # Variables 
        self.my_font = Font.Font(family="Super Boys", size = 16, weight = 'normal')
        self.my_font2 = Font.Font(family="Holla Weekend", size = 14, weight = 'normal')
        self.my_font3 = Font.Font(family="Find Cartoon", size = 12, weight = 'normal')
        self.my_font4 = Font.Font(family="Juicy Advice DEMO", size = 20, weight = 'normal')
        self.my_font5 = Font.Font(family="Genghis Khan", size = 14, weight = 'bold')
        self.my_font6 = Font.Font(family="SEA GARDENS", size = 16, weight = 'normal')
        

        # Aquí llamamos a todas las funciones necesarias
        self.crear_widgets()
        self.ver_tablaEgresos = None
        self.ver_tablaVentas = None
        self.ver_registro_Ventas = registro_ventas(self)
        self.ver_registro_egresos = registro_egresos(self)
        self.ver_perfil = None
        self.cerrar_ventanas()

    def crear_widgets(self):
        # Crear un marco para los widgets que se posicionarán con place
        self.frame_place = tk.Frame(self, bg = 'SeaGreen3')
        self.frame_place.pack(side="top", fill="both", expand=True)

        # -------------------------- BOTONES ------------------------- #
        self.btn_venta = tk.Button(self.frame_place, text="Registro de ingresos", width= 22, font = self.my_font6, command = self.abrir_registro_ventas)
        self.btn_venta.place(x=150, y = 80)

        self.btn_tabla_venta = tk.Button(self.frame_place, text="Tabla de ingresos", width=22, font= self.my_font6, command = self.abrir_tabla_ventas)
        self.btn_tabla_venta.place(x=150, y = 160)

        self.btn_egreso = tk.Button(self.frame_place, text="Registro de egresos", width=22, font= self.my_font6, command = self.abrir_registro_egresos)
        self.btn_egreso.place(x=150, y = 240)

        self.btn_tabla_egreso = tk.Button(self.frame_place, text="Tabla de egresos", width=22, font= self.my_font6, command = self.abrir_tabla_egresos)
        self.btn_tabla_egreso.place(x=150, y = 320)

        self.btn_perfil = tk.Button(self.frame_place, text="Perfil", width = 14, font= self.my_font6, fg='Black', command = self.abrir_perfil)
        self.btn_perfil.place(x = 205, y = 400)

        self.btn_salir = tk.Button(self.frame_place, text="Salir", width = 14, font = self.my_font6, fg='Black', command = self.cerrar_app)
        self.btn_salir.place(x = 205, y = 480)


    def abrir_registro_ventas(self):
        self.ver_registro_Ventas = registro_ventas(self)
        self.ver_registro_Ventas.deiconify()
        self.withdraw()

    def abrir_registro_egresos(self):
        self.ver_registro_egresos = registro_egresos(self)
        self.ver_registro_egresos.deiconify()
        self.withdraw()

    def abrir_tabla_ventas(self): 
        self.ver_tablaVentas = tabla_ventas(self)   	
        self.ver_tablaVentas.deiconify()
        self.ver_registro_Ventas.withdraw()
        self.withdraw()

    def abrir_tabla_egresos(self): 
        self.ver_tablaEgresos = tabla_egresos(self)   	
        self.ver_tablaEgresos.deiconify()
        self.withdraw()
        self.ver_registro_egresos.withdraw()

    '''def abrir_documentos(self):    	
    	#self.ver_documentacion.deiconify()
    	self.withdraw()'''

    def abrir_perfil(self): 
        self.ver_perfil = perfil(self,  usuario_logeado= self.usuario_logeado, main_menu=self.master)   	
        self.ver_perfil.deiconify()
        self.withdraw()

    def mostrar_menu_Principal(self):
        self.deiconify()
        if self.ver_tablaEgresos is not None:
            self.ver_tablaEgresos.withdraw()

        if self.ver_tablaVentas is not None:
            self.ver_tablaVentas.withdraw()

        if self.ver_registro_egresos is not None:
            self.ver_registro_egresos.withdraw()

        if self.ver_registro_Ventas is not None:
            self.ver_registro_Ventas.withdraw()

        if self.ver_perfil is not None:
            self.ver_perfil.withdraw()    

    	#self.ver_documentacion.withdraw()

    def cerrar_ventanas(self):
    	#self.ver_tablaVentas.withdraw()
    	#self.ver_tablaEgresos.withdraw()
    	self.ver_registro_Ventas.withdraw()
    	self.ver_registro_egresos.withdraw()
    	#self.ver_perfil.withdraw()
    	#self.ver_documentacion.withdraw()

    def cerrar_app(self):
    	self.destroy()
    	self.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = menu_Principal(root)
    app.mainloop()