import platform
import subprocess

def Borro():
    """Limpia la pantalla de la consola según el sistema operativo."""
    if platform.system() == "Windows":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run(["clear"])