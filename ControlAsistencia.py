import json, re, time
from datetime import datetime
from BorroPantalla import Borro  # Desde la aplicación BorroPantalla importo la funcion.

FILE_NAME = "asistencia.json"
Borro()


# 1. Función
def cargar_datos():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# 2. Función
def guardar_datos(datos):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


# 3. Función
def validar_formato_hora(hora_str):
    """Valida formato estricto de 24 horas (HH:MM)."""
    patron = r"^([01]\d|2[0-3]):([0-5]\d)$"
    return bool(re.match(patron, hora_str.strip()))


# 4. Función
def validar_id_empleado(emp_id):
    """Valida que el ID tenga el formato: 3 letras mayúsculas + 3 dígitos (ej. EMP001)."""
    patron = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(patron, emp_id.strip()))


# 5. Función
def calcular_horas(entrada, salida):
    """Calcula horas trabajadas en formato decimal."""
    fmt = "%H:%M"
    t_entrada = datetime.strptime(entrada, fmt)
    t_salida = datetime.strptime(salida, fmt)
    diferencia = (t_salida - t_entrada).total_seconds()
    
    # Validar coherencia temporal
    if diferencia < 0:
        return None
    # horas = diferencia.total_seconds() / 3600
    # return round(horas, 2)
    return round(diferencia / 3600, 2)

# 5. Función.
def buscar_registro_existente(registros, empleado_id, fecha):
    """Busca si el empleado ya fichó en la fecha actual."""
    for reg in registros:
        if reg.get("empleado") == empleado_id and reg.get("fecha") == fecha:
            return reg
    return None
def crear_registro(registros, guardar_datos_func):
    #  Captura del ID de empleado
    while True:
        emp_id = input("ID del empleado (ej. EMP001) o 'C' para cancelar: ").strip().upper()
        if emp_id == 'C':
            print("Registro cancelado.")
            time.sleep(2)
            Borro()
            return

        if validar_id_empleado(emp_id):
            break
        
        print("Formato de ID no válido. Introduce ID válido (ej. EMP001)")
        time.sleep(2)
        Borro()

    #  Gestiona formato de fecha actual
    fecha = datetime.now().strftime("%Y-%m-%d")
    
    #  Comprobación de registro existente en el día
    registro_existente = buscar_registro_existente(registros, emp_id, fecha)
    
    if registro_existente:
        print(f"\n El empleado {emp_id} ya tiene un registro hoy ({fecha}):")
        print(f"   Entrada actual: {registro_existente['entrada']}")
        print(f"   Salida actual : {registro_existente.get('salida', 'Pendiente')}")
        print("\n  Para realizar cambios, utiliza la opción 'Actualizar' en el menú principal.")
        time.sleep(3)  # Pausa previa para permitir lectura
        Borro()
        return
    
    #  Bucle independiente para la hora de entrada
    while True:
        entrada = input("Hora de entrada (HH:MM): ").strip()
        if validar_formato_hora(entrada):
            break
        print("Formato de hora inválido. Use HH:MM.")
        time.sleep(2)
        Borro()
            
    # 5. Bucle independiente para hora de salida
    while True:
        salida = input("Hora de salida (HH:MM): ").strip()
        
        if not validar_formato_hora(salida):
            print("Formato incorrecto. Usa HH:MM.")
            time.sleep(2)
            Borro()
            continue
        
        if salida <= entrada:
            print(f"La hora de salida ({salida}) no puede ser anterior o igual a la de entrada ({entrada}).")
            print("Introduce nuevamente la hora de salida.\n")
            time.sleep(2)
            Borro()
            continue  # Reintenta ÚNICAMENTE la hora de salida
        
        break  # Hora de salida completamente válida
        
    # Cálculo de horas y creación de nuevo registro
    horas_totales = calcular_horas(entrada, salida)
    nuevo_id = max([r.get("id", 0) for r in registros], default=0) + 1

    nuevo_registro = {
        "id": nuevo_id,
        "empleado": emp_id,
        "fecha": fecha,
        "entrada": entrada,
        "salida": salida,
        "horas_trabajadas": horas_totales
    }

    registros.append(nuevo_registro)
    print(f"\n Nuevo registro #{nuevo_id} guardado correctamente.")
    time.sleep(2)
    Borro()
    
    # Persistencia en JSON
    guardar_datos_func(registros)


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


# 10. Función_
def menu():
    registros = cargar_datos() #añado cargar_datos para cargar los datos en todo el menu
    while True:
        print("\n--- 🔑 CONTROL DE ASISTENCIA 🔑 ---\n")
        print("1. Registrar Entrada/Salida (Crear)")
        print("2. Ver Registros (Leer)")
        print("3. Actualizar Registro")
        print("4. Eliminar Registro")
        print("5. Salir")
        opcion = input("\nSeleccione una opción: ")
        # Creamos todo el CRUD
        if opcion == "1":
            crear_registro(registros, guardar_datos) # añado la lista y gurdar
        elif opcion == "2":
            leer_registros()
        elif opcion == "3":
            actualizar_registro()
        elif opcion == "4":
            eliminar_registro()
        elif opcion == "5":
            Borro()  # Borramos pantalla antes de salir.
            break
        else:
            print("Opción inválida en el menú.")


# Comienzo del program evitando interferencias de terceros. ❓
if __name__ == "__main__":
    menu()
