from tkinter import filedialog, messagebox
import subprocess
import shutil
import sys
import os



def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative)

def obtener_ffmpeg():
    # 1️⃣ buscar ffmpeg local (proyecto / AppImage / PyInstaller)
    ffmpeg_local = resource_path("ffmpeg")
    if os.path.exists(ffmpeg_local):
        return ffmpeg_local

    # 2️⃣ buscar ffmpeg del sistema
    ffmpeg_sistema = shutil.which("ffmpeg")
    if ffmpeg_sistema:
        return ffmpeg_sistema

    # 3️⃣ nada encontrado → error claro
    messagebox.showerror(
        "FFmpeg no encontrado",
        "No se encontró ffmpeg.\n\n"
        "Inclúyelo junto a la app o instálalo desde:\n"
        "https://ffmpeg.org/download.html"
    )
    return None

def seleccionar_video(entrada):
    archivo = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[("Videos", "*.mp4 *.avi *.mkv *.mov *.webm")]
    )
    if archivo:
        entrada.set(archivo)

def convertir(entrada, formato_salida, estado, progreso, ventana):
    if not entrada.get():
        messagebox.showerror("Error", "Selecciona un video")
        return
    
    # verfificar que los formmatos no sean iguales
    ext_entrada = os.path.splitext(entrada.get())[1].lower().lstrip('.')
    if ext_entrada == formato_salida.get().lower():
        messagebox.showerror("Error", "El formato de salida debe ser diferente al de entrada")
        return

    ffmpeg = obtener_ffmpeg()
    if not ffmpeg:
        return

    archivo_salida = filedialog.asksaveasfilename(
        title="Guardar video",
        defaultextension=f".{formato_salida.get()}",
        filetypes=[("Video", f"*.{formato_salida.get()}")]
    )

    if not archivo_salida:
        return

    comando = [ffmpeg, "-y", "-i", entrada.get(), archivo_salida]

    try:
        estado.set("⏳ Convirtiendo...")
        progreso.start(10)
        ventana.update()

        subprocess.run(comando, check=True)

        progreso.stop()
        estado.set("✅ Conversión completada")
        messagebox.showinfo("Listo", "Video convertido")

    except Exception as e:
        progreso.stop()
        estado.set("❌ Error")
        messagebox.showerror("Error", str(e))
