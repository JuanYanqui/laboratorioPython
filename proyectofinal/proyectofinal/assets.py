import io
import pandas as pd
import requests
from dagster import asset, AssetCheckResult, AssetExecutionContext, asset_check


FUENTE_COVID = "https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv"


# =========================================================================
# PASO 1: INGESTA DE DATOS
# =========================================================================
@asset(group_name="ingesta")
def obtener_datos(context: AssetExecutionContext) -> pd.DataFrame:
    """Descarga los datos de COVID-19 desde Our World in Data."""
    context.log.info(f"Solicitando datos desde {FUENTE_COVID}")

    resp = requests.get(FUENTE_COVID, timeout=30)
    resp.raise_for_status()

    df = pd.read_csv(io.StringIO(resp.text))
    context.log.info(f"Datos descargados: {df.shape[0]} filas y {df.shape[1]} columnas")
    return df


# =========================================================================
# PASO 2: PERFILADO BÁSICO
# =========================================================================
@asset(group_name="perfilado")
def generar_perfilado(context: AssetExecutionContext, obtener_datos: pd.DataFrame) -> pd.DataFrame:
    """Crea una tabla con métricas de calidad y cobertura de los datos."""
    context.log.info("Generando perfilado de los datos...")

    perfil = {
        "num_filas": len(obtener_datos),
        "num_columnas": len(obtener_datos.columns),
        "fechas": f"{obtener_datos['date'].min()} → {obtener_datos['date'].max()}",
        "paises_unicos": obtener_datos["country"].nunique(),
        "min_new_cases": float(obtener_datos["new_cases"].min()),
        "max_new_cases": float(obtener_datos["new_cases"].max()),
        "pct_nulos_vacunas": round(obtener_datos["people_vaccinated"].isna().mean() * 100, 2)
    }

    df_perfil = pd.DataFrame([perfil])
    df_perfil.to_csv("perfilado_covid.csv", index=False, encoding="utf-8")

    context.log.info("Perfilado exportado en perfilado_covid.csv")
    return df_perfil


# =========================================================================
# PASO 3: CHEQUEOS DE CALIDAD
# =========================================================================
@asset(group_name="calidad")
def chequeos_basicos(obtener_datos: pd.DataFrame):
    """Ejecuta chequeos básicos de integridad sobre los datos."""
    resultados = []

    # 1. Fechas no futuras
    max_fecha = pd.to_datetime(obtener_datos["date"]).max()
    passed = bool(max_fecha <= pd.Timestamp.today())
    resultados.append(AssetCheckResult(passed=passed, description="No hay fechas futuras"))

    # 2. Columnas clave no nulas
    for col in ["country", "date", "population"]:
        passed = bool(obtener_datos[col].notna().all())
        resultados.append(AssetCheckResult(passed=passed, description=f"Columna {col} sin nulos"))

    # 3. Población positiva
    passed = bool((obtener_datos["population"] > 0).all())
    resultados.append(AssetCheckResult(passed=passed, description="Población > 0"))

    return resultados


@asset_check(asset="obtener_datos", description="Validar unicidad de (country, date)")
def validar_unicidad(obtener_datos: pd.DataFrame) -> AssetCheckResult:
    """Confirma que cada país tenga una sola fila por fecha."""
    duplicados = obtener_datos.duplicated(subset=["country", "date"]).sum()
    return AssetCheckResult(
        passed=bool(duplicados == 0),
        description=f"Duplicados encontrados: {duplicados}"
    )


# =========================================================================
# PASO 4: PROCESAMIENTO
# =========================================================================
@asset(group_name="procesamiento")
def preparar_datos(context: AssetExecutionContext, obtener_datos: pd.DataFrame) -> pd.DataFrame:
    """Filtra, limpia y estandariza los datos para análisis."""
    df = obtener_datos.copy()
    filas_ini = len(df)

    # Filtrar países de interés
    df = df[df["country"].isin(["Ecuador", "Peru"])]

    # Eliminar nulos críticos
    df = df.dropna(subset=["new_cases", "people_vaccinated"])

    # Quitar duplicados
    df = df.drop_duplicates(subset=["country", "date"])

    # Ordenar por fecha
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["country", "date"])

    context.log.info(f"Filas: {filas_ini} → {len(df)} después de limpieza")

    return df[["country", "date", "new_cases", "people_vaccinated", "population"]]


# =========================================================================
# PASO 5: MÉTRICAS
# =========================================================================
@asset(group_name="metricas")
def incidencia_7d(preparar_datos: pd.DataFrame) -> pd.DataFrame:
    """Calcula incidencia acumulada a 7 días por cada 100,000 habitantes."""
    df = preparar_datos.copy()
    df["incidencia_diaria"] = (df["new_cases"] / df["population"]) * 100000
    df["incidencia_7d"] = df.groupby("country")["incidencia_diaria"].transform(lambda x: x.rolling(7).mean())
    return df[["country", "date", "incidencia_7d"]]


@asset(group_name="metricas")
def factor_semanal(preparar_datos: pd.DataFrame) -> pd.DataFrame:
    """Calcula el factor de crecimiento de casos semanal."""
    df = preparar_datos.copy()
    df["semana"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)

    resumen = (
        df.groupby(["country", "semana"])["new_cases"]
        .sum()
        .reset_index(name="casos_semana")
    )
    resumen["prev"] = resumen.groupby("country")["casos_semana"].shift(1)
    resumen["factor"] = resumen["casos_semana"] / resumen["prev"]

    return resumen.dropna()


# =========================================================================
# PASO 6: REPORTE
# =========================================================================
@asset(group_name="reportes")
def exportar_reporte(
    preparar_datos: pd.DataFrame,
    incidencia_7d: pd.DataFrame,
    factor_semanal: pd.DataFrame,
    generar_perfilado: pd.DataFrame
):
    """Genera un Excel consolidado con los resultados."""
    archivo = "covid_reporte.xlsx"
    with pd.ExcelWriter(archivo, engine="xlsxwriter") as writer:
        preparar_datos.to_excel(writer, sheet_name="Datos_Limpios", index=False)
        incidencia_7d.to_excel(writer, sheet_name="Incidencia7d", index=False)
        factor_semanal.to_excel(writer, sheet_name="FactorSemanal", index=False)
        generar_perfilado.to_excel(writer, sheet_name="Perfilado", index=False)

    return archivo
