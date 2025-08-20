import sqlite3
from constantes import ROLES, CONTRASEÑA_MAXIMA,CONTRASEÑA_MINIMO,NOMBRE_MAXIMO,NOMBRE_MINIMO, RUTA_BASE
import os

def abrir_base_de_datos(usar_row: bool = False):
    conexion=sqlite3.connect(os.path.join(RUTA_BASE, "db.db"))
    if (usar_row):
        conexion.row_factory=sqlite3.Row
    cursor=conexion.cursor()

    cursor.executescript(f"""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE CHECK(length(trim(nombre)) >= {NOMBRE_MINIMO} AND length(trim(nombre)) <= {NOMBRE_MAXIMO}),
            contraseña TEXT NOT NULL,
            rol TEXT CHECK(rol = NULL OR rol IN {ROLES})
        )
    """)
    return (conexion,cursor)
