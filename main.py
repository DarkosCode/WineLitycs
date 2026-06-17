from dataProcessing import procesarDatos
from visuals.matplot_utils import graficarEstacionalidadVarietales
from visuals.seaborn_utils import graficarVentasXCanal
from visuals.plotly_utils import graficarPlotlyBurbujas

def main():
    datos = procesarDatos()
    
    graficarEstacionalidadVarietales(datos["ventas"])
    graficarVentasXCanal(datos["ventas"])
    graficarPlotlyBurbujas(datos["consolidado"])

if __name__ == "__main__":
    main()
