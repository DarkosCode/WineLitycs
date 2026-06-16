import numpy as np
import matplotlib.pyplot as plt
from schema.ventas import Ventas

def graficarEstacionalidadVarietales(df):
    #? Genera un mapa de calor (heatmap) estático con Matplotlib que muestra la relación entre las unidades vendidas por varietal y la estación del año.

    if df is None or df.empty:
        print("El DataFrame está vacío o no existe.")
        return

    # 1. Agrupar y pivotar para obtener el total de unidades vendidas por Varietal y Estación
    pivot_df = (
        df.groupby([Ventas.COL_VARIETAL, Ventas.COL_ESTACION])[Ventas.COL_UNIDADESV]
        .sum()
        .unstack(fill_value=0)
    )

    # 2. Reordenar las columnas en orden cronológico de las estaciones del hemisferio sur
    ordenEstaciones = ['Verano', 'Otoño', 'Invierno', 'Primavera']
    columnas_existentes = [est for est in ordenEstaciones if est in pivot_df.columns]
    pivot_df = pivot_df.reindex(columns=columnas_existentes)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # paleta de colores
    im = ax.imshow(pivot_df.values, cmap='PuRd', aspect='auto')

    # 4. Configurar etiquetas de los ejes
    ax.set_xticks(np.arange(len(pivot_df.columns)))
    ax.set_yticks(np.arange(len(pivot_df.index)))
    ax.set_xticklabels(pivot_df.columns, fontsize=11)
    ax.set_yticklabels(pivot_df.index, fontsize=11)

    # 5. Agregar la barra de color (Colorbar) a la derecha
    cbar = ax.figure.colorbar(im, ax=ax, pad=0.04)
    cbar.ax.set_ylabel("Total Unidades Vendidas", rotation=-90, va="bottom", fontsize=11, labelpad=10)

    # 6. Añadir las anotaciones numéricas dentro de cada celda
    for i in range(len(pivot_df.index)):
        for j in range(len(pivot_df.columns)):
            val = pivot_df.values[i, j]
            ax.text(
                j, i, str(val), 
                ha="center", va="center", 
                color="black", fontsize=10
            )

    # 7. Personalizar diseño y títulos
    ax.set_title(
        "Estacionalidad de Ventas de Vino por Varietal\n(Frecuencia de Unidades Vendidas)", 
        fontsize=14, fontweight='bold', pad=20, color='#333333'
    )
    ax.set_xlabel("Estación del Año", fontsize=12, labelpad=10, fontweight='semibold')
    ax.set_ylabel("Varietal de Vino", fontsize=12, labelpad=10, fontweight='semibold')


    plt.tight_layout()
    plt.show()
