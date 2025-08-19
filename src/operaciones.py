from typing import Optional
from typing import Union

def suma(a: Union[int, float], b: Union[int, float]) -> float:
    return a + b

def division(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("No se puede dividir entre cero")
    return a / b
