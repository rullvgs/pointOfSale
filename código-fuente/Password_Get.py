#Password_Get.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import BD_Login
import bcrypt


class recuperar_contraseña(tk.Toplevel):
	def __init__(self, master = None):
		super().__init__(master)
		# Creamos una ventana
		self.title("recuperar contraseña")
		self.geometry("420x390")

		# Posicionamos la ventana a la mitad de pantalla
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla/2)-420/2)
		posicion_largo = int((largo_pantalla/2)-390/2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

		self.model = BD_Login.modelo(self)
		self.config(bg = 'azure2')

		# Ventanas secundarias
		self.frame_0 = tk.LabelFrame(self)
		self.frame_0.grid(columnspan = 6, column = 0, row = 0)
		self.frame_1 = tk.LabelFrame(self)
		self.frame_1.grid(columnspan = 6, column = 0, row = 1)
        # Llamamos a las funciones
		self.crear_ventana()

	def crear_ventana(self):
        # Resto del código...

        # ----------------------------- COMBOBOX ----------------------- #
		tk.Label(self, text = 'RECUPERAR CONTRASEÑA', font = ("Arial bold", 15), bg = 'azure2').place(x = 80, y = 10)
		tk.Label(self, text = '*Seleccione una pregunta y brinde la respuesta correcta', font=("Arial bold", 11), fg = 'navy', bg = 'azure2').place(x = 10, y = 90)
		preguntas = ["¿Cuál es el nombre de tu mascota?", "¿En qué ciudad naciste?", "¿Cuál es tu comida favorita?", "¿Nombre de tu película favorita?"]
		tk.Label(self, text="Responda", font = ('Arial bold', 12), bg = 'azure2').place(x=40, y=60)
		self.combo_preguntas = ttk.Combobox(self, values=preguntas, width = 28, state="readonly")
		self.combo_preguntas.place(x=210, y=60)

        # ----------------------------- ENTRADAS ----------------------- #
		tk.Label(self, text="Usuario:", font = ('Arial bold', 12), bg = 'azure2').place(x=40, y=130)
		self.ent_usuario = tk.Entry(self)
		self.ent_usuario.place(x=230, y=130)

		tk.Label(self, text="Respuesta:", font = ('Arial bold', 12), bg = 'azure2').place(x=40, y=160)
		self.ent_respuesta = tk.Entry(self)
		self.ent_respuesta.place(x=230, y=160)

		tk.Label(self, text="Nueva Contraseña:", font = ('Arial bold', 12), bg = 'azure2').place(x=40, y=190)
		self.ent_nueva_contraseña = tk.Entry(self, show="*")
		self.ent_nueva_contraseña.place(x=230, y=190)
		
		tk.Label(self, text="Confirmar Contraseña:", font = ('Arial bold', 12), bg = 'azure2').place(x=40, y=220)
		self.ent_confirmar_contraseña = tk.Entry(self, show="*")
		self.ent_confirmar_contraseña.place(x=230, y=220)

        # ----------------------------- BOTÓN ----------------------- #
		self.btn_recuperar = tk.Button(self, text="Recuperar Contraseña", font = ("Arial bold", 10), command=self.recuperar_contraseña)
		self.btn_recuperar.place(x=150, y=270)

		self.btn_login = tk.Button(self, text = 'Iniciar sesion', font = ('Arial bold',9), fg = 'Blue4', command = self.master.mostrar_Login)
		self.btn_login.place(x = 170, y = 310)
		
	def recuperar_contraseña(self):
		pregunta_seleccionada = self.combo_preguntas.get()
		usuario = self.ent_usuario.get()
		respuesta = self.ent_respuesta.get()
		nueva_contraseña = self.ent_nueva_contraseña.get()
		confirmar_contraseña = self.ent_confirmar_contraseña.get()

        # Validaciones de los datos
		if not pregunta_seleccionada or not usuario or not respuesta or not nueva_contraseña or not confirmar_contraseña:
			msg.showwarning("Advertencia", "Por favor, complete todos los campos.")
			return

		if nueva_contraseña != confirmar_contraseña:
			msg.showerror("Error", "Las contraseñas no coinciden.")
			return

		if len(nueva_contraseña) < 7:
			msg.showerror("Error", "La contraseña debe contener al menos 7 caracteres.")
			return

		respuesta_igual = self.model.verificar_respuesta(respuesta, usuario, pregunta_seleccionada)

		if not respuesta_igual:
			return

		# Convertimos la contraseña en un arreglo de bytes
		bytes = nueva_contraseña.encode('utf-8')
		# Generamos salt
		salt = bcrypt.gensalt()
		# Hacemos el Hash a la contraseña
		resultado = bcrypt.hashpw(bytes, salt)
		self.model.actualiza_contraseña(resultado, usuario)
		msg.showinfo("Éxito", "Contraseña actualizada exitosamente.")

		self.combo_preguntas.delete(0, 'end')
		self.combo_preguntas.insert(0, '')
		self.ent_usuario.delete(0, 'end')
		self.ent_usuario.insert(0, '')
		self.ent_respuesta.delete(0, 'end')
		self.ent_respuesta.insert(0, '')
		self.ent_nueva_contraseña.delete(0, 'end')
		self.ent_nueva_contraseña.insert(0, '')
		self.ent_confirmar_contraseña.delete(0, 'end')
		self.ent_confirmar_contraseña.insert(0, '')


		# Regresa la ventana de registro
		# self.master.mostrar_Login()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    app = recuperar_contraseña(root)
    app.mainloop()
