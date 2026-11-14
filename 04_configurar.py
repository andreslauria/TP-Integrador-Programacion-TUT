import importlib

comandos_importados = importlib.import_module("03_comandos")

validar = (
    comandos_importados.validar
)  # Importa la función validar desde el módulo 03_comandos


def comandos_de_canal(canal, display, acoplamiento, sonda, escala):
    # Comprueba que el canal sea uno de los dos permitidos.
    if canal not in ("CH1", "CH2"):
        return None

    return [
        f":{canal}:DISPlay {display}",
        f":{canal}:COUPling {acoplamiento}",
        f":{canal}:PROBe {sonda}",
        f":{canal}:SCALe {escala}",
    ]


### PRUEBAS DE VALIDACIÓN DE LA FUNCIÓN


comandos = comandos_de_canal("CH1", "ON", "DC", "10X", "1v")
print(comandos)
# Guarda las órdenes esperadas para el ejemplo de CH1.
assert comandos == [
    ":CH1:DISPlay ON",
    ":CH1:COUPling DC",
    ":CH1:PROBe 10X",
    ":CH1:SCALe 1v",
]

## Verificando que los comandos que genera esta funcion validan en la en la funcion del ejercicio 03_comandos.py
for comando in range(len(comandos) - 1):
    # Comprueba que validar acepte todas las órdenes generadas.
    print(comandos[comando])
    assert validar(comandos[comando]) is None


# Comprueba que validar acepte todas las órdenes generadas.
assert comandos_de_canal("CH2", "OFF", "AC", "1X", "2v") == [
    ":CH2:DISPlay OFF",
    ":CH2:COUPling AC",
    ":CH2:PROBe 1X",
    ":CH2:SCALe 2v",
]

# Comprueba que un canal no permitido devuelva None.
assert comandos_de_canal("CH3", "ON", "DC", "10X", "1v") is None

#print("¡Todos los asserts pasaron correctamente!")
