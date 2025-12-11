from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QComboBox,
                             QFrame, QScrollArea, QMessageBox, QFileDialog,
                             QSpacerItem, QSizePolicy, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from widgets import (Card, ModernLineEdit, AnimatedButton,
                     ResultCard, clear_layout)
from styles import STYLESHEET


class MainWindow(QMainWindow):
    # Signals for Controller
    model_changed = pyqtSignal(str)
    calculate_requested = pyqtSignal()
    clear_requested = pyqtSignal()
    export_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MedPredict")
        self.setMinimumSize(1200, 800)
        self.apply_styles()

        # Widgets references
        self.model_combo = None
        self.doctor_name_entry = None
        self.description_label = None
        self.input_layout = None
        self.input_container = None

        self.entries = {}
        self.error_labels = {}

        self.z_card = None
        self.p_card = None
        self.conclusion_label = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.create_header(main_layout)
        self.create_grid_content(main_layout)

    def create_header(self, parent_layout):
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(80)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)
        title = QLabel("🏥 Аминокислотный предиктор перинатальных осложнений")
        title.setObjectName("headerTitle")
        layout.addWidget(title)
        parent_layout.addWidget(header)

    def create_grid_content(self, parent_layout):
        """Создаёт сетку 2x3: Модель | ФИО врача
                                    Ввод   | Результаты
                                    Кнопки | Результаты"""
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(20, 10, 20, 20)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(15)

        model_card = self.create_model_card()
        doctor_card = self.create_doctor_card()

        grid_layout.addWidget(model_card, 0, 0)
        grid_layout.addWidget(doctor_card, 0, 1)

        input_card = self.create_input_card()
        results_card = self.create_results_card()

        grid_layout.addWidget(input_card, 1, 0)
        grid_layout.addWidget(results_card, 1, 1, 2, 1)

        buttons_widget = self.create_buttons_widget()
        grid_layout.addWidget(buttons_widget, 2, 0)

        grid_layout.setColumnStretch(0, 2)
        grid_layout.setColumnStretch(1, 1)

        # Настройка пропорций строк
        grid_layout.setRowStretch(0, 0)
        grid_layout.setRowStretch(1, 3)
        grid_layout.setRowStretch(2, 0)

        parent_layout.addWidget(grid_widget)

    def create_model_card(self):
        """Карточка выбора модели с описанием"""
        model_card = Card()
        model_card.setObjectName("selectorCard")
        model_layout = QVBoxLayout(model_card)
        model_layout.setContentsMargins(25, 20, 25, 20)
        model_layout.setSpacing(8)

        model_label = QLabel("Выберите модель диагностики:")
        model_label.setObjectName("sectionTitle")
        model_layout.addWidget(model_label)

        self.model_combo = QComboBox()
        self.model_combo.setObjectName("modelCombo")
        self.model_combo.setMinimumHeight(50)
        self.model_combo.currentIndexChanged.connect(
            lambda: self.model_changed.emit(self.model_combo.currentData())
        )
        model_layout.addWidget(self.model_combo)

        model_layout.addSpacing(6)

        self.description_label = QLabel()
        self.description_label.setObjectName("descriptionLabel")
        self.description_label.setWordWrap(True)
        self.description_label.setContentsMargins(0, 0, 0, 0)
        model_layout.addWidget(self.description_label)

        return model_card

    def create_doctor_card(self):
        """Карточка ФИО врача"""
        doctor_card = Card()
        doctor_card.setObjectName("selectorCard")
        doctor_layout = QVBoxLayout(doctor_card)
        doctor_layout.setContentsMargins(25, 20, 25, 20)
        doctor_layout.setSpacing(8)

        doctor_label = QLabel("👨‍⚕️ ФИО врача:")
        doctor_label.setObjectName("sectionTitle")
        doctor_layout.addWidget(doctor_label)

        self.doctor_name_entry = ModernLineEdit()
        self.doctor_name_entry.setPlaceholderText("Введите ФИО врача")
        self.doctor_name_entry.setMinimumHeight(50)
        doctor_layout.addWidget(self.doctor_name_entry)

        doctor_layout.addStretch()

        return doctor_card

    def create_input_card(self):
        """Карточка ввода параметров"""
        card = Card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(10)

        title = QLabel("📝 Ввод параметров")
        title.setObjectName("cardTitle")
        card_layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setObjectName("inputsScrollArea")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")

        self.input_container = QWidget()
        self.input_container.setStyleSheet("QWidget { background: #1e293b; }")
        self.input_layout = QVBoxLayout(self.input_container)
        self.input_layout.setSpacing(20)
        self.input_layout.setContentsMargins(5, 10, 5, 10)
        scroll.setWidget(self.input_container)

        card_layout.addWidget(scroll, 1)

        return card

    def create_buttons_widget(self):
        """Виджет с кнопками"""
        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        first_row = QHBoxLayout()
        first_row.setSpacing(15)

        calc_btn = AnimatedButton("🔍 Выполнить расчет", primary=True)
        calc_btn.clicked.connect(lambda: self.calculate_requested.emit())
        first_row.addWidget(calc_btn)

        clear_btn = AnimatedButton("🔄 Очистить поля")
        clear_btn.clicked.connect(lambda: self.clear_requested.emit())
        first_row.addWidget(clear_btn)
        button_layout.addLayout(first_row)

        export_btn = AnimatedButton("📄 Экспорт в PDF")
        export_btn.setObjectName("exportButton")
        export_btn.clicked.connect(lambda: self.export_requested.emit())
        button_layout.addWidget(export_btn)

        return button_widget

    def create_results_card(self):
        """Карточка результатов"""
        card = Card()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(20)

        title = QLabel("📊 Результаты диагностики")
        title.setObjectName("cardTitle")
        card_layout.addWidget(title)

        self.z_card = ResultCard("z-значение")
        card_layout.addWidget(self.z_card)

        self.p_card = ResultCard("Вероятность (p)")
        card_layout.addWidget(self.p_card)

        conclusion_card = Card()
        conclusion_layout = QVBoxLayout(conclusion_card)
        conclusion_layout.setContentsMargins(20, 20, 20, 20)
        conclusion_layout.setSpacing(10)

        conclusion_title = QLabel("Заключение:")
        conclusion_title.setObjectName("conclusionTitle")
        conclusion_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        conclusion_layout.addWidget(conclusion_title)

        self.conclusion_label = QLabel("-")
        self.conclusion_label.setObjectName("conclusionText")
        self.conclusion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conclusion_label.setWordWrap(True)
        conclusion_layout.addWidget(self.conclusion_label)

        card_layout.addWidget(conclusion_card)
        card_layout.addStretch()

        return card

    # === Data & UI helpers ===

    def set_model_options(self, models):
        self.model_combo.clear()
        for key, config in models.items():
            self.model_combo.addItem(config.name, key)

    def set_model_description(self, text):
        self.description_label.setText(f"📋 {text}")

    def create_input_fields(self, fields):
        self.clear_input_fields()

        for label, key in fields:
            field_widget = QWidget()
            field_widget.setStyleSheet("QWidget { background: transparent; }")
            field_layout = QVBoxLayout(field_widget)
            field_layout.setContentsMargins(0, 0, 0, 0)
            field_layout.setSpacing(6)

            field_label = QLabel(label)
            field_label.setObjectName("fieldLabel")
            field_layout.addWidget(field_label)

            entry = ModernLineEdit()
            entry.setPlaceholderText("Введите значение")
            entry.returnPressed.connect(lambda: self.calculate_requested.emit())
            entry.textChanged.connect(
                lambda txt, k=key: self._on_text_changed(k, txt)
            )
            field_layout.addWidget(entry)

            err = QLabel("")
            err.setObjectName("errorLabel")
            err.setVisible(False)
            field_layout.addWidget(err)

            self.entries[key] = entry
            self.error_labels[key] = err

            self.input_layout.addWidget(field_widget)

        self.input_layout.addStretch()

        if self.entries:
            first_entry = list(self.entries.values())[0]
            QTimer.singleShot(100, first_entry.setFocus)

    def _on_text_changed(self, key: str, text: str):
        pass

    def set_field_error(self, key: str, message: str = ""):
        if key in self.entries:
            self.entries[key].set_error(bool(message))
        if key in self.error_labels:
            lbl = self.error_labels[key]
            lbl.setText(message)
            lbl.setVisible(bool(message))

    def clear_field_errors(self):
        for key in self.entries:
            self.set_field_error(key, "")

    def clear_input_fields(self):
        clear_layout(self.input_layout)
        self.entries.clear()
        self.error_labels.clear()

    def get_input_values(self):
        return {k: v.text().strip() for k, v in self.entries.items()}

    def get_doctor_name(self):
        return self.doctor_name_entry.text().strip()

    def display_result(self, result):
        color_map = {'high': '#e74c3c', 'low': '#27ae60'}
        text_color = color_map.get(result.risk_level, '#2c3e50')

        self.z_card.set_value(f"{result.z_value:.4f}", "#4a90e2")
        self.p_card.set_value(f"{result.p_value:.4f} ({result.p_value*100:.2f}%)", "#4a90e2")
        self.conclusion_label.setText(result.conclusion)
        self.conclusion_label.setStyleSheet(
            f"color: {text_color}; font-size: 17px; font-weight: 600;"
        )

    def clear_results(self):
        self.z_card.set_value("-", "#4a90e2")
        self.p_card.set_value("-", "#4a90e2")
        self.conclusion_label.setText("-")
        self.conclusion_label.setStyleSheet(
            "color: #2c3e50; font-size: 17px; font-weight: 600;"
        )

    def show_message(self, title: str, text: str, level="info"):
        if level == "warning":
            QMessageBox.warning(self, title, text)
        elif level == "error":
            QMessageBox.critical(self, title, text)
        else:
            QMessageBox.information(self, title, text)

    def ask_save_filename(self) -> str:
        from datetime import datetime
        default_name = f"Результаты_диагностики_{datetime.now():%Y-%m-%d_%H-%M-%S}.pdf"
        fname, _ = QFileDialog.getSaveFileName(
            self, "Сохранить результаты в PDF", default_name, "PDF файлы (*.pdf)"
        )
        return fname

    def apply_styles(self):
        self.setStyleSheet(STYLESHEET)
