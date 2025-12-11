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

    def __init__(self):
        self.model_type = "endometriosis"

        # Нормальные значения (здоровые)
        # Тирозин: ~80.1 [72.8-92.4]
        self.TYROSINE_NORMAL = 80.1
        self.TYROSINE_NORMAL_MIN = 72.8
        self.TYROSINE_NORMAL_MAX = 92.4

        # Аргинин: ~120.3 [109.1-149.3]
        self.ARGININE_NORMAL = 120.3
        self.ARGININE_NORMAL_MIN = 109.1
        self.ARGININE_NORMAL_MAX = 149.3

        # NO: здоровые ~18.6 [10.4-24.7], больные ~35.2 [34.2-86.8]
        self.NO_HEALTHY = 18.6
        self.NO_HEALTHY_MIN = 10.4
        self.NO_HEALTHY_MAX = 24.7

        self.NO_DISEASE = 35.2
        self.NO_DISEASE_MIN = 34.2
        self.NO_DISEASE_MAX = 86.8

        # Пороговые значения для высокой вероятности
        self.TYROSINE_THRESHOLD = 100.0  # выше нормы
        self.ARGININE_THRESHOLD = 155.0  # выше нормы
        self.NO_THRESHOLD = 30.0  # граница между здоровыми и больными

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

            # Расчет z-значения с учетом отклонений от нормы
            # Тирозин: оценка от 0.1 до 3.0 в зависимости от отклонения
            if tyrosine > self.TYROSINE_THRESHOLD:
                tyrosine_score = 3.0
            elif tyrosine > self.TYROSINE_NORMAL_MAX:
                # Линейная интерполяция между нормой и порогом
                norm = self.TYROSINE_NORMAL_MAX
                thr = self.TYROSINE_THRESHOLD
                tyrosine_score = 0.1 + 2.9 * ((tyrosine - norm) / (thr - norm))
            else:
                tyrosine_score = 0.1

            # Аргинин: оценка от 0.1 до 2.5
            if arginine > self.ARGININE_THRESHOLD:
                arginine_score = 2.5
            elif arginine > self.ARGININE_NORMAL_MAX:
                norm = self.ARGININE_NORMAL_MAX
                thr = self.ARGININE_THRESHOLD
                arginine_score = 0.1 + 2.4 * ((arginine - norm) / (thr - norm))
            else:
                arginine_score = 0.1

            # NO: оценка от 0.1 до 2.0
            if no_level > self.NO_DISEASE:
                no_score = 2.0
            elif no_level > self.NO_THRESHOLD:
                thr = self.NO_THRESHOLD
                disease = self.NO_DISEASE
                no_score = 0.1 + 1.9 * ((no_level - thr) / (disease - thr))
            else:
                no_score = 0.1

            # Оценка жалоб
            complaint_score = 0
            if chronic_pain == 1:
                complaint_score += 1.5
            if dysmenorrhea == 1:
                complaint_score += 1.2
            if infertility == 1:
                complaint_score += 1.0

            # Возрастной фактор
            age_factor = 2.0 if (18 <= age <= 45) else -3.0

            z_value = (tyrosine_score + arginine_score + no_score +
                       complaint_score + age_factor)

            return z_value

        except Exception as e:
            print(f"Ошибка расчета z: {e}")
            return 0.0

    def is_biomarker_elevated(self, biomarker: str, value: float) -> bool:
        """Проверяет, повышен ли биомаркер"""
        if biomarker == "tyrosine":
            return value > self.TYROSINE_NORMAL_MAX
        elif biomarker == "arginine":
            return value > self.ARGININE_NORMAL_MAX
        elif biomarker == "no":
            return value > self.NO_HEALTHY_MAX
        return False

    def get_biomarker_risk_level(self, biomarker: str, value: float) -> float:
        """Получает уровень риска по биомаркеру (0-1)"""
        if biomarker == "tyrosine":
            if value <= self.TYROSINE_NORMAL_MAX:
                return 0.1
            elif value >= self.TYROSINE_THRESHOLD:
                return 0.9
            else:
                # Линейная интерполяция
                norm = self.TYROSINE_NORMAL_MAX
                thr = self.TYROSINE_THRESHOLD
                return 0.1 + 0.8 * ((value - norm) / (thr - norm))

        elif biomarker == "arginine":
            if value <= self.ARGININE_NORMAL_MAX:
                return 0.1
            elif value >= self.ARGININE_THRESHOLD:
                return 0.9
            else:
                norm = self.ARGININE_NORMAL_MAX
                thr = self.ARGININE_THRESHOLD
                return 0.1 + 0.8 * ((value - norm) / (thr - norm))

        elif biomarker == "no":
            if value <= self.NO_HEALTHY_MAX:
                return 0.1
            elif value >= self.NO_DISEASE:
                return 0.9
            else:
                healthy_max = self.NO_HEALTHY_MAX
                disease_val = self.NO_DISEASE
                return 0.1 + 0.8 * ((value - healthy_max) / (disease_val - healthy_max))

        return 0.1

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

            # Проверка возраста (18-45 лет - репродуктивный возраст)
            age_ok = 18 <= age <= 45
            if not age_ok:
                # Вне репродуктивного возраста вероятность очень низкая
                return 0.05

            # Анализ биомаркеров
            print(f"[DEBUG] Тирозин: {tyrosine} (норма: {self.TYROSINE_NORMAL_MAX})")
            print(f"[DEBUG] Аргинин: {arginine} (норма: {self.ARGININE_NORMAL_MAX})")
            print(f"[DEBUG] NO: {no_level} (норма здоровых: {self.NO_HEALTHY_MAX})")

            # Определяем уровни риска для каждого биомаркера
            tyrosine_risk = self.get_biomarker_risk_level("tyrosine", tyrosine)
            arginine_risk = self.get_biomarker_risk_level("arginine", arginine)
            no_risk = self.get_biomarker_risk_level("no", no_level)

            print(f"[DEBUG] Риск по тирозину: {tyrosine_risk:.3f}")
            print(f"[DEBUG] Риск по аргинину: {arginine_risk:.3f}")
            print(f"[DEBUG] Риск по NO: {no_risk:.3f}")

            # Подсчет жалоб
            complaint_count = chronic_pain + dysmenorrhea + infertility
            print(f"[DEBUG] Количество жалоб: {complaint_count}")

            # Базовый риск на основе биомаркеров (взвешенное среднее)
            # Веса: тирозин 40%, аргинин 35%, NO 25%
            base_risk = (
                    tyrosine_risk * 0.4 +
                    arginine_risk * 0.35 +
                    no_risk * 0.25
            )
            print(f"[DEBUG] Базовый риск: {base_risk:.3f}")

            # Модификатор жалоб
            if complaint_count == 0:
                complaint_modifier = 0.8  # снижаем риск при отсутствии жалоб
            elif complaint_count == 1:
                complaint_modifier = 1.1
            elif complaint_count == 2:
                complaint_modifier = 1.3
            else:  # 3 жалобы
                complaint_modifier = 1.5

            # Рассчитываем итоговую вероятность
            probability = min(0.95, base_risk * complaint_modifier)

            # Устанавливаем минимальную вероятность если хотя бы один биомаркер повышен
            elevated_count = 0
            if self.is_biomarker_elevated("tyrosine", tyrosine):
                elevated_count += 1
            if self.is_biomarker_elevated("arginine", arginine):
                elevated_count += 1
            if self.is_biomarker_elevated("no", no_level):
                elevated_count += 1

            if elevated_count >= 2 and probability < 0.3:
                probability = 0.3
            elif elevated_count == 1 and probability < 0.15:
                probability = 0.15
            elif elevated_count == 0 and probability < 0.05:
                probability = 0.05

            print(f"[DEBUG] Количество повышенных биомаркеров: {elevated_count}")
            print(f"[DEBUG] Итоговая вероятность: {probability:.3f}")

            return probability

        except Exception as e:
            print(f"Ошибка расчета вероятности: {e}")
            return 0.0

    def get_diagnosis(self, p: float, threshold: float = 0.5,
                      high_risk: str = "Высокая вероятность эндометриоза яичников",
                      low_risk: str = "Низкая вероятность эндометриоза яичников") -> Tuple[str, str]:
        """Возвращает диагноз и risk_level ('high'/'low') на основе вероятности"""
        if p > threshold:
            return high_risk, 'high'
        elif p > 0.3:
            return "Умеренная вероятность эндометриоза яичников", 'medium'
        else:
            return low_risk, 'low'

    def get_biomarker_status(self, values: Dict[str, Any]) -> Dict[str, Any]:
        """Получает статус биомаркеров"""
        try:
            tyrosine = float(values.get("tyrosine", 0))
            arginine = float(values.get("arginine", 0))
            no_level = float(values.get("no_level", 0))

            return {
                "tyrosine": {
                    "value": tyrosine,
                    "status": "норма" if tyrosine <= self.TYROSINE_NORMAL_MAX
                    else "повышен" if tyrosine <= self.TYROSINE_THRESHOLD
                    else "значительно повышен",
                    "normal_range": f"{self.TYROSINE_NORMAL_MIN}-{self.TYROSINE_NORMAL_MAX}",
                    "deviation": tyrosine - self.TYROSINE_NORMAL
                },
                "arginine": {
                    "value": arginine,
                    "status": "норма" if arginine <= self.ARGININE_NORMAL_MAX
                    else "повышен" if arginine <= self.ARGININE_THRESHOLD
                    else "значительно повышен",
                    "normal_range": f"{self.ARGININE_NORMAL_MIN}-{self.ARGININE_NORMAL_MAX}",
                    "deviation": arginine - self.ARGININE_NORMAL
                },
                "no_level": {
                    "value": no_level,
                    "status": "норма (здоровые)" if no_level <= self.NO_HEALTHY_MAX
                    else "пограничное" if no_level <= self.NO_THRESHOLD
                    else "характерно для заболевания",
                    "healthy_range": f"{self.NO_HEALTHY_MIN}-{self.NO_HEALTHY_MAX}",
                    "disease_range": f"{self.NO_DISEASE_MIN}-{self.NO_DISEASE_MAX}"
                }
            }
        except Exception as e:
            print(f"Ошибка анализа биомаркеров: {e}")
            return {}


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

    def get_diagnosis(self, p: float, threshold: float = 0.5,
                      high_risk: str = "Высокий риск заболевания",
                      low_risk: str = "Низкий риск заболевания") -> Tuple[str, str]:
        """Возвращает диагноз и risk_level"""
        if self.model_type in self.special_models:
            return self.special_models[self.model_type].get_diagnosis(
                p, threshold, high_risk, low_risk)
        else:
            if p > threshold:
                return high_risk, 'high'
            return low_risk, 'low'

    def get_biomarker_status(self, values: Dict[str, Any]) -> Dict[str, Any]:
        """Получает статус биомаркеров (только для эндометриоза)"""
        if self.model_type in self.special_models and self.model_type == "endometriosis":
            return self.special_models[self.model_type].get_biomarker_status(values)
        return {}


# Пример использования
if __name__ == "__main__":
    # Создаем модель
    model = MedicalModel("endometriosis")

    # Тестовые данные пациента с эндометриозом
    test_data = {
        "age": 30,
        "tyrosine": 105.0,  # повышен (норма до 92.4)
        "arginine": 165.0,  # повышен (норма до 149.3)
        "no_level": 38.0,   # характерно для заболевания (здоровые до 24.7)
        "chronic_pain": 1,
        "dysmenorrhea": 1,
        "infertility": 0
    }

    # Анализ биомаркеров
    analysis = model.get_biomarker_status(test_data)
    print("Анализ биомаркеров:")
    for biomarker, data in analysis.items():
        print(f"  {biomarker}: {data['value']} - {data['status']}")

    # Расчет вероятности
    probability = model.calculate_probability(test_data)
    print(f"\nВероятность эндометриоза: {probability:.1%}")

    # Диагноз
    diagnosis, risk_level = model.get_diagnosis(probability)
    print(f"Диагноз: {diagnosis}")
    print(f"Уровень риска: {risk_level}")