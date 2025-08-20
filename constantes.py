import sys
import os

PUERTO = 5000


NOMBRE_MINIMO=8
CONTRASEÑA_MINIMO=8
NOMBRE_MAXIMO=50
CONTRASEÑA_MAXIMA=30

ROLES=('administrador','docente','estudiante')


# Se obtiene la ruta de la interfaz
if getattr(sys, "frozen", False):
    # Ruta de la aplicación compilada con PyInstaller
    RUTA_BASE = sys._MEIPASS  # type: ignore
else:
    # Ruta de la aplicación no compilada
    RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
