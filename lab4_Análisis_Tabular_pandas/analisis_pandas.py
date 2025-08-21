import pandas as pd

# Cargar el archivo
df = pd.read_csv("Coaches.csv")

# Primeras filas
print(df.head())

# Info general: tipos de datos y nulos
print(df.info())

# Conteo de nulos por columna
print(df.isna().sum())

# Tamaño
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

# Columna derivada (ejemplo: unir nombre y apellido si existen)
if "FirstName" in df.columns and "LastName" in df.columns:
    df["FullName"] = df["FirstName"].str.strip() + " " + df["LastName"].str.strip()

# Normalizar texto (ejemplo: todo a minúsculas en 'Team')
if "Team" in df.columns:
    df["Team"] = df["Team"].str.lower()

# Manejar nulos (ejemplo: si existe Age, llenar nulos con la media)
if "Age" in df.columns:
    df["Age"] = df["Age"].fillna(df["Age"].mean())

if "Team" in df.columns and "Age" in df.columns:
    resumen = (
        df.groupby("Team")
        .agg(
            avg_age=("Age", "mean"),
            max_age=("Age", "max"),
            count=("Age", "count")
        )
        .reset_index()
    )
    print(resumen)

    # Exportar
    resumen.to_csv("resumen_pandas.csv", index=False)
