import flet as ft
from ui.home_page import home_page  
from ui.login_page import login_page
from ui.register_page import register_page
from database.connection_db import test_connection
from controllers.user_controller import UserController
from utils.security import hash_password
from models.user import User


if __name__ == "__main__":
    test_connection()


    def main(page: ft.Page):
        page.title = "Financial"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.LIGHT

        def route_change(e: ft.RouteChangeEvent):

            page.views.clear()
            
            if page.route == "/":
                page.views.append(home_page(page))
            elif page.route == "/login":
                page.views.append(login_page(page))
            elif page.route == "/register":
                page.views.append(register_page(page))
            
            page.update()

        page.on_route_change = route_change
        page.go("/")
    ft.app(target=main)