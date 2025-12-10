from dataclasses import dataclass
from typing import Dict, Tuple

@dataclass(frozen=True)
class DiagnosticResult:
    z_value: float
    p_value: float
    conclusion: str
    risk_level: str
    input_values: Dict[str, Tuple[str, float]]
