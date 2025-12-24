import flet as ft
from services.api_client import api_client

class LoginView(ft.View):
    def __init__(self, page):
        super().__init__(route="/login")
        from utils.i18n import i18n # Delayed import to avoid circular dependency if any, or just convenience
        self.page = page
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        self.url_field = ft.TextField(label=i18n.t("url"), value="127.0.0.1:8000", width=300)
        self.token_field = ft.TextField(label=i18n.t("token"), password=True, value="admin123", width=300)
        self.error_text = ft.Text("", color="red")
        
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(i18n.t("server_control"), size=30, weight=ft.FontWeight.BOLD),
                        ft.Container(height=20),
                        self.url_field,
                        self.token_field,
                        ft.ElevatedButton(i18n.t("connect"), on_click=self.login, width=300),
                        self.error_text
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=50,
                border_radius=10,
                bgcolor="surfaceVariant",
            )
        ]

    def login(self, e):
        url = self.url_field.value
        token = self.token_field.value
        
        if not url or not token:
            self.error_text.value = "Please fill all fields"
            self.update()
            return
            
        self.error_text.value = "Connecting..."
        self.update()
        
        if api_client.connect(url, token):
            self.page.go("/dashboard")
        else:
            self.error_text.value = "Connection failed. Check URL and Token."
            self.update()
