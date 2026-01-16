# utils/list_page.py
import flet as ft
from .date import formatar_data_br


def build_list_page(
    *,
    items: list,
    columns: list,
    on_item_click,
    search_bar=None,
    empty_message="Nenhum registro encontrado."
):
    # --------------------------------------------------
    # Header
    # --------------------------------------------------
    header = ft.Container(
        padding=ft.padding.symmetric(vertical=14, horizontal=16),
        bgcolor="#E5E7EB",
        border_radius=8,
        content=ft.Row(
            [
                ft.Text(
                    col["label"],
                    width=col.get("width", 150),
                    weight="bold",
                    size=15,
                    color="#111827",
                )
                for col in columns
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
    )

    # --------------------------------------------------
    # Coluna de linhas 
    # --------------------------------------------------
    rows = ft.Column(
        expand=True,
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
    )

    def on_hover(e):
        e.control.bgcolor = "#F0F9FF" if e.data == "true" else "#FFFFFF"
        e.control.update()

    if not items:
        rows.controls.append(
            ft.Text(empty_message, color="gray")
        )
    else:
        for item in items:
            row_controls = []

            for col in columns:
                value = getattr(item, col["field"], "-")

                if isinstance(value, bool):
                    value = "Ativa" if value else "Inativa"

                if col.get("type") == "date":
                    value = formatar_data_br(value)

                is_first_col = col == columns[0]

                row_controls.append(
                    ft.Text(
                        "-" if value is None else str(value),
                        width=col.get("width", 150),
                        size=15 if is_first_col else 14,
                        weight="bold" if is_first_col else None,
                        color="#111827" if is_first_col else "#374151",
                    )
                )

            rows.controls.append(
                ft.Container(
                    content=ft.Row(
                        row_controls,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.symmetric(vertical=12, horizontal=16),
                    bgcolor="#FFFFFF",
                    border=ft.border.only(
                        bottom=ft.BorderSide(1, "#E5E7EB")
                    ),
                    on_hover=on_hover,
                    on_click=lambda e, obj=item: on_item_click(obj),
                )
            )

    return ft.Column(
        expand=True,
        spacing=12,
        controls=[
            search_bar if search_bar else ft.Container(),
            header,
            rows,
        ],
    )

