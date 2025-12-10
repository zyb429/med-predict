@echo off
chcp 65001 >nul
echo ========================================
echo  Запуск MedPredict - Диагностика эндометриоза
echo ========================================
echo.

REM Проверка Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python не найден!
    echo.
    echo Установите Python 3.8+:
    echo 1. Перейдите на https://python.org
    echo 2. Скачайте установщик
    echo 3. Установите Python
    echo 4. Обязательно отметьте "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Проверка версии Python
python -c "import sys; exit(0) if sys.version_info >= (3, 8) else exit(1)" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Требуется Python 3.8 или выше!
    echo.
    python --version
    pause
    exit /b 1
)

echo ✓ Python обнаружен
python --version

echo.
echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo ========================================
echo  Запуск приложения...
echo ========================================
echo.

python MedicalApp.py

echo.
echo ========================================
echo  Приложение завершено
echo ========================================
pause