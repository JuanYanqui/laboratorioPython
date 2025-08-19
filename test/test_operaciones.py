import pytest
from src.operaciones import suma, division

def test_suma() -> None:
    assert suma(2, 3.0) == 5.0

def test_division_normal() -> None:
    assert division(10, 2) == 5.0

def test_division_cero() -> None:
    with pytest.raises(ValueError):
        division(10, 0)
