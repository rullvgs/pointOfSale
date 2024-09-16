# Ventana del login
import tkinter as tk
from tkinter import ttk
import BD_Login
import bcrypt
from Menú import abrir_menu
from Registro import abrir_registro
from tkinter import messagebox as msg

# Ventana del Login
ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("380x520")

# Posicionamos a la ventana a la mitad de nuestra pantalla
ancho_pantalla = ventana.winfo_screenwidth()
largo_pantalla = ventana.winfo_screenheight()
posicion_ancho = int((ancho_pantalla/2)-380/2)
posicion_largo = int((largo_pantalla/2)-520/2)
ventana.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

def usuario_click(event): # Cuando el usuario hace click en el textBox de usuario
    if ent_usuario.get() == 'Email/Usuario':
        ent_usuario.delete(0, "end") # Borra todo el texto en el Entry
        ent_usuario.insert(0, '') # Reemplaza el texto con una cadena vacía
        ent_usuario.config(fg = 'black')

def contra_click(event): # Acción en el textbox de contraseña
    if ent_in_contraseña.get() == 'Ingresa tu contraseña':
        ent_in_contraseña.delete(0, "end") # Borra todo el texto en el Entry
        ent_in_contraseña.insert(0, '') # Reemplaza el texto con una cadena vacía
        ent_in_contraseña.config(fg = 'black', show = "*")

def contra_focusout(event): # Acción en el textBox de contraseña
	if ent_usuario.get() == '':
		ent_usuario.insert(2, 'Email/Usuario')
		ent_usuario.config(fg = 'grey')
	elif ent_in_contraseña.get() == '':
		ent_in_contraseña.insert(0, 'Ingresa tu contraseña')
		ent_in_contraseña.config(fg = 'grey', show = '')

def click_button():
    ventana.destroy()
    abrir_registro()


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password, hashed_password)

def iniciar_sesion():
    # Recuperar los valores ingresados por el usuario
    usuario_ingresado = ent_usuario.get()
    contraseña_ingresada = ent_in_contraseña.get()

    # Validar los datos ingresados por el usuario
    if not usuario_ingresado or not contraseña_ingresada:
        # Mostrar un mensaje de error si el usuario o la contraseña están vacíos
        msg.showerror("Error", "Ingresa tu usuario y/o contraseña")
        return

    # Validar que la contraseña tenga más de 6 caracteres
    if len(contraseña_ingresada) < 7:
        msg.showerror("Error", "Contraseña/usuario incorrectos")
        return

    # Crear una instancia del modelo de la base de datos
    modelo_db = BD_Login.modelo()

    # Consultar la base de datos para verificar si el usuario y la contraseña son válidos
    usuario_en_db = modelo_db.muestra_usuario_login_pass(usuario_ingresado)
    if usuario_en_db:
        hashed_password = usuario_en_db[0][5]
        if check_password(contraseña_ingresada.encode(), hashed_password):
            ventana.destroy()
            abrir_menu()  # Con la función abrir_menu()
        else:
            msg.showerror("Error", "Contraseña/usuario incorrectos")
    else:
        msg.showerror("Error", "Contraseña/usuario incorrectos")


# Controles del Login
titulo_negocio = tk.Label(ventana, text = "LOGIN", font = ("Arial black", 22))
titulo_negocio.place(x = 135, y = 30)

# ------------------------------ Botones -------------------------------- #
boton_r = tk.Button(ventana, text = "Iniciar Sesión", font = (10), command = iniciar_sesion)
boton_r.place(x = 140, y = 350)

btn_recuperar_contraseña = tk.Button(ventana, text = "¿Olvidaste la contraseña?", fg = "blue", font = ('Helvetica 10 underline'), borderwidth = 0)
btn_recuperar_contraseña.place(x = 170, y = 280)

btn_registrarse = tk.Button(ventana, text = "Registrarse", font =  ("Arial",12), borderwidth = 0, command = click_button)
btn_registrarse.place(x = 246, y = 480)

# ---------------------------- ENTRYS ----------------------------- #
# Caja de texto para ingresar el nombre de usuario 
usuario = tk.StringVar()
ent_usuario = tk.Entry(ventana, width = 30, font = 6, textvariable = usuario)
ent_usuario.insert(0, 'Email/Usuario')
ent_usuario.bind('<FocusIn>', usuario_click)
ent_usuario.bind('<FocusOut>', contra_focusout)
ent_usuario.config(fg = 'grey')
ent_usuario.place(x = 50, y = 156)

# Caja de texto para ingresar la contraseña
contraseña = tk.StringVar()
ent_in_contraseña = tk.Entry(ventana, width = 30, font = 8, textvariable = contraseña)
ent_in_contraseña.insert(0, 'Ingresa tu contraseña')
ent_in_contraseña.bind('<FocusIn>', contra_click)
ent_in_contraseña.bind('<FocusOut>', contra_focusout)
ent_in_contraseña.config(fg = 'grey')
ent_in_contraseña.place(x = 50, y = 256)



#corremos la ventana
ventana.mainloop()