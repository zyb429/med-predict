import sys
import os

# Настройка Qt
os.environ["QT_ENABLE_HDPI_SCALING"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"

def get_base_path():
    """Получает базовый путь к приложению"""
    return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    print("=" * 50)
    print(f"Запуск MedPredict")
    print("=" * 50)

    try:
        # 1. Сначала создаем QApplication
        from PyQt6.QtWidgets import QApplication
        app = QApplication(sys.argv)

        # 2. Настраиваем пути импорта
        base_path = get_base_path()
        sys.path.insert(0, base_path)
        sys.path.insert(0, os.path.join(base_path, 'controllers'))
        sys.path.insert(0, os.path.join(base_path, 'views'))
        sys.path.insert(0, os.path.join(base_path, 'models'))

        # 3. Загружаем шрифты ДО импорта других модулей
        from PyQt6.QtGui import QFontDatabase, QIcon, QFont
        from PyQt6.QtCore import Qt

        font_dir = os.path.join(base_path, 'assets', 'fonts')
        print(f"Папка со шрифтами: {font_dir}")

        if os.path.exists(font_dir):
            # Загружаем все .ttf файлы Roboto
            for font_file in os.listdir(font_dir):
                if font_file.endswith('.ttf') and 'Roboto' in font_file:
                    font_path = os.path.join(font_dir, font_file)
                    font_id = QFontDatabase.addApplicationFont(font_path)
                    if font_id != -1:
                        families = QFontDatabase.applicationFontFamilies(font_id)
                        print(f"Загружен: {font_file} -> {families}")

        # 4. Проверяем, какие шрифты Roboto доступны
        all_families = QFontDatabase.families()
        roboto_families = [f for f in all_families if 'roboto' in f.lower()]
        print(f"\nДоступные шрифты Roboto: {roboto_families}")

        # 5. Устанавливаем шрифт приложения
        # Пробуем разные варианты имен
        font_names_to_try = ["Roboto", "Roboto Regular", "Roboto-Regular", "Roboto Regular"]
        selected_font = None

        for font_name in font_names_to_try:
            test_font = QFont(font_name, 10)
            # Проверяем, установлен ли шрифт (не используем exactMatch)
            if test_font.family() == font_name or font_name in test_font.family():
                selected_font = test_font
                print(f"✓ Используется шрифт: {font_name}")
                break

        if not selected_font and roboto_families:
            # Используем первый найденный Roboto
            selected_font = QFont(roboto_families[0], 10)
            print(f"✓ Используется первый доступный Roboto: {roboto_families[0]}")
        elif not selected_font:
            selected_font = QFont("Segoe UI", 10)
            print("✗ Roboto не найден, используется Segoe UI")

        app.setFont(selected_font)

        # # 6. Иконка
        # icon_path = os.path.join(base_path, "icon.ico")
        # if os.path.exists(icon_path):
        #     app.setWindowIcon(QIcon(icon_path))
        #     print(f"✓ Иконка загружена")
        # else:
        #     print(f"✗ Иконка не найдена")

        app.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # 7. Импортируем и создаем главное окно
        from views.main_window import MainWindow
        from controllers.main_controller import MainController

        window = MainWindow()
        controller = MainController(window, app)
        window.show()

        print("\n" + "=" * 50)
        print("Приложение запущено успешно!")
        print("=" * 50)

        sys.exit(app.exec())

    except Exception as e:
        print(f"\n✗ Ошибка запуска: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)