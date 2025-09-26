import flet as ft

def login_page(page: ft.Page):
    page.clean()
    
    txt_user = ft.TextField(label="Usuário", width=300)
    txt_pass = ft.TextField(label="Senha", password=True, width=300)
    
    def login_click(e):
        user = txt_user.value
        password = txt_pass.value
        # Aqui você chama a função do controller para autenticar
        print(f"Tentando login: {user} / {password}")
        page.add(ft.Text(f"Bem-vindo, {user}!"))
    
    btn_login = ft.ElevatedButton("Login", on_click=login_click)
    
    page.add(
        ft.Column(
            [txt_user, txt_pass, btn_login],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
