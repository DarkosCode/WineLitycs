import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def graficarVentasXCanal(df):
    """
    Genera un gráfico de barras agrupadas que compara las unidades vendidas
    por mes, discriminando por canal de venta.
    """
    if df is None or df.empty:
        print("El DataFrame está vacío o no existe.")
        return

    plt.figure(figsize=(12, 6))
    
    # Intentamos detectar si los meses están en inglés o español
    # basándonos en lo que hay en el DataFrame
    meses_en_df = df['Mes'].unique()
    
    # Lista de referencia en español (la que tenías)
    meses_es = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    # Lista de referencia en inglés (por si pandas generó nombres en inglés)
    meses_en = ["January", "February", "March", "April", "May", "June", 
                "July", "August", "September", "October", "November", "December"]
    
    # Decidir cuál usar basándonos en el primer mes que encontremos
    primer_mes = meses_en_df[0]
    if primer_mes in meses_en:
        meses_referencia = meses_en
    else:
        meses_referencia = meses_es

    # Filtrar solo los meses que tienen datos para mantener el orden
    orden_final = [m for m in meses_referencia if m in meses_en_df]

    sns.barplot(
        data=df, 
        x="Mes", 
        y="Unidades Vendidas", 
        hue="Canal de Venta", 
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
