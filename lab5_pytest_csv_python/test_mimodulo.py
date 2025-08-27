# test_mimodulo.py
import pytest
from mimodulo import sumar, invertir_texto, es_fecha_valida

# Tests para sumar
def test_sumar_valores_correctos():
    assert sumar(2, 3) == 5
    assert sumar(0, 0) == 0

def test_sumar_errores():
    with pytest.raises(ValueError):
        sumar("2", 3)

# Tests para invertir_texto
def test_invertir_texto_valido():
    assert invertir_texto("hola") == "aloh"
    assert invertir_texto("") == ""

def test_invertir_texto_error():
    with pytest.raises(ValueError):
        invertir_texto(123)

# Tests para es_fecha_valida
def test_fecha_valida():
    assert es_fecha_valida("2025-08-20")
    assert not es_fecha_valida("20-08-2025")
    assert not es_fecha_valida("2025/08/20")
