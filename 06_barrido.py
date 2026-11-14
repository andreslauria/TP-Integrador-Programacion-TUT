import importlib

# Importamos las utilidades de los otros ejercicios
comandos = importlib.import_module("03_comandos")
identificacion = importlib.import_module("01_identificacion")
magnitudes = importlib.import_module("02_magnitudes")

validar = comandos.validar
parsear_idn = identificacion.parsear_idn
con_unidad = magnitudes.con_unidad
a_numero = magnitudes.a_numero


def barrer(instrumento, canales):
    # 1. Identificación del equipo (Comando *IDN?)
    idn_respuesta = instrumento.preguntar("*IDN?")

    # Si parsear_idn falla (ej. menos de 4 campos), no seguimos
    info_equipo = parsear_idn(idn_respuesta)
    if info_equipo is None:
        return []

    # Lista para acumular mediciones
    mediciones = []

    # Diccionario de las magnitudes a medir
    definiciones_magnitud = {"FREQuency": "Hz", "PKPK": "V", "CYCRms": "V"}

    for canal in canales:
        for clave_magnitud, unidad_base in definiciones_magnitud.items():

            # Construcción del comando SCPI (siempre es consulta)
            comando = f":MEASUrement:{canal}:{clave_magnitud}?"

            # Leemos el valor del instrumento
            texto_crudo = instrumento.preguntar(comando)

            # Convertimos el texto a número usando a_numero
            valor_numerico = a_numero(texto_crudo)

            valor_final = con_unidad(valor_numerico, unidad_base)

            medicion = {
                "canal": canal,
                "magnitud": clave_magnitud,
                "valor y unidad": valor_final,
                "texto_crudo": texto_crudo,
            }

            mediciones.append(medicion)

    return mediciones


# ---- Clase "Marioneta" (Instrumento Falso Simplificado) ----


class InstrumentoFalso:
    """
    Simula un instrumento que responde siempre lo mismo.
    Ideal para probar barrer() sin conectar hardware real.
    """

    def __init__(self, idn="OWON,Fake,Osciloscopio,V1.0", valor_fijo="1.5"):
        """
        :param idn: Respuesta al comando *IDN? (debe tener 4 campos)
        :param valor_fijo: Valor que devolverá a CUALQUIER comando de medición.
        Puede ser un número ("1.5") o la cadena "ERROR".
        """
        self.respuesta_idn = idn
        self.valor_fijo = valor_fijo

    def preguntar(self, comando):
        if comando == "*IDN?":
            return self.respuesta_idn
        return self.valor_fijo


# PRUEBA


print("\n Medición con valor pequeño (verifica prefijo)")
instr_pequeno = InstrumentoFalso(idn="OWON,Fake,V1.0,1.2", valor_fijo="7.070000E-05")
lista_resultado = barrer(instr_pequeno, ["CH1"])
print("Resultado:")
for m in lista_resultado:
    print(m)

print("\n--- Caso 3: Medición con valor grande (verifica prefijos kM/kHz) ---")
instr_grande = InstrumentoFalso(idn="OK", valor_fijo="5000000.0") # 5 MHz, 5 MV
lista_resultado = barrer(instr_grande, ["CH1"])
print("Resultado con valor grande:")
for m in lista_resultado:
    print(m)