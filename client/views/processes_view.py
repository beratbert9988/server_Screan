import flet as ft
from services.api_client import api_client
from utils.i18n import i18n

class ProcessesView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.api = api_client
        
        self.search_field = ft.TextField(
            label=i18n.t("search_process"), 
            on_change=self.filter_processes,
            prefix_icon=ft.Icons.SEARCH
        )
        
        self.process_list = ft.ListView(expand=True, spacing=10, padding=10)
        self.all_processes = []
        
        self.controls = [
            ft.Row([
                ft.Text(i18n.t("process_manager"), size=30, weight="bold"),
                ft.IconButton(ft.Icons.REFRESH, on_click=self.refresh_data)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.search_field,
            ft.Divider(),
            ft.Container(content=self.process_list, expand=True)
        ]
        
    def did_mount(self):
        self.refresh_data(None)

    def refresh_data(self, e):
        self.all_processes = self.api.get_processes()
        self.render_list(self.all_processes)

    def filter_processes(self, e):
        query = self.search_field.value.lower()
        filtered = [p for p in self.all_processes if query in p['name'].lower()]
        self.render_list(filtered)

    def render_list(self, processes):
        self.process_list.controls.clear()
        # Limit to top 50 to avoid lag if too many
        for p in processes[:50]: 
            self.process_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.MEMORY),
                    title=ft.Text(f"{p['name']} (PID: {p['pid']})"),
                    subtitle=ft.Text(f"CPU: {p['cpu_percent']}% | Mem: {p['memory_percent']:.1f}% | User: {p['username']}"),
                    trailing=ft.IconButton(
                        ft.Icons.DELETE_FOREVER, 
                        icon_color="red",
                        tooltip="Kill Process",
                        on_click=lambda e, pid=p['pid']: self.kill_proc(pid)
                    )
                )
            )
        self.update()

    def kill_proc(self, pid):
        success, msg = self.api.kill_process(pid)
        if success:
            snack = ft.SnackBar(ft.Text(f"Process {pid} killed"))
            self.refresh_data(None)
        else:
            snack = ft.SnackBar(ft.Text(f"Failed to kill: {msg}"))
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()
