# utils/replace.py

# ----------------------------------------------------------
# Ajustar a formatação de valores para intuitivo ao usuario 
# ----------------------------------------------------------
def replace(data):
    if data is None:
        return "-"
    if isinstance(data, bool):
        return "Ativo" if data else "Inativo"
    return str(data)

# ----------------------------------------------------------
# Ajustar o formato do valor para float 
# ----------------------------------------------------------
def to_float(value):
    try:
        return float(str(value).replace(",", "."))
    except ValueError:
        return 0.0