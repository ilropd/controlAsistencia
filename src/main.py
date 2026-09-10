from func.registro import crear_registro, leer, eliminar_empleado
from func.repositorio import iniciar
from util.limpiar_pantalla import limpiar_pantalla


def menu():
    while True:
        print("\n---  CONTROL DE ASISTENCIA  ---\n")
        print("1. Registrar Entrada/Salida (Crear)")
        print("2. Ver Registros (Leer)")
        #print("3. Actualizar Registro")
        print("4. Eliminar Empleado")
        print("5. Salir")
        opcion = input("\nSeleccione una opción: ")
        # Creamos todo el CRUD
        if opcion == "1":
            crear_registro()
        elif opcion == "2":
            leer()
        elif opcion == "3":
            print("This feature is not implemented yet")
        elif opcion == "4":
            eliminar_empleado()
        elif opcion == "5":
            limpiar_pantalla()  # Borramos pantalla antes de salir.
            break
        else:
            print("Opción inválida en el menú.")


# Comienzo del program evitando interferencias de terceros.
if __name__ == "__main__":
    iniciar()
    menu()
