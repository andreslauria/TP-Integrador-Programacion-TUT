import math


def a_numero(texto):
    """
    Convierte una cadena en notación científica a un float.
    Devuelve None si el texto no se puede convertir.
    """
    try:
        return float(texto)
    except (ValueError, TypeError):
        return None


def con_unidad(valor, unidad):
    """
    Convierte un valor numérico a texto legible con prefijos SI.
    Mantiene el número entre 1 y 999.
    """
    if valor is None:
        return "N/A"
    if valor == 0:
        return f"0 {unidad}"

    signo = -1 if valor < 0 else 1
    abs_val = abs(valor)

    # 1. Encontrar el orden de magnitud inicial
    # Usamos round para evitar problemas de precisión de flotantes en el logaritmo
    # (ej: math.log10(1000) a veces da 2.9999999999999996)
    orden = math.floor(round(math.log10(abs_val), 10) / 3) * 3

    # 2. Escalar el número a ese orden
    escalado = abs_val / (10**orden)

    # 3. Redondear a 3 decimales
    escalado = round(escalado, 3)

    # 4. LA TRAMPA: Revisar si el redondeo nos empujó a 1000 o más
    if escalado >= 1000.0:
        escalado /= 1000.0
        orden += 3

    # Diccionario de prefijos
    prefijos = {-12: "p", -9: "n", -6: "u", -3: "m", 0: "", 3: "k", 6: "M", 9: "G"}

    # Manejar límites superior e inferior si nos salimos del diccionario
    if orden < -12:
        escalado *= 10 ** (orden - (-12))
        orden = -12
    elif orden > 9:
        escalado *= 10 ** (orden - 9)
        orden = 9

    prefijo = prefijos[orden]
    resultado = signo * escalado

    # Formatear a máximo 3 decimales, removiendo ceros inútiles
    str_val = f"{resultado:.3f}".rstrip("0").rstrip(".")

    if str_val == "-0":
        str_val = "0"
    return f"{str_val} {prefijo}{unidad}".replace("  ", " ")


# 1. Pruebas de a_numero(texto)
assert a_numero("1.000000E+03") == 1000.0
assert a_numero("2.500000E+05") == 250000.0
assert a_numero("7.070000E-01") == 0.707
assert a_numero("HOLA") is None
assert a_numero("") is None

# 2. Pruebas de la tabla del ejercicio
assert con_unidad(1000.0, "Hz") == "1 kHz"
assert con_unidad(a_numero("2.500000E+03"), "Hz") == "2.5 kHz"
assert con_unidad(2.0, "V") == "2 V"
assert con_unidad(0.707, "V") == "707 mV"

assert con_unidad(a_numero("Hola"), "V") == "N/A"

assert con_unidad(999.9999, "Hz") == "1 kHz"
assert con_unidad(0.9999, "A") == "999.9 mA"

### AGREGADOS POR LA IA
# 5. Prefijos en los extremos
assert con_unidad(0.000000000003, "F") == "3 pF"  # Pico
assert con_unidad(1500000000.0, "Hz") == "1.5 GHz"  # Giga

# 6. Valores negativos (importante en voltaje)
assert con_unidad(-5.0, "V") == "-5 V"
assert con_unidad(-0.015, "A") == "-15 mA"


print("Todas las pruebas pasaron OK.")
