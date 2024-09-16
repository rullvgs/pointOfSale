'''

import tkinter as tk

def command1():
    print("Comando 1 ejecutado")

def command2():
    print("Comando 2 ejecutado")

root = tk.Tk()

# Crear el widget Menubutton
menubutton = tk.Menubutton(root, text="Menú")
menubutton.pack()

# Crear el menú desplegable
menu = tk.Menu(menubutton, tearoff=0)
menubutton["menu"] = menu

# Agregar elementos al menú y asociarlos con comandos
menu.add_command(label="Comando 1", command=command1)
menu.add_command(label="Comando 2", command=command2)

root.mainloop()


'''


import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont

class PrintPreviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vista Previa de Impresión")

        self.label_frame = ttk.LabelFrame(root, text="Vista Previa de Impresión")
        self.label_frame.pack(padx=10, pady=10)

        self.tabla = ttk.Treeview(self.label_frame, columns=('ID', 'COMPROBANTE', 'FECHA', 'CONCEPTO', 'CATEGORIA', 'CANTIDAD', 'PRECIO_UNITARIO', 'PRECIO_FINAL'))
        self.tabla.heading('#0', text="\n", anchor='center')
        self.tabla.heading('ID', text='ID', anchor='center')
        self.tabla.heading('COMPROBANTE', text='COMPROBANTE', anchor='center')
        self.tabla.heading('FECHA', text='FECHA', anchor='center')
        self.tabla.heading('CONCEPTO', text='CONCEPTO', anchor='center')
        self.tabla.heading('CATEGORIA', text='CATEGORÍA', anchor='center')
        self.tabla.heading('CANTIDAD', text='CANTIDAD', anchor='center')
        self.tabla.heading('PRECIO_UNITARIO', text='  PRECIO\nUNITARIO', anchor='center')
        self.tabla.heading('PRECIO_FINAL', text='PRECIO FINAL', anchor='center')
        
        # Agregar datos de ejemplo a la tabla (puedes reemplazar esto con tus datos reales)
        for i in range(5):
            self.tabla.insert('', 'end', text='', values=(i+1, 'Comp{}'.format(i+1), '01/08/2023', 'Concepto {}'.format(i+1), 'Categoría {}'.format(i+1), i+1, '$10', '${}'.format((i+1)*10)))

        self.tabla.pack()

        self.btn_imprimir = tk.Button(root, text="Imprimir", command=self.imprimir)
        self.btn_imprimir.pack()

    def imprimir(self):
        image = self.create_printable_image()
        image.save("print_preview.png")

    def create_printable_image(self):
        image = Image.new("RGB", (400, 300), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        y = 10

        for item in self.tabla.get_children():
            values = self.tabla.item(item, 'values')
            line = 'ID: {}, Comprobante: {}, Fecha: {}, Concepto: {}, Categoría: {}, Cantidad: {}, Precio Unitario: {}, Precio Final: {}'.format(*values)
            draw.text((10, y), line, fill="black", font=font)
            y += 20

        return image

root = tk.Tk()
app = PrintPreviewApp(root)
root.mainloop()



from tkinter import *
from tkinter import ttk

root = Tk()
root.title("LabelFrame Ejemplo")

frame = LabelFrame(root, text="Datos de la Tabla", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# Configuración del tipo de letra
font = ("Courier", 10)

# Creación de las etiquetas y su ubicación en el grid
Label(frame, text="ID:\n", font=font).grid(row=0, column=0, sticky=W)
Label(frame, text="COMPROBANTE:\n", font=font).grid(row=1, column=0, sticky=W)
Label(frame, text="FECHA:\n", font=font).grid(row=2, column=0, sticky=W)
Label(frame, text="CONCEPTO:\n", font=font).grid(row=3, column=0, sticky=W)
Label(frame, text="CATEGORÍA:\n", font=font).grid(row=4, column=0, sticky=W)
Label(frame, text="CANTIDAD:\n", font=font).grid(row=5, column=0, sticky=W)
Label(frame, text="PRECIO UNITARIO:\n", font=font).grid(row=6, column=0, sticky=W)
Label(frame, text="PRECIO FINAL:\n", font=font).grid(row=7, column=0, sticky=W)
# Agregar las etiquetas para las firmas
Label(frame, text="Firma del que entrega", font=font).grid(row=9, column=0, sticky=W)
Label(frame, text="_____________________", font=font).grid(row=8, column=0, sticky=W)
Label(frame, text="Firma del cliente", font=font).grid(row=9, column=1, sticky=E)
Label(frame, text="_____________________", font=font).grid(row=8, column=1, sticky=E)

root.mainloop()
