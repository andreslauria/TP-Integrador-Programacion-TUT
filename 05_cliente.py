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
        print("Conexion establecida.\n")

    def cerrar(self):
        self.sock.close()
        print("Conexion cerrada.\n")

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
                respuesta = respuesta.rstrip("\n")
                if comando.strip() == "*IDN?":
                    return parsear(respuesta)
                return respuesta

            texto_nuevo = byte_data.decode("utf-8")
            respuesta += texto_nuevo

            # Verificamos si recibimos el salto de línea que marca el fin del mensaje
            if respuesta.endswith("\n"):
                respuesta = respuesta.rstrip("\n")
                if comando.strip() == "*IDN?":
                    return parsear(respuesta)
                return respuesta

            # Si no termina en \n, el bucle continúa esperando más datos


##PRUEBA MINIMA
if __name__ == "__main__":
    osciloscopio = Instrumento()  # Creo un objeto (instancia de la clase Instrumento)
    osciloscopio.conectar()
    respuesta_pars = osciloscopio.preguntar("*IDN?")
    print(f"El modelo del osciloscopio es: {respuesta_pars["modelo"]}")
    osciloscopio.cerrar()

    mutlimetro = Instrumento(
        puerto=5556
    )  # Creo un objeto (instancia de la clase Instrumento) con otro puerto
    mutlimetro.conectar()
    respuesta_pars = mutlimetro.preguntar("*IDN?")
    print(f"El modelo del multimetro es: {respuesta_pars["modelo"]}")
    mutlimetro.cerrar()
