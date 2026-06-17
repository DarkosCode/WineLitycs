import os
import webbrowser
import plotly.express as px
from schema.inventario import Inventario
from schema.ventas import Ventas

def graficarPlotlyBurbujas(df):    
    #? gráfico de burbujas interactivo con Plotly para analizar stock vs ventas.

    if df is None or df.empty:
        print("El DataFrame consolidado está vacío o no existe.")
        return
    
    # Creamos el gráfico de burbujas (scatter plot)
    fig = px.scatter(
        df,
        x=Ventas.COL_UNIDADESV,
        y=Inventario.COL_STOCK,
        size="Ingreso Total",
        color="Reposicion Necesaria",
        color_discrete_map={"SI": "#E74C3C", "NO": "#2ECC71"},
        title="<b>Análisis de Inventario vs. Popularidad de Ventas</b><br><sup>El tamaño de la burbuja representa el Ingreso Total. El color indica si requiere reposición.</sup>",
        labels={
            Ventas.COL_UNIDADESV: "Unidades Vendidas (Popularidad)",
            Inventario.COL_STOCK: "Stock Actual (Disponibilidad)",
            "Reposicion Necesaria": "¿Requiere Reposición?"
        },
        size_max=50,  # Tamaño máximo visual de las burbujas
        custom_data=["Varietal", "Linea", "Ingreso Total", Inventario.COL_REPOSICION, "Reposicion Necesaria"]
    )
    
    # Personalizar la plantilla de información emergente (Hover)
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]} (%{customdata[1]})</b><br>"
            "───────────────────────────────<br>"
            "<b>Popularidad:</b> %{x:,} botellas vendidas<br>"
            "<b>Stock Actual:</b> %{y:,} unidades<br>"
            "<b>Punto de Reposición:</b> %{customdata[3]:,} unidades<br>"
            "<b>Ingreso Total:</b> $%{customdata[2]:,.2f}<br>"
            "<b>¿Requiere Reposición?:</b> %{customdata[4]}<br>"
            "<extra></extra>"
        )
    )
    
    #? Esta configuracion de color y estilo fue realizada con la IA
    # Estilizado visual premium (Layout limpio, fuentes elegantes y fondo claro)
    fig.update_layout(
        title_font=dict(size=18, family="Arial", color="#2C3E50"),
        legend_title=dict(font=dict(size=12, color="#2C3E50")),
        legend=dict(
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#BDC3C7",
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor="#ECF0F1",
            zerolinecolor="#BDC3C7",
            showline=True,
            linewidth=1,
            linecolor="#BDC3C7"
        ),
        yaxis=dict(
            gridcolor="#ECF0F1",
            zerolinecolor="#BDC3C7",
            showline=True,
            linewidth=1,
            linecolor="#BDC3C7"
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # guardar el reporte interactivo HTML definiendo la ruta
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_html = os.path.join(base_dir, "visuals", "reporte_interactivo.html")
    
    # Guardar como archivo HTML autocontenido
    fig.write_html(ruta_html)
    print(f"Reporte interactivo guardado exitosamente en: {ruta_html}")
    
    # Intentar abrir el navegador web automáticamente
    try:
        # Intentamos primero con el mecanismo integrado de Plotly
        fig.show()
    except Exception as e:
        print(f"Advertencia al iniciar fig.show(): {e}. Intentando alternativa local...")
        try:
            # Fuerza la apertura del archivo HTML local usando el navegador del sistema
            webbrowser.open(f"file://{os.path.abspath(ruta_html)}")
        except Exception as e_inner:
            print(f"No se pudo abrir automáticamente el navegador web: {e_inner}")
            print(f"Por favor, abre manualmente el archivo: file://{os.path.abspath(ruta_html)}")
