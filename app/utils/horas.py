from datetime import datetime


def calcular_tiempo_trabajado(entrada, salida):
    if entrada and salida:
        hora_entrada = datetime.strptime(entrada, "%H:%M")
        hora_salida = datetime.strptime(salida, "%H:%M")

        worktime = hora_salida - hora_entrada

        # Convertir a horas/minutos
        total_seconds = int(worktime.total_seconds())
        horas, resto = divmod(total_seconds, 3600)
        minutos, segundos = divmod(resto, 60)

        return f"{horas:02d}:{minutos:02d}"
    else:
        return "Pendiente"
