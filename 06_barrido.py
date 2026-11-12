def barrer(instrumento, canales):
    # Lista vacía donde vamos a ir guardando cada medición (cada una va a ser un diccionario)
    mediciones = []

    # Diccionario que relaciona cada magnitud con su unidad correspondiente
    magnitudes = {
        "FREQuency": "Hz",   # la frecuencia se mide en Hertz
        "PKPK": "V",         # el voltaje pico a pico se mide en Volts
        "CYCRms": "V"        # el voltaje RMS (por ciclo) también se mide en Volts
    }

    for canal in canales:  # recorremos cada canal pedido, por ejemplo "CH1" y "CH2"
        for magnitud, unidad in magnitudes.items():  # recorremos las 3 magnitudes para ese canal

            # Armamos el comando SCPI exacto que hay que mandarle al instrumento
            comando = f":MEASUrement:{canal}:{magnitud}?"

            # Le preguntamos al instrumento y guardamos su respuesta tal cual, como texto
            texto_crudo = instrumento.preguntar(comando)

            # Tratamos de convertir ese texto a número
            try:
                valor = float(texto_crudo)  # si se puede convertir, acá queda el número
            except ValueError:
                valor = None  # si el instrumento contestó un error, no hay número válido

            # Armamos el diccionario con toda la info de esta medición puntual
            medicion = {
                "canal": canal,
                "magnitud": magnitud,
                "unidad": unidad,
                "texto_crudo": texto_crudo,
                "valor": valor
            }

            mediciones.append(medicion)  # la agregamos a la lista de resultados

    return mediciones  # devolvemos la lista completa (6 mediciones si son 2 canales x 3 magnitudes)


# ---- clase de mentira para probar sin el instrumento real ----
class InstrumentoFalso:
    # Simula un instrumento real: tiene el mismo método "preguntar" que usaría barrer()
    def __init__(self, respuesta_fija):
        self.respuesta_fija = respuesta_fija  # guardamos qué va a contestar siempre

    def preguntar(self, comando):
        # Sin importar qué comando le mandemos, siempre devuelve la misma respuesta
        return self.respuesta_fija


# ---- pruebas ----

# Caso 1: instrumento que siempre contesta un número válido
instrumento_ok = InstrumentoFalso("1.23")
resultado_ok = barrer(instrumento_ok, ["CH1", "CH2"])
assert len(resultado_ok) == 6  # 2 canales x 3 magnitudes = 6 mediciones
assert resultado_ok[0]["valor"] == 1.23  # el valor numérico se convirtió bien
assert resultado_ok[0]["texto_crudo"] == "1.23"  # el texto crudo se guardó tal cual

# Caso 2 (caso raro): instrumento que contesta un error, no un número
instrumento_error = InstrumentoFalso("ERROR")
resultado_error = barrer(instrumento_error, ["CH1"])
assert resultado_error[0]["valor"] is None  # no se pudo convertir, tiene que quedar en None
assert resultado_error[0]["texto_crudo"] == "ERROR"  # pero el texto crudo igual se guarda

# Caso 3 (caso raro): lista de canales vacía
resultado_vacio = barrer(instrumento_ok, [])
assert resultado_vacio == []  # sin canales, no debería haber ninguna medición

print("pruebas OK")
