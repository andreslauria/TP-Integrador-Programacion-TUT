"""
1 — Identificación del equipo
*IDN? es la primera consulta de cualquier práctica: si contesta, entonces el cable, la red,
el protocolo y el instrumento están todos vivos.
Escribí parsear_idn(respuesta) , que recibe el texto que devuelve *IDN? y devuelve un diccionario con las claves fabricante , modelo , serie y version.
Devuelve None si la respuesta no sirve.
Los campos vienen separados por comas. Ojo con esto: el osciloscopio contesta con cuatro campos y el multímetro con cinco.
OWON,ADS3202,25470803,V1.2.0
OWON,XDM1041,25470803,V4.4.0,3
Los dos tienen que entrar. El quinto campo del multímetro se descarta.
Casos que tu función tiene que contemplar: menos de cuatro campos, cadena vacía,
campos con espacios de más alrededor, y la respuesta ERROR: comando desconocido que
devuelve el instrumento cuando no entiende.
"""

import socket


def parsear_idn(respuesta):
    # Si la respuesta está vacía o no es un string, no sirve
    if not respuesta or not isinstance(respuesta, str):
        return None

    # Limpiamos saltos de línea y dividimos por comas
    campos = respuesta.strip().split(",")

    # El estándar IEEE 488.2 exige un mínimo de 4 campos
    if len(campos) < 4:
        return None

    # Limpiamos los espacios en blanco de cada campo por prolijidad
    campos = [campo.strip() for campo in campos]

    return {
        "fabricante": campos[0],
        "modelo": campos[1],
        "serie": campos[2],
        # Si hay 4 campos, toma el último. Si hay 5 (multímetro),
        # los une con una coma para no perder el dato extra.
        "version": ",".join(campos[3:]),
    }


# -----Pruebas------
assert parsear_idn("OWON,ADS3202,254,V1.0") is not None
assert parsear_idn("OWON,ADS3202,254") is None
assert parsear_idn("") is None
print("pruebas OK")
