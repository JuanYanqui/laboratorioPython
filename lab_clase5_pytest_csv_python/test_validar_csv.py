# test_validar_csv.py
import pytest
from validar_csv import leer_csv, validar_coaches

def test_csv_valido():
    data = leer_csv("Coaches.csv")
    errores = validar_coaches(data)
    assert errores == []

def test_csv_invalido():
    # Simular fila con errores
    data_invalida = [
        {"Name": "", "Country": "Japan", "Play": "Volleyball"},
        {"Name": "Juan", "Country": "", "Play": "Football"}
    ]
    errores = validar_coaches(data_invalida)
    assert len(errores) == 2  # Name o Country vacío en cada fila
