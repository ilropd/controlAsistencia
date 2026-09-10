import platform, subprocess


def Borro():
    """Limpia la pantalla de la consola según el sistema operativo actual.

    Usa el comando 'cls' ejecutado a través del shell si el sistema es
    Windows, o el comando 'clear' de forma directa si es un sistema Unix
    (Linux/macOS).
    """
    if platform.system() == "Windows":
        subprocess.run(["cls"], check=False, shell=True)
    else:
        subprocess.run(["clear"], check=False)
