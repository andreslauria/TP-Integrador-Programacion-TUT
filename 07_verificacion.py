# utilizamos la herramienta incorporada para trabajar la raiz cuadrada
import math


# definimos la primera funcion
def vrms_teorico(vpp):
    # Verificamos que vpp sea un número
    if not isinstance(vpp, (int, float)):
        return None

    # decartamos true y false
    if isinstance(vpp, bool):
        return None

    # Una tensión pico a pico negativa no tiene sentido
    if vpp < 0:
        return None

    # Fórmula del Vrms para una señal senoide:
    # Vrms = Vpp / (2 × raíz de 2)
    return vpp / (2 * math.sqrt(2))


# definimos la segunda funcion
def coincide(medido, teorico, tolerancia=0.02):
    # Verificamos que los valores sean números
    if not isinstance(medido, (int, float)):
        return False

    if not isinstance(teorico, (int, float)):
        return False

    if not isinstance(tolerancia, (int, float)):
        return False

    # Descartamos valores booleanos
    if isinstance(medido, bool):
        return False

    if isinstance(teorico, bool):
        return False

    if isinstance(tolerancia, bool):
        return False

    # Una tolerancia negativa no tiene sentido
    if tolerancia < 0:
        return False

    # Evitamos dividir por cero
    if teorico == 0:
        return medido == 0

    # Calculamos el error relativo:
    # |medido - teorico| / |teorico|
    error = abs(medido - teorico) / abs(teorico)

    # Devuelve True si el error está dentro de la tolerancia
    return error <= tolerancia


# definimos la tercera funcion
def verificar_canal(filas, canal):
    # Guardamos inicialmente las mediciones como None
    vpp = None
    vrms_medido = None

    # Recorremos todas las filas del resultado de barrer()
    for fila in filas:

        # Solo nos interesan las mediciones del canal pedido
        if fila["canal"] == canal:

            # Buscamos la medición pico a pico
            if fila["magnitud"] == "PKPK":
                vpp = fila["valor"]

            # Buscamos la medición RMS
            elif fila["magnitud"] == "CYCRms":
                vrms_medido = fila["valor"]

    # Si no encontramos alguna de las dos mediciones,
    # no podemos hacer la verificación
    if vpp is None or vrms_medido is None:
        return None

    # Calculamos cuál debería ser el Vrms
    # si la señal fuera una senoide
    teorico = vrms_teorico(vpp)

    # Si el Vpp no era válido
    if teorico is None:
        return None

    # Comparamos el valor medido con el teórico
    coinciden = coincide(vrms_medido, teorico)

    # Devolvemos el resultado como diccionario
    return {
        "canal": canal,
        "vpp": vpp,
        "vrms_medido": vrms_medido,
        "vrms_teorico": teorico,
        "coinciden": coinciden,
    }


# ---- pruebas ----
if __name__ == "__main__":
    # Prueba 1:
    # Una senoide de 2 V pico a pico tiene aproximadamente
    # 0.707 V RMS.
    assert abs(vrms_teorico(2.0) - 0.70710678) < 0.0001

    # Prueba 2 (caso raro):
    # Un valor negativo no tiene sentido como Vpp.
    assert vrms_teorico(-2.0) is None

    # Prueba 3:
    # Un valor cercano al teórico, dentro del 2 %, coincide.
    assert coincide(0.71, 0.70710678) is True


    # Prueba 4:
    # Un valor alejado del teórico no coincide.
    assert coincide(1.0, 0.70710678) is False


    # Prueba 5:
    # Formato real de las filas que devuelve barrer().
    filas_senoide = [
        {
            "canal": "CH1",
            "magnitud": "FREQuency",
            "unidad": "Hz",
            "texto_crudo": "1000",
            "valor": 1000.0,
        },
        {
            "canal": "CH1",
            "magnitud": "PKPK",
            "unidad": "V",
            "texto_crudo": "2.0",
            "valor": 2.0,
        },
        {
            "canal": "CH1",
            "magnitud": "CYCRms",
            "unidad": "V",
            "texto_crudo": "0.707",
            "valor": 0.707,
        },
    ]

    resultado = verificar_canal(filas_senoide, "CH1")

    assert resultado is not None
    assert resultado["coinciden"] is True


    # Una señal cuadrada de 2 Vpp tiene Vrms = 1 V.
    # Pero nuestra función calcula el valor teórico de una SENOIDE:
    # aproximadamente 0.707 V.
    #
    # Por lo tanto, NO deben coincidir.

    filas_cuadrada = [
        {
            "canal": "CH1",
            "magnitud": "PKPK",
            "unidad": "V",
            "texto_crudo": "2.0",
            "valor": 2.0,
        },
        {
            "canal": "CH1",
            "magnitud": "CYCRms",
            "unidad": "V",
            "texto_crudo": "1.0",
            "valor": 1.0,
        },
    ]

    resultado_cuadrada = verificar_canal(filas_cuadrada, "CH1")

    assert resultado_cuadrada is not None
    assert resultado_cuadrada["coinciden"] is False


    # Caso raro: el canal no existe.
    assert verificar_canal(filas_senoide, "CH99") is None


    # Caso raro: lista vacía.
    assert verificar_canal([], "CH1") is None

    print("pruebas OK")
