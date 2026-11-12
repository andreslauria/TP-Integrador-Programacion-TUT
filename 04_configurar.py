from pathlib import Path  # Permite construir la ruta al archivo del ejercicio 3.
from runpy import run_path  # Permite ejecutar ese archivo y obtener su función validar.


validar = run_path(str(Path(__file__).with_name("03_comandos.py")))["validar"]  # Reutiliza el validador del ejercicio 3.


def comandos_de_canal(canal, display, acoplamiento, sonda, escala):  # Define la función con los datos para configurar el canal.
    """Devuelve las cuatro órdenes de configuración para CH1 o CH2."""  # Describe el resultado de la función.
    if canal not in ("CH1", "CH2"):  # Comprueba que el canal sea uno de los dos permitidos.
        return None  # Indica que no se puede configurar un canal distinto de CH1 o CH2.

    return [  # Devuelve las cuatro órdenes en el orden requerido.
        f":{canal}:DISPlay {display}",  # Configura la visualización del canal.
        f":{canal}:COUPling {acoplamiento}",  # Configura el acoplamiento del canal.
        f":{canal}:PROBe {sonda}",  # Configura la sonda del canal.
        f":{canal}:SCALe {escala}",  # Configura la escala del canal.
    ]  # Finaliza y devuelve la lista de órdenes.


comandos = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")  # Guarda las órdenes esperadas para el ejemplo de CH1.
assert comandos == [  # Comprueba que se devuelva exactamente la lista pedida.
    ":CH1:DISPlay ON",  # Espera que la primera orden active la pantalla.
    ":CH1:COUPling DC",  # Espera que la segunda orden configure el acoplamiento.
    ":CH1:PROBe 10X",  # Espera que la tercera orden configure la sonda.
    ":CH1:SCALe 1v",  # Espera que la cuarta orden configure la escala.
]  # Finaliza la lista comparada.
assert all(validar(comando) is None for comando in comandos)  # Comprueba que validar acepte todas las órdenes generadas.
assert comandos_de_canal("CH2", "OFF", "AC", "1X", "2v") == [  # Comprueba también el formato de las órdenes para CH2.
    ":CH2:DISPlay OFF",  # Espera que la primera orden desactive la pantalla.
    ":CH2:COUPling AC",  # Espera que la segunda orden configure el acoplamiento.
    ":CH2:PROBe 1X",  # Espera que la tercera orden configure la sonda.
    ":CH2:SCALe 2v",  # Espera que la cuarta orden configure la escala.
]  # Finaliza la lista comparada para CH2.
assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None  # Comprueba que un canal no permitido devuelva None.

print("¡Todos los asserts pasaron correctamente!")  # Informa que todas las pruebas terminaron bien.
