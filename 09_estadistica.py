# Calcula las estadísticas principales de una lista de valores.
def resumen(valores):
    # Cuenta los datos; sin valores no se puede calcular el resumen.
    n = len(valores)
    if n == 0:
        return None

    # Calcula el promedio y el desvío estándar muestral.
    promedio = sum(valores) / n
    if n == 1:
        desvio = 0.0
    else:
        desvio = (sum((v - promedio) ** 2 for v in valores) / (n - 1)) ** 0.5

    # Devuelve los resultados con las claves solicitadas.
    return {
        "n": n,
        "minimo": min(valores),
        "maximo": max(valores),
        "promedio": promedio,
        "desvio": desvio
    }


# Devuelve las posiciones de los valores fuera del rango indicado.
def fuera_de_rango(valores, minimo, maximo):
    posiciones = []

    # Los extremos se incluyen: solo se marcan valores menores o mayores.
    for posicion, valor in enumerate(valores):
        if valor < minimo or valor > maximo:
            posiciones.append(posicion)

    return posiciones


# ---- pruebas ----

# Comprueba el caso vacío y el desvío de una lista con un único valor.
assert resumen([]) is None
assert resumen([7]) == {
    "n": 1,
    "minimo": 7,
    "maximo": 7,
    "promedio": 7.0,
    "desvio": 0.0
}

# Verifica las estadísticas y el desvío muestral de una lista sencilla.
resultado = resumen([1, 2, 3])
assert resultado["n"] == 3
assert resultado["minimo"] == 1
assert resultado["maximo"] == 3
assert resultado["promedio"] == 2.0
assert resultado["desvio"] == 1.0

# Confirma que los extremos del rango cuentan como adentro.
assert fuera_de_rango([0, 1, 2, 3, 4], 1, 3) == [0, 4]

# Informa que todas las pruebas terminaron correctamente.
if __name__ == "__main__":
    print("pruebas OK")
