import socket
import importlib


# Función para abrir la conexión y devolver el socket
def conectar(host="127.0.0.1", puerto=5555):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, puerto))
    return sock


# Función para enviar un comando sin esperar respuesta
def enviar(sock, comando):
    # Aseguramos que termine con salto de línea
    mensaje = f"{comando.strip()}\n"
    sock.sendall(mensaje.encode("utf-8"))


# Función para enviar una consulta y leer la respuesta
def preguntar(sock, comando):
    enviar(sock, comando)

    # Recibimos datos hasta encontrar el salto de línea "\n"
    respuesta = b""
    while b"\n" not in respuesta:
        chunk = sock.recv(1024)
        if not chunk:  # Si se corta la conexión
            break
        respuesta += chunk

    return respuesta.decode("utf-8").strip()


# Función para cerrar la conexión del socket
def cerrar(sock):
    sock.close()


# ==========================================
# Script de prueba (Ejecución principal)
# ==========================================
if __name__ == "__main__":
    # 1. Importar la función parsear_idn del ejercicio 1
    modulo_idn = importlib.import_module("01_identificacion")
    parsear_idn = modulo_idn.parsear_idn

    # 2. Conectar al instrumento (Osciloscopio en puerto 5555 por defecto)
    print("Conectando al instrumento en 127.0.0.1:5555...")
    try:
        conexion_osciloscopio = conectar()

        # 3. Mandar consulta (QUERY)
        respuesta_cruda = preguntar(conexion_osciloscopio, "*IDN?")
        print(f"Respuesta cruda recibida: {respuesta_cruda}")

        # 4. Parsear con la función del ejercicio anterior
        datos_parseados = parsear_idn(respuesta_cruda)
        print(f"Diccionario parseado: {datos_parseados}")

        # 5. Comprobación de éxito
        if datos_parseados and datos_parseados.get("modelo") == "ADS3202":
            print("\n¡Prueba EXITOSA! El modelo parseado es ADS3202.")
        else:
            print("\nError: El diccionario devuelto no contiene el modelo esperado.")

    except ConnectionRefusedError:
        print(
            "Error: No se pudo conectar. Asegúrate de que el instrumento virtual (instrumento_virtual.py) esté corriendo."
        )
    finally:
        # 6. Siempre cerramos la conexión al terminar
        if "conexion_osciloscopio" in locals():
            cerrar(conexion_osciloscopio)
            print("Conexión cerrada.")
