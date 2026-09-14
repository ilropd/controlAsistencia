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


#Funcion para mostrar registros 
def mostrar_registros(registros):
    """Muestra una lista de registros de asistencia en formato tabla.
    Args: registros(list): lista de registros que se va a mostrar
    Returns: Ninguno""" 
    print(
        f"{'ID':<5} | "
        f"{'Empleado':<8} | "
        f"{'Fecha':<10} | "
        f"{'Entrada':<7} | "
        f"{'Salida':<9} | "
        f"{'Horas':<6}"
    )

    print("-" * 61)
    
    for r in registros:
        print(
            f"{r['id']:<5} | "
            f"{r['empleado']:<8} | "
            f"{r['fecha']:<10} | "
            f"{r['entrada']:<7} | "
            f"{r['salida']:<9} | "
            f"{r['horas_trabajadas']:<6}"
        )

def buscar_registro_por_id(registros, reg_id):
    """Busca un registro concreto por su ID.
    Args: registros(list), reg_id(int): id del registro
    Returns: dict: registro encontrado, None: registro no encontrado
    """
    for registro in registros:
        if registro["id"] == reg_id:
            return registro

    return None

def buscar_registros_por_empleado(datos, emp_id):
    """Obtiene todos los registros de un empleado
    Args: datos(list), emp_id(int): Id del empleado
    Retrns: list: Regsitros del empleado"""
    return [
        registro for registro in datos
        if registro["empleado"] == emp_id
    ]

def solicitar_id_empleado():
    """Solicita y valida el Id de un empleado
    Returns: str: Id del empleado valido"""
    while True:
        emp_id = input("Ingrese el ID del empleado: ").strip().upper()

        if validar_id_empleado(emp_id):
            return emp_id

        print("ID de empleado inválido.")

def solicitar_registro_a_eliminar(registros_empleado):
    """Solicita un Id de registro hasta encontrar uno del empleado
    Args: registros_empleados(list): registros del empleado
    Returns: dict: registros selecionado para eliminar"""
    while True:
        try:
            reg_id = int(
                input("Ingrese el ID del registro a eliminar: ").strip()
            )
        except ValueError:
            print("ID inválido.")
            continue
    
        registro_seleccionado = buscar_registro_por_id(
            registros_empleado,
            reg_id
        )
    
        if registro_seleccionado is None:
            print("El registro indicado no pertenece a este empleado.")
            continue
    
        return registro_seleccionado

def solicitar_opcion_eliminacion():
    """Muestra el menú de eliminacion y solicita una opcion valida
    Returns:opcion(str): opcion selecionada por el usuario"""
    while True:
        print("\n1. Eliminar un registro")
        print("2. Eliminar todos los registros")
        print("3. Cancelar")

        opcion = input("Seleccione una opción: ").strip()

        if opcion in ("1", "2", "3"):
            return opcion

        print("Opción inválida.")

def solicitar_confirmacion(mensaje):
    """Solicita al usuario una confirmación mediante s/n.
    Args: mensaje(str): Mensaje que se mostrará
    Returns: booleano (True confirmacion, False si cancela)"""
    while True:
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        
        if respuesta == "s":
            return True
        
        if respuesta == "n":
            return False
        
        print("Opción invalida. Introduzca s o n")

        
def eliminar_un_registro(datos, registros_empleado):
    """Eliminar un registro de un empleado despues de solicitar confirmacion
    Args: datos(list), registros_empleados(list): registros pertencientes al empleado
    Returns: Ninguno"""
    
    registro_seleccionado = solicitar_registro_a_eliminar(
        registros_empleado
    )   

    mostrar_registros([registro_seleccionado])

    if solicitar_confirmacion(
        "¿Está seguro de que desea eliminar este registro?"
    ):
        datos.remove(registro_seleccionado)
        guardar_datos(datos)
        print("\nRegistro eliminado correctamente.")
    else:
        print("Eliminación cancelada.")

    time.sleep(1)
    

def eliminar_todos_registros(datos, emp_id):
    """Elimina todos los registros de un empleado
    Args: datos(list), emp_id(str): Id del empleado
    Returns: Ninguno"""
    if solicitar_confirmacion(
        f"¿Está seguro de que desea eliminar todos los registros de {emp_id}?"
    ):
        datos = [
            registro for registro in datos
            if registro["empleado"] != emp_id
        ]

        guardar_datos(datos)
        print("\nTodos los registros del empleado han sido eliminados.")
    else:
        print("Eliminación cancelada.")

    time.sleep(1)


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
    
    if datos is None:
        return
    
    if not datos:
        print("No hay registros en el sistema.")
        time.sleep(5)  # Aplico un Temporizador.
        Borro()
        return
    
    mostrar_registros(datos)


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


# 9. Función para Eliminar Registro
def eliminar_registro():
    """Gestiona el proceso para eliminar registros de un empleado
    Returns: Ninguno"""
    datos = cargar_datos()
    
    if datos is None:
        time.sleep(1)
        return
    
    if not datos:
        print("No hay registros en el sistema")
        time.sleep(1)
        return
    
    emp_id = solicitar_id_empleado()
    
    registros_empleado = buscar_registros_por_empleado(
        datos,
        emp_id
    )
    
    if not registros_empleado:
        print("No hay registros para este empleado.")
        time.sleep(1)
        return
    
    mostrar_registros(registros_empleado)
            
    opcion = solicitar_opcion_eliminacion()

    if opcion == "1":
        eliminar_un_registro(datos, registros_empleado)
        

    elif opcion == "2":
        eliminar_todos_registros(datos, emp_id)
        

    elif opcion == "3":
        print("Eliminación cancelada.")
        time.sleep(1)
        


# 10. Función_
def menu():
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
            crear_registro()
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
