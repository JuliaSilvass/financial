import flet as ft

def register_page(page: ft.Page):

    # Campos de cadastro
    txt_user = ft.TextField(label="Nome", width=300)
    txt_email = ft.TextField(label="Email", width=300)
    txt_pass = ft.TextField(label="Senha", password=True, width=300)
    txt_pass_confirm = ft.TextField(label="Confirmar Senha", password=True, width=300)

    # Função do botão de registrar
    def register_click(e):
        user = txt_user.value
        email = txt_email.value
        password = txt_pass.value
        password_confirm = txt_pass_confirm.value

        if password != password_confirm:
            page.snack_bar = ft.SnackBar(ft.Text("As senhas não coincidem!"))
        else:
            # Aqui você chamaria o controller para criar o usuário no banco
            page.snack_bar = ft.SnackBar(ft.Text(f"Usuário {user} cadastrado com sucesso!"))
        page.snack_bar.open = True
        page.update()

    #Função do botão de voltar para home
    def backToHome_click(e):
        page.go("/")
    

    # Botão de registrar
    btn_register = ft.ElevatedButton(
        text="Registrar",
        style=ft.ButtonStyle(
            bgcolor={"": "#44CFA1"},
            color={"": "white"},
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=register_click
    )

    # Botão de Voltar para Home
    btn_backToHome = ft.IconButton(
        icon=ft.Icons.HOME,
        icon_color="white",
        bgcolor="#44CFA1",
        on_click=backToHome_click
    )


    # Retornar a View com os controles
    return ft.View(
        route="/register",
        controls=[
            ft.Column(
                controls=[  
                    ft.Text("Registrar-se", theme_style="displayMedium", size=40, weight="bold", color="#44CFA1"),
                    ft.Text("Preencha os campos abaixo para criar uma nova conta.", size=20),
                        txt_user, 
                        txt_email, 
                        txt_pass, 
                        txt_pass_confirm, 
                        btn_register,
                        btn_backToHome],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        ],
        horizontal_alignment="center",
        vertical_alignment="center"
    )
