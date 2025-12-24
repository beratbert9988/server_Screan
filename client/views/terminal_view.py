import flet as ft
from services.api_client import api_client
from utils.i18n import i18n

class TerminalView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        
        self.output_area = ft.TextField(
            multiline=True,
            read_only=True,
            text_style=ft.TextStyle(font_family="monospace"),
            expand=True,
            bgcolor="#1e1e1e",
            color="#00ff00",
            border_color="transparent"
        )
        
        self.input_field = ft.TextField(
            label=i18n.t("command"), 
            on_submit=self.run_command,
            multiline=False,
            expand=True
        )

        self.run_btn = ft.ElevatedButton(i18n.t("run"), on_click=self.run_command)

        self.controls = [
            ft.Text(i18n.t("remote_terminal"), size=30, weight="bold"),
            ft.Divider(),
            ft.Container(
                content=self.output_area,
                height=400,
                border=ft.border.all(1, "outline"),
                border_radius=5,
                padding=10,
            ),
            ft.Row([
                self.input_field,
                self.run_btn
            ])
        ]

    def run_command(self, e):
        cmd = self.input_field.value
        if not cmd:
            return
        
        self.output_area.value += f"\n$ {cmd}\n"
        self.input_field.value = ""
        self.update()
        
        res = api_client.execute_command(cmd)
        
        if "error" in res:
             self.output_area.value += f"Error: {res['error']}\n"
        else:
            if res.get('stdout'):
                self.output_area.value += res['stdout']
            if res.get('stderr'):
                self.output_area.value += f"STDERR:\n{res['stderr']}"
                
        self.output_area.value += "\n"
        self.update()
