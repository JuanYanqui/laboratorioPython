from dagster import build_op_context
from proyectofinal.assets import (
    obtener_datos,
    generar_perfilado,
    preparar_datos,
    incidencia_7d,
    factor_semanal,
    exportar_reporte,
    chequeos_basicos,
    validar_unicidad,
)

def run_pipeline():
    context = build_op_context()

    # Ejecutar assets
    df_datos = obtener_datos(context)
    df_perfil = generar_perfilado(context, df_datos)
    chequeos_basicos(df_datos)
    validar_unicidad(df_datos)
    df_limpio = preparar_datos(context, df_datos)
    df_incidencia = incidencia_7d(df_limpio)
    df_factor = factor_semanal(df_limpio)
    archivo = exportar_reporte(df_limpio, df_incidencia, df_factor, df_perfil)

    print(f"Pipeline finalizado. Reporte generado: {archivo}")

if __name__ == "__main__":
    run_pipeline()
