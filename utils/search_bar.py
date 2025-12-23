# utils/search_bar.py
import flet as ft


def build_search_bar(
    *,
    hint_text="Pesquisar...",
    on_change
):
    """
    Barra de pesquisa reutilizável.

    on_change: função chamada sempre que o texto mudar
               recebe o texto digitado
    """

    search_field = ft.TextField(
        hint_text=hint_text,
        prefix_icon=ft.Icons.SEARCH,
        height=42,
        bgcolor="#FFFFFF",
        border_radius=10,
        filled=True,
        on_change=lambda e: on_change(e.control.value),
    )

    return ft.Container(
        content=search_field,
        padding=ft.padding.only(bottom=12),
    )
