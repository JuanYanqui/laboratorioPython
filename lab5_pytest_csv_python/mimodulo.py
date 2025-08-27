from datetime import datetime

def sumar(a: int, b: int) -> int:
    """Suma dos números enteros."""
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Ambos parámetros deben ser enteros")
    return a + b

def invertir_texto(texto: str) -> str:
    """Invierte un texto dado."""
    if not isinstance(texto, str):
        raise ValueError("El parámetro debe ser una cadena")
    return texto[::-1]

def es_fecha_valida(fecha: str) -> bool:
    """Verifica si una cadena tiene formato de fecha 'YYYY-MM-DD'."""
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False
