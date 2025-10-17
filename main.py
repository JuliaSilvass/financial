import flet as ft
from ui.home_page import home_page
from ui.login_page import login_page
from ui.register_page import register_page
from ui.dashboard_page import dashboard_page
from ui.ambiente_page import ambiente_cadastrar_page, ambiente_listar_page

from database.connection_db import test_connection

# -------------------------------------------------------------
# Função principal
# -------------------------------------------------------------
def main(page: ft.Page):
    page.title = "Financial"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Testa conexão com o banco (só na inicialização)
    test_connection()

    # ---------------------------------------------------------
    # Sistema de Rotas
    # ---------------------------------------------------------
    def route_change(e: ft.RouteChangeEvent):
        route = page.route
        page.views.clear()

        # Rotas principais
        routes = {
            "/": home_page,
            "/login": login_page,
            "/register": register_page,
            "/dashboard": dashboard_page,
            "/ambiente/cadastrar": ambiente_cadastrar_page,
            "/ambiente/listar": ambiente_listar_page,
        #     "/ambiente/editar": ambiente_editar_page,
        }

        # Se a rota existir, renderiza a página correspondente
        if route in routes:
            page.views.append(routes[route](page))
        else:
            page.views.append(home_page(page))  # rota padrão (fallback)

        page.update()

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
