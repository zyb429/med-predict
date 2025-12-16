from typing import Dict, Callable, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class Complaint(Enum):
    """Перечисление для жалоб"""
    NO = 0
    YES = 1

@dataclass
class PatientData:
    """Данные пациента"""
    patient_id: str
    age: int
    tyrosine: float  # тирозин, мкмоль/л
    arginine: float  # аргинин, мкмоль/л
    no_level: float  # NO, мкмоль/л
    chronic_pain: int  # хроническая тазовая боль (0 или 1)
    dysmenorrhea: int  # дисменорея (0 или 1)
    infertility: int  # бесплодие (0 или 1)
    date_of_analysis: str

@dataclass
class DiagnosticResult:
    """Результат диагностики"""
    patient_id: str
    z_value: float
    probability: float
    risk_level: str
    interpretation: str
    recommendations: List[str]
    date: str
    parameters: Dict[str, float]
    complaints: Dict[str, str]

class ModelConfig:
    """Конфигурация медицинской модели"""
    def __init__(self, name: str, z_formula: str, params: List[str],
                 fields: List[Tuple[str, str]], threshold: float,
                 calc_function: Callable, high_risk: str, low_risk: str,
                 description: str):
        self.name = name
        self.z_formula = z_formula
        self.params = params
        self.fields = fields
        self.threshold = threshold
        self.calc_function = calc_function
        self.high_risk = high_risk
        self.low_risk = low_risk
        self.description = description

    def calculate_z(self, values: Dict[str, Any]) -> float:
        """Вычисляет z-значение на основе входных данных"""
        return self.calc_function(values)


class EndometriosisDiagnosticSystem:
    """Система диагностики эндометриоза яичников"""

    # Референсные значения
    TYROSINE_THRESHOLD = 123.6  # мкмоль/л
    ARGININE_THRESHOLD = 181.3  # мкмоль/л
    NO_THRESHOLD = 36.8  # мкмоль/л

    def __init__(self):
        self.archive = []

    def _check_age(self, age: int) -> bool:
        """Проверка возраста (18-45 лет)"""
        result = 18 <= age <= 45
        print(f"[DEBUG] Проверка возраста: {age} в диапазоне 18-45 = {result}")
        return result

    def _check_complaints(self, patient_data: PatientData) -> bool:
        """Проверка наличия жалоб"""
        return (patient_data.chronic_pain == 1 or
                patient_data.dysmenorrhea == 1 or
                patient_data.infertility == 1)

    def _check_biomarkers(self, patient_data: PatientData) -> bool:
        """Проверка биохимических показателей"""
        return (patient_data.tyrosine > self.TYROSINE_THRESHOLD and
                patient_data.arginine > self.ARGININE_THRESHOLD and
                patient_data.no_level > self.NO_THRESHOLD)

    def _calculate_probability(self, patient_data: PatientData) -> float:
        """Расчет вероятности эндометриоза"""
        print(f"[DEBUG _calculate_probability] Начало расчета для пациента {patient_data.patient_id}")

        # Базовые условия
        age_ok = 18 <= patient_data.age <= 45
        biomarkers_high = (patient_data.tyrosine > self.TYROSINE_THRESHOLD and
                           patient_data.arginine > self.ARGININE_THRESHOLD and
                           patient_data.no_level > self.NO_THRESHOLD)
        has_complaints = (patient_data.chronic_pain == 1 or
                          patient_data.dysmenorrhea == 1 or
                          patient_data.infertility == 1)

        print(f"[DEBUG] age_ok: {age_ok}")
        print(f"[DEBUG] biomarkers_high: {biomarkers_high}")
        print(f"[DEBUG] has_complaints: {has_complaints}")
        print(f"[DEBUG] Тирозин: {patient_data.tyrosine} > {self.TYROSINE_THRESHOLD} = {patient_data.tyrosine > self.TYROSINE_THRESHOLD}")
        print(f"[DEBUG] Аргинин: {patient_data.arginine} > {self.ARGININE_THRESHOLD} = {patient_data.arginine > self.ARGININE_THRESHOLD}")
        print(f"[DEBUG] NO: {patient_data.no_level} > {self.NO_THRESHOLD} = {patient_data.no_level > self.NO_THRESHOLD}")
        print(f"[DEBUG] chronic_pain: {patient_data.chronic_pain}")
        print(f"[DEBUG] dysmenorrhea: {patient_data.dysmenorrhea}")
        print(f"[DEBUG] infertility: {patient_data.infertility}")

        if not age_ok:
            print(f"[DEBUG] Возраст не в диапазоне 18-45")
            return 0.0

        # Если все три показателя выше порога И есть жалобы
        if biomarkers_high and has_complaints:
            print(f"[DEBUG] Условия выполнены: biomarkers_high={biomarkers_high}, has_complaints={has_complaints}")

            # Начинаем с базовой вероятности 85%
            probability = 85.0
            print(f"[DEBUG] Базовая вероятность: {probability}")

            # Подсчитываем количество жалоб
            complaint_count = 0
            if patient_data.chronic_pain == 1:
                complaint_count += 1
            if patient_data.dysmenorrhea == 1:
                complaint_count += 1
            if patient_data.infertility == 1:
                complaint_count += 1

            print(f"[DEBUG] Количество жалоб: {complaint_count}")

            # Добавляем процент за жалобы (до 10% максимум)
            # Каждая жалоба добавляет примерно 3.33% (10% / 3)
            complaint_bonus = complaint_count * (10.0 / 3.0)
            print(f"[DEBUG] Бонус за жалобы: {complaint_bonus}")

            probability += complaint_bonus
            print(f"[DEBUG] Вероятность после добавления бонуса: {probability}")

            # Корректное ограничение - не более 95%
            if probability > 95.0:
                print(f"[DEBUG] Вероятность {probability} > 95, ограничиваю до 95")
                probability = 95.0
            elif probability < 70.0:
                print(f"[DEBUG] Вероятность {probability} < 70, устанавливаю 70")
                probability = 70.0

            print(f"[DEBUG] Финальная вероятность: {probability}")
            return probability

        # Если условия не выполнены - низкая вероятность
        print(f"[DEBUG] Условия не выполнены. biomarkers_high={biomarkers_high}, has_complaints={has_complaints}")
        return 5.0

    def _calculate_z_value(self, patient_data: PatientData) -> float:
        """Расчет Z-значения для логистической регрессии"""
        tyrosine_score = 3.0 if patient_data.tyrosine > self.TYROSINE_THRESHOLD else 0.1
        arginine_score = 2.5 if patient_data.arginine > self.ARGININE_THRESHOLD else 0.1
        no_score = 2.0 if patient_data.no_level > self.NO_THRESHOLD else 0.1

        complaint_score = 0
        if patient_data.chronic_pain == 1:
            complaint_score += 1.5
        if patient_data.dysmenorrhea == 1:
            complaint_score += 1.2
        if patient_data.infertility == 1:
            complaint_score += 1.0

        age_factor = 2.0 if self._check_age(patient_data.age) else -5.0

        return (tyrosine_score + arginine_score + no_score +
                complaint_score + age_factor)

    def diagnose(self, patient_data: PatientData) -> DiagnosticResult:
        """Основная функция диагностики"""
        print(f"\n[DEBUG] ===== НАЧАЛО ДИАГНОСТИКИ =====")
        print(f"[DEBUG] Вызов diagnose для пациента: {patient_data.patient_id}")

        # Расчет вероятности
        probability = self._calculate_probability(patient_data)

        # ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА: если вероятность > 95, исправляем
        if probability > 95.0:
            print(f"[FIX] Вероятность {probability}% > 95%, исправляю на 95%")
            probability = 95.0

        print(f"[DEBUG] Исправленная вероятность: {probability}%")

        # Расчет Z-значения
        z_value = self._calculate_z_value(patient_data)

        # Определение уровня риска
        risk_level = "ВЫСОКИЙ" if probability >= 70 else "НИЗКИЙ"
        print(f"[DEBUG] Финальные значения: probability={probability}%, risk_level={risk_level}, z_value={z_value}")

        # Генерация интерпретации
        interpretation, recommendations = self._generate_interpretation(probability, patient_data)

        # Формирование результата
        result = DiagnosticResult(
            patient_id=patient_data.patient_id,
            z_value=z_value,
            probability=probability,
            risk_level=risk_level,
            interpretation=interpretation,
            recommendations=recommendations,
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            parameters={
                "tyrosine": patient_data.tyrosine,
                "arginine": patient_data.arginine,
                "no_level": patient_data.no_level,
                "age": patient_data.age
            },
            complaints={
                "chronic_pain": "есть" if patient_data.chronic_pain == 1 else "нет",
                "dysmenorrhea": "есть" if patient_data.dysmenorrhea == 1 else "нет",
                "infertility": "есть" if patient_data.infertility == 1 else "нет"
            }
        )

        # Архивация
        self.archive.append(asdict(result))

        print(f"[DEBUG] ===== КОНЕЦ ДИАГНОСТИКИ =====")
        return result

    def _generate_interpretation(self, probability: float, patient_data: PatientData) -> Tuple[str, List[str]]:
        """Генерация интерпретации и рекомендаций"""
        if probability >= 70:
            interpretation = (
                f"ВЫСОКИЙ РИСК РАЗВИТИЯ ЭНДОМЕТРИОЗА ЯИЧНИКОВ.\n"
                f"Вероятность: {probability:.1f}%\n\n"
                f"Обоснование:\n"
                f"1. Все биохимические показатели превышают референсные значения:\n"
                f"   - Тирозин: {patient_data.tyrosine:.1f} мкмоль/л (норма < {self.TYROSINE_THRESHOLD})\n"
                f"   - Аргинин: {patient_data.arginine:.1f} мкмоль/л (норма < {self.ARGININE_THRESHOLD})\n"
                f"   - NO: {patient_data.no_level:.1f} мкмоль/л (норма < {self.NO_THRESHOLD})\n"
                f"2. Наличие клинических жалоб."
            )

            recommendations = []
            if patient_data.chronic_pain == 1:
                recommendations.append("Консультация гинеколога-эндокринолога")
            if patient_data.dysmenorrhea == 1:
                recommendations.append("УЗИ органов малого таза")
            if patient_data.infertility == 1:
                recommendations.append("Консультация репродуктолога")

            recommendations.extend([
                "Определение уровня CA-125 в сыворотке крови",
                "МРТ органов малого таза",
                "Лапароскопическая диагностика"
            ])
        else:
            interpretation = (
                f"НИЗКАЯ ВЕРОЯТНОСТЬ ЭНДОМЕТРИОЗА ЯИЧНИКОВ.\n"
                f"Вероятность: {probability:.1f}%\n\n"
                f"Обоснование:\n"
                f"Биохимические показатели в пределах нормы или отсутствуют клинические жалобы."
            )
            recommendations = [
                "Плановый осмотр гинеколога 1 раз в год",
                "Повторный анализ через 6 месяцев при сохранении жалоб"
            ]

        return interpretation, recommendations

    def save_archive(self, filename: str = "endometriosis_archive.json"):
        """Сохранение архива в файл"""
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.archive, f, ensure_ascii=False, indent=2)

    def load_archive(self, filename: str = "endometriosis_archive.json"):
        """Загрузка архива из файла"""
        import json
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.archive = json.load(f)
        except FileNotFoundError:
            self.archive = []


class ModelRepository:
    """Репозиторий всех доступных медицинских моделей"""
    @staticmethod
    def get_all_models() -> Dict[str, ModelConfig]:
        """Возвращает все доступные модели"""
        def endometriosis_calc(values: Dict[str, Any]) -> float:
            """Функция расчета Z для эндометриоза"""
            system = EndometriosisDiagnosticSystem()
            try:
                patient_data = PatientData(
                    patient_id="temp",
                    age=values.get("age", 30),
                    tyrosine=values.get("tyrosine", 0),
                    arginine=values.get("arginine", 0),
                    no_level=values.get("no_level", 0),
                    chronic_pain=values.get("chronic_pain", 0),
                    dysmenorrhea=values.get("dysmenorrhea", 0),
                    infertility=values.get("infertility", 0),
                    date_of_analysis=""
                )
                return system._calculate_z_value(patient_data)
            except Exception as e:
                print(f"Ошибка расчета Z: {e}")
                return 0.0

        return {
            "endometriosis_diagnostics": ModelConfig(
                name="Диагностика рисков развития эндометриоза яичников",
                description="",
                z_formula="Z = f(Тирозин, Аргинин, NO, жалобы)",
                params=[
                    "Тирозин — концентрация тирозина в плазме крови (мкмоль/л)",
                    "Аргинин — концентрация аргинина в плазме крови (мкмоль/л)",
                    "NO — уровень оксида азота в плазме крови (мкмоль/л)",
                    "Жалобы — наличие хронической тазовой боли, дисменореи, бесплодия"
                ],
                fields=[
                    ("Возраст (18-45 лет)", "age"),
                    ("Тирозин (мкмоль/л)", "tyrosine"),
                    ("Аргинин (мкмоль/л)", "arginine"),
                    ("NO (мкмоль/л)", "no_level"),
                    ("Хроническая тазовая боль (0-нет, 1-есть)", "chronic_pain"),
                    ("Дисменорея (0-нет, 1-есть)", "dysmenorrhea"),
                    ("Бесплодие (0-нет, 1-есть)", "infertility")
                ],
                threshold=0.7,
                calc_function=endometriosis_calc,
                high_risk="Высокий риск эндометриоза яичников (вероятность >70%)",
                low_risk="Низкий риск эндометриоза яичников (вероятность <70%)"
            )
        }


# Добавим также MedicalModel если требуется
class MedicalModel:
    """Медицинская модель для совместимости"""
    def __init__(self, model_config: ModelConfig):
        self.config = model_config
        self.system = EndometriosisDiagnosticSystem()

    def predict(self, values: Dict[str, Any]) -> DiagnosticResult:
        """Прогнозирование на основе входных данных"""
        try:
            patient_data = PatientData(
                patient_id="prediction",
                age=values.get("age", 30),
                tyrosine=values.get("tyrosine", 0),
                arginine=values.get("arginine", 0),
                no_level=values.get("no_level", 0),
                chronic_pain=values.get("chronic_pain", 0),
                dysmenorrhea=values.get("dysmenorrhea", 0),
                infertility=values.get("infertility", 0),
                date_of_analysis=datetime.now().strftime("%Y-%m-%d")
            )
            return self.system.diagnose(patient_data)
        except Exception as e:
            print(f"Ошибка предсказания: {e}")
            # Возвращаем пустой результат при ошибке
            return DiagnosticResult(
                patient_id="error",
                z_value=0.0,
                probability=0.0,
                risk_level="ОШИБКА",
                interpretation=f"Ошибка расчета: {str(e)}",
                recommendations=["Проверьте входные данные"],
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                parameters={},
                complaints={}
            )