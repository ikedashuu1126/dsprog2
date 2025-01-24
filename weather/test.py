import sqlite3
import flet as ft

def main(page: ft.Page):
    # データベース接続と取得
    conn = sqlite3.connect("weather_forecast.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, weather, temp_min, temp_max FROM weather_forecast ORDER BY date")
    weather_records = cursor.fetchall()
    conn.close()

    # UIレイアウト
    weather_cards = []
    for record in weather_records:
        date, weather, temp_min, temp_max = record
        weather_cards.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"日付: {date}"),
                    ft.Text(f"天気: {weather}"),
                    ft.Text(f"最低気温: {temp_min}℃"),
                    ft.Text(f"最高気温: {temp_max}℃")
                ]),
                padding=10,
                border_radius=5,
                bgcolor=ft.colors.AMBER_100
            )
        )
    
    page.add(ft.Column(weather_cards))
    page.update()

ft.app(target=main)