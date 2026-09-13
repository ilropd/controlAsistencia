# Actualización de registros de empleados

## Descripción

El módulo implementa la función `actualizar_registro()`, cuya finalidad es buscar y modificar un registro de jornada laboral asociado a un empleado.

La función permite actualizar:

- La hora de entrada.
- La hora de salida.
- El estado de la salida (`Pendiente`).
- El total de horas trabajadas, recalculándolo automáticamente cuando corresponde.

Los datos se cargan desde un archivo JSON, se modifican en memoria y finalmente se guardan de nuevo en el almacenamiento.

---

## Función principal

```python
actualizar_registro()
```

La función no recibe parámetros. Toda la información necesaria se solicita interactivamente al usuario mediante la consola.

### Flujo general

El funcionamiento de la función puede resumirse en los siguientes pasos:

1. Cargar todos los registros almacenados.
2. Solicitar y validar el ID del empleado.
3. Buscar los registros asociados al empleado.
4. Solicitar la fecha del registro que se desea modificar.
5. Solicitar una nueva hora de entrada.
6. Solicitar una nueva hora de salida.
7. Validar la coherencia entre las horas.
8. Actualizar los datos correspondientes.
9. Recalcular las horas trabajadas cuando sea necesario.
10. Guardar los cambios.
11. Informar al usuario de que la actualización se ha realizado correctamente.

---

## Dependencias

La función utiliza varios módulos internos del proyecto:

```python
from datetime import datetime

from app.json_utils.cargar_json import cargar_datos
from app.json_utils.guardar_json import guardar_datos
from app.utils import calcular_tiempo_trabajado
from app.utils.mensajes import msg
from app.utils import limpiar_pantalla
from app.utils import validar_id_empleado
```

### `datetime`

Se utiliza para validar y convertir:

- Fechas con formato `DD/MM/YYYY`.
- Horas con formato `HH:MM`.

### `cargar_datos()`

Carga en memoria los registros almacenados en el archivo JSON.

### `guardar_datos(datos)`

Guarda en el archivo JSON los registros después de haber sido modificados.

### `calcular_tiempo_trabajado()`

Calcula el tiempo trabajado a partir de la hora de entrada y la hora de salida.

### `msg()`

Centraliza los mensajes mostrados al usuario, permitiendo mantener los textos de la aplicación separados de la lógica principal.

### `limpiar_pantalla()`

Limpia la consola después de determinadas operaciones para mejorar la interacción con el usuario.

### `validar_id_empleado()`

Comprueba que el identificador introducido por el usuario cumple el formato establecido para los empleados.

---

## Búsqueda del empleado

El primer paso consiste en cargar todos los registros:

```python
datos = cargar_datos()
```

A continuación, se solicita el identificador del empleado:

```python
empleado_id = input(msg("id_del_empleado")).upper()
```

El ID se convierte a mayúsculas y posteriormente se valida:

```python
if not validar_id_empleado(empleado_id):
    raise ValueError
```

Después se buscan todos los registros pertenecientes al empleado:

```python
coincidencias = [
    data for data in datos
    if data.get("empleado") == empleado_id
]
```

### Situaciones posibles

#### ID con formato incorrecto

Se muestra un mensaje de error y se vuelve a solicitar el identificador.

#### Empleado sin registros

Si no existe ningún registro asociado al empleado, se informa al usuario y se permite realizar una nueva búsqueda.

#### Un único registro

El registro encontrado se muestra directamente.

#### Varios registros

Se muestran todos los registros asociados al empleado para que el usuario pueda identificar posteriormente el correspondiente a la fecha deseada.

---

## Selección de la fecha

Una vez identificado el empleado, se solicita la fecha del registro:

```python
fecha = datetime.strptime(
    input(msg("introduzca_fecha_para_cambios.")),
    "%d/%m/%Y"
).date()
```

El formato obligatorio es:

```text
DD/MM/YYYY
```

Por ejemplo:

```text
15/03/2026
```

La función busca posteriormente un registro que coincida tanto con el empleado como con la fecha seleccionada.

Si no existe ninguna coincidencia, se informa al usuario y se vuelve a solicitar una fecha.

---

## Modificación de la hora de entrada

La hora de entrada debe introducirse en formato:

```text
HH:MM
```

Por ejemplo:

```text
08:30
```

También existe la posibilidad de pulsar `Enter` sin introducir ningún valor.

En ese caso:

```python
entrada = None
```

y se conserva la hora de entrada que ya tenía el registro.

Esto permite modificar únicamente la hora de salida sin tener que volver a introducir la hora de entrada.

---

## Modificación de la hora de salida

La hora de salida también utiliza el formato:

```text
HH:MM
```

También puede dejarse vacía para mantener el valor existente.

Además, existe un estado especial:

```text
Pendiente
```

Este estado permite representar una jornada que todavía no tiene una hora de salida registrada.

Cuando se introduce:

```text
pendiente
```

se almacena:

```python
data_encontrada["salida"] = "Pendiente"
data_encontrada["horas_trabajadas"] = "Pendiente"
```

---

## Validación de horarios

Cuando se introduce una nueva hora de salida y también se ha introducido una nueva hora de entrada, se comprueba que la salida sea posterior a la entrada:

```python
if entrada is not None and salida <= entrada:
    print(msg("hora_salida_posterior_hora_entrada"))
    continue
```

Por ejemplo:

```text
Entrada: 08:30
Salida:  17:00
```

es válido.

Mientras que:

```text
Entrada: 17:00
Salida:  08:30
```

no es válido.

La función solicita nuevamente la hora de salida en este último caso.

---

## Actualización de los datos

La hora de entrada solo se modifica cuando el usuario ha introducido un nuevo valor:

```python
if entrada is not None:
    data_encontrada["entrada"] = entrada.strftime("%H:%M")
```

De esta forma, pulsar `Enter` conserva el valor anterior.

La hora de salida funciona de manera similar:

```python
if salida is not None:
    ...
```

Si el usuario introduce `Pendiente`, tanto la salida como las horas trabajadas pasan a tener ese estado.

---

## Recalculo de horas trabajadas

Cuando existen una hora de entrada y una hora de salida válidas, se recalcula automáticamente el tiempo trabajado:

```python
data_encontrada["horas_trabajadas"] = calcular_tiempo_trabajado(
    data_encontrada["entrada"],
    data_encontrada["salida"]
)
```

El cálculo únicamente se realiza cuando la salida no está establecida como:

```text
Pendiente
```

Por tanto:

### Registro completo

```text
Entrada:          08:00
Salida:           16:30
Horas trabajadas: 08:30
```

### Registro pendiente

```text
Entrada:          08:00
Salida:           Pendiente
Horas trabajadas: Pendiente
```

---

## Persistencia de los cambios

Una vez finalizada la modificación, todos los datos se guardan mediante:

```python
guardar_datos(datos)
```

Esto permite que los cambios realizados en memoria queden almacenados permanentemente en el archivo JSON utilizado por la aplicación.

---

## Manejo de errores

La función utiliza bloques `try/except` para controlar entradas incorrectas del usuario.

### Identificador

Se controla cualquier error relacionado con la validación del ID:

```python
except ValueError:
```

### Fecha

Se controla una fecha introducida con un formato incorrecto:

```text
31/02/2026
```

o con un formato diferente de:

```text
DD/MM/YYYY
```

### Horas

Se valida que las horas respeten el formato:

```text
HH:MM
```

Por ejemplo:

```text
09:45
```

es válido, mientras que:

```text
9.45
```

no lo es.

---

## Estructura esperada de un registro

La función trabaja con registros que contienen, como mínimo, información similar a:

```json
{
    "empleado": "EMP001",
    "fecha": "12/09/2026",
    "entrada": "08:00",
    "salida": "16:30",
    "horas_trabajadas": "08:30"
}
```

Cuando la jornada todavía no ha finalizado:

```json
{
    "empleado": "EMP001",
    "fecha": "12/09/2026",
    "entrada": "08:00",
    "salida": "Pendiente",
    "horas_trabajadas": "Pendiente"
}
```

---

## Características principales

- Validación del identificador del empleado.
- Búsqueda de registros por empleado.
- Selección del registro mediante fecha.
- Validación de fechas.
- Validación de horas.
- Posibilidad de conservar valores existentes pulsando `Enter`.
- Posibilidad de establecer una salida como `Pendiente`.
- Validación de que la hora de salida sea posterior a la entrada.
- Recalculo automático de las horas trabajadas.
- Persistencia de los cambios en JSON.
- Gestión de errores de entrada.
- Mensajes de usuario centralizados mediante `msg()`.

---

## Resumen del flujo

```text
Cargar registros
       │
       ▼
Solicitar ID empleado
       │
       ▼
Validar ID
       │
       ├── Inválido ──────► Volver a solicitar
       │
       ▼
Buscar registros
       │
       ├── No encontrado ─► Volver a solicitar
       │
       ▼
Solicitar fecha
       │
       ├── Fecha inválida ─► Volver a solicitar
       │
       ▼
Localizar registro
       │
       ▼
Modificar entrada
       │
       ▼
Modificar salida
       │
       ├── Pendiente
       │
       ▼
Validar horarios
       │
       ▼
Recalcular horas trabajadas
       │
       ▼
Guardar datos
       │
       ▼
Mostrar confirmación
```

---

## Resultado

La función `actualizar_registro()` proporciona una interfaz de consola para modificar de forma controlada los registros de jornada de los empleados, manteniendo las validaciones necesarias para evitar datos inconsistentes y actualizando automáticamente el tiempo trabajado cuando se dispone de una entrada y una salida válidas.