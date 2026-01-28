import tkinter as tk
from tkinter import ttk
import utils

ventana = tk.Tk()
ventana.title("Video Converter")
ventana.geometry("450x330")
ventana.resizable(False, False)

entrada = tk.StringVar()
formato_salida = tk.StringVar(value="mp4")
estado = tk.StringVar()

tk.Label(ventana, text="Video de entrada").pack(pady=5)
tk.Entry(ventana, textvariable=entrada, width=55).pack()
tk.Button(
    ventana,
    text="Seleccionar",
    command=lambda: utils.seleccionar_video(entrada)
).pack(pady=5)

tk.Label(ventana, text="Formato de salida").pack(pady=5)
tk.OptionMenu(ventana, formato_salida, "mp4", "avi", "mkv", "webm").pack()

progreso = ttk.Progressbar(ventana, mode="indeterminate")
progreso.pack(pady=10, fill=tk.X, padx=20)

tk.Button(
    ventana,
    text="Convertir",
    bg="#4CAF50",
    fg="white",
    command=lambda: utils.convertir(
        entrada, formato_salida, estado, progreso, ventana
    )
).pack(pady=15)

tk.Label(ventana, textvariable=estado).pack()

ventana.mainloop()
