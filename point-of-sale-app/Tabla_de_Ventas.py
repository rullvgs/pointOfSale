import tkinter as tk
from tkinter import ttk 
from tkcalendar import DateEntry

# Creamos la ventana
ventana = tk.Tk()
ventana.title("Tabla de Ventas")
ventana.geometry("920x680")

# Posicionamos a la ventana a la mitad de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
largo_pantalla = ventana.winfo_screenheight()
posicion_ancho = int((ancho_pantalla/2)-920/2)
posicion_largo = int((largo_pantalla/2)-680/2)
ventana.geometry("+{}+{}".format(posicion_ancho, posicion_largo))

# ----------------------- CONTENEDORES (FRAME) ------------------------- #
cnt_barra_superior = tk.LabelFrame(ventana, width=920, height=37)
cnt_barra_superior.place(x=0, y=0)

cnt_editor = tk.LabelFrame(ventana, width=920, height=30)
cnt_editor.place(x=0, y=36)

cnt_tabla = tk.LabelFrame(ventana, width=920, height=612)
cnt_tabla.place(x=0, y=65)

canvas = tk.Canvas(cnt_tabla, width=895, height=612)
canvas.pack(side=tk.LEFT)
# ---------------------------- FUNCIONES ------------------------------ #

def ent_click(event):
    if ent_buscar.get() == 'Buscar':
        ent_buscar.delete(0, 'end')
        ent_buscar.insert(0, '')
        ent_buscar.config(fg='black')

def ent_no_click(event):
    if ent_buscar.get() == '':
        ent_buscar.insert(0, 'Buscar')
        ent_buscar.config(fg='gray')


# ------------------------ TEXTO (LABELS) --------------------------- #

exportar = tk.Label(cnt_barra_superior, text="Exportar", font=("Arial", 11))
exportar.place(x=295, y=5)

gen_reporte = tk.Label(cnt_barra_superior, text="Generar reporte", font=("Arial", 11))
gen_reporte.place(x=155, y=5)

exportar = tk.Label(cnt_barra_superior, text="Menú Principal", font=("Arial", 11))
exportar.place(x=20, y=5)

# ----------------- CAJAS DE TEXTO (ENTRYS) ------------------- #

buscar = tk.StringVar()
ent_buscar = tk.Entry(cnt_barra_superior, width=16, font=1, textvariable=buscar)
ent_buscar.insert(0, 'Buscar')
ent_buscar.config(fg='gray')
ent_buscar.bind('<FocusIn>', ent_click)
ent_buscar.bind('<FocusOut>', ent_no_click)
ent_buscar.place(x=690, y=5)

title_name = tk.StringVar()
ent_t_name = tk.Entry(canvas, width=12, font=20, textvariable=title_name)
ent_t_name.insert(0, 'NOMBRE')
ent_t_name.config(state="readonly")
ent_t_name.place(x=4, y=12)


# ---------------------------- ÍCONOS ------------------------- #
calendario = DateEntry(ventana, locale='es_MX', date_pattern='dd/mm/yyyy',
                       background='orange', foreground='black', bordercolor='green',
                       normalbackground='white', normalforeground='black',
                       weekendbackground='white', weekendforeground='red',
                       headersbackground='lightgreen', headersforeground='black')
calendario.place(x=580, y=5)

# ------------------------ SCROLLBARS --------------------------#

scrollbar = tk.Scrollbar(cnt_tabla, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)














# Corremos la ventana
ventana.mainloop()
