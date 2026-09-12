import re
from datetime import datetime

from app.registros.actualizar import actualizar_registro
from app.registros.crear import crear_registro
from app.registros.eliminar import eliminar_registro
from app.registros.leer import leer_registros
from utils.pantalla import limpiar_pantalla

limpiar_pantalla()

# 3. Función
def validar_formato_hora(hora):
    patron = r"^([01]\d|2[0-3]):([0-5]\d)$"
    return bool(re.match(patron, hora))

# 5. Función
def calcular_horas(entrada, salida):
    fmt = "%H:%M"
    t_entrada = datetime.strptime(entrada, fmt)
    t_salida = datetime.strptime(salida, fmt)
    diferencia = t_salida - t_entrada
    horas = diferencia.total_seconds() / 3600
    return round(horas, 2)


# 10. Función
def menu():
    while True:
        print("\n---  CONTROL DE ASISTENCIA  ---\n")
        print("1. Registrar Entrada/Salida (Crear)")
        print("2. Ver Registros (Leer)")
        print("3. Actualizar Registro")
        print("4. Eliminar Registro")
        print("5. Salir")
        opcion = input("\nSeleccione una opción: ")
        # Creamos todo el CRUD
        if opcion == "1":
            crear_registro()
        elif opcion == "2":
            leer_registros()
        elif opcion == "3":
            actualizar_registro()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            limpiar_pantalla() # Borramos pantalla antes de salir.
            break
        else:
            print("Opción inválida en el menú.")

# Comienzo del program evitando interferencias de terceros.
if __name__ == "__main__":
    menu()
    