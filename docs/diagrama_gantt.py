import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

# sujeto a cambios!!!!!!!!
data = {
    'Tarea': [
        'Decisión del tema y herramientas',
        'Documentación e investigación',
        'Planificación detallada',
        'Primeras pruebas y ajustes',
        'Desarrollo del sistema de control difuso',
        'Entrega Arquitectura',
        'Prototipo funcional y pruebas',
        'Entrega Prototipo Tecnológico',
        'Entrega Estructura de la Memoria',
        'Pruebas finales y revisión',
        'Defensa del proyecto y Memoria final'
    ],
    'Inicio': [
        '2024-09-23', 
        '2024-09-23', 
        '2024-10-02', 
        '2024-10-02', 
        '2024-10-16', # sit control
        '2024-10-28', 
        '2024-11-03', 
        '2024-11-12', 
        '2024-11-19', 
        '2024-11-26', 
        '2024-12-08'
    ],
    'Fin': [
        '2024-10-02', 
        '2024-10-27', 
        '2024-10-09', 
        '2024-10-23', 
        '2024-11-19', # sit control
        '2024-11-03', 
        '2024-11-12', 
        '2024-11-19', 
        '2024-11-26', 
        '2024-12-08', 
        '2024-12-18'
    ]
}


df = pd.DataFrame(data)

#formato datetime
df['Inicio'] = pd.to_datetime(df['Inicio'])
df['Fin'] = pd.to_datetime(df['Fin'])


fig, ax = plt.subplots(figsize=(10, 6))

# barras
for idx, row in df.iterrows():
    ax.barh(row['Tarea'], (row['Fin'] - row['Inicio']).days, left=row['Inicio'], height=0.9, align='center')

ax.xaxis.set_major_locator(mdates.DayLocator(interval=3)) # esto hay q hacerlo para las fechas

ax.xaxis.set_major_formatter(DateFormatter("%d-%b"))



ax.set_yticks(range(len(df)))
ax.set_yticklabels(df['Tarea'])
ax.set_xlabel('Fecha')
ax.set_title('Planificación del Proyecto - Diagrama de Gantt')
ax.grid(True, axis='x', linestyle='--')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
