from flask import Flask
from ventana import abrir_ventana
import sys
from typing import Callable
from threading import Thread, Event

PUERTO = 5000

app = Flask(__name__,  static_url_path="/")

def correr_servidor():
      app.run(
            host="0.0.0.0",
            #debug=True,
            port=PUERTO,
        )

def iniciar_flask_en_hilo(evento_listo):
    try:
        # Señal que el backend se ha iniciado
        evento_listo.set()
        # Se inicia el servidor
        correr_servidor()
    except Exception as e:
        print(f"Configuracion del backend fallida: {str(e)}")
        evento_listo.set()
        sys.exit(1)

if __name__ == "__main__":
    # Se crea un evento para indicar que el inicio del backend se ha completado
    backend_listo = Event()

    # Se inicia el backend en un hilo separado
    hilo_de_flask = Thread(target=iniciar_flask_en_hilo, args=(backend_listo,))
    hilo_de_flask.daemon = True
    hilo_de_flask.start()

    print("Esperando a que se complete la configuracion del backend...")
    backend_listo.wait()
    print(
        "Configuracion del backend completada, iniciando la interfaz de usuario..."
    )

    # Se inicia la interfaz de usuario       
    abrir_ventana()