from tkinter import Tk, messagebox, ttk
from webbrowser import open
import socket
import qrcode
import qrcode.image.svg
from PIL import ImageTk, Image,ImageDraw,ImageFont
import os

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

LAN = not ip.startswith("127")

def generar_imagen_qr():
    from main import PUERTO

    url = f'http://{ip}:{PUERTO}'

    png = qrcode.make(url)
    png.save('static/qr.png')
    svg = qrcode.make(url, image_factory=qrcode.image.svg.SvgPathImage)
    svg.save('static/qr.svg')


def abrir_navegador(label):
    ip_address = label.cget("text")
    url = f"http://{ip_address}"
    try:
        open(url)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir el navegador: {e}")


def abrir_ventana():
    from main import PUERTO

    ventana = Tk()
    ventana.title("Registro Comunal")
    ventana.resizable(False, False)
    ventana.configure()

    root = ttk.Frame(
        ventana,
        padding="20 20 15 15",
    )
    root.pack(expand=True, fill="both")

    ttk.Label(
        root,
        text="Servidor iniciado",
        font=("Segoe UI", 15, "bold"),
    ).pack(pady=(0, 20))

    ttk.Label(
        root,
        text="Para acceder a la aplicación, haz click o ingresa la siguiente dirección en el navegador:",
        foreground="#6A6A6A",
        font=("Segoe UI", 11),
    ).pack(padx=10)

    ip_label = ttk.Label(
        root,
        text=f"127.0.0.1:{PUERTO}",
        foreground="blue",
        cursor="hand2",
        font=("Segoe UI", 14, "underline", "bold"),
    )

    ip_label.pack(pady=10)

    # Asignar el evento de click
    ip_label.bind("<Button-1>", lambda _: abrir_navegador(ip_label))

    if LAN:
        f = ttk.Frame(root)
        f.pack(pady=(20, 0))

        ttk.Label(
            f,
            text="O ingresa la siguiente dirección en el navegador de otro dispositivo (ambos deben estar conectados a la misma red):",
            foreground="#6A6A6A",
            font=("Segoe UI", 11),
        ).pack(padx=10)

        ttk.Label(
            f,
            text=f"{ip}:{PUERTO}",
            foreground="blue",
            cursor="hand2",
            font=("Segoe UI", 14, "underline", "bold"),
        ).pack(pady=10)

        img = Image.open('static/qr.png')
        qr = ImageTk.PhotoImage(img)
        panel = ttk.Label(f, image=qr)
        panel.pack(pady=(10,0))

    root.mainloop()
