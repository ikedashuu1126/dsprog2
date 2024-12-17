import requests
import flet as ft

# 気象庁APIのエンドポイント
AREA_API_URL = "https://www.jma.go.jp/bosai/common/const/area.json"

# 地域リストを取得する関数
def fetch_area_data():
    try:
        response = requests.get(AREA_API_URL)
        if response.status_code == 200:
            return response.json().get("offices", [])  # "offices" のリストを返す
        else:
            print(f"APIエラー: {response.status_code}")
            return []
    except Exception as e:
        print(f"データ取得エラー: {e}")
        return []

# 天気情報を取得する関数
def fetch_weather_data(area_code):
    try:
        WEATHER_API_URL = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        response = requests.get(WEATHER_API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"天気情報APIエラー: {response.status_code}")
            return None
    except Exception as e:
        print(f"天気情報取得エラー: {e}")
        return None

# メインアプリ
def main(page: ft.Page):
    page.title = "天気予報アプリ"
    page.padding = 20
    page.theme_mode = "light"

    # ドロップダウンと天気情報表示用UIコンポーネント
    area_dropdown = ft.Dropdown(label="地域を選択", options=[], width=300)
    weather_cards = ft.Column(spacing=10, expand=True)

    # サイドバーのコンテナ
    sidebar = ft.Container(
        content=ft.Column(
            controls=[ft.Text("地域選択", size=20, weight="bold"), area_dropdown],
            spacing=20,
        ),
        padding=20,
        width=350,
        bgcolor="#f5f5f5",
        border_radius=10,
    )

    # 天気カードの作成関数
    def create_weather_card(title, temp_min, temp_max, weather):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=18, weight="bold"),
                    ft.Row(
                        [
                            ft.Text(f"最低気温: {temp_min}°C", size=14),
                            ft.Text(f"最高気温: {temp_max}°C", size=14),
                        ],
                        spacing=20,
                    ),
                    ft.Text(f"天気: {weather}", size=14),
                ],
                spacing=5,
            ),
            padding=15,
            bgcolor="#e0f7fa",
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.GREY_400),
        )

    # 天気情報取得後の処理
    def load_weather(e):
        area_code = e.control.value
        if not area_code:
            return
        
        weather_data = fetch_weather_data(area_code)
        if weather_data:
            weather_cards.controls.clear()
            forecasts = weather_data[0]["timeSeries"][0]["areas"][0]
            weathers = forecasts["weathers"]  # 天気情報
            temps_min = forecasts["tempsMin"]  # 最低気温
            temps_max = forecasts["tempsMax"]  # 最高気温

            # 取得した天気情報をカードとして追加
            for i in range(len(weathers)):
                weather_cards.controls.append(
                    create_weather_card(
                        f"予報日 {i+1}",
                        temps_min[i] if i < len(temps_min) else "N/A",
                        temps_max[i] if i < len(temps_max) else "N/A",
                        weathers[i],
                    )
                )
            page.update()

    # 地域データの読み込み
    def load_areas():
        areas = fetch_area_data()
        for area in areas:
            if isinstance(area, dict):
                area_dropdown.options.append(ft.dropdown.Option(area["code"], area["name"]))
        page.update()

    # イベントハンドラ
    area_dropdown.on_change = load_weather

    # ページのUIレイアウト
    page.add(
        ft.Row(
            controls=[
                sidebar,  # サイドバー
                ft.Container(  # メインエリア
                    content=ft.Column(
                        controls=[
                            ft.Text("天気予報", size=24, weight="bold"),
                            weather_cards,
                        ],
                        spacing=20,
                    ),
                    expand=True,
                    padding=20,
                ),
            ],
            expand=True,
        )
    )

    # 初期化処理
    load_areas()

# アプリケーション起動
ft.app(target=main)