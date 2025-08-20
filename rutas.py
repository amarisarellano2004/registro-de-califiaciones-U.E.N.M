import sqlite3
from db.db import abrir_base_de_datos
from flask import render_template, request, flash, Blueprint, jsonify, redirect, session
from constantes import (
    NOMBRE_MAXIMO,
    NOMBRE_MINIMO,
    CONTRASEÑA_MINIMO,
    CONTRASEÑA_MAXIMA,
)

rutas = Blueprint("rutas", __name__)


@rutas.route("/login", methods=["GET", "POST"])
def login():
    sesion = session.get('usuario', '')

    if sesion:
        return redirect('/')

    datos = {}

    if request.method == "POST":
        conexion, cursor = abrir_base_de_datos()

        print(request.form)
        datos = request.form

        if len(datos["usuario"]) < NOMBRE_MINIMO:
            flash(
                f"El usuario debe contener al menos {NOMBRE_MINIMO} caracteres", "error"
            )
        elif len(datos["usuario"]) > NOMBRE_MAXIMO:
            flash(
                f"el usuario debe contener menos de {NOMBRE_MAXIMO} caracteres", "error"
            )
        else:
            usuario_en_base_de_datos = cursor.execute('SELECT nombre FROM usuarios WHERE nombre = ?', (datos['usuario'],)).fetchone()

            if not usuario_en_base_de_datos:
                flash('El usuario no se encuentra registrado', 'error')
            elif len(datos["contraseña"]) < CONTRASEÑA_MINIMO:
                flash(
                    f"La contraseña debe contener al menos {CONTRASEÑA_MINIMO} caracteres",
                    "error",
                )
            elif len(datos["contraseña"]) > CONTRASEÑA_MAXIMA:
                flash(
                    f"la contraseña debe contener maximo {CONTRASEÑA_MAXIMA} caracteres",
                    "error",
                )
            else:
                from main import encriptado

                contraseña_en_la_base_de_datos = (cursor.execute('SELECT contraseña FROM usuarios WHERE nombre = ? LIMIT 1', (datos['usuario'], )).fetchone())[0]

                if not encriptado.check_password_hash(contraseña_en_la_base_de_datos, datos['contraseña']):
                    flash('Su contraseña es incorreta intentalo de nuevo', 'error')
                else:
                    flash("Ha iniciado sesion con exito ", "exito")
                    session['usuario'] = datos['usuario']
                    return redirect('/')

    return render_template(
        "login.html",
        datos = datos,
        NOMBRE_MINIMO=NOMBRE_MINIMO,
        CONTRASEÑA_MINIMO=CONTRASEÑA_MINIMO,
        NOMBRE_MAXIMO=NOMBRE_MAXIMO,
        CONTRASEÑA_MAXIMA=CONTRASEÑA_MAXIMA,
    )


@rutas.route("/registro", methods=["GET", "POST"])
def registro():
    sesion = session.get('usuario', '')

    if sesion:
        return redirect('/')

    datos={}
    if request.method == "POST":
        datos = request.form
        conexion, cursor = abrir_base_de_datos()

        if len(datos["usuario"]) < NOMBRE_MINIMO:
            flash(
                f"El usuario debe contener al menos {NOMBRE_MINIMO} caracteres", "error"
            )
        elif len(datos["usuario"]) > NOMBRE_MAXIMO:
            flash(
                f"el usuario debe contener menos de {NOMBRE_MAXIMO} caracteres", "error"
            )
        else:
            nombre_ya_existe = cursor.execute('SELECT id FROM usuarios WHERE nombre = ? LIMIT 1',(datos["usuario"].strip(),)).fetchone()

            if nombre_ya_existe:
                flash(" El nombre de usuario ya esta registrado","error")

            elif len(datos["contraseña"]) < CONTRASEÑA_MINIMO:
                flash(
                    f"La contraseña debe contener al menos {CONTRASEÑA_MINIMO} caracteres",
                    "error",
                )
            elif len(datos["contraseña"]) > CONTRASEÑA_MAXIMA:
                flash(
                    f"la contraseña debe contener maximo {CONTRASEÑA_MAXIMA} caracteres",
                    "error",
                )
            else:
                from main import encriptado

                contraseña = datos["contraseña"].strip()

                contraseña_encriptada = encriptado.generate_password_hash (contraseña).decode('utf-8')

                cursor.execute(
                    "INSERT INTO usuarios (nombre,contraseña) values(?, ?)",
                    (datos["usuario"].strip() ,contraseña_encriptada),
                )
                conexion.commit()

                session['usuario'] = datos['usuario']
                flash("Los datos han sido guardado con exito", "exito")
                return redirect('/')

        conexion.close()

    return render_template(
        "registro.html",
        datos = datos,
        NOMBRE_MINIMO=NOMBRE_MINIMO,
        CONTRASEÑA_MINIMO=CONTRASEÑA_MINIMO,
        NOMBRE_MAXIMO=NOMBRE_MAXIMO,
        CONTRASEÑA_MAXIMA=CONTRASEÑA_MAXIMA,
    )

@rutas.route("/usuarios")
def usuarios():
    conexion,cursor = abrir_base_de_datos(True)

    usuarios = cursor.execute("SELECT * FROM usuarios").fetchall()
    return [dict(row) for row in usuarios]

@rutas.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        session.pop('usuario')
        return redirect('/login')
    return render_template('inicio.html')
