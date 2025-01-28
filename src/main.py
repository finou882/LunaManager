import flet as ft
import random
import datetime
import calendar
from flet import Container, ElevatedButton, Page, LoginEvent
from flet.auth.providers.google_oauth_provider import GoogleOAuthProvider
import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
import webbrowser

load_dotenv()

ClientID = os.getenv('ClientID')
ClientSecret = os.getenv('ClientSecret')
RedirectUrl = os.getenv('RedirectUrl')

# Wasequeクラスの定義
class Waseque:
    def __init__(self, number, title, description="", date=None):
        self.number = number
        self.title = title
        self.description = description
        self.date = date  # 日程を追加

# サンプルWasequeデータの作成（サンプル数を増やす）
sample_waseques = [
    Waseque("WQ039", "Waseque Project 39: Game Development", "ゲーム開発プロジェクト", datetime.date(2024, 12, 1)),
    Waseque("WQ050", "Waseque Project 50: Mobile App", "モバイルアプリ開発", datetime.date(2024, 4, 15)),
    Waseque("WQ035", "Waseque Project 35: Web Development", "Webアプリケーション開発", datetime.date(2024, 5, 1)),
    Waseque("WQ042", "Waseque Project 42: AI Development", "AI開発プロジェクト", datetime.date(2024, 5, 15)),
    Waseque("WQ048", "Waseque Project 48: IoT Project", "IoTプロジェクト", datetime.date(2024, 6, 1)),
    Waseque("WQ037", "Waseque Project 37: Data Science", "データサイエンス", datetime.date(2024, 6, 15)),
    Waseque("WQ045", "Waseque Project 45: Blockchain", "ブロックチェーン開発", datetime.date(2024, 7, 1))
]

def view_waseque_details(page: ft.Page, waseque):
    # AppBarをページのプロパティとして設定
    page.appbar = ft.AppBar(
        title=ft.Text(waseque.title),
        bgcolor=ft.Colors.BLACK54,
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            on_click=lambda _: page.go("/home")
        ),
    )
    page.update()

    return ft.View(
        f"/waseque/{waseque.number}",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.ListTile(
                                        title=ft.Text(waseque.title, size=20, weight=ft.FontWeight.BOLD),
                                        subtitle=ft.Text(f"Waseque Number: {waseque.number}"),
                                    ),
                                    ft.Container(
                                        content=ft.Text(waseque.description),
                                        padding=ft.padding.all(16),
                                    ),
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    "Back",
                                                    icon=ft.icons.ARROW_BACK,
                                                    on_click=lambda _: page.go("/home"),
                                                    style=ft.ButtonStyle(
                                                        color=ft.colors.WHITE,
                                                        bgcolor=ft.colors.GREY_700,
                                                    ),
                                                ),
                                                ft.ElevatedButton(
                                                    "Join Project",
                                                    icon=ft.icons.PERSON_ADD,
                                                    style=ft.ButtonStyle(
                                                        color=ft.colors.WHITE,
                                                        bgcolor=ft.colors.BLUE_400,
                                                    ),
                                                    on_click=lambda _: (
                                                        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"エントリー完了:ワセクエ:{waseque.number}"))),
                                                        page.go("/home")
                                                    )
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        padding=ft.padding.all(16),
                                    ),
                                ]),
                            ),
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                expand=True,
            ),
        ],
    )

def Settings(page: ft.Page):
    page.title = "LinK"

    def toggle_theme(e):
        if e.control.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    def open_link(e):
        webbrowser.open("https://ja.pngtree.com/freepng/a-modern-stylized-fox-with-sharp-geometric-lines-and-bold-head-shape_19753618.html")

    rail = create_navigation_rail(page, selected_index=1)  # Settingsページのインデックスを選択

    return ft.View(
        "/settings",
        [
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    [
                                        ft.Text("Dark Mode"),
                                        ft.Switch(
                                            value=page.theme_mode == ft.ThemeMode.DARK,
                                            on_change=toggle_theme
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.GestureDetector(
                                    on_tap=open_link,
                                    child=ft.Text(
                                        "からの PNG 画像 ja.pngtree.com",
                                        color=ft.Colors.BLUE,
                                        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                                    ),
                                ),
                            ],
                            spacing=20,
                        ),
                        padding=20,  # Containerでpaddingを設定
                    ),
                ],
                expand=True,
            )
        ],
    )

def create_navigation_rail(page: ft.Page, selected_index: int = 0):
    def handle_rail_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.go("/home")
        elif selected_index == 1:
            page.go("/settings")
        elif selected_index == 2:
            page.go("/community")
        elif selected_index == 3:
            page.go("/messages")

    return ft.NavigationRail(
        selected_index=selected_index,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        height=700,
        bgcolor=ft.Colors.BLACK54,
        leading=ft.Container(
            content=ft.Image(
                src="images/logos/50px_white.png",
                width=50,
                height=50,
                fit=ft.ImageFit.CONTAIN,
            ),
            margin=ft.margin.only(bottom=20),
        ),
        group_alignment=-0.9,
        on_change=handle_rail_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD_OUTLINED,
                selected_icon=ft.Icons.DASHBOARD,
                label="Dashboard",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINED,
                selected_icon=ft.Icons.PEOPLE,
                label="Community",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FORUM_OUTLINED,
                selected_icon=ft.Icons.FORUM,
                label="Messages",
            ),
        ],
    )

def main(page: ft.Page):
    page.title = "LinK"
    page.bgcolor = ft.Colors.BLACK87

    def route_change(route):
        troute = ft.TemplateRoute(route.route)
        page.views.clear()

        if troute.match("/"):
            page.go("/login")
        elif troute.match("/login"):
            page.views.append(Login(page))
        elif troute.match("/home"):
            page.views.append(Home(page))
        elif troute.match("/Settings"):
            page.views.append(Settings(page))
        elif troute.match("/waseque/:number"):
            number = route.route.split("/")[-1]
            waseque = next((w for w in sample_waseques if w.number == number), None)
            if waseque:
                page.views.append(view_waseque_details(page, waseque))
        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

def Home(page: ft.Page):
    def handle_waseque_click(e):
        waseque_number = e.control.data
        page.go(f"/waseque/{waseque_number}")

    def handle_rail_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.go("/home")
        elif selected_index == 1:
            page.go("/settings")
        elif selected_index == 2:
            page.go("/community")
        elif selected_index == 3:
            page.go("/messages")

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        height=700,
        bgcolor=ft.Colors.BLACK54,
        leading=ft.Container(
            content=ft.Image(
                src="./assets/50px_white.png",
                width=50,
                height=50,
                fit=ft.ImageFit.CONTAIN,
            ),
            margin=ft.margin.only(bottom=20),
        ),
        group_alignment=-0.9,
        on_change=handle_rail_change,  # イベントハンドラを追加
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD_OUTLINED,
                selected_icon=ft.Icons.DASHBOARD,
                label="Dashboard",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINED,
                selected_icon=ft.Icons.PEOPLE,
                label="Community",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FORUM_OUTLINED,
                selected_icon=ft.Icons.FORUM,
                label="Messages",
            ),
        ],
    )

    # サンプル数を取得して、適切な数を選択
    sample_size = min(5, len(sample_waseques))
    
    return ft.View(
        "/home",
        [
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            # Today's Pickup
                                            ft.Card(
                                                content=ft.Container(
                                                    content=ft.Column([
                                                        ft.ListTile(
                                                            leading=ft.Icon(ft.Icons.STAR_OUTLINED, color=ft.Colors.AMBER_400),
                                                            title=ft.Text("Today's Pickup", size=20, weight=ft.FontWeight.BOLD),
                                                        ),
                                                        # Wasequeカードのリスト
                                                        ft.GridView(
                                                            controls=[
                                                                ft.Card(
                                                                    content=ft.ListTile(
                                                                        leading=ft.Icon(ft.Icons.WORKSPACE_PREMIUM, color=ft.Colors.BLUE_400),
                                                                        title=ft.Text(waseque.title, weight=ft.FontWeight.BOLD),
                                                                        subtitle=ft.Text(f"#{waseque.number}"),
                                                                        data=waseque.number,
                                                                        on_click=handle_waseque_click,
                                                                    ),
                                                                )
                                                                for waseque in random.sample(sample_waseques, sample_size)
                                                            ],
                                                            runs_count=1,
                                                            spacing=10,
                                                            run_spacing=10,
                                                            height=400,
                                                            child_aspect_ratio=5.0,
                                                        ),
                                                    ]),
                                                    padding=10,
                                                ),
                                            ),
                                            # Overview
                                            ft.Card(
                                                content=ft.Container(
                                                    content=ft.Column([
                                                        ft.ListTile(
                                                            leading=ft.Icon(ft.Icons.ANALYTICS_OUTLINED, color=ft.Colors.BLUE_400),
                                                            title=ft.Text("Overview", size=20, weight=ft.FontWeight.BOLD),
                                                        ),
                                                        ft.Row([
                                                            ft.Card(
                                                                content=ft.Container(
                                                                    content=ft.Column([
                                                                        ft.Text("Total Waseques", color=ft.Colors.GREY_500),
                                                                        ft.Text(str(len(sample_waseques)), size=32, weight=ft.FontWeight.BOLD),
                                                                    ], spacing=5),
                                                                    padding=15,
                                                                ),
                                                                width=150,
                                                            ),
                                                            ft.Card(
                                                                content=ft.Container(
                                                                    content=ft.Column([
                                                                        ft.Text("Active Projects", color=ft.Colors.GREY_500),
                                                                        ft.Text("28", size=32, weight=ft.FontWeight.BOLD),
                                                                    ], spacing=5),
                                                                    padding=15,
                                                                ),
                                                                width=150,
                                                            ),
                                                        ], spacing=20),
                                                    ]),
                                                    padding=20,
                                                ),
                                            ),
                                        ],
                                        spacing=20,
                                        scroll=ft.ScrollMode.ALWAYS,
                                        expand=True,
                                    ),
                                    expand=True,
                                    padding=20,
                                ),
                            ],
                            expand=True,
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        ],
    )

def Login(page: ft.Page):
    page.title = "LinK"
    page.bgcolor = ft.Colors.BLACK87  # 背景色を暗めに設定

    provider = GoogleOAuthProvider(
        client_id=ClientID,
        client_secret=ClientSecret,
        redirect_url=RedirectUrl
    )

    def login_button_click(e):
        page.go("/home")  # Immediately redirect to /home

    def on_login(e: LoginEvent):
        if not e.error:
            print("Login successful!")
            print("Email:", page.auth.user.get("email", "No email found"))
            toggle_login_buttons()

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        print("Logged out.")
        toggle_login_buttons()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logout_button.visible = page.auth is not None
        page.update()

    login_button = ElevatedButton("Login with Google", on_click=login_button_click)
    logout_button = ElevatedButton("Logout", on_click=logout_button_click)
    toggle_login_buttons()

    page.on_login = on_login
    page.on_logout = on_logout

    return ft.View(
        "/login",
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Image(
                                            src=r"C:\Users\finou\Documents\Projects\Projects2\LinK\src\assets\50px_white.png",
                                            width=150,
                                            height=150,
                                            fit=ft.ImageFit.CONTAIN,
                                        ),
                                        ft.Text("Welcome back!", size=16, color=ft.Colors.GREY_400),
                                        ft.Container(height=20),
                                        login_button,
                                    ],
                                    spacing=15,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                width=400,
                                height=500,
                                padding=ft.padding.all(40),
                                border_radius=15,
                                bgcolor=ft.Colors.BLACK54,
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=25,
                                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_100),
                                    offset=ft.Offset(0, 4)
                                ),
                                border=ft.border.all(0.5, ft.Colors.BLUE_GREY_700),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            )
        ],
    )


if __name__ == "__main__":
    ft.app(target=main, port=8000, view=ft.AppView.WEB_BROWSER)
