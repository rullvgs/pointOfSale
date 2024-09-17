# Main_Menu	
import tkinter as tk
from tkinter import ttk
from Registro_App import registro_App
from Login_App import loginApp
from Menu_Principal import menu_Principal
from Password_Get import recuperar_contraseña


class main_App(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.withdraw()
		self.usuario_logeado = None
		#self.main_menu = None
		self.ventana_login = loginApp(self)
		self.ventana_registro = registro_App(self)
		self.ventana_contraseña = recuperar_contraseña(self)
		self.mostrar_Login()


	def mostrar_Login(self):
		self.ventana_login.deiconify()
		self.ventana_registro.withdraw()
		self.ventana_contraseña.withdraw()

	def mostrar_Registro(self):
		self.ventana_registro.deiconify()
		self.ventana_login.withdraw()
		self.ventana_contraseña.withdraw()

	def mostrar_get_password(self):
		self.ventana_contraseña.deiconify()
		self.ventana_registro.withdraw()
		self.ventana_login.withdraw()


	def mostrar_menu_Principal(self):
		self.ventana_principal = menu_Principal(self, usuario_logeado = self.usuario_logeado)
		self.ventana_principal.deiconify()
		self.ventana_login.withdraw()


if __name__ == "__main__":
	app = main_App()
	app.mainloop()