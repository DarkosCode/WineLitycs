import pandas as pd
from sources.inventario_csv import cargarInventario
from sources.ventas_csv import cargarVentas

def procesar_datos():
    # 1. Cargar los DataFrames desde los archivos CSV
    df_inventario = cargarInventario()
    df_ventas = cargarVentas()
    
    # 2. Agrupar las ventas por Varietal y Linea para calcular totales
    # Sumamos las columnas "Unidades Vendidas" e "Ingreso Total" de cada vino
    ventas_resumen = df_ventas.groupby(['Varietal', 'Linea'])[['Unidades Vendidas', 'Ingreso Total']].sum().reset_index()
    
    # 3. Cruzar (Merge) el inventario con el resumen de ventas
    # Usamos 'inner' porque queremos analizar los vinos que existen en ambos datasets
    df_consolidado = pd.merge(df_inventario, ventas_resumen, on=['Varietal', 'Linea'], how='inner')
    
    return df_consolidado

if __name__ == "__main__":
    # Prueba rápida para imprimir el resultado
    df = procesar_datos()
    print(df)
