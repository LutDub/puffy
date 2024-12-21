import os
import flet as ft
import json
from datetime import datetime

PROGRESS_FILE = "progress.json"

def load_progress():
    try:
        with open(PROGRESS_FILE, "r") as file:
            data = json.load(file)
            return {
                "nickname": data.get("nickname", ""),
                "initial_limit": data.get("initial_limit", 0),
                "current_score": data.get("current_score", 0),
                "progress": data.get("progress", 0),
                "last_update": data.get("last_update", None),
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"nickname": "", "initial_limit": 0, "current_score": 0, "progress": 0, "last_update": None}

def save_progress(nickname, initial_limit, current_score, progress, last_update):
    with open(PROGRESS_FILE, "w") as file:
        json.dump({
            "nickname": nickname,
            "initial_limit": initial_limit,
            "current_score": current_score,
            "progress": progress,
            "last_update": last_update,
        }, file)

async def main(page: ft.Page):
    page.title = "Puffy"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    progress_data = load_progress()
    nickname = progress_data["nickname"]
    initial_limit = progress_data["initial_limit"]
    current_score = progress_data["current_score"]
    progress = progress_data["progress"]
    last_update = progress_data["last_update"]

    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"Текущая дата: {current_date}, Последнее обновление: {last_update}")

    if last_update is None:
        last_update = current_date
        save_progress(nickname, initial_limit, current_score, progress, last_update)

    if last_update != current_date:
        print(f"Смена дня обнаружена. Обновляем очки...")
        days_diff = (datetime.now() - datetime.strptime(last_update, "%Y-%m-%d")).days
        old_score = current_score
        for _ in range(days_diff):
            current_score *= 0.95  # Уменьшаем на 5% каждый день
        print(f"Новый текущий счет: {current_score}")

        score_difference = int(old_score - current_score)

        last_update = current_date
        save_progress(nickname, initial_limit, current_score, progress, last_update)

        welcome_message = f"Привет, с новым днем! Лимит нажатий изменился на {score_difference} (с {int(old_score)} до {int(current_score)})."

        snack_bar = ft.SnackBar(content=ft.Text(welcome_message), open=True)
        page.overlay.append(snack_bar)
        page.update()

    def register_user(event):
        nonlocal nickname, initial_limit, current_score, progress, last_update
        nickname = nickname_input.value.strip()
        try:
            initial_limit = int(limit_input.value.strip())
        except ValueError:
            initial_limit = 0

        if nickname and initial_limit > 0:
            current_score = initial_limit
            progress = 0
            last_update = datetime.now().strftime("%Y-%m-%d")
            save_progress(nickname, initial_limit, current_score, progress, last_update)
            registration_modal.open = False
            page.update()

    def decrease_score(event):
        nonlocal current_score, progress
        if current_score > 0:
            current_score = int(current_score) - 1  # Округляем до целого
            progress = max(0, progress + 1 / initial_limit)
            save_progress(nickname, initial_limit, current_score, progress, last_update)
            update_ui()
        else:
            snack_bar.open = True
            page.update()

    def update_ui():
        score_text.value = f"Осталось: {int(current_score)}"  # Округляем до целого
        progress_bar.value = progress
        page.update()

    def delete_progress(event):
        nonlocal nickname, initial_limit, current_score, progress, last_update
        nickname, initial_limit, current_score, progress, last_update = "", 0, 0, 0, None
        save_progress(nickname, initial_limit, current_score, progress, last_update)
        page.overlay.append(ft.SnackBar(ft.Text("Прогресс удален"), open=True))
        page.update()

    nickname_input = ft.TextField(label="Введите никнейм", width=300)
    limit_input = ft.TextField(label="Введите число (до 1000)", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    register_button = ft.ElevatedButton("Зарегистрироваться", on_click=register_user)

    registration_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Регистрация"),
        content=ft.Column([nickname_input, limit_input, register_button], spacing=20),
    )

    score_text = ft.Text(f"Осталось: {int(current_score)}", size=30, color="#ffffff")
    progress_bar = ft.ProgressBar(value=progress, width=300, bgcolor="#bf6524", color="#ff8b1f")

    image_path = "C:/Users/shart/Documents/puffy/assets/smoke.png"  # Путь к изображению

    # Проверим, существует ли файл изображения
    if os.path.exists(image_path):
        print(f"Изображение найдено по пути: {image_path}")
    else:
        print(f"Изображение не найдено по пути: {image_path}")

    # Замена кнопки на изображение с использованием GestureDetector
    click_image = ft.GestureDetector(
        on_tap=decrease_score,  # Привязываем обработчик кликов
        content=ft.Image(
            src=image_path,  # Указание пути к изображению в папке assets
            width=200,
            height=200
        )
    )

    delete_button = ft.ElevatedButton("Удалить прогресс", on_click=delete_progress)

    if not nickname or initial_limit <= 0:
        page.dialog = registration_modal
        registration_modal.open = True

    page.add(
        ft.Row([ft.Text(f"Никнейм: {nickname}", size=20, color="#ff8b1f")], alignment=ft.MainAxisAlignment.START),
        ft.Column([score_text, progress_bar, click_image, delete_button], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
    )

    update_ui()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
