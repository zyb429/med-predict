from typing import Dict, Optional
from PyQt6.QtWidgets import QApplication, QMessageBox
from models import (MedicalModel, ModelRepository, ModelConfig,
                    DiagnosticResult, PDFExporter)
from views import MainWindow


class MainController:
    def __init__(self, view: MainWindow, app: QApplication):
        self.view = view
        self.app = app

        self.model_repo = ModelRepository.get_all_models()
        self.pdf_exporter = PDFExporter()

        self.current_model: Optional[ModelConfig] = None
        self.medical_model: Optional[MedicalModel] = None  # Новый MedicalModel
        self.last_result: Optional[DiagnosticResult] = None

        self._setup_connections()  # Изменено на _setup_connections (с подчеркиванием)
        self._initialize_ui()      # Изменено на _initialize_ui (с подчеркиванием)

    def _setup_connections(self):  # Добавлен метод
        """Настройка соединений сигналов и слотов"""
        self.view.model_changed.connect(self.on_model_changed)
        self.view.calculate_requested.connect(self.on_calculate_requested)
        self.view.clear_requested.connect(self.on_clear_requested)
        self.view.export_requested.connect(self.on_export_requested)

    def _initialize_ui(self):  # Добавлен метод
        """Инициализация пользовательского интерфейса"""
        self.view.set_model_options(self.model_repo)
        if self.model_repo:
            first_key = next(iter(self.model_repo))
            self.view.model_combo.setCurrentIndex(0)
            self.on_model_changed(first_key)

    def on_model_changed(self, model_key: str):
        self.current_model = self.model_repo[model_key]

        # Определяем тип модели для MedicalModel
        # Проверяем, есть ли "endometriosis" в ключе модели
        model_type = "endometriosis" if "endometriosis" in model_key.lower() else "logistic"

        # Создаем MedicalModel с правильным типом
        self.medical_model = MedicalModel(model_type=model_type)

        self.view.set_model_description(self.current_model.description)
        self.view.create_input_fields(self.current_model.fields)
        self.view.clear_results()
        self.last_result = None

    def on_calculate_requested(self):
        if not self.current_model or not self.medical_model:
            self.view.show_message(
                "Ошибка", "Модель не выбрана или не инициализирована",
                "error"
            )
            return

        raw_values = self.view.get_input_values()
        validation = self._validate_inputs(raw_values)
        self.view.clear_field_errors()

        for key, msg in validation.errors.items():
            self.view.set_field_error(key, msg)

        if validation.errors:
            first_err = next(iter(validation.errors))
            self.view.entries[first_err].setFocus()
            return

        try:
            clean_values = {
                k: float(v.replace(",", ".")) for k, v in raw_values.items()
            }

            # Теперь передаем ВСЕ данные в calculate_probability
            z = self.medical_model.calculate_z(clean_values)
            p = self.medical_model.calculate_probability(clean_values)

            diagnosis, risk_level = self.medical_model.get_diagnosis(
                p, self.current_model.threshold,
                self.current_model.high_risk,
                self.current_model.low_risk
            )

            input_values = {}
            for label, key in self.current_model.fields:
                input_values[key] = (label, clean_values[key])

            result = DiagnosticResult(
                z_value=z,
                p_value=p,
                conclusion=diagnosis,
                risk_level=risk_level,
                input_values=input_values
            )
            self.last_result = result
            self.view.display_result(result)

        except Exception as e:
            self.view.show_message(
                "Ошибка", f"Не удалось выполнить расчёт: \n{e}",
                "error"
            )

    def _validate_inputs(self, raw_values: Dict[str, str]):
        class ValidationResult:
            def __init__(self):
                self.errors = {}

        res = ValidationResult()
        for key, raw in raw_values.items():
            s = raw.strip().replace(",", ".")
            if not s:
                res.errors[key] = "Заполните поле"
                continue
            try:
                float(s)
            except ValueError:
                res.errors[key] = "Введите число (напр. 12.34)"
        return res

    def on_clear_requested(self):
        self.view.clear_input_fields()
        self.view.clear_results()
        self.last_result = None
        if self.current_model:
            self.view.create_input_fields(self.current_model.fields)

    def on_export_requested(self):
        if not self.last_result:
            self.view.show_message("Нет данных", "Сначала выполните расчёт.", "warning")
            return

        doctor_name = self.view.get_doctor_name()
        if not doctor_name:
            msg = QMessageBox(self.view)
            msg.setIcon(QMessageBox.Icon.Question)
            msg.setWindowTitle("ФИО врача не указано")
            msg.setText("Продолжить экспорт без указания ФИО врача?")
            yes_btn = msg.addButton("Да", QMessageBox.ButtonRole.YesRole)
            no_btn = msg.addButton("Нет", QMessageBox.ButtonRole.NoRole)
            msg.setDefaultButton(no_btn)
            msg.exec()
            if msg.clickedButton() == no_btn:
                self.view.doctor_name_entry.setFocus()
                return

        filename = self.view.ask_save_filename()
        if not filename:
            return

        try:
            self.pdf_exporter.export_results(
                filename=filename,
                model_name=self.current_model.name,
                doctor_name=doctor_name,
                input_values=self.last_result.input_values,
                z_value=self.last_result.z_value,
                p_value=self.last_result.p_value,
                conclusion=self.last_result.conclusion,
                formula=self.current_model.z_formula,
            )
            self.view.show_message("Успешно", f"Результаты сохранены в: \n{filename}")
        except Exception as e:
            self.view.show_message("Ошибка экспорта", f"{e}", "error")