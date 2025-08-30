# Instrucciones Para Iniciar el Proyecto - COVID-19 Pipeline

Este documento detalla paso a paso cómo iniciar el proyecto correctamente desde cero, incluyendo creación de entorno, instalación de dependencias y ejecución del pipeline.

---

## 1. Ingresar a la carpeta del proyecto
Abrir en el codespace y ejecutar
```bash
cd proyectofinal/
```

## 2. Crear y activar entorno virtual
**Crear el entorno virtual:**
```bash
python3 -m venv .venv
```
**Activar entorno virtual:**
- Linux / Mac:
```bash
source .venv/bin/activate
```
- Windows:
```bash
.venv\Scripts\activate
```
> Nota: Es importante activar el entorno antes de instalar dependencias.

## 3. Instalar dependencias
Dentro del entorno virtual activado, instalar todas las librerías necesarias:
```bash
pip install -r requirements.txt
```

**Dependencias principales:**
- `dagster`, `dagster-webserver`, `dagster-dg-cli` → Orquestación del pipeline.
- `pandas` → Procesamiento de datos.
- `duckdb` → Opcional, para grandes datasets.
- `pyarrow` → Lectura/escritura eficiente de archivos.
- `openpyxl`, `XlsxWriter` → Exportación a Excel.
- `requests` → Descarga de datos desde OWID.

## 4. Ejecutar Dagster (opcional)
Para revisar la UI de Dagster y monitorear los assets:
```bash
dagster dev -f proyectofinal/definitions.py
```
Abrir en el navegador: `http://localhost:3000`

## 5. Ejecutar el pipeline completo
Usando el script `run_pipeline.py`:
```bash
python run_pipeline.py
```
Esto realizará automáticamente:
1. Descargar los datos desde OWID.
2. Generar perfilado de calidad de datos.
3. Ejecutar chequeos de integridad y unicidad.
4. Filtrar y limpiar datos para Ecuador y Perú.
5. Calcular métricas: `incidencia_7d` y `factor_semanal`.
6. Exportar resultados a `covid_reporte.xlsx`.

## 6. Verificar archivos generados
- `perfilado_covid.csv` → Resumen de perfilado de datos crudos.
- `covid_reporte.xlsx` → Reporte consolidado con hojas: `Datos_Limpios`, `Incidencia7d`, `FactorSemanal`, `Perfilado`.

## 7. Recomendaciones
- Ejecutar siempre dentro del entorno virtual activado.
- Revisar la terminal para logs de ejecución y validaciones.
- Dagster UI ayuda a inspeccionar el estado de cada asset y cachés de ejecución.

---
**Fin de la guía de inicio.**

