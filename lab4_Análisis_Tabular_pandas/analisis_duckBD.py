import duckdb

# Contar coaches por "Play"
print(duckdb.sql("SELECT Play, COUNT(*) AS n FROM 'Coaches.csv' GROUP BY Play").df())

# Agrupar por "Play" y calcular métricas ficticias (ejemplo: longitud promedio del nombre)
query = """
SELECT 
    Play,
    AVG(LENGTH(Name)) AS avg_name_len,
    MAX(LENGTH(Name)) AS max_name_len,
    COUNT(*) AS n
FROM 'Coaches.csv'
GROUP BY Play
"""
resumen_duck = duckdb.sql(query).df()
print(resumen_duck)

# Exportar resultado
duckdb.sql(f"""
COPY (
    {query}
) TO 'resumen_duck.csv' (HEADER, DELIMITER ',')
""")
