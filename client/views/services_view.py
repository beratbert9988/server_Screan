import flet as ft
from services.api_client import api_client
from utils.i18n import i18n

class ServicesView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.api = api_client
        
        self.search_field = ft.TextField(
            label=i18n.t("search_service"), 
            on_change=self.filter_services,
            prefix_icon=ft.Icons.SEARCH
        )
        
        self.service_list = ft.ListView(expand=True, spacing=10, padding=10)
        self.all_services = []
        
        self.controls = [
            ft.Row([
                ft.Text(i18n.t("service_manager"), size=30, weight="bold"),
                ft.IconButton(ft.Icons.REFRESH, on_click=self.refresh_data)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.search_field,
            ft.Divider(),
            ft.Container(content=self.service_list, expand=True)
        ]
        
    def did_mount(self):
        self.refresh_data(None)

    def refresh_data(self, e):
        self.all_services = self.api.get_services()
        self.render_list(self.all_services)

    def filter_services(self, e):
        query = self.search_field.value.lower()
        if not query:
            self.render_list(self.all_services)
            return
        filtered = [s for s in self.all_services if query in s['unit'].lower()]
        self.render_list(filtered)

    def render_list(self, services):
        self.service_list.controls.clear()
        # Limit for performance
        display_services = services[:50] if services else []
        
        for s in display_services:
            is_active = s['active'] == 'active'
            status_color = "green" if is_active else "red"
            
            self.service_list.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SETTINGS, color=status_color),
                    title=ft.Text(s['unit']),
                    subtitle=ft.Text(f"State: {s['active']} ({s['sub']})"),
                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT,
                        items=[
                            ft.PopupMenuItem(
                                text=i18n.t("start"), 
                                icon=ft.Icons.PLAY_ARROW,
                                on_click=lambda e, name=s['unit']: self.manage_svc(name, "start")
                            ),
                             ft.PopupMenuItem(
                                text=i18n.t("stop"), 
                                icon=ft.Icons.STOP,
                                on_click=lambda e, name=s['unit']: self.manage_svc(name, "stop")
                            ),
                             ft.PopupMenuItem(
                                text=i18n.t("restart"), 
                                icon=ft.Icons.RESTART_ALT,
                                on_click=lambda e, name=s['unit']: self.manage_svc(name, "restart")
                            ),
                        ]
                    )
                )
            )
        self.update()

    def manage_svc(self, name, action):
        success, msg = self.api.manage_service(name, action)
        if success:
            snack = ft.SnackBar(ft.Text(f"Service {name} {action}ed"))
            self.refresh_data(None)
        else:
            snack = ft.SnackBar(ft.Text(f"Failed: {msg}"))
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()
