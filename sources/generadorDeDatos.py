import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

#! Archivo para la generacion del dataset a trabajar luego, creado con ayuda de la IA Gemini con reglas y pedidos especificos
#! Teniendo en cuenta la estructura del proyecto definida en base a las clases de Programacion (sobretodo la clase donde 
#! se vio todo lo de pacientes, schema, etc.)

# Determinar la raíz del proyecto (un nivel arriba de 'sources/')
#? Esto es para que si se ejecuta desde otro lado, o desde otra carpeta, nos aseguremos de que igual siempre salga bien
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 1. Crear la carpeta 'data' en la raíz del proyecto
os.makedirs(DATA_DIR, exist_ok=True)

# Fijar semilla para reproducibilidad (Esto garantiza que la aleatoriedad sea idéntica siempre)
np.random.seed(42)

#! Configuración de parámetros de negocio de la Bodega
varietales = ['Malbec', 'Cabernet Sauvignon', 'Tempranillo', 'Torrontés'] #? 4 varietales de vino máximos
lineas = ['Joven', 'Reserva', 'Gran Reserva'] #? Lineas pensadas segun maduracion (tiempo) del vino
canales = ['Mercado Interno', 'Exportación'] #? Canales de venta, impacto en el precio


#! --- GENERACIÓN DEL INVENTARIO (dataset; stock actual en depósito) ---
inventario_list = []
for var in varietales:
    for lin in lineas:
        # Lógica de negocio: Las líneas premium tienen menos stock físico y umbrales más altos
        if lin == 'Gran Reserva':
            stock_actual = np.random.randint(1500, 4000)
            punto_reposicion = 2500  # Requiere más tiempo de anticipación por la crianza
        elif lin == 'Reserva':
            stock_actual = np.random.randint(4000, 9000)
            punto_reposicion = 3500
        else: # Joven
            stock_actual = np.random.randint(8000, 20000)
            punto_reposicion = 5000  # Alta rotación, reposición estándar

        inventario_list.append({
            'Varietal': var,
            'Linea': lin,
            'Stock_Actual': stock_actual,
            'Punto_Reposicion': punto_reposicion
        })

df_inventario = pd.DataFrame(inventario_list)
# Guardar inventario usando DATA_DIR
inventario_path = os.path.join(DATA_DIR, 'inventario.csv')
df_inventario.to_csv(inventario_path, index=False)
print(f"✅ Archivo '{inventario_path}' creado con éxito.")


#! --- GENERACIÓN DE HISTÓRICO DE VENTAS (1200 registros para poblar los gráficos) ---
print("⏳ Generando histórico de ventas (1200 transacciones)...")
n_ventas = 1200

# Generar fechas aleatorias a lo largo de todo el año 2025 (para capturar estacionalidad mensual)
fecha_inicio = datetime(2025, 1, 1)
fechas = [fecha_inicio + timedelta(days=int(np.random.randint(0, 365))) for _ in range(n_ventas)]

ventas_list = []
for i in range(n_ventas):
    fecha = fechas[i]
    var = np.random.choice(varietales)
    lin = np.random.choice(lineas)
    canal = np.random.choice(canales, p=[0.6, 0.4]) # 60% consumo local, 40% exportación
    
    # Simulación de estacionalidad real mendocina según el mes
    mes = fecha.month
    factor_estacional = 1.0
    if var == 'Torrontés' and mes in [11, 12, 1, 2]: # El blanco explota en verano
        factor_estacional = 1.6
    elif var in ['Malbec', 'Cabernet Sauvignon'] and mes in [5, 6, 7, 8]: # Los tintos pesan más en invierno
        factor_estacional = 1.5

    # Cantidades vendidas (En botellas individuales)
    cant_base = np.random.randint(24, 240) 
    unidades_vendidas = int(cant_base * factor_estacional)

    #! Definición de Precios Base (Escala homogénea en USD equivalentes para comparar rentabilidad)
    if lin == 'Gran Reserva':
        precio_base = 45.0 if canal == 'Exportación' else 30.0
    elif lin == 'Reserva':
        precio_base = 22.0 if canal == 'Exportación' else 15.0
    else: 
        precio_base = 12.0 if canal == 'Exportación' else 8.0
    #? Es decir siempre es mas barato a la venta local
        
    # Genera un factor al azar entre 0.95 (95%) y 1.05 (105%)
    factor_variacion = np.random.uniform(0.95, 1.05)
    # Se lo aplicamos al precio base
    precio_unitario = round(precio_base * factor_variacion, 2)

    ventas_list.append({
        'Fecha': fecha.strftime('%Y-%m-%d'),
        'Varietal': var,
        'Linea': lin,
        'Canal': canal,
        'Unidades_Vendidas': unidades_vendidas,
        'Precio_Unitario': precio_unitario
    })

df_ventas = pd.DataFrame(ventas_list)
# Ordenar cronológicamente las ventas para que los gráficos temporales tengan sentido directo
df_ventas = df_ventas.sort_values('Fecha').reset_index(drop=True)
# Guardar ventas usando DATA_DIR
ventas_path = os.path.join(DATA_DIR, 'ventas.csv')
df_ventas.to_csv(ventas_path, index=False)
print(f"✅ Archivo '{ventas_path}' creado con éxito.")
print("\n🎉 ¡Listo! Datos sintéticos generados en la raíz del proyecto.")
