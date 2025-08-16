from flask import Flask
from livereload import Server
from ventana import abrir_ventana
import sys
from typing import Callable
from threading import Thread, Event

PUERTO = 5000

app = Flask(__name__,  static_url_path="/")

app.config['SECRET_KEY'] ='1234'
app.debug = True

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        datos = (request.form)

        if len(datos ["usuario"]) < 8:
            flash("El usuario debe contener al menos 8 caracteres", 'error')
        elif len(datos["contraseña"]) < 5:
            flash('La contraseña debe contener al menos 5 caracteres', "error")
        else:
            flash("Ha iniciado sesion con exito ","exito")

    return render_template('login.html')

@app.route('/registro', methods =['GET','POST'])
def registro():
    if request.method == 'POST':
        datos = (request.form)

        if len(datos ["usuario"]) < 8:
            flash("El usuario debe contener al menos 8 caracteres", 'error')
        elif len(datos["contraseña"]) < 5:
            flash('La contraseña debe contener al menos 5 caracteres', "error")
        else:
            flash("Los datos han sido guardado con exito","exito")

    return render_template('registro.html')


def correr_servidor():
    servidor = Server(app.wsgi_app)
    servidor.watch('*/**')
    servidor.serve(
        port=PUERTO,
        host="0.0.0.0",
    )

    """
    app.run(
        host="0.0.0.0",
        debug=True,
        port=PUERTO,
    )
    """

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