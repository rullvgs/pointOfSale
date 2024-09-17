# Registro_App
import tkinter as tk
from tkinter import ttk
import bcrypt
import BD_Login
from tkinter import messagebox as msg
from validate_email import validate_email
from tips_app import Tooltip

class registro_App(tk.Toplevel):
	def __init__(self, master = None):
		super().__init__(master)
		self.title("Registro")
		self.geometry("420x520")
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla/2)-420/2)
		posicion_largo = int((largo_pantalla/2)-520/2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))
		
		self.crear_widgets_registro()
		self.diseño_registro_app()



	def crear_widgets_registro(self):

		#--------------------TEXTOS (Labels)------------------------------- #
		self.welcome = tk.Label(self, text = "CREAR CUENTA", textvariable = 30, font = ("Arial Black", 22), bg = 'pale green2')
		self.welcome.place(x = 80, y = 15) # TEXTO DE LA VENTANA

		# ----------------------------- BOTONES --------------------------- #
		self.btn_regresar = tk.Button(self, text = "Iniciar sesión", width = 10, font = ("Arial old", 11), borderwidth = 0, command = self.master.mostrar_Login)
		#self.btn_regresar = tk.Button(self, text = "Iniciar sesión", width = 10, font = ("Arial old", 11), borderwidth = 0)
		self.btn_regresar.place(x = 300, y = 480)

		self.Registro = tk.Button(self, text = "Registrarse", width = 14, font = ("Arial old", 11), command = self.registro)
		self.Registro.place(x = 140, y = 440)

		# ----------------------------- TEXBOXT PARA EL REGISTRO ------------------------------ #
		self.name = tk.StringVar() # Nombres
		self.ent_name = tk.Entry(self, width = 26, font = 12, textvariable = self.name)
		self.ent_name.insert(0, "Nombre(s)")
		self.ent_name.config(fg = 'gray')
		self.ent_name.bind('<FocusIn>', lambda event: self.usuario_click(event, self.ent_name))
		self.ent_name.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_name))
		self.ent_name.place(x = 90, y = 80)

		self.Apellidos_Pa = tk.StringVar() # Apellidos
		self.ent_Apellidos_Pa = tk.Entry(self, width = 12, font = 12, textvariable = self.Apellidos_Pa)
		self.ent_Apellidos_Pa.insert(0, "Apellido paterno")
		self.ent_Apellidos_Pa.config(fg  = 'gray')
		self.ent_Apellidos_Pa.bind('<FocusIn>', lambda event: self.usuario_click(event, self.ent_Apellidos_Pa))
		self.ent_Apellidos_Pa.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_Apellidos_Pa))
		self.ent_Apellidos_Pa.place(x = 90, y = 120)

		self.Apellidos_Ma = tk.StringVar() # Apellidos
		self.ent_Apellidos_Ma = tk.Entry(self, width = 12, font = 12, textvariable = self.Apellidos_Ma)
		self.ent_Apellidos_Ma.insert(0, "Apellido materno")
		self.ent_Apellidos_Ma.config(fg  = 'gray')
		self.ent_Apellidos_Ma.bind('<FocusIn>', lambda event: self.usuario_click(event, self.ent_Apellidos_Ma))
		self.ent_Apellidos_Ma.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_Apellidos_Ma))
		self.ent_Apellidos_Ma.place(x = 215, y = 120)

		self.nickName = tk.StringVar() # usuario
		self.ent_nickName = tk.Entry(self, width = 26, font = 14, textvariable = self.nickName)
		self.ent_nickName.insert(0, "Usuario")
		self.ent_nickName.config(fg = 'gray')			
		self.ent_nickName.bind('<FocusIn>', lambda event: self.usuario_click(event, self.ent_nickName))			
		self.ent_nickName.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_nickName))			
		self.ent_nickName.place(x = 90, y = 160)

		self.correo = tk.StringVar() # Correo electrónico
		self.ent_correo = tk.Entry(self, width = 26, font = 14, textvariable = self.correo)
		self.ent_correo.insert(0, "Correo electrónico")
		self.ent_correo.config(fg = 'gray')
		self.ent_correo.bind('<FocusIn>', lambda event: self.usuario_click(event, self.ent_correo))
		self.ent_correo.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_correo))
		self.ent_correo.place(x = 90, y = 200)

		self.contraseña = tk.StringVar() # Contraseña
		self.ent_contraseña = tk.Entry(self, width = 26, font = 14, textvariable = self.contraseña)
		self.ent_contraseña.insert(0, "Contraseña")
		self.ent_contraseña.config(fg = 'gray')
		self.ent_contraseña.bind('<FocusIn>', self.contraseña_click)
		self.ent_contraseña.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_contraseña))
		self.ent_contraseña.place(x = 90, y = 240)

		self.conf_password = tk.StringVar() # Confirmación de contraseña
		self.ent_password = tk.Entry(self, width = 26, font = 14, textvariable = self.conf_password)
		self.ent_password.insert(0, "Confirmar contraseña")
		self.ent_password.config(fg = 'gray')
		self.ent_password.bind('<FocusIn>', self.password_click)
		self.ent_password.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_password))
		self.ent_password.place(x = 90, y = 280)

		self.telefono = tk.StringVar()
		self.ent_telefono = tk.Entry(self, width = 26, font = 14, textvariable = self.telefono)
		self.ent_telefono.insert(0, "Número de teléfono")
		self.ent_telefono.config(fg = 'gray')
		self.ent_telefono.bind('<FocusIn>', lambda event: self.usuario_click(event, self.ent_telefono))
		self.ent_telefono.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_telefono))
		self.ent_telefono.place(x = 90, y = 320)

		preguntas = ["¿Cuál es el nombre de tu mascota?", "¿En qué ciudad naciste?", "¿Cuál es tu comida favorita?", "¿Nombre de tu película favorita?"]
		tk.Label(self, text="Responda", font = ('Arial bold', 12), bg = 'pale green2').place(x=60, y=360)
		self.combo_preguntas = ttk.Combobox(self, values=preguntas, width = 28, state="readonly")
		self.combo_preguntas.place(x=160, y=360)
		Tooltip(self.combo_preguntas,'Estas preguntas son con fines de \nrecuperar su contraseña en caso de que lo necesite')

		tk.Label(self, text="Respuesta:", font = ('Arial bold', 12), bg = 'pale green2').place(x=60, y=400)
		self.ent_respuesta = tk.Entry(self)
		self.ent_respuesta.place(x=200, y=400)

    # -------------------------------- DISEÑO DEL FOMR DE REGISTRO ---------------------------- #
	def usuario_click(self, event, entry):
		if entry.get() in ['Nombre(s)', 'Apellidos', 'Correo electrónico', 'Contraseña', 'Confirmar contraseña', 'Número de teléfono', 'Apellido paterno', 'Apellido materno', 'Usuario']:
			entry.delete(0, "end")
			entry.insert(0, '')
			entry.config(fg = 'black')

	def contraseña_click(self, event):
		if self.ent_contraseña.get() == 'Contraseña':
			self.ent_contraseña.delete(0, "end") # Borra todo el texto en el Entry
			self.ent_contraseña.insert(0, '') # Reemplaza el texto con una cadena vacía
			self.ent_contraseña.config(fg = 'black', show = "*")
	def password_click(self, event):
		if self.ent_password.get() == 'Confirmar contraseña':
			self.ent_password.delete(0, "end") # Borra todo el texto en el Entry
			self.ent_password.insert(0, '') # Reemplaza el texto con una cadena vacía
			self.ent_password.config(fg = 'black', show = "*")
			


	def usuario_no_click(self, event, entry):
		if entry.get() == '':
			if entry == self.ent_name:
				entry.insert(0, 'Nombre(s)')
			elif entry == self.ent_Apellidos_Pa:
				entry.insert(0, 'Apellido paterno')
			elif entry == self.ent_Apellidos_Ma:
				entry.insert(0, 'Apellido materno')
			elif entry == self.ent_nickName:
				entry.insert(0, 'Usuario')
			elif entry == self.ent_correo:
				entry.insert(0, 'Correo electrónico')
			elif entry == self.ent_contraseña:
				entry.insert(0, 'Contraseña')
				entry.config(show = '')
			elif entry == self.ent_password:
				entry.insert(0, 'Confirmar contraseña')
				entry.config(show = '')
			elif entry == self.ent_telefono:
				entry.insert(0, 'Número de teléfono')
			entry.config(fg = 'grey')

	def hash_contrasena(self, contrasena):
		# Convertimos la contraseña en un arreglo de bytes
		bytes = contrasena.encode('utf-8')

        # Generamos salt
		salt = bcrypt.gensalt()
		
        # Hacemos el Hash a la contraseña
		self.resultado = bcrypt.hashpw(bytes, salt)
		return self.resultado

	def registro(self):
        # Recuperar los valores ingresados por el usuario
		self.nombre = self.ent_name.get()
		self.ap_paterno = self.ent_Apellidos_Pa.get()
		self.ap_materno = self.ent_Apellidos_Ma.get()
		self.usuario = self.ent_nickName.get()
		self.correo = self.ent_correo.get()
		self.contrasena = self.ent_contraseña.get()
		self.telefono = self.ent_telefono.get()
		pregunta_seleccionada = self.combo_preguntas.get()
		respuesta = self.ent_respuesta.get()

        # Validar que no haya campos vacíos
		if not (self.nombre and self.ap_paterno and self.ap_materno and self.usuario and self.correo and self.contrasena and self.telefono):
			msg.showerror("Error", "Por favor, completa todos los campos.")
			return

		if self.nombre == "Nombre(s)" or self.ap_paterno == "Apellido paterno" or self.ap_materno == "Apellido materno" or self.telefono == "Número de teléfono" or pregunta_seleccionada == '' or respuesta == '':
			msg.showerror("Error", "Por favor, ingresa tus datos.")
			return

		# Validar que el número de teléfono sea válido
		if not self.telefono.isdigit() or len(self.telefono) != 10:
			msg.showerror("Error", "Ingrese un número telefónico válido")
			return

		# Validar que el correo electrónico sea válido
		'''valido = validate_email(self.correo, verify = True)
		if valido:
			pass
		else:
			msg.showerror("Error", "Ingrese un e-mail válido")
			return'''



        # Verificar que las contraseñas coincidan
		self.confirmar_contrasena = self.ent_password.get()
		if self.contrasena != self.confirmar_contrasena:
			msg.showerror("Error", "Las contraseñas no coinciden.")
			return

        # Validar que la contraseña tenga al menos 7 caracteres
		if len(self.contrasena) < 7:
			msg.showerror("Error", "La contraseña debe tener al menos 7 caracteres.")
			return

        # Cifrar la contraseña antes de guardarla en la base de datos
		self.hashed_password = self.hash_contrasena(self.contrasena)

        # Crear una instancia del modelo de la base de datos
		self.modelo = BD_Login.modelo(self)

		# Verificar si ya existe un usuario con ese nombre, correo o número de teléfono
		#mensaje_error = self.modelo.usuario_existe(self.usuario, self.correo, self.telefono)

        # Insertar el usuario en la base de datos
		mensaje_error = self.modelo.inserta_usuario(self.nombre, self.ap_paterno, self.ap_materno, self.usuario, self.hashed_password, self.correo, self.telefono, pregunta_seleccionada, respuesta)
		if mensaje_error:
			if mensaje_error == "¡Registro exitoso!":
				# Mostrar un mensaje de éxito
				msg.showinfo("Registro Exitoso", mensaje_error)
				self.master.mostrar_Login()
			else:
				msg.showerror("Error", mensaje_error)
				return

	def diseño_registro_app(self):
		self.config(bg = 'pale green2')

if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	app = registro_App(root)
	app.mainloop()