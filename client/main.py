import flet as ft
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.processes_view import ProcessesView
from views.terminal_view import TerminalView
from views.services_view import ServicesView
from views.settings_view import SettingsView
from utils.i18n import i18n
from core.settings_manager import settings_manager

def main(page: ft.Page):
    page.title = "Server Control Panel"
    
    # Load Settings
    theme_mode = settings_manager.get("theme_mode")
    color_scheme = settings_manager.get("color_scheme")
    language = settings_manager.get("language")

    page.theme_mode = ft.ThemeMode.DARK if theme_mode == "dark" else ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=color_scheme)
    i18n.set_locale(language)

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 0
    page.window_width = 1000
    page.window_height = 800

    def route_change(route):
        page.views.clear()
        
        # Always allow Login
        if page.route == "/login":
            page.views.append(LoginView(page))
        else:
            # For other routes, add dashboard layout (Sidebar + Content)
            # But for simplicity in this Flet app, we will use a Tabs approach in the main view 
            # OR just swap the whole view. 
            # Let's use a MainView that holds the navigation for authenticated state.
            if page.route == "/dashboard":
                page.views.append(MainLayout(page, "dashboard"))
            elif page.route == "/processes":
                page.views.append(MainLayout(page, "processes"))
            elif page.route == "/terminal":
                page.views.append(MainLayout(page, "terminal"))
            elif page.route == "/services":
                page.views.append(MainLayout(page, "services"))
            elif page.route == "/settings":
                page.views.append(MainLayout(page, "settings"))
            else:
                 page.views.append(LoginView(page))
                 
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go("/login")

class MainLayout(ft.View):
    def __init__(self, page, active_tab):
        super().__init__(route=f"/{active_tab}")
        self.page = page
        self.active_tab = active_tab
        
        # Navigation Rail
        self.rail = ft.NavigationRail(
            selected_index={"dashboard":0, "processes":1, "services":2, "terminal":3, "settings":4}.get(active_tab, 0),
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD, 
                    selected_icon=ft.Icons.DASHBOARD, 
                    label=i18n.t("dashboard")
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.MEMORY, 
                    selected_icon=ft.Icons.MEMORY_OUTLINED, 
                    label=i18n.t("processes")
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS, 
                    selected_icon=ft.Icons.SETTINGS_APPLICATIONS, 
                    label=i18n.t("services")
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.TERMINAL, 
                    selected_icon=ft.Icons.TERMINAL_OUTLINED, 
                    label=i18n.t("terminal")
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SETTINGS, 
                    selected_icon=ft.Icons.SETTINGS_OUTLINED, 
                    label=i18n.t("settings")
                ),
            ],
            on_change=self.nav_change,
        )

        # Content Area
        if active_tab == "dashboard":
            self.content_area = DashboardView()
        elif active_tab == "processes":
            self.content_area = ProcessesView()
        elif active_tab == "services":
            self.content_area = ServicesView()
        elif active_tab == "terminal":
            self.content_area = TerminalView()
        elif active_tab == "settings":
            self.content_area = SettingsView(page)
        else:
            self.content_area = ft.Text("Unknown")
            
        self.controls = [
            ft.Row(
                [
                    self.rail,
                    ft.VerticalDivider(width=1),
                    ft.Column([self.content_area], expand=True, alignment=ft.MainAxisAlignment.START)
                ],
                expand=True,
            )
        ]

    def nav_change(self, e):
        idx = e.control.selected_index
        if idx == 0:
            self.page.go("/dashboard")
        elif idx == 1:
            self.page.go("/processes")
        elif idx == 2:
            self.page.go("/services")
        elif idx == 3:
            self.page.go("/terminal")
        elif idx == 4:
            self.page.go("/settings")

if __name__ == "__main__":
    ft.app(target=main)
