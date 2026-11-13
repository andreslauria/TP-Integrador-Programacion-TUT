def es_consulta(comando):
    """
    Devuelve True si el comando termina en '?', False en caso contrario.
    """
    return comando.endswith("?")


def validar(comando):
    """
    Valida un comando SCPI según las reglas dadas.
    Devuelve None si es válido o el mensaje de error correspondiente si no lo es.
    """
    # No puede estar vacío
    if not comando:
        return "No puede estar vacío"

    # Empieza con : o con *
    if not (comando.startswith(":") or comando.startswith("*")):
        return "Debe empezar con : o con *"

    # No hay dos espacios seguidos
    if "  " in comando:
        return "Hay dos espacios seguidos, debe haber uno solo"

    # Hay a lo sumo un ?
    if comando.count("?") > 1:
        return "Hay mas de un signo ?"

    # El ? va al final
    # Si existe un '?', obligatoriamente debe estar en la última posición
    if "?" in comando and not comando.endswith("?"):
        return "El ? va al final"

    # Separamos validaciones entre consultas y órdenes
    # Como ya descartamos que haya dos espacios seguidos, la cantidad de espacios
    # determina la cantidad de argumentos.
    if es_consulta(comando):
        # Una consulta no lleva argumento (no debe tener espacios)
        if comando.count(" ") != 0:
            return "Una consulta no lleva argumento"
    else:
        # Una orden lleva un solo argumento (debe tener exactamente un espacio)
        if comando.count(" ") != 1:
            return "Una orden lleva un solo argumento"

    # Si pasó todas las validaciones, está bien formado
    return None


print(validar(""))
print(f"El comando ingresado: :CH1:DIS?Play, error: {validar(":CH1:DIS?Play")}")
# ==========================================
# BLOQUE DE PRUEBAS (ASSERTS)
# ==========================================

# 1. Pruebas para es_consulta()
assert es_consulta(":CH1:DISPlay?") is True
assert es_consulta(":CH1:DISPlay ON") is False

# 2. Pruebas para validar() - Casos VÁLIDOS (deben devolver None)
assert validar(":CH1:DISPlay ON") is None
assert validar(":CH1:DISPlay?") is None
assert validar("*IDN?") is None

# 3. Pruebas para validar() - Casos INVÁLIDOS (según tabla de reglas)

# Regla: No puede estar vacío
assert validar("") == "No puede estar vacío"

# Regla: Empieza con : o con *
assert validar("CH1:DISPlay ON") == "Debe empezar con : o con *"

# Regla: No hay dos espacios seguidos
assert validar(":CH1:DISPlay  ON") == "Hay dos espacios seguidos, debe haber uno solo"

# Regla: Hay a lo sumo un ?
assert validar(":CH1:DISPlay??") == "Hay mas de un signo ?"

# Regla: El ? va al final
assert validar(":CH1:DIS?Play") == "El ? va al final"

# Regla: Una orden lleva un solo argumento
# (El ejemplo ":CH1:SCALe 1 v" tiene 2 espacios, por lo que son 2 argumentos)
assert validar(":CH1:SCALe 1 v") == "Una orden lleva un solo argumento"
# (También verificamos qué pasa si una orden no tiene argumentos / cero espacios)
assert validar(":CH1:SCALe") == "Una orden lleva un solo argumento"

# Regla: Una consulta no lleva argumento
assert validar(":CH1:DISPlay ON?") == "Una consulta no lleva argumento"

print("¡Todas las pruebas pasaron correctamente!")
