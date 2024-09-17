# Perfil_Usuario
import tkinter as tk
from tkinter import ttk
import BD_Login
from tkinter import messagebox as msg
import bcrypt
import tkinter.font as Font
from validate_email import validate_email



class perfil(tk.Toplevel):
	def __init__(self, master = None, usuario_logeado = None, main_menu = None):
		super().__init__(master)

		self.title("Perfil")
		self.geometry("760x640")
        # Posicionamos a la ventana a la mitad de nuestra pantalla
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla / 2) - 760 / 2)
		posicion_largo = int((largo_pantalla / 2) - 640 / 2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

		self.usu_logeado = usuario_logeado
		self.main_menu = main_menu

		self.model = BD_Login.modelo(self)

		self.frame_0 = tk.LabelFrame(self, text  = '', background = 'SteelBlue2')
		self.frame_0.grid(columnspan = 1, column = 0, row = 0, padx = 10, pady = 5)
		self.frame_1 = tk.LabelFrame(self, text = '')
		self.frame_1.grid(columnspan = 1, column = 1, row = 0)

		# Variables 
		self.my_font = Font.Font(family="Super Boys", size = 24, weight = 'bold')
		self.my_font2 = Font.Font(family="Holla Weekend", size = 14, weight = 'normal')
		self.my_font3 = Font.Font(family="Find Cartoon", size = 22, weight = 'normal')
		self.my_font4 = Font.Font(family="Juicy Advice DEMO", size = 20, weight = 'normal')
		self.titulo = tk.Label(self.frame_0, text = self.usu_logeado, font = self.my_font, fg = 'green4', bg = 'SteelBlue2')

        # Aquí llamamos a todas las funciones necesarias
		self.diseño_1()
		self.crear_widgets()
		self.widgets_perfil()
	
	def crear_widgets(self):
		self.diseño_1()

        # Crear un marco para los widgets que se posicionarán con grid

		# ------------------------- LABELS --------------------------- #
		self.titulo = tk.Label(self.frame_0, text = self.usu_logeado, font = self.my_font3, fg = 'black', bg = 'lime green')
		self.titulo.grid(column = 0, row = 4, padx = 60, sticky = 'w')

		#tk.Label(self.frame_0, text = " ").grid(column = 0, row = 0, pady = 15)
		tk.Label(self.frame_0, text = " ", fg = 'SteelBlue2', bg='lime green').grid(column = 0, row = 1,)
		tk.Label(self.frame_0, text = " ",fg = 'SteelBlue2',bg='lime green').grid(column = 0, row = 2, pady = 15)
		tk.Label(self.frame_0, text = " ",fg = 'SteelBlue2',bg='lime green').grid(column = 0, row = 3, pady = 15)
		tk.Label(self.frame_0, text = " ",bg='lime green').grid(column = 0, row = 5, pady = 15)
		tk.Label(self.frame_0, text = " ",fg = 'SteelBlue2',bg='lime green').grid(column = 0, row = 10, pady = 15)
		tk.Label(self.frame_0, text = " ",fg = 'SteelBlue2',bg='lime green').grid(column = 0, row = 11, pady = 15)
		tk.Label(self.frame_0, text = " ",fg = 'SteelBlue2',bg='lime green').grid(column = 0, row = 12, pady = 15)
		tk.Label(self.frame_0, text = " ",fg = 'SteelBlue2',bg='lime green').grid(column = 0, row = 13, pady = 35)
		tk.Label(self.frame_0, text = " ",bg='lime green').grid(column = 0, row = 14, pady = 15)



		# ------------------------- BOTONES -------------------------- #
		self.cancelar = tk.Button(self.frame_0, text = "Regresar", font = ("Arial", 10), bg ='LightBlue1', command = self.master.mostrar_menu_Principal)
		#self.cancelar = tk.Button(self.frame_0, text = "Regresar", width = 10, font = ('Arial bold', 10), bg ='LightBlue1')
		self.cancelar.grid(column = 0, row = 0, sticky = "w")

		self.btn_editar_perfil = tk.Button(self.frame_0, text = "Editar Perfil                                                       ", font = ("Arial", 12), bg = 'light cyan', command = self.mostrar_editar_perfil)
		self.btn_editar_perfil.grid(column = 0, row = 6, sticky = "ew")

		self.btn_editar_contraseña = tk.Button(self.frame_0, text = "Cambiar Contraseña                                       ", font = ("Arial", 12),bg = 'light cyan', command = self.mostrar_cambiar_contraseña)
		self.btn_editar_contraseña.grid(column = 0, row = 7, sticky = "ew")

		self.btn_equipos = tk.Button(self.frame_0, text = "Equipos                                                           ", font = ("Arial", 12), bg = 'light cyan', command = self.mostrar_equipos)
		self.btn_equipos.grid(column = 0, row = 8, sticky = "ew")

		#
		#self.btn_apariencia = tk.Button(self.frame_0, text = "Apariencia                                  ", font = ("Arial", 12), bg = 'light cyan')
		#self.btn_apariencia.grid(column = 0, row = 8, sticky = "ew")

	def widgets_perfil(self):
		self.datos_usuario = self.model.obtener_datos_usuario(self.master.usuario_logeado)
		self.nombre_bd = str(self.datos_usuario[0])
		self.apellido_paterno_bd = str(self.datos_usuario[1])
		self.apellido_materno_bd = str(self.datos_usuario[2])
		self.nickname_bd = str(self.datos_usuario[3])
		self.correo_bd = str(self.datos_usuario[4])
		self.telefono_bd = self.datos_usuario[5]
		
		self.name = tk.StringVar() # Nombres
		self.ent_name = tk.Entry(self, width = 26, font = 12, textvariable = self.name)
		self.ent_name.insert(0, self.nombre_bd)
		self.ent_name.config(fg = 'gray')
		#self.ent_name.bind('<FocusIn>', lambda event: self.on_entry_focus_in(event, self.nombre_bd))
		#self.ent_name.bind('<FocusOut>', lambda event: self.on_entry_focus_out(event, self.nombre_bd))

		self.Apellidos_Pa = tk.StringVar() # Apellidos
		self.ent_Apellidos_Pa = tk.Entry(self, width = 12, font = 12, borderwidth = 1, textvariable = self.Apellidos_Pa)
		self.ent_Apellidos_Pa.insert(0, self.apellido_paterno_bd)
		#self.ent_Apellidos_Pa.bind('<FocusIn>', lambda event: self.on_entry_focus_in(event, self.apellido_paterno_bd))
		#self.ent_Apellidos_Pa.bind('<FocusOut>', lambda event: self.on_entry_focus_out(event, self.apellido_paterno_bd))
		self.ent_Apellidos_Pa.config(fg  = 'gray')
		self.Apellidos_Ma = tk.StringVar() # Apellidos
		self.ent_Apellidos_Ma = tk.Entry(self, width = 12, font = 12, borderwidth = 1, textvariable = self.Apellidos_Ma)
		self.ent_Apellidos_Ma.insert(0, self.apellido_materno_bd)
		self.ent_Apellidos_Ma.config(fg  = 'gray')

		self.nickName = tk.StringVar() # usuario
		self.ent_nickName = tk.Entry(self, width = 26, font = 14, borderwidth=2, relief="groove",  textvariable = self.nickName)
		self.ent_nickName.insert(0, self.usu_logeado)
		#self.ent_nickName.bind('<FocusIn>', lambda event: self.on_entry_focus_in(event, self.usu_logeado))
		#self.ent_nickName.bind('<FocusOut>', lambda event: self.on_entry_focus_out(event, self.usu_logeado))
		self.ent_nickName.config(fg = 'gray')

		self.correo = tk.StringVar() # Correo electrónico
		self.ent_correo = tk.Entry(self, width = 26, font = 14, textvariable = self.correo)
		self.ent_correo.insert(0, self.correo_bd)
		#self.ent_correo.bind('<FocusIn>', lambda event: self.on_entry_focus_in(event, self.correo_bd))
		#self.ent_correo.bind('<FocusOut>', lambda event: self.on_entry_focus_out(event, self.correo_bd))
		self.ent_correo.config(fg = 'gray')

		self.telefono = tk.StringVar()
		self.ent_telefono = tk.Entry(self, width = 26, font = 14, textvariable = self.telefono)
		self.ent_telefono.insert(0, self.telefono_bd)
		#self.ent_telefono.bind('<FocusIn>', lambda event: self.on_entry_focus_in(event, self.telefono_bd))
		#self.ent_telefono.bind('<FocusOut>', lambda event: self.on_entry_focus_out(event, self.telefono_bd))
		self.ent_telefono.config(fg = 'gray')

		self.btn_modificar_datos = tk.Button(self, text = "Guardar", font = ("Arial", 12),bg = 'light cyan', command = self.actualizar_datos_usuario)
		# Widgets de cambiar contraseña
		self.vieja_contraseña = tk.StringVar() # Contraseña
		self.ent_vieja_contraseña = tk.Entry(self, width = 26, font = 14, textvariable = self.vieja_contraseña)
		self.ent_vieja_contraseña.insert(0, "Contraseña antigua")
		self.ent_vieja_contraseña.bind('<FocusIn>', self.contraseña_antiguo_click)
		self.ent_vieja_contraseña.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_vieja_contraseña))
		self.ent_vieja_contraseña.config(fg = 'gray')

		self.nueva_contraseña = tk.StringVar() # Contraseña
		self.ent_nueva_contraseña = tk.Entry(self, width = 26, font = 14, textvariable = self.nueva_contraseña)
		self.ent_nueva_contraseña.insert(0, "Nueva contraseña")
		self.ent_nueva_contraseña.bind('<FocusIn>', self.contraseña_click)
		self.ent_nueva_contraseña.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_nueva_contraseña))
		self.ent_nueva_contraseña.config(fg = 'gray')

		self.conf_password = tk.StringVar() # Confirmación de contraseña
		self.ent_password = tk.Entry(self, width = 26, font = 14, textvariable = self.conf_password)
		self.ent_password.insert(0, "Confirmar contraseña")
		self.ent_password.bind('<FocusIn>', self.password_click)
		self.ent_password.bind('<FocusOut>', lambda event: self.usuario_no_click(event, self.ent_password))
		self.ent_password.config(fg = 'gray')

		self.btn_actualizar_contraseña = tk.Button(self, text = "Actualizar Contraseña", font = ("Arial", 12),bg = 'light cyan', command = self.modificar_contraseña)
		self.diseño_1()
			
	def mostrar_editar_perfil(self):
	    self.frame_0.destroy()
	    self.frame_0 = tk.LabelFrame(self, text  = '')
	    self.frame_0.grid(columnspan = 1, column = 0, row = 0, padx = 10, pady = 5)
	    self.crear_widgets()

	    self.rellenar_datos_perfil()
	    self.ent_vieja_contraseña.delete(0, 'end')
	    self.ent_vieja_contraseña.insert(0, 'Contraseña antigua')
	    self.ent_vieja_contraseña.config(fg = 'gray', show = '')

	    self.ent_nueva_contraseña.delete(0, 'end')
	    self.ent_nueva_contraseña.insert(0, 'Nueva contraseña')
	    self.ent_nueva_contraseña.config(fg = 'gray', show = '')

	    self.ent_password.delete(0, 'end')
	    self.ent_password.insert(0, 'Confirmar contraseña')	    
	    self.ent_password.config(fg = 'gray', show = '')

	    # Ocultar los widgets de cambiar contraseña
	    self.geometry("760x640")
	    # Posicionamos a la ventana a la mitad de nuestra pantalla
	    ancho_pantalla = self.winfo_screenwidth()
	    largo_pantalla = self.winfo_screenheight()
	    posicion_ancho = int((ancho_pantalla / 2) - 760 / 2)
	    posicion_largo = int((largo_pantalla / 2) - 640 / 2)
	    self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

	    self.frame_1.destroy()
	    self.ent_vieja_contraseña.place_forget()
	    self.ent_nueva_contraseña.place_forget()
	    self.ent_password.place_forget()
	    self.btn_actualizar_contraseña.place_forget()
	    
	    # Mostrar los widgets de editar perfil
	    self.ent_name.place(x = 420, y = 200)
	    self.ent_Apellidos_Pa.place(x = 420, y = 250)
	    self.ent_Apellidos_Ma.place(x = 545, y = 250)
	    self.ent_nickName.place(x = 420, y = 300)
	    self.ent_correo.place(x = 420, y = 350)
	    self.ent_telefono.place(x = 420, y = 400)
	    self.btn_modificar_datos.place(x = 500, y = 455)
	    self.btn_editar_perfil.config(bg = 'SeaGreen2')
	    self.diseño_1()

	def mostrar_cambiar_contraseña(self):
	    self.rellenar_datos_perfil()
	    self.ent_vieja_contraseña.delete(0, 'end')
	    self.ent_vieja_contraseña.insert(0, 'Contraseña antigua')
	    self.ent_vieja_contraseña.config(fg = 'gray', show = '')

	    self.ent_nueva_contraseña.delete(0, 'end')
	    self.ent_nueva_contraseña.insert(0, 'Nueva contraseña')
	    self.ent_nueva_contraseña.config(fg = 'gray', show = '')

	    self.ent_password.delete(0, 'end')
	    self.ent_password.insert(0, 'Confirmar contraseña')
	    self.ent_password.config(fg = 'gray', show = '')
	    # Ocultar los widgets de editar perfil
	    self.geometry("760x640")
	    # Posicionamos a la ventana a la mitad de nuestra pantalla
	    ancho_pantalla = self.winfo_screenwidth()
	    largo_pantalla = self.winfo_screenheight()
	    posicion_ancho = int((ancho_pantalla / 2) - 760 / 2)
	    posicion_largo = int((largo_pantalla / 2) - 640 / 2)
	    self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

	    self.frame_1.destroy()
	    self.ent_name.place_forget()
	    self.ent_Apellidos_Pa.place_forget()
	    self.ent_Apellidos_Ma.place_forget()
	    self.ent_nickName.place_forget()
	    self.ent_correo.place_forget()
	    self.ent_telefono.place_forget()
	    self.btn_modificar_datos.place_forget()
	    
	    # Mostrar los widgets de cambiar contraseña
	    self.ent_vieja_contraseña.place(x = 420, y = 200)
	    self.ent_nueva_contraseña.place(x = 420, y = 250)
	    self.ent_password.place(x = 420, y = 300)
	    self.btn_actualizar_contraseña.place(x = 460, y = 345)

	    self.btn_editar_contraseña.config(bg = 'SeaGreen2')
	    self.btn_editar_perfil.config(bg = 'light cyan')
	    self.btn_equipos.config(bg = 'light cyan')

	def click_cambiar_contraseña(self):
		self.frame_0.destroy()
		self.frame_0 = tk.LabelFrame(self, text  = ' ')
		self.frame_0.grid(columnspan = 1, column = 0, row = 0, padx = 10)
		self.crear_widgets()
		self.rellenar_datos_perfil()

		# Eliminar widgets de la función edtiar perfil
		if hasattr(self, 'ent_vieja_contraseña'):
			self.ent_name.place_forget()
			self.ent_Apellidos_Pa.place_forget()
			self.ent_Apellidos_Ma.place_forget()
			self.ent_correo.place_forget()
			self.ent_nickName.place_forget()
			self.btn_modificar_datos.place_forget()
			self.ent_telefono.place_forget()

			# Mostramos los widgets
			self.ent_vieja_contraseña.place(x = 420, y = 300)
			self.ent_nueva_contraseña.place(x = 420, y = 350)
			self.ent_password.place(x = 420, y = 400)
			self.btn_editar.place(x = 500, y = 455)

		else:

			self.ent_name.place(x = 420, y = 200)
			self.ent_Apellidos_Pa.place(x = 420, y = 250)
			self.ent_Apellidos_Ma.place(x = 545, y = 250)
			self.ent_correo.place(x = 420, y = 350)
			self.ent_nickName.place(x = 420, y = 300)
			self.btn_modificar_datos.place(x = 500, y = 455)
			self.ent_telefono.place(x = 420, y = 400)

	def mostrar_equipos(self):
		self.frame_1.destroy()
		#self.btn_equipos.config(state = 'disabled')
		# Crear un marco para los widgets que se posicionarán con grid
		self.frame_1 = tk.LabelFrame(self, text = ' ')
		self.frame_1.grid(columnspan = 1, column = 1, row = 0)

		#B-------------_________________________ BOTONES ________________________ -------------------------
		self.btn_eliminar_equipo = tk.Button(self.frame_1, text = 'Eliminar equipo', command = self.eliminar_equipo)
		self.btn_eliminar_equipo.grid(column = 0, row = 1, sticky = 'e')

		# Ocultar los widgets de editar perfil
		self.ent_name.place_forget()
		self.ent_Apellidos_Pa.place_forget()
		self.ent_Apellidos_Ma.place_forget()
		self.ent_nickName.place_forget()
		self.ent_correo.place_forget()
		self.ent_telefono.place_forget()
		self.btn_modificar_datos.place_forget()

	    # Ocultar los widgets de cambiar contraseña
		self.ent_vieja_contraseña.place_forget()
		self.ent_nueva_contraseña.place_forget()
		self.ent_password.place_forget()
		self.btn_actualizar_contraseña.place_forget()

		tk.Label(self.frame_1, text = '                                                                                        ').grid(column = 1, row = 0)
		self.frame_tabla = tk.Frame(self.frame_1)
		self.frame_tabla.grid(columnspan = 6, column = 0, row = 2, sticky = "W", padx = 10, pady = 5)
		self.tabla = ttk.Treeview(self.frame_tabla, height = 18)
		self.tabla.grid(column = 0, row = 0, padx = 10)
		self.ladox = tk.Scrollbar(self.frame_tabla, orient = tk.HORIZONTAL, command = self.tabla.xview)
		self.ladox.grid(column = 0, row = 1, sticky = "ew")
		self.ladoy = tk.Scrollbar(self.frame_tabla, orient = tk.VERTICAL, command = self.tabla.yview)
		self.ladoy.grid(column = 1, row = 0, sticky = "ns")

		self.tabla['columns'] = ('', 'EQUIPOS')		
		self.tabla.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla.column('', minwidth = 40, width = 40, anchor = 'center')
		self.tabla.column('EQUIPOS', minwidth = 200, width = 250, anchor = 'center')

		self.tabla.heading('#0', anchor = 'center')
		self.tabla.heading('', text = 'N°', anchor = 'center')
		self.tabla.heading('EQUIPOS', text = 'EQUIPOS',anchor = 'center')

		nombres_equipos = self.model.obtener_equipos()
		contador = 1
		for dato in nombres_equipos:
		    self.tabla.insert('', 'end', text = '', values = (contador, dato))
		    contador += 1
		self.tabla.bind('<<TreeviewSelect>>', self.mostrar_integrantes)

		self.btn_equipos.config(bg = 'SeaGreen2')
		self.btn_editar_contraseña.config(bg = 'light cyan')
		self.btn_editar_perfil.config(bg = 'light cyan')

	def mostrar_integrantes(self, event):
		self.geometry("1030x640")

		# Posicionamos a la ventana a la mitad de nuestra pantalla
		ancho_pantalla = self.winfo_screenwidth()
		largo_pantalla = self.winfo_screenheight()
		posicion_ancho = int((ancho_pantalla / 2) - 1030 / 2)
		posicion_largo = int((largo_pantalla / 2) - 640 / 2)
		self.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

		self.btn_eliminar_integrante = tk.Button(self.frame_1, text = 'Eliminar integrante', command = self.eliminar_usuario)
		self.btn_eliminar_integrante.grid(column = 3, row = 1)

		self.frame_tabla2 = tk.Frame(self.frame_1)
		self.frame_tabla2.grid(columnspan = 6, column = 3, row = 2, sticky = "W", padx = 10, pady = 5)
		self.tabla2 = ttk.Treeview(self.frame_tabla2, height = 18)
		self.tabla2.grid(column = 0, row = 0, padx = 10)
		self.ladox2 = tk.Scrollbar(self.frame_tabla2, orient = tk.HORIZONTAL, command = self.tabla2.xview)
		self.ladox2.grid(column = 0, row = 1, sticky = "ew")
		self.ladoy2 = tk.Scrollbar(self.frame_tabla2, orient = tk.VERTICAL, command = self.tabla2.yview)
		self.ladoy2.grid(column = 1, row = 0, sticky = "ns")

		self.tabla2['columns'] = ('', 'INTEGRANTES')		
		self.tabla2.column("#0", minwidth = 0, width = 0, anchor = 'center')
		self.tabla2.column('', minwidth = 40, width = 40, anchor = 'center')
		self.tabla2.column('INTEGRANTES', minwidth = 200, width = 220, anchor = 'center')

		self.tabla2.heading('#0', anchor = 'center')
		self.tabla2.heading('', text = 'N°', anchor = 'center')
		self.tabla2.heading('INTEGRANTES', text = 'INTEGRANTES',anchor = 'center')
		# Obtener el índice de la fila seleccionada
		selected_indices = self.tabla.selection()
		if selected_indices:
		    selected_index = selected_indices[0]
		    # Realizar la acción deseada con el índice de la fila seleccionada
		    selected_values = self.tabla.item(selected_index)['values']
		    self.equipo = selected_values[1]

		    #Obtener usuarios
		    nombres_integrantes = self.model.obtener_usuarios(self.equipo)
		    contador = 1
		    for dato in nombres_integrantes:
			    self.tabla2.insert('', 'end', text = '', values = (contador, dato))
			    contador += 1
		else:
		    pass
			
	def eliminar_usuario(self):
		if self.tabla2.focus() == '':
			msg.showerror("Error", "Selecciona un usuario de la tabla, por favor")
			return
		# Obtener el índice de la fila seleccionada
		selected_index2 = self.tabla2.selection()[0]
	    # Obtener los valores de la fila seleccionada
		selected_values = self.tabla2.item(selected_index2)['values']
		integrante = selected_values[1]
	    # Realizar la acción deseada con los valores de la fila seleccionada
		respuesta = msg.askyesno("Pregunta", f"Esta acción eliminará a {integrante} y todo su registro. ¿Desea continuar?")
		if respuesta:
			self.model.eliminar_usuario(integrante)
			nombres_integrantes = self.model.obtener_usuarios(self.equipo)
			self.tabla2.delete(*self.tabla2.get_children())
			contador = 1
			for dato in nombres_integrantes:
			    self.tabla2.insert('', 'end', text = '', values = (contador, dato))
			    contador += 1
		else:
			pass

	def eliminar_equipo(self):
		if self.tabla.focus() == '':
			msg.showerror("Error", "Selecciona un equipo de la tabla, por favor")
			return

		respuesta = msg.askyesno("Pregunta", f"Esta acción eliminará al equipo {self.equipo} y toda información relacionada, como sus integrantes y sus registros. ¿Desea continuar?")
		if respuesta:
			self.model.eliminar_equipo(self.equipo)
			nombres_equipos = self.model.obtener_equipos()
			self.tabla.delete(*self.tabla.get_children())
			contador = 1
			for dato in nombres_equipos:
			    self.tabla.insert('', 'end', text = '', values = (contador, dato))
			    contador += 1
		else:
			pass

	def actualizar_datos_usuario(self):
		usuario = self.usu_logeado

		nombre = self.ent_name.get()
		apellido_pa = self.ent_Apellidos_Pa.get()
		apellido_ma = self.ent_Apellidos_Ma.get()
		usuario2 = self.ent_nickName.get()
		correo = self.ent_correo.get()
		telefono = self.ent_telefono.get()

		self.datos_usuario = self.model.obtener_datos_usuario(self.usu_logeado)
		nombre_bd = str(self.datos_usuario[0])
		apellido_paterno_bd = str(self.datos_usuario[1])
		apellido_materno_bd = str(self.datos_usuario[2])
		nickname_bd = str(self.datos_usuario[3])
		correo_bd = str(self.datos_usuario[4])
		telefono_bd = self.datos_usuario[5]

		datos_validos = False

		datos_validos = False

		if (nombre != '') and (nombre != nombre_bd):
		    self.model.actualiza_nombre(nombre, usuario)
		    datos_validos = True

		if (apellido_pa != ''):
		    self.model.actualiza_apellido_pa(apellido_pa, usuario)
		    datos_validos = True

		if (apellido_ma != '') and (apellido_ma != apellido_materno_bd):
		    self.model.actualiza_apellido_ma(apellido_ma, usuario)
		    datos_validos = True

		if (usuario2 != '') and (usuario2 != usuario):
		    dato = self.model.actualiza_usuario(usuario, usuario2)
		    if dato:
		    	self.main_menu.usuario_logeado = usuario2
		    	self.master.usuario_logeado = usuario2
		    	self.usu_logeado = usuario2
		    	self.titulo = tk.Label(self.frame_0, text = usuario2, font = ("Arial Black", 20))
		    	self.titulo.destroy()
		    	self.titulo = tk.Label(self.frame_0, text = usuario2, font = self.my_font3,fg = 'black', bg = 'lime green').grid(column = 0, row = 4, padx = 60, sticky= 'ew')
		    	datos_validos = True
		    else:
		    	return

		if (correo != '') and (correo != correo_bd):
		    # Validar que el correo electrónico sea válido
			'''valido = validate_email(correo, verify = True)
			if valido:
				self.model.actualiza_correo(correo, usuario)
		    	datos_validos = True
			else:
				msg.showerror("Error", "Ingrese un e-mail válido")
				return'''
			self.model.actualiza_correo(correo, usuario)
			datos_validos = True


		if (telefono != '') and (telefono != telefono_bd):
		    if len(telefono) == 10:
		        self.model.actualiza_telefono(telefono, usuario)
		        datos_validos = True
		    else:
		        msg.showerror("Error", 'Ingresa un número de teléfono válido')
		        return

		if datos_validos:
		    msg.showinfo("Operación exitosa", f'Los datos se han modificado exitosamente')
		else:
		    msg.showerror("Error", "Ingresa tus nuevos datos")

	def modificar_contraseña(self):
		usuario = self.usu_logeado
		contraseña = self.ent_vieja_contraseña.get().encode("utf-8")

		# Obtener la contraseña hasheada almacenada en la base de datos
		hashed_password = self.model.obtener_contraseña(usuario)

		# Verificar si la contraseña ingresada por el usuario coincide con la contraseña hasheada almacenada en la base de datos
		if bcrypt.checkpw(contraseña, hashed_password):
			nueva_contraseña = self.ent_nueva_contraseña.get()
			if len(nueva_contraseña) < 7:
				msg.showerror("Error", "La contraseña debe tener al menos 7 caracteres.")
				return
			confirma_contraseña = self.ent_password.get()

			if nueva_contraseña == confirma_contraseña:
				# Convertimos la contraseña en un arreglo de bytes
				bytes = nueva_contraseña.encode('utf-8')
				# Generamos salt
				salt = bcrypt.gensalt()
				# Hacemos el Hash a la contraseña
				resultado = bcrypt.hashpw(bytes, salt)
				self.model.actualiza_contraseña(resultado, usuario)
				msg.showinfo("Éxito", "La contraseña ha sido modificada exitósamente")
				self.ent_vieja_contraseña.delete(0, 'end')
				self.ent_vieja_contraseña.insert(0, 'Contraseña antigua')
				self.ent_vieja_contraseña.config(fg = 'gray', show = '')

				self.ent_nueva_contraseña.delete(0, 'end')
				self.ent_nueva_contraseña.insert(0, 'Nueva contraseña')
				self.ent_nueva_contraseña.config(fg = 'gray', show = '')

				self.ent_password.delete(0, 'end')
				self.ent_password.insert(0, 'Confirmar contraseña')
				self.ent_password.config(fg = 'gray', show = '')
			else:
				msg.showerror("Error", "Las contraseñas no coinciden")
		else:
		    msg.showerror("Error", "Contraseña ingresada incorrecta")

	def on_entry_focus_in(self, event, default_text):
		entry_widget = event.widget
		if entry_widget.get() == default_text:
			entry_widget.delete(0, tk.END)
			entry_widget.config(fg="black")

	def on_entry_focus_out(self, event, default_text):
		entry_widget = event.widget
		if not entry_widget.get():
			entry_widget.insert(0, default_text)
			entry_widget.config(fg="gray")

	def contraseña_antiguo_click(self, event):
		if self.ent_vieja_contraseña.get() == "Contraseña antigua":
			self.ent_vieja_contraseña.delete(0, "end")
			self.ent_vieja_contraseña.insert(0, '') 
			self.ent_vieja_contraseña.config(fg = 'black', show = "*")

	def contraseña_click(self, event):
		if self.ent_nueva_contraseña.get() == 'Nueva contraseña':
			self.ent_nueva_contraseña.delete(0, "end")
			self.ent_nueva_contraseña.insert(0, '') 
			self.ent_nueva_contraseña.config(fg = 'black', show = "*")

	def password_click(self, event):
		if self.ent_password.get() == 'Confirmar contraseña':
			self.ent_password.delete(0, "end")
			self.ent_password.insert(0, '') 
			self.ent_password.config(fg = 'black', show = "*")

	def usuario_no_click(self, event, entry):
		if entry.get() == '':
			if entry == self.ent_vieja_contraseña:
				entry.insert(0, 'Contraseña antigua')
			elif entry == self.ent_nueva_contraseña:
				entry.insert(0, 'Nueva contraseña')
			elif entry == self.ent_password:
				entry.insert(0, 'Confirmar contraseña')
			entry.config(fg = 'gray', show = '')

	def rellenar_datos_perfil(self):
		self.datos_usuario = self.model.obtener_datos_usuario(self.usu_logeado)
		self.nombre_bd = str(self.datos_usuario[0])
		self.apellido_paterno_bd = str(self.datos_usuario[1])
		self.apellido_materno_bd = str(self.datos_usuario[2])
		self.nickname_bd = str(self.datos_usuario[3])
		self.correo_bd = str(self.datos_usuario[4])
		self.telefono_bd = self.datos_usuario[5]

		self.ent_name.delete(0, tk.END)
		self.ent_name.insert(0, self.nombre_bd)
		self.ent_name.config(fg="black")

		self.ent_Apellidos_Pa.delete(0, tk.END)
		self.ent_Apellidos_Pa.insert(0, self.apellido_paterno_bd)
		self.ent_Apellidos_Pa.config(fg="black")

		self.ent_Apellidos_Ma.delete(0, tk.END)
		self.ent_Apellidos_Ma.insert(0, self.apellido_materno_bd)
		self.ent_Apellidos_Ma.config(fg="black")

		self.ent_nickName.delete(0, tk.END)
		self.ent_nickName.insert(0, self.nickname_bd)
		self.ent_nickName.config(fg="black")

		self.ent_correo.delete(0, tk.END)
		self.ent_correo.insert(0, self.correo_bd)
		self.ent_correo.config(fg="black")

		self.ent_telefono.delete(0, tk.END)
		self.ent_telefono.insert(0, self.telefono_bd)
		self.ent_telefono.config(fg="black")

	def diseño_1(self):
		self.frame_0.config(background = 'lime green')
		self.config(bg = 'SeaGreen2')






if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	app = perfil(root)
	app.mainloop()