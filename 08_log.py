# definimos la funcion
def analizar_linea(linea):
    # Quitamos espacios al principio y al final
    linea = linea.strip()

    # Ignoramos las líneas vacías y los comentarios
    if not linea or linea.startswith("#"):
        return None, None

    # Separamos los campos usando cualquier espacio en blanco
    campos = linea.split()

    # Verificamos que existan exactamente seis campos
    if len(campos) != 6:
        return None, "Cantidad de campos incorrecta"

    fecha, hora, equipo, canal, magnitud, valor = campos

    # Verificamos que la hora tenga el formato correcto
    partes_hora = hora.split(":")

    if len(partes_hora) != 3:
        return None, "Formato de hora incorrecto"

    if not all(parte.isdigit() for parte in partes_hora):
        return None, "Formato de hora incorrecto"

    horas, minutos, segundos = map(int, partes_hora)

    # Verificamos que la hora exista
    if horas > 23 or minutos > 59 or segundos > 59:
        return None, "Hora imposible"

    # Verificamos que el canal sea válido
    if canal not in ("CH1", "CH2"):
        return None, "Canal incorrecto"

    # Verificamos que la magnitud sea válida
    if magnitud not in ("FREQ", "PKPK", "CYCRMS"):
        return None, "Magnitud incorrecta"

    # Intentamos convertir el valor a número
    try:
        valor = float(valor)
    except ValueError:
        return None, "Valor no numérico"

    # Guardamos los datos de la medición
    medicion = {
        "fecha": fecha,
        "hora": hora,
        "equipo": equipo,
        "canal": canal,
        "magnitud": magnitud,
        "valor": valor
    }

    return medicion, None

# definimos la segunda funcion
def leer_log(ruta):
    # Diccionario donde agrupamos las mediciones
    series = {}

    # Lista donde guardamos las líneas rechazadas
    rechazadas = []

    # Abrimos el archivo para leerlo
    with open(ruta, "r", encoding="utf-8") as archivo:

        # Recorremos cada línea del archivo con su número
        for numero, linea in enumerate(archivo, start=1):

            # Analizamos la línea
            medicion, motivo = analizar_linea(linea)

            # Si no hay medición ni motivo, la línea fue ignorada
            if medicion is None and motivo is None:
                continue

            # Si hay un motivo, guardamos la línea rechazada
            if motivo is not None:
                rechazadas.append({
                    "numero": numero,
                    "linea": linea.rstrip("\n"),
                    "motivo": motivo
                })
                continue

            # Creamos una clave para identificar cada serie
            clave = (
                medicion["equipo"],
                medicion["canal"],
                medicion["magnitud"]
            )

            # Si la serie todavía no existe, creamos una lista
            if clave not in series:
                series[clave] = []

            # Agregamos el valor a su serie correspondiente
            series[clave].append(medicion["valor"])

    # Devolvemos las series y las líneas rechazadas
    return series, rechazadas


# ---- pruebas ----

# Prueba 1: línea válida
medicion, motivo = analizar_linea(
    "2026-09-08 09:14:02 ADS3202 CH1 FREQ 1000.5"
)

assert medicion["valor"] == 1000.5
assert motivo is None


# Prueba 2: hora imposible
medicion, motivo = analizar_linea(
    "2026-09-08 25:61:00 ADS3202 CH1 FREQ 1000"
)

assert medicion is None
assert motivo == "Hora imposible"


# Prueba 3: línea vacía
medicion, motivo = analizar_linea("")

assert medicion is None
assert motivo is None


# Prueba 4: línea con tabulaciones
medicion, motivo = analizar_linea(
    "2026-09-08\t09:14:02\tADS3202\tCH1\tPKPK\t2.0"
)

assert medicion["valor"] == 2.0
assert motivo is None


# Prueba 5: valor que no se puede convertir a número
medicion, motivo = analizar_linea(
    "2026-09-08 09:14:02 ADS3202 CH1 FREQ ERROR"
)

assert medicion is None
assert motivo == "Valor no numérico"


# Prueba 6: leer el archivo real de la cátedra
series, rechazadas = leer_log("mediciones.log")

# Comprobamos que las funciones devuelvan los datos esperados
assert isinstance(series, dict)
assert isinstance(rechazadas, list)

# Comprobamos que se hayan encontrado mediciones
assert len(series) > 0

# Mostramos un resumen de los resultados
print("Series encontradas:", len(series))


series, rechazadas = leer_log("prueba_mediciones.log")

assert len(series) == 2
assert len(rechazadas) == 1
assert rechazadas[0]["numero"] == 3


# Prueba 7: verificar que se agruparon correctamente los valores
assert series[("ADS3202", "CH1", "PKPK")] == [2.0]


print("pruebas OK")