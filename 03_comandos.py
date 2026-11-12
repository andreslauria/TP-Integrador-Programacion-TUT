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
    # 1. No puede estar vacío
    if not comando:
        return "No puede estar vacío"

    # 2. Empieza con : o con *
    if not (comando.startswith(":") or comando.startswith("*")):
        return "Empieza con : o con *"

    # 3. No hay dos espacios seguidos
    if "  " in comando:
        return "No hay dos espacios seguidos"

    # 4. Hay a lo sumo un ?
    if comando.count("?") > 1:
        return "Hay mas de un signo ?"

    # 5. El ? va al final
    # Si existe un '?', obligatoriamente debe estar en la última posición
    if "?" in comando and not comando.endswith("?"):
        return "El ? va al final"

    # Separamos validaciones entre consultas y órdenes
    # Como ya descartamos que haya dos espacios seguidos, la cantidad de espacios
    # determina la cantidad de argumentos.
    if es_consulta(comando):
        # 7. Una consulta no lleva argumento (no debe tener espacios)
        if " " in comando:
            return "Una consulta no lleva argumento"
    else:
        # 6. Una orden lleva un solo argumento (debe tener exactamente un espacio)
        # Nota: el texto de la regla contrasta "un solo" vs "a lo sumo un".
        # Por lo tanto, exigimos que haya exactamente 1 espacio (1 argumento).
        # Si en tu materia permiten órdenes sin argumentos (ej: *RST), cambiá `!= 1` por `> 1`.
        if comando.count(" ") != 1:
            return "Una orden lleva un solo argumento"

    # Si pasó todas las validaciones, está bien formado
    return None


print(validar(""))

# ==========================================
# BLOQUE DE PRUEBAS (ASSERTS)
# ==========================================

# 1. Pruebas para es_consulta()
assert es_consulta(":CH1:DISPlay?") is True, "Fallo: Debería detectar que es consulta"
assert (
    es_consulta(":CH1:DISPlay ON") is False
), "Fallo: Debería detectar que NO es consulta"

# 2. Pruebas para validar() - Casos VÁLIDOS (deben devolver None)
assert validar(":CH1:DISPlay ON") is None, "Fallo: Comando válido rechazado"
assert validar(":CH1:DISPlay?") is None, "Fallo: Consulta válida rechazada"
assert validar("*IDN?") is None, "Fallo: Consulta válida con * rechazada"

# 3. Pruebas para validar() - Casos INVÁLIDOS (según tabla de reglas)

# Regla: No puede estar vacío
assert validar("") == "No puede estar vacío"

# Regla: Empieza con : o con *
assert validar("CH1:DISPlay ON") == "Empieza con : o con *"

# Regla: No hay dos espacios seguidos
assert validar(":CH1:DISPlay  ON") == "No hay dos espacios seguidos"

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

print("¡Todos los asserts pasaron correctamente!")
