import math
from dataclasses import dataclass
from typing import Tuple, Dict, Optional, Any
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
    z_value: float
    p_value: float
    conclusion: str
    risk_level: str
    input_values: Dict[str, Tuple[str, float]]


class EndometriosisModel:
    """Модель для диагностики эндометриоза яичников"""

    # Референсные значения
    TYROSINE_THRESHOLD = 123.6  # мкмоль/л
    ARGININE_THRESHOLD = 181.3  # мкмоль/л
    NO_THRESHOLD = 36.8  # мкмоль/л

    def __init__(self):
        self.model_type = "endometriosis"

    def calculate_z(self, values: Dict[str, Any]) -> float:
        """Вычисляет z-значение на основе входных данных"""
        try:
            # Преобразуем значения
            age = int(values.get("age", 0))
            tyrosine = float(values.get("tyrosine", 0))
            arginine = float(values.get("arginine", 0))
            no_level = float(values.get("no_level", 0))
            chronic_pain = int(values.get("chronic_pain", 0))
            dysmenorrhea = int(values.get("dysmenorrhea", 0))
            infertility = int(values.get("infertility", 0))

            # Расчет z-значения
            tyrosine_score = 3.0 if tyrosine > self.TYROSINE_THRESHOLD else 0.1
            arginine_score = 2.5 if arginine > self.ARGININE_THRESHOLD else 0.1
            no_score = 2.0 if no_level > self.NO_THRESHOLD else 0.1

            complaint_score = 0
            if chronic_pain == 1:
                complaint_score += 1.5
            if dysmenorrhea == 1:
                complaint_score += 1.2
            if infertility == 1:
                complaint_score += 1.0

            age_factor = 2.0 if (18 <= age <= 45) else -5.0

            z_value = (tyrosine_score + arginine_score + no_score +
                       complaint_score + age_factor)

            return z_value

        except Exception as e:
            print(f"Ошибка расчета z: {e}")
            return 0.0

    def calculate_probability(self, values: Dict[str, Any]) -> float:
        """Вычисляет вероятность эндометриоза на основе всех данных"""
        try:
            # Преобразуем значения
            age = int(values.get("age", 0))
            tyrosine = float(values.get("tyrosine", 0))
            arginine = float(values.get("arginine", 0))
            no_level = float(values.get("no_level", 0))
            chronic_pain = int(values.get("chronic_pain", 0))
            dysmenorrhea = int(values.get("dysmenorrhea", 0))
            infertility = int(values.get("infertility", 0))

            # Базовые условия
            age_ok = 18 <= age <= 45
            biomarkers_high = (tyrosine > self.TYROSINE_THRESHOLD and
                               arginine > self.ARGININE_THRESHOLD and
                               no_level > self.NO_THRESHOLD)
            has_complaints = (chronic_pain == 1 or
                              dysmenorrhea == 1 or
                              infertility == 1)

            print(f"[DEBUG] age_ok: {age_ok}")
            print(f"[DEBUG] biomarkers_high: {biomarkers_high}")
            print(f"[DEBUG] has_complaints: {has_complaints}")

            if not age_ok:
                return 0.0

            # Если все три показателя выше порога И есть жалобы
            if biomarkers_high and has_complaints:
                # Начинаем с базовой вероятности 85%
                probability_percent = 85.0

                # Подсчитываем количество жалоб
                complaint_count = 0
                if chronic_pain == 1:
                    complaint_count += 1
                if dysmenorrhea == 1:
                    complaint_count += 1
                if infertility == 1:
                    complaint_count += 1

                print(f"[DEBUG] complaint_count: {complaint_count}")

                # Добавляем процент за жалобы (до 10% максимум)
                # Каждая жалоба добавляет примерно 3.33% (10% / 3)
                complaint_bonus = complaint_count * (10.0 / 3.0)
                print(f"[DEBUG] complaint_bonus: {complaint_bonus}")

                probability_percent += complaint_bonus
                print(f"[DEBUG] probability после добавления бонуса: {probability_percent}")

                # Корректное ограничение - не более 95%
                if probability_percent > 95.0:
                    probability_percent = 95.0
                elif probability_percent < 70.0:
                    probability_percent = 70.0

                probability = probability_percent / 100.0
                print(f"[DEBUG] Финальная вероятность: {probability}")
                return probability

            # Если условия не выполнены - низкая вероятность
            return 0.05

        except Exception as e:
            print(f"Ошибка расчета вероятности: {e}")
            return 0.0

    def get_diagnosis(self, p: float, threshold: float,
                      high_risk: str, low_risk: str) -> Tuple[str, str]:
        """Возвращает диагноз и risk_level ('high'/'low') на основе вероятности"""
        if p > threshold:
            return high_risk, 'high'
        return low_risk, 'low'


class MedicalModel:
    """Универсальный класс для математических расчётов медицинских моделей"""
    def __init__(self, model_type: str = "logistic"):
        self.model_type = model_type
        self.special_models = {
            "endometriosis": EndometriosisModel()
        }

    def calculate_z(self, values: Dict[str, Any]) -> float:
        """Вычисляет z-значение"""
        if self.model_type in self.special_models:
            return self.special_models[self.model_type].calculate_z(values)
        else:
            # Для стандартных моделей нужна своя логика расчета z
            # Здесь можно добавить общую логику или оставить пустой
            return 0.0

    def calculate_probability(self, values: Dict[str, Any]) -> float:
        """Вычисляет вероятность на основе всех данных"""
        if self.model_type in self.special_models:
            return self.special_models[self.model_type].calculate_probability(values)
        else:
            # Для стандартных моделей используем логистическую функцию от z
            z = self.calculate_z(values)
            return 1 / (1 + math.exp(-z))

    def get_diagnosis(self, p: float, threshold: float,
                      high_risk: str, low_risk: str) -> Tuple[str, str]:
        """Возвращает диагноз и risk_level"""
        if self.model_type in self.special_models:
            return self.special_models[self.model_type].get_diagnosis(
                p, threshold, high_risk, low_risk)
        else:
            if p > threshold:
                return high_risk, 'high'
            return low_risk, 'low'


# Модель для совместимости со старым кодом
class CompatibleMedicalModel:
    """Класс для совместимости со старым кодом"""
    def __init__(self):
        pass

    @staticmethod
    def calculate_probability(z: float, model_type: str = "logistic") -> float:
        """Старый метод, работает только с z"""
        if model_type == "endometriosis":
            # Не можем рассчитать без данных пациента
            return 0.0
        else:
            return 1 / (1 + math.exp(-z))

    @staticmethod
    def get_diagnosis(p: float, threshold: float,
                      high_risk: str, low_risk: str) -> Tuple[str, str]:
        if p > threshold:
            return high_risk, 'high'
        return low_risk, 'low'