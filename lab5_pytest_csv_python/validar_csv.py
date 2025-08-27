# validar_csv.py
import csv

def leer_csv(ruta):
    with open(ruta, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def validar_coaches(data):
    columnas_obligatorias = {"Name", "Country", "Play"} 
    errores = []

    for i, fila in enumerate(data, start=1):
        # Columnas
        if not columnas_obligatorias.issubset(fila.keys()):
            errores.append(f"Fila {i}: columnas faltantes")
        # Valores obligatorios
        if not fila['Name'] or not fila['Country']:
            errores.append(f"Fila {i}: Name o Country vacío")
    
    return errores
