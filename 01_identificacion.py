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


def query_scpi(port, command="*IDN?"):
    """Envía un comando SCPI por TCP/IP y devuelve la respuesta en texto."""
    host = "127.0.0.1"  # localhost

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2.0)
        try:
            s.connect((host, port))
            cmd_with_term = f"{command}\n"
            s.sendall(cmd_with_term.encode("utf-8"))

            data = s.recv(1024)
            return data.decode("utf-8").strip()

        except ConnectionRefusedError:
            print(f"[-] Error: Simulador en puerto {port} no está corriendo.")
            return None
        except socket.timeout:
            print(f"[-] Error: Timeout en el puerto {port}.")
            return None
        except Exception as e:
            print(f"[-] Error inesperado en puerto {port}: {e}")
            return None


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
