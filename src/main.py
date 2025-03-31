import flet as ft
import json
from urllib import request, error

def get_classes():
    try:
        with request.urlopen("http://127.0.0.1:3001/classes") as response:
            data = response.read()
            classes = json.loads(data)
            return sorted(classes, key=lambda x: x["id"])[:10]
    except error.URLError:
        return []

def get_class_detail(class_id):
    try:
        with request.urlopen(f"http://127.0.0.1:3001/classes/{class_id}") as response:
            data = response.read()
            return json.loads(data)
    except error.URLError:
        return None

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def home_page():
        classes = get_classes()
        return ft.Column(
            controls=[
                ft.Text("Classes", size=30, weight=ft.FontWeight.BOLD),
                ft.Column(
                controls=[
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.SCHOOL),
                                        title=ft.Text(f"{class_data['name'] or 'No name'}"),
                                        subtitle=ft.Text(
                                            f"Teacher: {class_data['teacher']} | Instructor: {class_data['instructor']}"
                                        ),
                                    ),
                                    ft.Row(
                                        [
                                            ft.TextButton(
                                                "Details",
                                                on_click=lambda e, id=class_data['id']: e.page.go(f"/class/{id}")
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            width=400,
                            padding=10,
                        ),
                    ) for class_data in classes
                ],
                scroll=ft.ScrollMode.AUTO,
            )
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    def class_detail_page(class_id):
        class_data = get_class_detail(class_id)
        if not class_data:
            return ft.Text("Class not found")
        
        return ft.Column(
            controls=[
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.SCHOOL),
                                    title=ft.Text(f"{class_data['name'] or 'No name'}", size=24),
                                ),
                                ft.Divider(),
                                ft.Text(f"Teacher: {class_data['teacher']}", size=16),
                                ft.Text(f"Instructor: {class_data['instructor']}", size=16),
                                ft.Text(f"Summary: {class_data['summary']}", size=16),
                            ]
                        ),
                        width=400,
                        padding=20,
                    )
                ),
                ft.ElevatedButton(
                    "Back to Home",
                    on_click=lambda e: e.page.go("/")
                ),
            ]
        )

    def search_page():
        return ft.Column(
            controls=[
                ft.Text("Search Page", size=30, weight=ft.FontWeight.BOLD),
                ft.TextField(label="Search...", prefix_icon=ft.Icons.SEARCH),
                ft.ListView(
                    controls=[
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.ARTICLE),
                            title=ft.Text(f"Search Result {i}")
                        ) for i in range(1, 5)
                    ],
                    height=200,
                )
            ]
        )

    def chat_page():
        return ft.Column(
            controls=[
                ft.Text("Chat Page", size=30, weight=ft.FontWeight.BOLD),
                ft.ListView(
                    controls=[
                        ft.ListTile(
                            leading=ft.CircleAvatar(content=ft.Text(f"U{i}")),
                            title=ft.Text(f"User {i}"),
                            subtitle=ft.Text("Last message...")
                        ) for i in range(1, 4)
                    ],
                    height=200,
                )
            ]
        )

    def settings_page():
        return ft.Column(
            controls=[
                ft.Text("Settings Page", size=30, weight=ft.FontWeight.BOLD),
                ft.Switch(label="Dark Mode"),
                ft.Slider(label="Volume", min=0, max=100, value=50),
                ft.TextField(label="Username"),
                ft.ElevatedButton("Save Settings")
            ]
        )

    def handle_drawer_change(e):
        selected_index = e.control.selected_index
        routes = ["/", "/search", "/chat", "/settings"]
        if selected_index is not None and 0 <= selected_index < len(routes):
            page.go(routes[selected_index])
            page.drawer.open = False
        page.update()

    def handle_drawer_dismiss(e):
        page.drawer.open = False
        page.update()

    def Nbar_clicked(e):
        print("Drawer clicked")  # デバッグ用
        if page.drawer:
            page.drawer.open = not page.drawer.open
            print(f"Drawer open: {page.drawer.open}")  # デバッグ用
            page.update()

    def check_item_clicked(e):
        page.update()

    # イベントハンドラを定義した後にドロワーを定義
    drawer = ft.NavigationDrawer(
        on_change=handle_drawer_change,
        on_dismiss=handle_drawer_dismiss,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Home",
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SEARCH_OUTLINED,
                label="Search",
                selected_icon=ft.Icons.SEARCH,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.CHAT_OUTLINED,
                label="Chat",
                selected_icon=ft.Icons.CHAT,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                label="Settings",
                selected_icon=ft.Icons.SETTINGS,
            ),
        ],
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    
    # ドロワーをページに追加
    page.drawer = drawer
    
    def create_appbar():
        return ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.MENU,
                on_click=Nbar_clicked
            ),
            leading_width=40,
            title=ft.Text("Luna Manager"),
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[
                ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.Icons.FILTER_3, on_click=Nbar_clicked),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),
                        ft.PopupMenuItem(
                            text="Checked item", 
                            checked=False, 
                            on_click=check_item_clicked
                        ),
                    ]
                ),
            ],
        )
    
    def route_change(route):
        page.views.clear()
        
        # クラス詳細ページのルートをチェック
        if page.route.startswith("/class/"):
            class_id = int(page.route.split("/")[-1])
            content = class_detail_page(class_id)
        else:
            # ページコンテンツのマッピング
            page_contents = {
                "/": home_page(),
                "/search": search_page(),
                "/chat": chat_page(),
                "/settings": settings_page(),
            }
            content = page_contents.get(page.route, home_page())
        
        page.views.append(
            ft.View(
                route=page.route,
                drawer=page.drawer,
                controls=[
                    create_appbar(),
                    ft.Container(
                        content=content,
                        padding=20,
                    )
                ]
            )
        )
        
        page.update()

    # ルート変更のイベントハンドラを設定
    page.on_route_change = route_change
    
    # 初期ルートを設定
    page.go('/')

ft.app(target=main, port=3000)