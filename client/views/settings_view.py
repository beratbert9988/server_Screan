import flet as ft
from utils.i18n import i18n
from core.settings_manager import settings_manager
import os

class SettingsView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        
        self.theme_dropdown = ft.Dropdown(
            label=i18n.t("theme"),
            width=200,
            options=[
                ft.dropdown.Option("dark", i18n.t("dark")),
                ft.dropdown.Option("light", i18n.t("light")),
            ],
            value="dark" if page.theme_mode == ft.ThemeMode.DARK else "light",
            on_change=self.theme_changed
        )
        
        self.color_dropdown = ft.Dropdown(
            label="Color Scheme",
            width=200,
            options=[
                ft.dropdown.Option("blue", "Blue"),
                ft.dropdown.Option("green", "Green"),
                ft.dropdown.Option("red", "Red"),
                ft.dropdown.Option("purple", "Purple"),
                ft.dropdown.Option("orange", "Orange"),
                ft.dropdown.Option("yellow", "Yellow"),
                ft.dropdown.Option("pink", "Pink"),
                ft.dropdown.Option("cyan", "Cyan"),
                ft.dropdown.Option("teal", "Teal"),
                ft.dropdown.Option("indigo", "Indigo"),
            ],
            value=settings_manager.get("color_scheme"),
            on_change=self.color_changed
        )
        
        self.lang_dropdown = ft.Dropdown(
            label=i18n.t("language"),
            width=200,
            options=[
                ft.dropdown.Option("en", "English"),
                ft.dropdown.Option("tr", "Türkçe"),
                ft.dropdown.Option("de", "Deutsch"),
                ft.dropdown.Option("es", "Español"),
                ft.dropdown.Option("fr", "Français"),
            ],
            value=i18n.locale,
            on_change=self.lang_changed
        )

        self.controls = [
            ft.Text(i18n.t("settings"), size=30, weight="bold"),
            ft.Divider(),
            ft.Container(
                content=ft.Column([
                    self.theme_dropdown,
                    self.color_dropdown,
                    self.lang_dropdown,
                ]),
                padding=20,
                bgcolor="surfaceVariant",
                border_radius=10
            )
        ]

    def theme_changed(self, e):
        mode = self.theme_dropdown.value
        self.page.theme_mode = ft.ThemeMode.DARK if mode == "dark" else ft.ThemeMode.LIGHT
        settings_manager.set("theme_mode", mode)
        self.page.update()

    def color_changed(self, e):
        color_name = self.color_dropdown.value
        self.page.theme = ft.Theme(color_scheme_seed=color_name)
        settings_manager.set("color_scheme", color_name)
        self.page.update()

    def lang_changed(self, e):
        lang = self.lang_dropdown.value
        i18n.set_locale(lang)
        settings_manager.set("language", lang)
        # We need to refresh the UI to show new strings
        # We need to refresh the UI to show new strings
        # Simplest way: reload current page/view
        self.page.go("/settings") # Force re-route or similar 
        # But actually in main.py route_change clears views, so going to same route might trigger update if logical
        # Better: use a snackbar to say "Language changed"
        self.page.snack_bar = ft.SnackBar(ft.Text(f"Language changed to {lang}. Please navigate to refresh."))
        self.page.snack_bar.open = True
        self.page.update()
