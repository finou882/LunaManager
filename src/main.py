import flet as ft
import json
from urllib import request, error
import os
from flet.auth.providers import Auth0OAuthProvider
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

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

    # Auth0プロバイダーの設定
    provider = Auth0OAuthProvider(
        client_id=os.getenv("AUTH0_CLIENT_ID"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        domain=os.getenv("AUTH0_DOMAIN"),
        redirect_url="http://localhost:3000/oauth_callback",
    )

    def login_button_click(e):
        page.login(provider)

    def on_login(e):
        if not e.error:
            toggle_auth_buttons()
            # ログイン成功時にユーザー情報を表示
            print("User ID:", page.auth.user.id)
            print("Access token:", page.auth.token.access_token)
            # トークンを保存
            page.client_storage.set("auth_token", page.auth.token.to_json())
            page.go("/")
        else:
            print("Login error:", e.error)

    def logout_button_click(e):
        page.client_storage.remove("auth_token")
        page.logout()
        page.go("/")

    def on_logout(e):
        toggle_auth_buttons()

    def toggle_auth_buttons():
        auth_buttons.controls[0].visible = page.auth is None  # login button
        auth_buttons.controls[1].visible = page.auth is not None  # logout button
        page.update()

    # 認証ボタンのコンテナ
    auth_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                "Sign in",
                icon=ft.icons.LOGIN,
                on_click=login_button_click,
            ),
            ft.ElevatedButton(
                "Sign out",
                icon=ft.icons.LOGOUT,
                on_click=logout_button_click,
                visible=False,
            ),
        ],
        spacing=10,
    )

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
                *auth_buttons.controls,  # 認証ボタンを展開
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

    # ログインイベントハンドラの設定
    page.on_login = on_login
    page.on_logout = on_logout

    # 保存されたトークンでの自動ログイン
    saved_token = page.client_storage.get("auth_token")
    if saved_token:
        try:
            page.login(provider, saved_token=saved_token)
        except Exception as e:
            print(f"Auto login failed: {e}")
            page.client_storage.remove("auth_token")

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
        def perform_search(e):
            query = search_field.value.strip()
            if query:
                # クエリがある場合、クラス名に基づいてフィルタリング
                filtered_classes = [class_data for class_data in get_classes() if query.lower() in class_data['name'].lower()]
            else:
                # クエリが空の場合、すべてのクラスをID順で取得
                filtered_classes = get_classes()

            # 検索結果を表示
            search_results.controls.clear()
            for class_data in filtered_classes:
                search_results.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.SCHOOL),
                        title=ft.Text(f"{class_data['name'] or 'No name'}"),
                        subtitle=ft.Text(
                            f"Teacher: {class_data['teacher']} | Instructor: {class_data['instructor']}"
                        ),
                        on_click=lambda e, id=class_data['id']: e.page.go(f"/class/{id}")
                    )
                )
            search_results.update()

        search_field = ft.TextField(label="Search...", prefix_icon=ft.Icons.SEARCH, on_change=perform_search)
        search_results = ft.ListView(height=200)

        return ft.Column(
            controls=[
                ft.Text("Search Page", size=30, weight=ft.FontWeight.BOLD),
                search_field,
                search_results,
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

    # 初期状態でのボタン表示制御
    toggle_auth_buttons()

# python-dotenvのインストールが必要
# pip install python-dotenv

ft.app(target=main, port=2000, view=ft.WEB_BROWSER)