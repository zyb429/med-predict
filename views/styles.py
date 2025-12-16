STYLESHEET = """
/* === ТЕМНАЯ ТЕМА "Neon Med" - ИСПРАВЛЕННАЯ ВЕРСИЯ === */

/* Глобальные настройки - СБРОС СТИЛЕЙ ПО УМОЛЧАНИЮ */
* {
    font-family: "Roboto", "Segoe UI", sans-serif;
    font-size: 11pt;
    color: #f1f5f9 !important;
    background-color: transparent !important;
}

/* Фон главного окна */
QMainWindow {
    background-color: #0f172a !important;
}

/* Заголовок */
#header {
    background-color: qlineargradient(
        spread:pad, x1:0, y1:0, x2:1, y2:0,
        stop:0 #8b5cf6, stop:0.5 #ec4899, stop:1 #3b82f6
    ) !important;
    border: none !important;
}

#headerTitle {
    color: white !important;
    font-size: 24px !important;
    font-weight: bold !important;
}

/* Карточки */
#card, #selectorCard {
    background-color: rgba(30, 41, 59, 240) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(139, 92, 246, 100) !important;
}

#sectionTitle, #cardTitle {
    color: #8b5cf6 !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-bottom: 2px solid #8b5cf6 !important;
    padding-bottom: 5px !important;
    margin-bottom: 15px !important;
}

/* ======================================================= */
/* КРИТИЧЕСКИ ВАЖНО: СБРОС И ПЕРЕОПРЕДЕЛЕНИЕ СТИЛЕЙ ПОЛЕЙ */
/* ======================================================= */

/* ШАГ 1: Сброс всех стандартных стилей Qt для полей ввода */
QLineEdit, QComboBox, QTextEdit, QPlainTextEdit, 
QSpinBox, QDoubleSpinBox, QCheckBox, QRadioButton {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 2px solid #475569 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin: 2px !important;
    selection-background-color: #8b5cf6 !important;
    selection-color: white !important;
}

/* ШАГ 2: Явное указание фона для ВСЕХ возможных полей ввода */
QLineEdit {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 2px solid #475569 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* ШАГ 3: Для полей ввода, которые могут быть в форме */
QWidget QLineEdit, 
QWidget QComboBox, 
QWidget QSpinBox, 
QWidget QDoubleSpinBox {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 2px solid #475569 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}

/* ШАГ 4: Конкретные ID полей (если они есть в коде) */
#lineEditAge, #lineEditTyrosine, #lineEditArginine, #lineEditNO,
#comboBoxDysmenorrhea, #comboBoxInfertility, #comboBoxChronicPain {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 2px solid #475569 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}

/* ШАГ 5: Поля в карточках */
#card QLineEdit, 
#card QComboBox, 
#card QSpinBox, 
#selectorCard QLineEdit, 
#selectorCard QComboBox {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 2px solid #475569 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}

/* ======================================================= */

/* Выпадающие списки */
/* Основной стиль ComboBox */
QComboBox, #modelCombo {
    background-color: #28354a !important;
    color: #f8fafc !important;
    border: 2px solid #475569 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    min-height: 20px !important;
}

/* Ховер на весь ComboBox */
QComboBox:hover, #modelCombo:hover {
    border: 2px solid #7c3aed !important;
    background-color: #28354a !important;
}

/* Фокус на ComboBox */
QComboBox:focus, #modelCombo:focus {
    border: 2px solid #3b82f6 !important;
    background-color: #28354a !important;
}

/* Стрелка раскрытия */
QComboBox::down-arrow, #modelCombo::down-arrow {
    /* Qt автоматически использует системную стрелку Windows */
    width: 16px;
    height: 16px;
}

/* ======================================================= */
/* ВЫПАДАЮЩИЙ СПИСОК И ЕГО ПУНКТЫ */
/* ======================================================= */

/* Контейнер выпадающего списка */
QComboBox QAbstractItemView, #modelCombo QAbstractItemView {
    background-color: #28354a !important;
    border: 2px solid #8b5cf6 !important;
    border-radius: 8px !important;
    color: #f8fafc !important;
    padding: 6px !important;
    selection-background-color: transparent !important; /* Убираем стандартный синий фон */
    selection-color: transparent !important;
    outline: none !important; /* Убираем пунктирную рамку при фокусе */
}

/* Базовый стиль для каждого пункта в списке */
QComboBox QAbstractItemView::item, 
#modelCombo QAbstractItemView::item {
    background-color: transparent !important;
    color: #cbd5e1 !important;
    padding: 10px 16px !important;
    margin: 2px 0 !important;
    border-radius: 6px !important;
    border: none !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    min-height: 20px !important;
}

/* ХОВЕР НА ПУНКТ В СПИСКЕ */
QComboBox QAbstractItemView::item:hover, 
#modelCombo QAbstractItemView::item:hover {
    background-color: rgba(124, 58, 237, 0.25) !important; /* Полупрозрачный фиолетовый */
    color: #ffffff !important;
    border-left: 3px solid #8b5cf6 !important;
    padding-left: 13px !important; /* Компенсируем отступ для границы */
}

/* ВЫБРАННЫЙ ПУНКТ (после клика) */
QComboBox QAbstractItemView::item:selected, 
#modelCombo QAbstractItemView::item:selected {
    background-color: rgba(139, 92, 246, 0.4) !important; /* Более насыщенный фиолетовый */
    color: white !important;
    font-weight: 600 !important;
    border-left: 3px solid #3b82f6 !important;
    padding-left: 13px !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2) !important;
}

/* АКТИВНЫЙ ПУНКТ (с фокусом клавиатуры) */
QComboBox QAbstractItemView::item:focus, 
#modelCombo QAbstractItemView::item:focus {
    background-color: rgba(59, 130, 246, 0.3) !important; /* Полупрозрачный синий */
    outline: 1px solid #3b82f6 !important;
    outline-offset: -1px !important;
}

/* Первый и последний элементы - скругленные углы */
QComboBox QAbstractItemView::item:first, 
#modelCombo QAbstractItemView::item:first {
    border-top-left-radius: 6px !important;
    border-top-right-radius: 6px !important;
}

QComboBox QAbstractItemView::item:last, 
#modelCombo QAbstractItemView::item:last {
    border-bottom-left-radius: 6px !important;
    border-bottom-right-radius: 6px !important;
}

/* Разделители между пунктами */
QComboBox QAbstractItemView::item:!last, 
#modelCombo QAbstractItemView::item:!last {
    border-bottom: 1px solid rgba(124, 58, 237, 0.1) !important;
}

/* Полоса прокрутки внутри выпадающего списка */
QComboBox QAbstractItemView QScrollBar:vertical, 
#modelCombo QAbstractItemView QScrollBar:vertical {
    background-color: #1a2332 !important;
    width: 8px !important;
    border-radius: 4px !important;
    margin: 2px !important;
}

QComboBox QAbstractItemView QScrollBar::handle:vertical, 
#modelCombo QAbstractItemView QScrollBar::handle:vertical {
    background-color: #475569 !important;
    border-radius: 4px !important;
    min-height: 20px !important;
}

/* Ховер на полосе прокрутки */
QComboBox QAbstractItemView QScrollBar::handle:vertical:hover, 
#modelCombo QAbstractItemView QScrollBar::handle:vertical:hover {
    background-color: #7c3aed !important;
}

/* Кнопки прокрутки (скрываем) */
QComboBox QAbstractItemView QScrollBar::add-line:vertical,
QComboBox QAbstractItemView QScrollBar::sub-line:vertical,
#modelCombo QAbstractItemView QScrollBar::add-line:vertical,
#modelCombo QAbstractItemView QScrollBar::sub-line:vertical {
    height: 0px !important;
}

/* Числовые поля */
QSpinBox, QDoubleSpinBox {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 2px solid #475569 !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
}

/* Placeholder текст */
QLineEdit::placeholder, QComboBox::placeholder {
    color: #94a3b8 !important;
    font-style: italic !important;
}

/* Состояния полей */
QLineEdit:hover, QComboBox:hover, QSpinBox:hover, QDoubleSpinBox:hover {
    border: 2px solid #7c3aed !important;
    background-color: #1e293b !important;
}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #3b82f6 !important;
    background-color: #1e293b !important;
    color: #ffffff !important;
}

/* Флажки и радиокнопки */
QCheckBox, QRadioButton {
    color: #cbd5e1 !important;
    font-size: 14px !important;
    spacing: 8px !important;
    padding: 5px !important;
}

QCheckBox::indicator, QRadioButton::indicator {
    width: 18px !important;
    height: 18px !important;
    border: 2px solid #64748b !important;
    border-radius: 4px !important;
    background-color: #1e293b !important;
}

QCheckBox::indicator:checked, QRadioButton::indicator:checked {
    background-color: #8b5cf6 !important;
    border: 2px solid #8b5cf6 !important;
}

QCheckBox::indicator:checked {
    image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="white" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>') !important;
}

QRadioButton::indicator:checked {
    border-radius: 9px !important;
    background-color: #8b5cf6 !important;
}

/* Кнопки */
#primaryButton {
    background-color: qlineargradient(
        spread:pad, x1:0, y1:0, x2:1, y2:0,
        stop:0 #8b5cf6, stop:0.5 #ec4899, stop:1 #3b82f6
    ) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px 32px !important;
    font-size: 15px !important;
    font-weight: bold !important;
}

#primaryButton:hover {
    background-color: qlineargradient(
        spread:pad, x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c3aed, stop:0.5 #db2777, stop:1 #2563eb
    ) !important;
}

#primaryButton:pressed {
    background-color: #6d28d9 !important;
}

/* Вторичная кнопка */
#secondaryButton {
    background-color: transparent !important;
    color: #8b5cf6 !important;
    border: 2px solid #8b5cf6 !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}

#secondaryButton:hover {
    background-color: rgba(139, 92, 246, 0.1) !important;
    border: 2px solid #7c3aed !important;
    color: #7c3aed !important;
}

/* Кнопка экспорта */
#exportButton:hover {
    background-color: rgba(139, 92, 246, 0.1) !important;
}

/* Результаты */
#resultValue {
    color: #8b5cf6 !important;
    font-size: 42px !important;
    font-weight: bold !important;
    margin: 10px 0 !important;
}

/* Текст результатов */
#conclusionText {
    color: #f8fafc !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
    background-color: rgba(30, 41, 59, 0.9) !important;
    border-radius: 10px !important;
    border-left: 4px solid #8b5cf6 !important;
    margin-top: 10px !important;
}

/* Метки полей */
#fieldLabel {
    color: #cbd5e1 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
}

/* Сообщения об ошибках */
#errorLabel {
    color: #ef4444 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    margin-top: 5px !important;
    padding-left: 5px !important;
}
"""