import json, re, sys, time
from datetime import datetime
from BorroPantalla import Borro  # Desde la aplicación BorroPantalla importo la funcion.

## Mejor usar esto para asegurar que el archivo JSON siempre esta en el mismo lugar,
## en la misma carpeta del archivo principal
# from pathlib import Path
# FILE_NAME = Path(__file__).parent / "asistencia.json"

FILE_NAME = "asistencia.json"


# 1. Función
def cargar_datos() -> list | None:
    """
    Carga y valida la estructura de los datos del archivo JSON.

    Comprueba que el contenido del archivo sea una lista y, si contiene registros,
    verifica que cada registro sea un diccionario con todos los campos requeridos.

    Returns:
        list:
            Lista de registros si el archivo tiene una estructura válida.
        []:
            Si el archivo no existe o la lista de registros está vacía.
        None:
        Si el archivo contiene una estructura no válida o está dañado.
    """
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            datos = json.load(f)

        # El archivo debe contener una lista
        if not isinstance(datos, list):
            print("\n❌ La estructura del archivo JSON no es válida.")
            return None

        # Si la lista está vacía, los datos son válidos
        if not datos:
            return datos

        campos_requeridos = {
            "id",
            "empleado",
            "fecha",
            "entrada",
            "salida",
            "horas_trabajadas",
        }

        # Verificamos la estructura de cada registro
        for registro in datos:
            if not isinstance(registro, dict):
                print("\n❌ La estructura de los registros no es válida.")
                return None

            if not campos_requeridos.issubset(registro):
                print("\n❌ Un registro no contiene todos los campos requeridos.")
                return None

        return datos
    # Si no hay archivo, el sistema devuelva la lista vacía
    except FileNotFoundError:
        return []

    # Si el archivo ya existe, el sistema devuelva None para salir el programa
    # Un usuario no pueda usar el programa si el archivo json está dañado
    except json.JSONDecodeError:
        print("\n❌ El archivo JSON está dañado.")
        return None


# 2. Función
def guardar_datos(datos):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# 3. Función
def validar_formato_hora(hora):
    patron = r"^([01]\d|2[0-3]):([0-5]\d)$"
    return bool(re.match(patron, hora))


# 4. Función
def validar_id_empleado(emp_id):
    patron = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(patron, emp_id))


# 5. Función
def calcular_horas(entrada, salida):
    fmt = "%H:%M"
    t_entrada = datetime.strptime(entrada, fmt)
    t_salida = datetime.strptime(salida, fmt)
    diferencia = t_salida - t_entrada
    horas = diferencia.total_seconds() / 3600
    return round(horas, 2)


# 6. Función
def crear_registro():
    datos = cargar_datos()
    emp_id = input("ID del empleado (ej. EMP001): ").upper()
    if not validar_id_empleado(emp_id):
        print(
            "❌ Formato de ID inválido. Debe ser 3 letras y 3 números (ej. EMP001).❌"
        )
        time.sleep(5)  # Aplico un Temporizador.
        Borro()
        return

    # Gestionamos formato de fechas y horas.
    fecha = datetime.now().strftime("%Y-%m-%d")
    entrada = input("Hora de entrada (HH:MM): ")
    if not validar_formato_hora(entrada):
        print("Formato de hora inválido. Use HH:MM.")
        return

    salida = input("Hora de salida (HH:MM, presione Enter si queda pendiente): ")
    horas_trabajadas = 0.0
    if salida:
        if not validar_formato_hora(salida):
            print("Formato de hora de salida inválido.")
            return
        horas_trabajadas = calcular_horas(entrada, salida)

    nuevo_id = 1 if not datos else datos[-1]["id"] + 1

    registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "fecha": fecha,
        "entrada": entrada,
        "salida": salida if salida else "Pendiente",
        "horas_trabajadas": horas_trabajadas,
    }

    # Alta de registros en el archivo.
    datos.append(registro)
    guardar_datos(datos)
    print("Registro guardado exitosamente.")


# 7. Función
def leer_registros():
    datos = cargar_datos()
    if not datos:
        print("No hay registros en el sistema.")
        time.sleep(5)  # Aplico un Temporizador.
        Borro()
        return
    for r in datos:
        print(
            f"ID: {r['id']} | Empleado: {r['empleado']} | Fecha: {r['fecha']} | Entrada: {r['entrada']} | Salida: {r['salida']} | Horas: {r['horas_trabajadas']}"
        )


# 8. Función
def actualizar_registro():
    datos = cargar_datos()
    try:
        reg_id = int(input("Ingrese el ID del registro a actualizar: "))
    except ValueError:
        print("ID inválido.")
        return

    for r in datos:
        if r["id"] == reg_id:
            print(f"Registro encontrado: {r}")
            nueva_entrada = input(f"Nueva entrada [{r['entrada']}]: ") or r["entrada"]
            if not validar_formato_hora(nueva_entrada):
                print("Hora de entrada inválida.")
                return

            nueva_salida = input(f"Nueva salida [{r['salida']}]: ") or r["salida"]
            if nueva_salida != "Pendiente" and not validar_formato_hora(nueva_salida):
                print("Hora de salida inválida.")
                return

            r["entrada"] = nueva_entrada
            r["salida"] = nueva_salida
            if nueva_salida != "Pendiente":
                r["horas_trabajadas"] = calcular_horas(nueva_entrada, nueva_salida)
            else:
                r["horas_trabajadas"] = 0.0

            guardar_datos(datos)
            print("Registro actualizado correctamente.")
            return
    print("Registro no encontrado.")


# 9. Función
def eliminar_registro():
    datos = cargar_datos()
    try:
        reg_id = int(input("Ingrese el ID del registro a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return

    nuevos_datos = [r for r in datos if r["id"] != reg_id]
    if len(nuevos_datos) == len(datos):
        print("Registro no encontrado.")
    else:
        guardar_datos(nuevos_datos)
        print("Registro eliminado correctamente.")


# 10. Funcion
def salir_registro() -> None:
    """
    Solicita confirmación al usuario antes de salir del programa.
    Muestra una pregunta de confirmación y permite responder con 's'/'si' para salir o 'n'/'no' para continuar en el programa.
    Si la respuesta no es válida, vuelve a solicitar la confirmación.

    Returns:
        None: Si el usuario decide continuar, vuelve al menú principal.
    """
    while True:
        salir = (
            input("\n❓ ¿Está seguro de que desea salir del programa (s/n)? ")
            .strip()
            .lower()
        )

        if salir in ("s", "si"):
            print("\n👋 ¡Hasta pronto!")
            time.sleep(2)
            Borro()
            sys.exit(0)

        elif salir in ("n", "no"):
            Borro()
            return

        else:
            print(
                "\n❌ Opción no válida. Por favor, introduce 's' para Sí o 'n' para No."
            )
            time.sleep(2)

            # "\033[4A" — subir el cursor 4 líneas
            # # "\033[J" — limpiar la pantalla desde el cursor hacia abajo
            print("\033[4A\033[J", end="")


# 11. Función_
def menu() -> None:
    Borro()
    while True:
        menu = [
            "1. Registrar Entrada/Salida (Crear)",
            "2. Ver Registros (Leer)",
            "3. Actualizar Registro",
            "4. Eliminar Registro",
            "5. Salir",
        ]
        print("\n--- 🔑 CONTROL DE ASISTENCIA 🔑 ---\n")
        print("\n".join(menu))

        opcion = input("\nSeleccione una opción: ").strip()

        match opcion:
            case "1":
                crear_registro()
            case "2":
                leer_registros()
            case "3":
                actualizar_registro()
            case "4":
                eliminar_registro()
            case "5":
                salir_registro()
            case _:
                input(
                    "\n❌ Opción inválida en el menú. Pulsa [ENTER] para volver al menú principal."
                )
                Borro()


# Comienzo del program evitando interferencias de terceros. ❓
if __name__ == "__main__":
    menu()
