import tkinter as tk
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Mostrar Fecha Actual")

        self.fecha_actual = tk.StringVar()

        self.label_fecha = tk.Label(self.root, textvariable=self.fecha_actual, font=("Arial", 12))
        self.label_fecha.pack(padx=20, pady=20)

        self.actualizar_fecha()

    def actualizar_fecha(self):
        now = datetime.now()
        formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")
        self.fecha_actual.set("Fecha y Hora Actual:\n" + formatted_date)
        self.root.after(1000, self.actualizar_fecha)  # Actualizar cada segundo

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()