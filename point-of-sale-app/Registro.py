# Ventana para el registro de nuevos usiuarios 
import tkinter as tk
from tkinter import ttk 
import bcrypt
import BD_Login
from tkinter import messagebox as msg

def abrir_registro():
    ventana = tk.Tk()
    ventana.title("Registro")
    ventana.geometry("420x520")
    ancho_pantalla = ventana.winfo_screenwidth()
    largo_pantalla = ventana.winfo_screenheight()
    posicion_ancho = int((ancho_pantalla/2)-420/2)
    posicion_largo = int((largo_pantalla/2)-520/2)
    ventana.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

    # ------------- function ---------------- #

    #def check_password(plain_text_password, hashed_password):
    #    return bcrypt.checkpw(plain_text_password, hashed_password)

    def hash_contrasena(contrasena):
        # Convertimos la contraseña en un arreglo de bytes
        bytes = contrasena.encode('utf-8')

        # Generamos salt
        salt = bcrypt.gensalt()

        # Hacemos el Hash a la contraseña
        resultado = bcrypt.hashpw(bytes, salt)
        return resultado

    def abrir_login():
        ventana.destroy()
        import Login
        ventana_login = Login.Tk()  # Crear una nueva instancia de la ventana de inicio de sesión
        ventana_login.mainloop()# Aquí creas la nueva instancia de la ventana de inicio de sesión (Login)
        # y la muestras con el método `mainloop()` como lo hiciste anteriormente.


    def registro():
        # Recuperar los valores ingresados por el usuario
        nombre = ent_name.get()
        ap_paterno = ent_Apellidos_Pa.get()
        ap_materno = ent_Apellidos_Ma.get()
        usuario = ent_nickName.get()
        correo = ent_correo.get()
        contrasena = ent_contraseña.get()
        telefono = ent_telefono.get()

        # Validar que no haya campos vacíos
        if not (nombre and ap_paterno and ap_materno and usuario and correo and contrasena and telefono):
            msg.showerror("Error", "Por favor, completa todos los campos.")
            return

        # Verificar que las contraseñas coincidan
        confirmar_contrasena = ent_password.get()
        if contrasena != confirmar_contrasena:
            msg.showerror("Error", "Las contraseñas no coinciden.")
            return

        # Validar que la contraseña tenga al menos 7 caracteres
        if len(contrasena) < 7:
            msg.showerror("Error", "La contraseña debe tener al menos 7 caracteres.")
            return

        # Cifrar la contraseña antes de guardarla en la base de datos
        hashed_password = hash_contrasena(contrasena)

        # Crear una instancia del modelo de la base de datos
        modelo = BD_Login.modelo()

        # Insertar el usuario en la base de datos
        modelo.inserta_usuario(nombre, ap_paterno, ap_materno, usuario, hashed_password, correo, telefono)

        # Mostrar un mensaje de éxito
        msg.showinfo("Registro Exitoso", "¡Registro exitoso!")


    # AQUÍ NOMÁS PARA DAR DISEÑO AL REGISTRO ----------------------------
    def usuario_click(event, entry):
        if entry.get() in ['Nombre(s)', 'Apellidos', 'Correo electrónico', 'Contraseña', 'Confirmar contraseña', 'Número de teléfono', 'Apellido paterno', 'Apellido materno', 'Usuario']:
            entry.delete(0, "end")
            entry.insert(0, '')
            entry.config(fg = 'black')

    def usuario_no_click(event, entry):
        if entry.get() == '':
            if entry == ent_name:
                entry.insert(0, 'Nombre(s)')
            elif entry == ent_Apellidos_Pa:
                entry.insert(0, 'Apellido paterno')
            elif entry == ent_Apellidos_Ma:
                entry.insert(0, 'Apellido materno')
            elif entry == ent_nickName:
                entry.insert(0, 'Usuario')
            elif entry == ent_correo:
                entry.insert(0, 'Correo electrónico')
            elif entry == ent_contraseña:
                entry.insert(0, 'Contraseña')
            elif entry == ent_password:
                entry.insert(0, 'Confirmar contraseña')
            elif entry == ent_telefono:
                entry.insert(0, 'Número de teléfono')
            entry.config(fg = 'grey')


    #--------------------TEXTOS (Labels)------------------------------- #
    welcome = tk.Label(ventana, text = "CREAR CUENTA", textvariable = 30, font = ("Arial Black", 22))
    welcome.place(x = 80, y = 50) # TEXTO DE LA VENTANA	

    # --------------------- Cajas de texto ---------------------------- # 
    name = tk.StringVar() # Nombres
    ent_name = tk.Entry(ventana, width = 26, font = 12, textvariable = name)
    ent_name.insert(0, "Nombre(s)")
    ent_name.config(fg = 'gray')
    ent_name.bind('<FocusIn>', lambda event: usuario_click(event, ent_name))
    ent_name.bind('<FocusOut>', lambda event: usuario_no_click(event, ent_name))
    ent_name.place(x = 90, y = 110)

    Apellidos_Pa = tk.StringVar() # Apellidos
    ent_Apellidos_Pa = tk.Entry(ventana, width = 12, font = 12, textvariable = Apellidos_Pa)
    ent_Apellidos_Pa.insert(0, "Apellido paterno")
    ent_Apellidos_Pa.config(fg  = 'gray')
    ent_Apellidos_Pa.bind('<FocusIn>', lambda event: usuario_click(event, ent_Apellidos_Pa))
    ent_Apellidos_Pa.bind('<FocusOut>', lambda event: usuario_no_click(event, ent_Apellidos_Pa))
    ent_Apellidos_Pa.place(x = 90, y = 160)

    Apellidos_Ma = tk.StringVar() # Apellidos
    ent_Apellidos_Ma = tk.Entry(ventana, width = 12, font = 12, textvariable = Apellidos_Ma)
    ent_Apellidos_Ma.insert(0, "Apellido materno")
    ent_Apellidos_Ma.config(fg  = 'gray')
    ent_Apellidos_Ma.bind('<FocusIn>', lambda event: usuario_click(event, ent_Apellidos_Ma))
    ent_Apellidos_Ma.bind('<FocusOut>', lambda event: usuario_no_click(event, ent_Apellidos_Ma))
    ent_Apellidos_Ma.place(x = 215, y = 160)

    nickName = tk.StringVar() # usuario
    ent_nickName = tk.Entry(ventana, width = 26, font = 14, textvariable = nickName)
    ent_nickName.insert(0, "Usuario")
    ent_nickName.config(fg = 'gray')
    ent_nickName.bind('<FocusIn>', lambda event: usuario_click(event, ent_nickName))
    ent_nickName.bind('<FocusOut>', lambda event: usuario_no_click(event, ent_nickName))
    ent_nickName.place(x = 90, y = 210)

    correo = tk.StringVar() # Correo electrónico
    ent_correo = tk.Entry(ventana, width = 26, font = 14, textvariable = correo)
    ent_correo.insert(0, "Correo electrónico")
    ent_correo.config(fg = 'gray')
    ent_correo.bind('<FocusIn>', lambda event: usuario_click(event, ent_correo))
    ent_correo.bind('<FocusOut>', lambda event: usuario_no_click(event, ent_correo))
    ent_correo.place(x = 90, y = 260)

    contraseña = tk.StringVar() # Contraseña
    ent_contraseña = tk.Entry(ventana, width = 26, font = 14, textvariable = contraseña)
    ent_contraseña.insert(0, "Contraseña")
    ent_contraseña.config(fg = 'gray')
    ent_contraseña.bind('<FocusIn>', lambda event: usuario_click(event, ent_contraseña))
    ent_contraseña.bind('<FocusOut>', lambda event: usuario_no_click(event, ent_contraseña))
    ent_contraseña.place(x = 90, y = 310)

    conf_password = tk.StringVar() # Confirmación de contraseña
    ent_password = tk.Entry(ventana, width = 26, font = 14, textvariable = conf_password)
    ent_password.insert(0, "Confirmar contraseña")
    ent_password.config(fg = 'gray')
    ent_password.bind('<FocusIn>', lambda event: usuario_click(event, ent_password))
    ent_password.bind('<FocusOut>', lambda event: usuario_no_click(event, ent_password))
    ent_password.place(x = 90, y = 360)

    telefono = tk.StringVar()
    ent_telefono = tk.Entry(ventana, width = 26, font = 14, textvariable = telefono)
    ent_telefono.insert(0, "Número de teléfono")
    ent_telefono.config(fg = 'gray')
    ent_telefono.bind('<FocusIn>', lambda event: usuario_click(event, ent_telefono))
    ent_telefono.bind('<FocusOut>', lambda event: usuario_no_click(event, ent_telefono))
    ent_telefono.place(x = 90, y = 410)

    # ---------------------------- Botónes ---------------------------- #

    Registro = tk.Button(ventana, text = "Registrarse", width = 14, font = ("Arial old", 11), command = registro)
    Registro.place(x = 150, y = 440)

    btn_regresar = tk.Button(ventana, text = "Iniciar sesión", width = 10, font = ("Arial old", 11), borderwidth = 0, command = abrir_login)
    btn_regresar.place(x = 300, y = 480)

    # Corremos la ventana
    ventana.mainloop()

