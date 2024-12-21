import flet as ft
import asyncio
import json
import os
from datetime import datetime

PROGRESS_FILE = "progress.json"  # Файл для сохранения прогресса

def load_progress():
    try:
        with open(PROGRESS_FILE, "r") as file:
            data = json.load(file)
            return data.get("nickname", ""), data.get("date", ""), data.get("score", 0), data.get("progress", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return "", "", 0, 0

def save_progress(nickname, date, score, progress):
    with open(PROGRESS_FILE, "w") as file:
        json.dump({
            "nickname": nickname,
            "date": date,
            "score": score,
            "progress": progress
        }, file)

def delete_progress():
    try:
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
    except Exception as e:
        print(f"Error deleting file: {e}")

async def main(page: ft.Page):
    page.title = "Puffy"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#141221"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Загрузка данных из файла
    nickname, saved_date, saved_score, saved_progress = load_progress()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Проверка, является ли сегодня новым днем
    is_new_day = current_date != saved_date
    score_direction = 1 if is_new_day else -1  # Если новый день, увеличиваем, иначе уменьшаем
    initial_score = 0 if is_new_day else saved_score

    async def score_up(event: ft.ContainerTapEvent):
        nonlocal score_direction
        score.data += score_direction
        score.value = str(score.data)

        image.scale = 0.95
        progress_bar.value = max(0, progress_bar.value + (1 / 100) * score_direction)

        # Показываем SnackBar, если счет достигает 100
        if score_direction == 1 and score.data % 100 == 0:
            snack_bar = ft.SnackBar(
                content=ft.Container(
                    content=ft.Text(
                        value="Лимит исчерпан",
                        size=20,
                        color="#ff8b1f",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    bgcolor="#25223a",
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                ),
                bgcolor="#141221",
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            progress_bar.value = 0

        # Сохраняем прогресс в файл
        save_progress(nickname, current_date, score.data, progress_bar.value)
        page.update()

        await reset_image()

    async def reset_image():
        await asyncio.sleep(0.1)
        image.scale = 1
        score_counter.opacity = 0
        page.update()

    # Стартовый экран (если нет данных в файле)
    if not nickname:
        def on_submit(event):
            nonlocal nickname, saved_date
            nickname = nickname_input.value
            saved_date = current_date  # Сохраняем дату регистрации
            save_progress(nickname, saved_date, 0, 0)
            show_main_program(page)

        nickname_input = ft.TextField(label="Введите никнейм", autofocus=True)
        submit_button = ft.ElevatedButton("Начать", on_click=on_submit)

        page.add(nickname_input, submit_button)
    else:
        # Переход к основной части программы
        show_main_program(page)

    # Кнопка для удаления прогресса
    def on_delete_progress(event):
        delete_progress()
        page.controls.clear()
        page.add(ft.Text("Прогресс удален. Начните с новым никнеймом!"))
        page.update()

    delete_button = ft.ElevatedButton("Удалить прогресс", on_click=on_delete_progress)
    page.add(delete_button)

    page.update()

def show_main_program(page):
    # Извлечение данных из сохраненных переменных
    nickname, saved_date, saved_score, saved_progress = load_progress()
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Проверка, новый ли день
    is_new_day = current_date != saved_date
    print(is_new_day)
    if is_new_day:
        print("nov")
        score_direction = -1
    else:
        print("star")
        score_direction = 1
    initial_score = 0 if is_new_day else saved_score

    # Создание элементов интерфейса
    score = ft.Text(value=str(initial_score), size=100, data=initial_score)
    score_counter = ft.Text(
        size=50,
        animate_opacity=ft.Animation(duration=600, curve=ft.AnimationCurve.BOUNCE_IN),
    )
    image = ft.Image(
        src="smoke.png",
        fit=ft.ImageFit.CONTAIN,
        animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE),
    )
    progress_bar = ft.ProgressBar(
        value=saved_progress if not is_new_day else 0,
        width=page.width - 100,
        height=10,
        color="#ff8b1f",
        bgcolor='#bf6524',
    )

    async def score_up(event: ft.ContainerTapEvent):
        nonlocal score_direction
        score.data += score_direction
        score.value = str(score.data)

        image.scale = 0.95
        progress_bar.value = max(0, progress_bar.value + (1 / 100) * score_direction)

        # Показываем SnackBar, если счет достигает 100
        if score_direction == 1 and score.data % 100 == 0:
            snack_bar = ft.SnackBar(
                content=ft.Container(
                    content=ft.Text(
                        value="Лимит исчерпан",
                        size=20,
                        color="#ff8b1f",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    bgcolor="#25223a",
                    border_radius=ft.BorderRadius(10, 10, 10, 10),
                ),
                bgcolor="#141221",
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            progress_bar.value = 0

        # Сохраняем прогресс в файл
        save_progress(nickname, current_date, score.data, progress_bar.value)
        page.update()

        await reset_image()

    async def reset_image():
        await asyncio.sleep(0.1)
        image.scale = 1
        score_counter.opacity = 0
        page.update()

    # Добавление элементов на страницу
    page.controls.clear()

    # Добавляем элементы интерфейса
    page.add(
        score,
        ft.Container(
            content=ft.Stack(controls=[image, score_counter]),
            on_click=score_up,
            margin=ft.Margin(0, 0, 0, 30),
        ),
        ft.Container(
            content=progress_bar,
            border_radius=ft.BorderRadius(10, 10, 10, 10),
        ),
    )

    page.update()

if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8000)
