import pytest
from src.operaciones import suma, division

def test_suma():
    assert suma(2, 3.0) == 5.0

def test_division_normal():
    assert division(10, 2) == 5.0

def test_division_cero():
    with pytest.raises(ValueError):
        division(10, 0)
