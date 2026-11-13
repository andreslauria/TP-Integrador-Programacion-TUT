import socket
import importlib

parsear = importlib.import_module("01_identificacion").parsear_idn


class Instrumento:
    comando = ""

    def __init__(self, host="127.0.0.1", puerto=5555):
        self.host = host
        self.puerto = puerto
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def conectar(self):
        self.sock.connect((self.host, self.puerto))
        print("Conexion establecida")

    def cerrar(self):
        self.sock.close()
        print("Conexion cerrada")

    def enviar(self, comando):
        self.comando = comando
        mensaje = f"{comando.strip()}\n"
        self.sock.sendall(mensaje.encode("utf-8"))
        print(f"Se envia mensaje: {mensaje}")

    def preguntar(self, comando):
        # Llamamos a enviar. Asumimos que 'enviar' agrega internamente el '\n'.
        self.enviar(comando)
        respuesta = ""
        while True:
            byte_data = self.sock.recv(4096)

            # Si no llega más datos (conexión cerrada por el servidor o error de red)
            if not byte_data:
                return respuesta

            texto_nuevo = byte_data.decode("utf-8")
            respuesta += texto_nuevo

            # Verificamos si recibimos el salto de línea que marca el fin del mensaje
            if respuesta.endswith("\n"):
                # Devolvemos la respuesta completa sin el último "\n" para mayor limpieza
                return respuesta.rstrip("\n")

            # Si no termina en \n, el bucle continúa esperando más datos


##PRUEBA MINIMA

osciloscopio = Instrumento()  # Creo un objeto (instancia de la clase Instrumento)
osciloscopio.conectar()
respuesta = osciloscopio.preguntar("*IDN?")
print(parsear(respuesta))
osciloscopio.cerrar()

mutlimetro = Instrumento(
    puerto=5556
)  # Creo un objeto (instancia de la clase Instrumento) con otro puerto
mutlimetro.conectar()
respuesta = mutlimetro.preguntar("*IDN?")
print(parsear(respuesta))
mutlimetro.cerrar()
