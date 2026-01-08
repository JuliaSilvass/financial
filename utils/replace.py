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

