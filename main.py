import flet as ft
from database.connection_db import test_connection
from controllers.user_controller import UserController
from utils.security import hash_password
from models.user import User
from ui.login_page import login_page  


if __name__ == "__main__":
    test_connection()

    def main(page: ft.Page):
        page.title = "Financial App"
        page.window_width = 400
        page.window_height = 600
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.LIGHT

        login_page(page)
    
    ft.app(target=main)