# Login_App
import tkinter as tk
from tkinter import ttk
import BD_Login
import bcrypt
from tkinter import messagebox as msg


class loginApp(tk.Toplevel):
	def __init__(self, master = None):
		super().__init__(master)
		# Ventana del Login
		self.title("Login")
		self.geometry("380x520")


		# Posicionamos a la ventana a la mitad de nuestra pantalla
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla/2)-380/2)
		posicion_largo = int((largo_pantalla/2)-520/2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))
		self.config(bg = 'pale green')
		self.crear_widgets()

	def crear_widgets(self):
		# Controles del Login
		self.titulo_negocio = tk.Label(self, text = "LOGIN", font = ("Arial black", 22), bg = 'pale green')
		self.titulo_negocio.place(x = 135, y = 30)

		# ------------------------------ Botones -------------------------------- #

		self.btn_registrarse = tk.Button(self, text = "¿No tienes cuenta? Regístrate", fg = "blue", font = ('Helvetica 10 underline'), borderwidth = 0, bg = 'pale green', command = self.master.mostrar_Registro)
		#self.btn_registrarse = tk.Button(self, text = "Registrarse", fg = "blue", font = ('Helvetica 10 underline'), borderwidth = 0)
		self.btn_registrarse.place(x = 175, y = 480)

		self.boton_r = tk.Button(self, text = "Iniciar Sesión", font = (10), command = self.verificar_credenciales)
		self.boton_r.place(x = 140, y = 340)

		self.btn_recuperar_contraseña = tk.Button(self, text = "¿Olvidaste la contraseña?", fg = "blue", font = ('Helvetica 10 underline'), borderwidth = 0, bg = 'pale green', command = self.master.mostrar_get_password)
		self.btn_recuperar_contraseña.place(x = 200, y = 460)

		# ---------------------------- ENTRYS ----------------------------- #
		# Caja de texto para ingresar el nombre de usuario 
		self.usuario = tk.StringVar()
		self.ent_usuario = tk.Entry(self, width = 30, font = 6, textvariable = self.usuario)
		self.ent_usuario.insert(0, 'Email/Usuario')
		self.ent_usuario.bind('<FocusIn>', self.usuario_click)
		self.ent_usuario.bind('<FocusOut>', self.contra_focusout)
		self.ent_usuario.config(fg = 'grey')
		self.ent_usuario.place(x = 50, y = 156)

		# Caja de texto para ingresar la contraseña
		self.contraseña = tk.StringVar()
		self.ent_in_contraseña = tk.Entry(self, width = 30, font = 8, textvariable = self.contraseña)
		self.ent_in_contraseña.insert(0, 'Ingresa tu contraseña')
		self.ent_in_contraseña.bind('<FocusIn>', self.contra_click)
		self.ent_in_contraseña.bind('<FocusOut>', self.contra_focusout)
		self.ent_in_contraseña.config(fg = 'grey')
		self.ent_in_contraseña.place(x = 50, y = 256)

	def check_password(self, plain_text_password, hashed_password):
		return bcrypt.checkpw(plain_text_password, hashed_password)

	def verificar_credenciales(self):
		# Recuperar los valores ingresados por el usuario
	    self.usuario_ingresado = self.ent_usuario.get()
	    self.contraseña_ingresada = self.ent_in_contraseña.get()

	    # Validar los datos ingresados por el usuario
	    if not self.usuario_ingresado or not self.contraseña_ingresada:
	        # Mostrar un mensaje de error si el usuario o la contraseña están vacíos
	        msg.showerror("Error", "Ingresa tu usuario y/o contraseña")
	        return

	    # Crear una instancia del modelo de la base de datos
	    modelo_db = BD_Login.modelo(self)

	    # Consultar la base de datos para verificar si el usuario y la contraseña son válidos
	    usuario_en_db = modelo_db.muestra_usuario_login_pass(self.usuario_ingresado)
	    if usuario_en_db:
	        self.hashed_password = usuario_en_db[0][5]
	        if self.check_password(self.contraseña_ingresada.encode(), self.hashed_password):
	        	self.master.usuario_logeado = self.ent_usuario.get()
	        	self.master.mostrar_menu_Principal()
	        else:
	            msg.showerror("Error", "Por favor, ingresa un usuario y/o contraseña válidos")
	    else:
	        msg.showerror("Error", "Por favor, ingresa un usuario y/o contraseña válidos")

	def usuario_click(self, event): # Cuando el usuario hace click en el textBox de usuario
	    if self.ent_usuario.get() == 'Email/Usuario':
	        self.ent_usuario.delete(0, "end") # Borra todo el texto en el Entry
	        self.ent_usuario.insert(0, '') # Reemplaza el texto con una cadena vacía
	        self.ent_usuario.config(fg = 'black')

	def contra_click(self, event): # Acción en el textbox de contraseña
	    if self.ent_in_contraseña.get() == 'Ingresa tu contraseña':
	        self.ent_in_contraseña.delete(0, "end") # Borra todo el texto en el Entry
	        self.ent_in_contraseña.insert(0, '') # Reemplaza el texto con una cadena vacía
	        self.ent_in_contraseña.config(fg = 'black', show = "*")

	def contra_focusout(self, event): # Acción en el textBox de contraseña
		if self.ent_usuario.get() == '':
			self.ent_usuario.insert(2, 'Email/Usuario')
			self.ent_usuario.config(fg = 'grey')
		elif self.ent_in_contraseña.get() == '':
			self.ent_in_contraseña.insert(0, 'Ingresa tu contraseña')
			self.ent_in_contraseña.config(fg = 'grey', show = '')




if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	app = loginApp(root)
	app.mainloop()



