import importlib
from pathlib import Path

# Reutiliza las funciones implementadas en los ejercicios anteriores.
con_unidad = importlib.import_module("02_magnitudes").con_unidad
Instrumento = importlib.import_module("05_cliente").Instrumento
barrer = importlib.import_module("06_barrido").barrer
verificar_canal = importlib.import_module("07_verificacion").verificar_canal
leer_log = importlib.import_module("08_log").leer_log
resumen = importlib.import_module("09_estadistica").resumen


def armar_informe(idn, series, verificaciones):
    """Construye el informe como texto, sin imprimir ni abrir archivos."""
    lineas = [
        "INFORME DE MEDICIONES\n",
        (
            f"Instrumento: {idn['fabricante']} {idn['modelo']} "
            f"(serie {idn['serie']}, version {idn['version']})"
        ),
        "",
        "Series del log:",
    ]

    unidades = {"FREQ": "Hz", "PKPK": "V", "CYCRMS": "V"}

    for (equipo, canal, magnitud), valores in series.items():
        estadistica = resumen(valores)
        unidad = unidades.get(magnitud, "")

        if estadistica is None:
            linea = (
                f"{equipo} {canal} {magnitud}: n=0, "
                "promedio=N/A, minimo=N/A, maximo=N/A"
            )
        else:
            linea = (
                f"{equipo} {canal} {magnitud}: n={estadistica['n']}, "
                f"promedio={con_unidad(estadistica['promedio'], unidad)}, "
                f"minimo={con_unidad(estadistica['minimo'], unidad)}, "
                f"maximo={con_unidad(estadistica['maximo'], unidad)}"
            )
        lineas.append(linea)

    lineas.extend(["", "Verificaciones:"])
    for verificacion in verificaciones:
        if verificacion is None:
            lineas.append("No se pudo verificar: faltan mediciones.")
            continue

        resultado = "OK" if verificacion["coinciden"] else "NO COINCIDE"
        lineas.append(
            f"{verificacion['canal']}: {resultado} "
            f"(Vrms medido {con_unidad(verificacion['vrms_medido'], 'V')}, "
            f"teorico {con_unidad(verificacion['vrms_teorico'], 'V')})"
        )

    return "\n".join(lineas)


def main():
    # Identifica el osciloscopio y mide ambos canales en vivo.
    instrumento = Instrumento()
    try:
        instrumento.conectar()
        idn = instrumento.preguntar("*IDN?")
        if idn is None:
            raise RuntimeError("No se pudo identificar el instrumento.")

        mediciones = barrer(instrumento, ["CH1", "CH2"])
        verificaciones = [
            verificar_canal(mediciones, canal) for canal in ("CH1", "CH2")
        ]
    finally:
        instrumento.cerrar()

    # Resume el log de mediciones y muestra el informe final.
    ruta_log = Path(__file__).with_name("mediciones.log")
    series, _ = leer_log(str(ruta_log))
    print(armar_informe(idn, series, verificaciones))


if __name__ == "__main__":
    main()
