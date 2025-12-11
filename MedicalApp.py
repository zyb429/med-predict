import sys
import os
import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

# Настройка Qt
os.environ["QT_ENABLE_HDPI_SCALING"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"

def get_base_path():
    """Получает базовый путь к приложению"""
    # Если приложение собрано PyInstaller, получаем путь к временной папке
    if getattr(sys, 'frozen', False):
        # Для onefile сборки - временная папка распаковки
        if hasattr(sys, '_MEIPASS'):
            return sys._MEIPASS
        # Для обычной сборки
        return os.path.dirname(sys.executable)
    # Для разработки
    return os.path.dirname(os.path.abspath(__file__))

def get_resource_path(relative_path):
    """Получает корректный путь к ресурсу для разработки и для собранного приложения"""
    base_path = get_base_path()

    # Для разработки - ресурсы в корневой папке проекта
    if not getattr(sys, 'frozen', False):
        resource_path = os.path.join(base_path, relative_path)
    # Для PyInstaller onefile - ресурсы во временной папке
    elif hasattr(sys, '_MEIPASS'):
        resource_path = os.path.join(sys._MEIPASS, relative_path)
    # Для PyInstaller onedir - ресурсы рядом с исполняемым файлом
    else:
        resource_path = os.path.join(os.path.dirname(sys.executable), relative_path)

    return resource_path

if __name__ == "__main__":
    print("=" * 50)
    print(f"Запуск MedPredict")
    print("=" * 50)

    # Проверяем пути для отладки
    print(f"Python executable: {sys.executable}")
    print(f"Frozen: {getattr(sys, 'frozen', False)}")
    if hasattr(sys, '_MEIPASS'):
        print(f"MEIPASS: {sys._MEIPASS}")

    try:
        # 1. Сначала создаем QApplication
        app = QApplication(sys.argv)

        # 2. Устанавливаем иконку приложения ДО создания главного окна
        icon_paths_to_try = [
            get_resource_path("assets/icons/app.ico"),  # Основной путь для PyInstaller
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/icons/app.ico"),  # Для разработки
            os.path.join(os.path.dirname(sys.executable), "assets/icons/app.ico"),  # Альтернативный путь
            "assets/icons/app.ico",  # Относительный путь
        ]

        icon_loaded = False
        for icon_path in icon_paths_to_try:
            try:
                if os.path.exists(icon_path):
                    app_icon = QIcon(icon_path)
                    if not app_icon.isNull():
                        app.setWindowIcon(app_icon)
                        print(f"✓ Иконка загружена из: {icon_path}")
                        icon_loaded = True
                        break
                    else:
                        print(f"⚠ Иконка не загружена (null) из: {icon_path}")
                else:
                    print(f"⚠ Файл не найден: {icon_path}")
            except Exception as e:
                print(f"⚠ Ошибка загрузки иконки {icon_path}: {e}")

        if not icon_loaded:
            print("✗ Иконка не найдена ни по одному из путей")

        # 3. Настраиваем пути импорта
        base_path = get_base_path()
        sys.path.insert(0, base_path)
        sys.path.insert(0, os.path.join(base_path, 'controllers'))
        sys.path.insert(0, os.path.join(base_path, 'views'))
        sys.path.insert(0, os.path.join(base_path, 'models'))

        # 4. Загружаем шрифты
        from PyQt6.QtGui import QFontDatabase, QFont
        from PyQt6.QtCore import Qt

        # Ищем шрифты в нескольких возможных местах
        font_dirs_to_try = [
            get_resource_path("assets/fonts"),  # Для PyInstaller
            os.path.join(base_path, 'assets', 'fonts'),  # Для разработки
            os.path.join(os.path.dirname(sys.executable), 'assets', 'fonts'),  # Альтернативный
        ]

        font_dir = None
        for fd in font_dirs_to_try:
            if os.path.exists(fd):
                font_dir = fd
                print(f"Папка со шрифтами: {font_dir}")
                break

        if font_dir and os.path.exists(font_dir):
            # Загружаем все .ttf файлы Roboto
            for font_file in os.listdir(font_dir):
                if font_file.endswith('.ttf') and 'Roboto' in font_file:
                    font_path = os.path.join(font_dir, font_file)
                    font_id = QFontDatabase.addApplicationFont(font_path)
                    if font_id != -1:
                        families = QFontDatabase.applicationFontFamilies(font_id)
                        print(f"Загружен: {font_file} -> {families}")

        # 5. Проверяем, какие шрифты Roboto доступны
        all_families = QFontDatabase.families()
        roboto_families = [f for f in all_families if 'roboto' in f.lower()]
        print(f"\nДоступные шрифты Roboto: {roboto_families}")

        # 6. Устанавливаем шрифт приложения
        font_names_to_try = ["Roboto", "Roboto Regular", "Roboto-Regular", "Roboto Regular"]
        selected_font = None

        for font_name in font_names_to_try:
            test_font = QFont(font_name, 10)
            if test_font.family() == font_name or font_name in test_font.family():
                selected_font = test_font
                print(f"✓ Используется шрифт: {font_name}")
                break

        if not selected_font and roboto_families:
            selected_font = QFont(roboto_families[0], 10)
            print(f"✓ Используется первый доступный Roboto: {roboto_families[0]}")
        elif not selected_font:
            selected_font = QFont("Segoe UI", 10)
            print("✗ Roboto не найден, используется Segoe UI")

        app.setFont(selected_font)
        app.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        # 7. Импортируем и создаем главное окно
        from views.main_window import MainWindow
        from controllers.main_controller import MainController

        window = MainWindow()

        # Устанавливаем иконку и для окна тоже
        if icon_loaded:
            window.setWindowIcon(app_icon)
            print("✓ Иконка установлена для главного окна")

        # Устанавливаем заголовок окна (важно для панели задач)
        window.setWindowTitle("MedPredict")

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