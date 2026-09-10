from datetime import date, datetime, timedelta


# ============================================================
# CONVERSIONES
# ============================================================

def convertir_fecha(fecha):
    """
    Convierte una fecha del JSON (YYYY-MM-DD) a un objeto date.
    """
    return datetime.strptime(fecha, "%Y-%m-%d").date()


def convertir_hora(hora):
    """
    Convierte una hora del JSON (HH:MM:SS) a un objeto time.
    """
    return datetime.strptime(hora, "%H:%M").time()


# ============================================================
# CÁLCULO DE UN INTERVALO
# ============================================================

def calcular_intervalo(entrada, salida):
    """
    Calcula la duración de un intervalo de trabajo.

    entrada: objeto time
    salida: objeto time o None

    Retorna timedelta.
    """

    if salida is None:
        return timedelta()

    inicio = datetime.combine(date.today(), entrada)
    fin = datetime.combine(date.today(), salida)

    return fin - inicio


# ============================================================
# CÁLCULO DE UN REGISTRO
# ============================================================

def calcular_registro(registro):
    """
    Calcula la duración de un registro del JSON.
    """

    entrada = convertir_hora(registro["entrada"])

    salida = None

    if registro["salida"] is not None:
        salida = convertir_hora(registro["salida"])

    return calcular_intervalo(entrada, salida)


# ============================================================
# BUSCAR REGISTROS POR EMPLEADO
# ============================================================

def buscar_por_empleado(datos, empleado_id):
    """
    Devuelve todos los registros pertenecientes
    a un empleado.
    """

    return [
        registro
        for registro in datos["data"]
        if registro["empleado"] == empleado_id
    ]


# ============================================================
# BUSCAR REGISTROS POR EMPLEADO Y FECHA
# ============================================================

def buscar_por_fecha(datos, empleado_id, fecha):
    """
    Devuelve los registros de un empleado
    correspondientes a una fecha.

    fecha debe ser YYYY-MM-DD.
    """

    return [
        registro
        for registro in datos["data"]
        if (
                registro["empleado"] == empleado_id
                and registro["fecha"] == fecha
        )
    ]


# ============================================================
# HORAS DE UN EMPLEADO EN UN DÍA
# ============================================================

def calcular_horas_dia(datos, empleado_id, fecha):
    """
    Calcula el total trabajado por un empleado
    en una fecha determinada.

    Retorna timedelta.
    """

    registros = buscar_por_fecha(
        datos,
        empleado_id,
        fecha
    )

    total = timedelta()

    for registro in registros:
        total += calcular_registro(registro)

    return total


# ============================================================
# HORAS DE UN EMPLEADO EN UN MES
# ============================================================

def calcular_horas_mes(datos, empleado_id, año, mes):
    """
    Calcula el total trabajado por un empleado
    durante un mes.

    año: int
    mes: int

    Retorna timedelta.
    """

    total = timedelta()

    for registro in datos["data"]:

        if registro["empleado"] != empleado_id:
            continue

        fecha = convertir_fecha(registro["fecha"])

        if fecha.year != año or fecha.month != mes:
            continue

        total += calcular_registro(registro)

    return total


# ============================================================
# HORAS TOTALES DE UN EMPLEADO
# ============================================================

def calcular_horas_totales(datos, empleado_id):
    """
    Calcula todas las horas registradas de un empleado.

    Retorna timedelta.
    """

    total = timedelta()

    registros = buscar_por_empleado(
        datos,
        empleado_id
    )

    for registro in registros:
        total += calcular_registro(registro)

    return total


# ============================================================
# CONVERSIÓN A HORAS DECIMALES
# ============================================================

def horas_decimales(duracion):
    """
    Convierte un timedelta a horas decimales.

    Ejemplo:
        8:30:00 -> 8.5
    """

    return round(
        duracion.total_seconds() / 3600,
        2
    )


# ============================================================
# FORMATO HORAS:MINUTOS
# ============================================================

def formato_duracion(duracion):
    """
    Convierte timedelta a HH:MM.

    Ejemplo:
        8:25:00 -> "08:25"
    """

    segundos = int(duracion.total_seconds())

    horas, resto = divmod(segundos, 3600)
    minutos = resto // 60

    return f"{horas:02d}:{minutos:02d}"
