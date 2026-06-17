import pandas as pd
from sources.inventario_csv import cargarInventario
from sources.ventas_csv import cargarVentas

def procesarDatos():
    #? Cargar los DataFrames desde los CSV, pero pasando primero por los sources que estructuran
    dfInventario = cargarInventario()
    dfVentas = cargarVentas()
    
    #? Agrupar las ventas por Varietal y Linea para calcular totales, sumar las columnas "Unidades Vendidas" e "Ingreso Total" de cada vino
    ventasResumen = dfVentas.groupby(['Varietal', 'Linea'])[['Unidades Vendidas', 'Ingreso Total']].sum().reset_index()
    
    #? Cruzar ('Mergear') el inventario con el resumen de ventas
    #? Usamos 'inner' porque queremos analizar los vinos que existen en ambos datasets
    dfConsolidado = pd.merge(dfInventario, ventasResumen, on=['Varietal', 'Linea'], how='inner') 
    #? Al hacerlo como inner, se logra que solo se tomen en cnta cuando haya valores en las dos fuentes de datos
    
    #? Retornamos los DataFrames estructurados en un diccionario
    return {
        "inventario": dfInventario,
        "ventas": dfVentas,
        "consolidado": dfConsolidado
    }

if __name__ == "__main__":
    resultados = procesarDatos()
