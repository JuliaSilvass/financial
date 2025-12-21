import flet as ft


def show_alert(page: ft.Page, title: str, message: str):
    """Dialog padrão de alerta (apenas OK)"""
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


def show_confirm_dialog(page: ft.Page, title: str, message: str, on_confirm):
    """
    Dialog padrão de confirmação (Confirmar / Cancelar)
    on_confirm: função executada quando o usuário confirmar
    """

    dialog = ft.CupertinoAlertDialog(
        title=ft.Text(title),
        content=ft.Text(message),
        actions=[
            ft.CupertinoDialogAction(
                text="Cancelar",
                is_destructive_action=False,
                on_click=lambda e: page.close(dialog),
            ),
            ft.CupertinoDialogAction(
                text="Confirmar",
                is_destructive_action=True,
                on_click=lambda e: (
                    page.close(dialog),
                    on_confirm()
                ),
            ),
        ],
    )

    page.open(dialog)


