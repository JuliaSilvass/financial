# utils/sidebar.py
import flet as ft
from services.session_manager import SessionManager

def build_sidebar(page: ft.Page, user: dict, menu_items: list, active_route: str = ""):
    def logout_click(e):
        SessionManager.logout()
        page.go("/")

    buttons = []
    for item in menu_items:
        route = item["route"]
        is_active = (active_route == route)

        buttons.append(
            ft.Container(
                width=float("inf"),
                content=ft.ElevatedButton(
                    text=item["label"],
                    icon=item.get("icon"),
                    disabled=is_active,
                    on_click=None if is_active else (lambda e, r=route: page.go(r)),
                    style=ft.ButtonStyle(
                        bgcolor={
                            "": "#38A08B" if is_active else "#B2DFDB",
                            "hovered": "#3AB08F",
                        },
                        color={
                            "": "#1E3D59",
                        },
                        padding=ft.padding.symmetric(vertical=14),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color="#38A08B",
                    ),
                ),
            )
        )

    return ft.Container(
        width=230,
        padding=ft.padding.all(15),
        bgcolor="#E0F7FA",
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=8, color="#C8E6C9"),
        content=ft.Column(
            expand=True,
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text(
                    f"Olá, {user['nome']}",
                    size=20,
                    weight="bold",
                    color="#1E3D59",
                ),
                ft.Divider(height=2, thickness=1, color="#44CFA1"),
                *buttons,
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Logout",
                    bgcolor="#F28B82",
                    color="white",
                    on_click=logout_click,
                    style=ft.ButtonStyle(
                        padding=ft.padding.symmetric(vertical=12),
                        shape=ft.RoundedRectangleBorder(radius=8),
                        overlay_color="#E57373",
                    ),
                ),
            ],
        ),
    )
