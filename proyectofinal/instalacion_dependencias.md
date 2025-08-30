# Instrucciones de Instalación de Dependencias - Proyecto COVID-19

Este documento explica cómo preparar el entorno y ejecutar el pipeline correctamente.

---

## 1. Clonar el repositorio
```bash
git clone <repo_url>
cd proyectofinal
```

## 2. Crear entorno virtual
**Linux / Mac:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```
**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

## 3. Instalar dependencias
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

## 4. Verificar instalación de Dagster
```bash
dagster dev -f proyectofinal/definitions.py
```

## 5. Ejecutar pipeline
```bash
python run_pipeline.py
```
Esto generará los archivos:
- `perfilado_covid.csv`
- `covid_reporte.xlsx`

---

> Nota: Asegúrate de que tu Python sea >=3.10 y de tener permisos de escritura en el directorio del proyecto.

