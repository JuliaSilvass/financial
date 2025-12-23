# utils/date.py
from datetime import datetime

# ----------------------------------------------------------
# Formata data para o formato brasileiro
# ----------------------------------------------------------
def formatar_data_br(data):
    if not data:
        return "-"
    if isinstance(data, str):
        return data
    if isinstance(data, datetime):
        return data.strftime("%d/%m/%Y %H:%M")
    return str(data)