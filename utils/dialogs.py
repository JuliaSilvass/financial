import flet as ft


def show_alert(page: ft.Page, title: str, message: str):
    dialog = ft.CupertinoAlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.CupertinoDialogAction(
                text="OK",
                on_click=lambda e: page.close(dialog),
            )
        ],
    )

    page.open(dialog)


def close_alert(page: ft.Page):
    if page.dialog:
        page.dialog.open = False
        page.update()
