import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt

# Создаем приложение
app = QApplication(sys.argv)

# Загружаем шрифты
base_dir = os.path.dirname(os.path.abspath(__file__))
if "tests" in base_dir:
    base_dir = os.path.dirname(base_dir)  # Поднимаемся на уровень выше

font_dir = os.path.join(base_dir, 'assets', 'fonts')

print(f"Базовая директория: {base_dir}")
print(f"Директория шрифтов: {font_dir}")

if os.path.exists(font_dir):
    # Загружаем основные шрифты Roboto
    for font_file in ['Roboto-Regular.ttf', 'Roboto-Bold.ttf']:
        font_path = os.path.join(font_dir, font_file)
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"✓ {font_file} загружен -> {families}")

# Проверяем доступные шрифты
all_families = QFontDatabase.families()
print(f"\nВсего шрифтов: {len(all_families)}")
roboto_families = [f for f in all_families if 'roboto' in f.lower()]
print(f"Шрифты Roboto: {roboto_families}")

# Создаем тестовое окно
window = QWidget()
layout = QVBoxLayout(window)

# Тест 1: Пробуем разные варианты Roboto
if roboto_families:
    for i, font_name in enumerate(roboto_families[:3]):  # Первые 3 варианта
        label = QLabel(f"Тест {i+1}: {font_name} - размер 12")
        font = QFont(font_name, 12)
        label.setFont(font)
        layout.addWidget(label)
else:
    label = QLabel("Шрифты Roboto не найдены")
    layout.addWidget(label)

# Тест 2: Просто "Roboto"
label_simple = QLabel("Просто 'Roboto' размер 14")
font_simple = QFont("Roboto", 14)
label_simple.setFont(font_simple)
layout.addWidget(label_simple)

# Тест 3: Segoe UI для сравнения
label_segoe = QLabel("Segoe UI для сравнения")
font_segoe = QFont("Segoe UI", 12)
label_segoe.setFont(font_segoe)
layout.addWidget(label_segoe)

window.setWindowTitle("Тест шрифтов Roboto")
window.resize(600, 300)
window.show()

print("\nЕсли видите текст разными шрифтами - шрифты работают!")
sys.exit(app.exec())