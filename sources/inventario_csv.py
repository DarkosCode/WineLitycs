import os
import pandas as pd
import numpy as np
from schema.inventario import Inventario

def cargarInventario():
    #? ↘ Esto asegura q se lea siempre bien la ruta, sea donde sea que estes parado
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_csv = os.path.join(base_dir, "data", "inventario.csv")
    
    dfCsv = pd.read_csv(ruta_csv)
    
    #? Renombrar columnas para que coincidan con el 'schema'
    dfCsv = dfCsv.rename(columns={"Varietal": Inventario.COL_VARIETAL,
                                  "Linea": Inventario.COL_LINEA,
                                  "Stock_Actual": Inventario.COL_STOCK,
                                  "Punto_Reposicion": Inventario.COL_REPOSICION})     
    
    #? Limpieza de nulos, convertidor de valores float
    dfCsv[Inventario.COL_STOCK] = dfCsv[Inventario.COL_STOCK].fillna(0).astype(int)
        #* Ayudita propia de memoria; el metodo fillna() solo va a convertir a 0 los valores NaN

    #? Columna agregada, que dice si se necesita reposicion, teniendo en cuenta el stock y el punto
    dfCsv['Reposicion Necesaria'] = np.where(
        dfCsv[Inventario.COL_STOCK] < dfCsv[Inventario.COL_REPOSICION], "SI", "NO")

    return dfCsv
