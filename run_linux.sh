#!/bin/bash
echo "========================================"
echo " Запуск MedPredict - Диагностика эндометриоза"
echo "========================================"
echo

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    echo
    echo "Установите Python 3.8+:"
    echo "sudo apt update"
    echo "sudo apt install python3 python3-pip"
    exit 1
fi

# Проверка версии Python
python3 -c "import sys; sys.exit(0) if sys.version_info >= (3, 8) else sys.exit(1)"
if [ $? -ne 0 ]; then
    echo "❌ Требуется Python 3.8 или выше!"
    echo
    python3 --version
    exit 1
fi

echo "✓ Python обнаружен"
python3 --version

echo
echo "Установка зависимостей..."
pip3 install -r requirements.txt

echo
echo "========================================"
echo " Запуск приложения..."
echo "========================================"
echo

python3 MedicalApp.py

echo
echo "========================================"
echo " Приложение завершено"
echo "========================================"