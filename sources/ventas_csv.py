import os
import pandas as pd
from schema.ventas import Ventas

def cargarVentas():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_csv = os.path.join(base_dir, "data", "ventas.csv")
    dfCsv = pd.read_csv(ruta_csv) 
    dfCsv = dfCsv.rename(columns={"Fecha": Ventas.COL_FECHA,
                              "Varietal": Ventas.COL_VARIETAL,
                              "Linea": Ventas.COL_LINEA,
                              "Canal": Ventas.COL_CANAL,
                              "Unidades_Vendidas": Ventas.COL_UNIDADESV, 
                              "Precio_Unitario": Ventas.COL_PRECIOU}) 
    
    dfCsv[Ventas.COL_UNIDADESV] = dfCsv[Ventas.COL_UNIDADESV].fillna(0).astype(int)
    dfCsv[Ventas.COL_PRECIOU] = dfCsv[Ventas.COL_PRECIOU].fillna(0).astype(float)
    
    #? Columa nueva de ingresos totales
    dfCsv['Ingreso Total'] = dfCsv[Ventas.COL_UNIDADESV] * dfCsv[Ventas.COL_PRECIOU]
    
    #? Colunna nueva de extraccion de Mes
    dfCsv[Ventas.COL_FECHA] = pd.to_datetime(dfCsv[Ventas.COL_FECHA])
    dfCsv['Mes'] = dfCsv[Ventas.COL_FECHA].dt.month_name()
    
    #? Columna nueva de Estacion (Hemisferio Sur)
    def obtener_estacion(mes):
        if mes in [12, 1, 2]:
            return 'Verano'
        elif mes in [3, 4, 5]:
            return 'Otoño'
        elif mes in [6, 7, 8]:
            return 'Invierno'
        else:
            return 'Primavera'
            
    dfCsv[Ventas.COL_ESTACION] = dfCsv[Ventas.COL_FECHA].dt.month.apply(obtener_estacion)
    
    return dfCsv