import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# ---------- Funciones ----------
def seleccionar_video():
    archivo = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[("Videos", "*.mp4 *.avi *.mkv *.mov *.webm")]
    )
    if archivo:
        entrada.set(archivo)

def convertir():
    if not entrada.get():
        messagebox.showerror("Error", "Selecciona un video")
        return

    formato = formato_salida.get()
    if not formato:
        messagebox.showerror("Error", "Selecciona un formato")
        return

    archivo_entrada = entrada.get()
    nombre_base = os.path.splitext(archivo_entrada)[0]
    archivo_salida = f"{nombre_base}_convertido.{formato}"

    comando = [
        "ffmpeg",
        "-y",
        "-i", archivo_entrada,
        archivo_salida
    ]

    try:
        estado.set("⏳ Convirtiendo...")
        ventana.update()

        subprocess.run(
            comando,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        estado.set("✅ Conversión completada")
        messagebox.showinfo("Listo", f"Video guardado como:\n{archivo_salida}")

    except Exception as e:
        estado.set("❌ Error")
        messagebox.showerror("Error", str(e))


# ---------- Interfaz ----------
ventana = tk.Tk()
ventana.title("Conversor de Video")
ventana.geometry("450x250")
ventana.resizable(False, False)

entrada = tk.StringVar()
formato_salida = tk.StringVar()
estado = tk.StringVar()

tk.Label(ventana, text="Video de entrada").pack(pady=5)
tk.Entry(ventana, textvariable=entrada, width=50).pack()
tk.Button(ventana, text="Seleccionar", command=seleccionar_video).pack(pady=5)

tk.Label(ventana, text="Formato de salida").pack(pady=5)
tk.OptionMenu(ventana, formato_salida, "mp4", "avi", "mkv", "webm").pack()

tk.Button(
    ventana,
    text="Convertir",
    bg="#4CAF50",
    fg="white",
    command=convertir
).pack(pady=15)

tk.Label(ventana, textvariable=estado).pack()

ventana.mainloop()
