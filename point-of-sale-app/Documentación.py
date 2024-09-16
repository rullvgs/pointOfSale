import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import json

class FotoPerfilApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Foto de Perfil")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.label_foto = tk.Label(self.frame, text="Foto de Perfil")
        self.label_foto.pack()

        self.boton_cargar = tk.Button(self.frame, text="Cargar Foto", command=self.cargar_foto)
        self.boton_cargar.pack()

        self.boton_eliminar = tk.Button(self.frame, text="Eliminar Foto", command=self.eliminar_foto)
        self.boton_eliminar.pack()

        self.foto_perfil = None
        self.label_imagen = tk.Label(self.frame)
        self.label_imagen.pack()

        self.cargar_foto_guardada()

    def cargar_foto(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de Imagen", "*.png;*.jpg;*.jpeg;*.gif"), ("Todos los archivos", "*.*")])
        if archivo:
            imagen = Image.open(archivo)
            imagen = imagen.resize((150, 150), Image.ANTIALIAS)
            
            # Crear una máscara circular
            mascara = Image.new("L", imagen.size, 0)
            draw = ImageDraw.Draw(mascara)
            draw.ellipse((0, 0, imagen.width, imagen.height), fill=255)
            
            # Aplicar la máscara a la imagen
            imagen_circular = Image.new("RGBA", imagen.size)
            imagen_circular.paste(imagen, mask=mascara)
            
            self.foto_perfil = ImageTk.PhotoImage(imagen_circular)

            self.label_imagen.config(image=self.foto_perfil)
            self.label_imagen.image = self.foto_perfil

            self.guardar_ruta_imagen(archivo)

    def cargar_foto_guardada(self):
        try:
            with open("config.json", "r") as f:
                data = json.load(f)
                ruta_imagen = data.get("ruta_imagen", "")
                if ruta_imagen:
                    imagen = Image.open(ruta_imagen)
                    imagen = imagen.resize((150, 150), Image.ANTIALIAS)

                    # Crear una máscara circular
                    mascara = Image.new("L", imagen.size, 0)
                    draw = ImageDraw.Draw(mascara)
                    draw.ellipse((0, 0, imagen.width, imagen.height), fill=255)

                    # Aplicar la máscara a la imagen
                    imagen_circular = Image.new("RGBA", imagen.size)
                    imagen_circular.paste(imagen, mask=mascara)

                    self.foto_perfil = ImageTk.PhotoImage(imagen_circular)

                    self.label_imagen.config(image=self.foto_perfil)
                    self.label_imagen.image = self.foto_perfil
        except FileNotFoundError:
            pass

    def guardar_ruta_imagen(self, ruta):
        data = {"ruta_imagen": ruta}
        with open("config.json", "w") as f:
            json.dump(data, f)

    def eliminar_foto(self):
        try:
            self.foto_perfil = None
            self.label_imagen.config(image="")
            self.guardar_ruta_imagen("")
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = FotoPerfilApp(root)
    root.mainloop()