import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from schema.ventas import Ventas

def graficarVentasXCanal(df):

    #?Check de si se crearon los datos o no antes de ejecutar los graficos
    if df is None or df.empty:
        print("El DataFrame está vacío o no existe.")
        return

    plt.figure(figsize=(12, 6))
    orden_final = df.sort_values(by=Ventas.COL_FECHA)["Mes"].unique()

    sns.barplot(
        data=df, 
        x="Mes", 
        y=Ventas.COL_UNIDADESV, 
        hue=Ventas.COL_CANAL, 
        order=orden_final,
        estimator=sum, 
        errorbar=None, 
        palette="viridis"
    )
    
    plt.title("Unidades Vendidas por Mes y Canal de Venta")
    plt.xlabel("Mes")
    plt.ylabel("Total Unidades Vendidas")
    plt.legend(title="Canal de Venta", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
