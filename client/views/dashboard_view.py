import flet as ft
import threading
import time
from services.api_client import api_client
from utils.i18n import i18n

class DashboardView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.scroll = ft.ScrollMode.AUTO
        
        # CPU
        self.cpu_progress = ft.ProgressBar(width=400, color="blue", bgcolor="#222222", value=0)
        self.cpu_text = ft.Text("CPU: 0%", size=20)
        
        # RAM
        self.ram_progress = ft.ProgressBar(width=400, color="purple", bgcolor="#222222", value=0)
        self.ram_text = ft.Text("RAM: 0%", size=20)
        
        # Disk
        self.disk_progress = ft.ProgressBar(width=400, color="green", bgcolor="#222222", value=0)
        self.disk_text = ft.Text("Disk: 0%", size=20)

        self.controls = [
            ft.Text(i18n.t("dashboard"), size=30, weight="bold"),
            ft.Divider(),
            ft.Container(
                content=ft.Column([
                    ft.Text(i18n.t("cpu")),
                    self.cpu_text,
                    self.cpu_progress,
                    ft.Container(height=20),
                    ft.Text(i18n.t("ram")),
                    self.ram_text,
                    self.ram_progress,
                    ft.Container(height=20),
                    ft.Text(i18n.t("disk")),
                    self.disk_text,
                    self.disk_progress,
                ]),
                padding=20,
                bgcolor="surfaceVariant",
                border_radius=10
            ),
            ft.Container(height=20),
            ft.Text(i18n.t("power_controls"), size=30, weight="bold"),
            ft.Divider(),
            ft.Row([
                ft.ElevatedButton(
                    i18n.t("restart"), 
                    icon=ft.Icons.RESTART_ALT, 
                    color="white", 
                    bgcolor="orange",
                    on_click=self.restart_click
                ),
                ft.ElevatedButton(
                    i18n.t("shutdown"), 
                    icon=ft.Icons.POWER_SETTINGS_NEW, 
                    color="white", 
                    bgcolor="red",
                    on_click=self.shutdown_click
                ),
            ])
        ]
        
        self.running = True
        # Start background thread to update stats
        # Note: In Flet, UI updates must happen in the main thread or via page.update() 
        # but we need to be careful with contexts. 
        # We will use a basic loop that checks `self.page` existence.
        self.is_mounted = False

    def did_mount(self):
        self.is_mounted = True
        self.running = True
        threading.Thread(target=self.update_loop, daemon=True).start()

    def will_unmount(self):
        self.is_mounted = False
        self.running = False

    def update_loop(self):
        while self.running:
            stats = api_client.get_stats()
            if stats:
                self.cpu_progress.value = stats['cpu_percent'] / 100
                self.cpu_text.value = f"CPU: {stats['cpu_percent']}%"
                
                self.ram_progress.value = stats['ram_percent'] / 100
                self.ram_text.value = f"RAM: {stats['ram_percent']}% ({stats['ram_used'] // 1024 // 1024} MB / {stats['ram_total'] // 1024 // 1024} MB)"

                self.disk_progress.value = stats['disk_percent'] / 100
                self.disk_text.value = f"Disk: {stats['disk_percent']}%"
                
                if self.is_mounted and self.page:
                    try:
                        self.update()
                    except:
                        pass
            time.sleep(2)

    def restart_click(self, e):
        self.confirm_action("Restart", self.do_restart)

    def shutdown_click(self, e):
        self.confirm_action("Shutdown", self.do_shutdown)

    def confirm_action(self, action, func):
        def close_dlg(e):
            dlg.open = False
            self.page.update()

        def do_it(e):
            dlg.open = False
            self.page.update()
            func()

        dlg = ft.AlertDialog(
            title=ft.Text(i18n.t("confirm")),
            content=ft.Text(i18n.t("confirm_msg", action=action)),
            actions=[
                ft.TextButton(i18n.t("cancel"), on_click=close_dlg),
                ft.TextButton(i18n.t("yes"), on_click=do_it, style=ft.ButtonStyle(color="red")),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def do_restart(self):
        api_client.reboot_system()
        self.page.snack_bar = ft.SnackBar(ft.Text("Reboot command sent..."))
        self.page.snack_bar.open = True
        self.page.update()

    def do_shutdown(self):
        api_client.shutdown_system()
        self.page.snack_bar = ft.SnackBar(ft.Text("Shutdown command sent..."))
        self.page.snack_bar.open = True
        self.page.update()
