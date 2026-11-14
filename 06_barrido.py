import importlib

# Importamos las utilidades de los otros ejercicios
magnitudes = importlib.import_module("02_magnitudes")
a_numero = magnitudes.a_numero


def barrer(instrumento, canales):

    # Lista para acumular mediciones
    mediciones = []

    # Diccionario de las magnitudes a medir
    magnitudes = {"FREQuency": "Hz", "PKPK": "V", "CYCRms": "V"}

    for canal in canales:
        for magnitud, unidad in magnitudes.items():

            # Construcción del comando SCPI (siempre es consulta)
            comando = f":MEASUrement:{canal}:{magnitud}?"

            # Leemos el valor del instrumento
            texto_crudo = instrumento.preguntar(comando)

            # Convertimos el texto a número usando a_numero
            valor = float(texto_crudo)

            medicion = {
                "canal": canal,
                "magnitud": magnitud,
                "unidad": unidad,
                "texto_crudo": texto_crudo,
                "valor": valor,
            }

            mediciones.append(medicion)

    return mediciones


# ---- Clase "Marioneta" (Instrumento Falso Simplificado) ----


class InstrumentoFalso:
    # Simula un instrumento real: tiene el mismo método "preguntar" que usaría barrer()
    def __init__(self, respuesta_fija):
        self.respuesta_fija = respuesta_fija  # guardamos qué va a contestar siempre

    def preguntar(self, comando):
        # Sin importar qué comando le mandemos, siempre devuelve la misma respuesta
        return self.respuesta_fija


if __name__ == "__main__":
    # Caso 1: instrumento que siempre contesta un número válido
    instrumento_ok = InstrumentoFalso("1.23")
    resultado_ok = barrer(instrumento_ok, ["CH1", "CH2"])
    assert len(resultado_ok) == 6
    assert resultado_ok[0]["valor"] == 1.23
    assert resultado_ok[0]["texto_crudo"] == "1.23"

    # Caso 2: instrumento que contesta un error, no un número
    instrumento_error = InstrumentoFalso("ERROR")
    resultado_error = barrer(instrumento_error, ["CH1"])
    assert resultado_error[0]["valor"] is None
    assert resultado_error[0]["texto_crudo"] == "ERROR"

    # Caso 3: lista de canales vacía
    resultado_vacio = barrer(instrumento_ok, [])
    assert resultado_vacio == []

    print("pruebas OK")
