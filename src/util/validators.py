import re

def validar_id_empleado(emp_id):
    patron = r"^[A-Z]{3}\d{3}$"
    return bool(re.match(patron, emp_id))