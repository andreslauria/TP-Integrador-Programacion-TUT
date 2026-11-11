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
``` python
if valor is None:
        return "N/A" 
```
Prompt: 
Genera algunas pruebas adicionales utilizando assert