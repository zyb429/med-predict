# build.py
# Для сборки в .exe выполнить python .\build.py
import PyInstaller.__main__
import shutil
import os

# Очистка предыдущих сборок
if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

# Параметры сборки
PyInstaller.__main__.run([
    'MedicalApp.py',                # Главный файл приложения
    #'--onefile',
    # Один исполняемый файл
    '--onedir',
    '--windowed',             # Для GUI приложений
    '--icon=assets/icons/app.ico',         # Иконка приложения
    '--name=MedPredict',      # Имя приложения
    '--add-data=assets;assets',       # Добавляем папку с моделями
    '--add-data=models;models',       # Добавляем папку с моделями
    '--add-data=views;views',         # Добавляем папку с view
    '--noconsole',  # Убираем консоль для чистого GUI
    '--clean'                 # Очистка перед сборкой
])
