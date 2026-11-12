Ejercicio_1
Prompt:
tengo una programa en python que simula estos equipos: ADS3202 — osciloscopio y el XDM1041 — multímetro , en los puertos 5555 y 5556 en el localhost.
Como hago desde otro archivo python enviarle un \*IDN? (importando SOCKET). (con esta sentencia nos explico el query para pedir los datos a los instrumentos pero no hace falta para este ejercicio.)

- Escribí una funcion parsear_idn(respuesta), que recibe el texto que devuelve el query \*IDN?. Esta funcion devuelve un diccionario con las claves fabricante , modelo , serie y version .
- Devuelve None si la respuesta no sirve.
- Los campos vienen separados por comas.

Que Contesto:

El uso de \*IDN? como el "Hola Mundo" (o ping) de la instrumentación es una excelente práctica. Si esa consulta pasa, tienes garantizada la capa física y de transporte.
Aquí tienes la función. Para resolver la discrepancia de que el osciloscopio devuelve 4 campos y el multímetro 5 (generalmente porque reporta la versión de hardware y de software por separado), la función agrupa todos los campos a partir del cuarto dentro de la clave version. De esta forma, conservas toda la información manteniendo exactamente las cuatro claves que pediste. (el codigo)

Ejercicio_2:

Prompt:
el siguiente archivo, llamesmole magnitudes.py pide lo siguiente:

Los equipos OWON devuelven los números en notación científica: 1.000000E+03 . Para una

persona eso no se lee.

Escribí dos funciones. a) a_numero(texto) convierte "1.000000E+03" en el número 1000.0 ,

y devuelve None si el texto no es un número. b) con_unidad(valor, unidad) hace el camino

inverso y devuelve el texto que leería un humano:

Llamada Resultado

con_unidad(1000.0, "Hz") 1 kHz

con_unidad(2500.0, "Hz") 2.5 kHz

con_unidad(2.0, "V") 2 V

con_unidad(0.707, "V") 707 mV

con_unidad(0.0005, "s") 500 us

con_unidad(0.0, "V") 0 V

Los diez ejercicios TUT · Programación

Prof. Pablo E. Hernández · Prof. Candela Fernández Ibáñez 8 / 17

La regla es elegir el prefijo que deje el número entre 1 y 999. Los prefijos que tenés que

soportar son p , n , u , m , ninguno, k , M y G .

U N C A SO Q U E S E L E E S C A PA A C A S I TO DO E L M U N DO

con_unidad(999.9999, "Hz") tiene que dar 1 kHz , no 1000 Hz .

El número entra en el rango 1 a 999 antes de redondear, pero al redondear a tres decima‐

les se convierte en 1000 y se sale. Si tu programa redondea y no vuelve a mirar, devuelve

una unidad mal elegida.

Que Contesto:

Este es un problema clásico de programación para instrumentación: pasar de la notación que entiende la máquina a formato "ingeniería" para el ojo humano.

El profesor fue muy bueno al dejarte ese comentario sobre el 999.9999. El truco para resolver este caso "trampa" es redondear el número ANTES de decidir el prefijo final. Si al redondear el número trepa a 1000.0, lo dividimos por 1000 y subimos un nivel de prefijo.

Aquí tienes el código completo para tu archivo magnitudes.py

Prompt:
se puede poner lo que devuelve a_numero dentro de con_unidad
Que Contesto:
Sí, totalmente. En Python puedes anidar funciones, pasando el resultado de una directamente como argumento de la otra.
Recordá que programamos a_numero(texto) para que devuelva None si el texto está roto o no es un número.
Si haces con_unidad(a_numero("TEXTO_ROTO"), "V"), le estarías pasando un None a la función con_unidad. Cuando con_unidad intente hacer matemáticas con ese None (como abs(None) o buscar si es mayor a cero), el programa va a crashear con un TypeError.

Qué cambiaste:
Se corrige con un

```python
if valor is None:
        return "N/A"
```

Prompt:
Genera algunas pruebas adicionales utilizando assert

###Ejercicio 6###
Prompt:
tengo un programa llamado instrumento_virtual.py corriendo en segundo plano que simula un osciloscopio ADS3202 y el multímetro XDM1041, en la direccion 127.0.0.1 en los puertos 5555 y 5556 respectivamentete.

Acá aparece la red. Es menos de lo que parece: SCPI por LAN es texto plano sobre una
conexión TCP, una línea por comando, y socket viene con Python.
Escribí una clase Instrumento con tres métodos:
Método Qué hace
enviar(comando) manda una orden y no espera nada — es ENVIAR
preguntar(comando) manda una consulta y devuelve la respuesta — es QUERY
cerrar() cierra la conexión
Al crear el objeto se le pasan la dirección y el puerto, con 127.0.0.1 y 5555 como valores por defecto.

Cada comando se manda terminado en un salto de línea ( "\n" ). Cada respuesta viene terminada de la misma forma. Ese salto de línea es el que marca dónde termina un mensaje y empieza el siguiente; sin él, el instrumento se queda esperando para siempre.
Prueba mínima: con el instrumento virtual corriendo, preguntar("*IDN?") tiene que devolver OWON,ADS3202,25470803,V1.2.0 . Y esa respuesta, pasada por parsear_idn del ejercicio 1, tiene que dar un diccionario con modelo igual a ADS3202 .

IMPORTANTE: HACERLO CON PROGRAMACION FUNCIONAL NO POO.

Que Contesto:

Para resolver este ejercicio utilizando un enfoque de programación funcional (sin clases ni objetos de la conexión), en lugar de instanciar un objeto con sus métodos, vamos a definir funciones puras o de primer orden que reciban el socket (la conexión) como argumento.
Como el archivo 01_identificacion.py comienza con un número, se debe utilizar importlib para importarlo correctamente en el script.
Aquí tienes el código de solución:

```python

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
    sock.sendall(mensaje.encode('utf-8'))
# Función para enviar una consulta y leer la respuesta
def preguntar(sock, comando):
    enviar(sock, comando)
    # Recibimos datos hasta encontrar el salto de línea "\n"
    respuesta = b""
    while b"\n" not in respuesta:
        chunk = sock.recv(1024)
        if not chunk: # Si se corta la conexión
            break
        respuesta += chunk
        
    return respuesta.decode('utf-8').strip()
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
        print("Error: No se pudo conectar. Asegúrate de que el instrumento virtual (instrumento_virtual.py) esté corriendo.")
    finally:
        # 6. Siempre cerramos la conexión al terminar
        if 'conexion_osciloscopio' in locals():
            cerrar(conexion_osciloscopio)
            print("Conexión cerrada.")
```

Notas sobre la implementación:
- El estado de la conexión se mantiene en la variable conexion_osciloscopio y viaja pasándose explícitamente a enviar(), preguntar() y cerrar(). De este modo se evita la Programación Orientada a Objetos.
- En preguntar(sock, comando), implementé un bucle while b"\n" not in respuesta que lee iterativamente el buffer del socket de red hasta detectar el carácter de nueva línea garantizando que no se pierda información ni se quede esperando indefinidamente si el mensaje es corto o largo.
- Para probar el multímetro, solo tienes que llamar a conectar(puerto=5556) en el bloque principal.