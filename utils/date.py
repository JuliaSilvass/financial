# utils/date.py
import flet as ft
from datetime import date, datetime

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

def date_picker_br (page: ft.Page, label="Data"):
    data_field = ft.TextField(
        label=label,
        width=350,
        read_only=True,
        hint_text="Ex: 01/01/2000",
    )

    def on_date_change(e):
        if e.control.value:
            data_field.value = e.control.value.strftime("%d/%m/%Y")
            page.update()

    date_picker = ft.DatePicker(
        first_date=date(1999, 1, 1),
        last_date=date(3000, 12, 31),
        on_change=on_date_change,
    )

    page.overlay.append(date_picker)

    def open_picker(e):
        date_picker.open = True
        page.update()

    calendar_button = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        tooltip="Selecionar data",
        on_click=open_picker
    )

    return (
        ft.Row(
            controls=[data_field, calendar_button],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        data_field
    )