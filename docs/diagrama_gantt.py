import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

# sujeto a cambios!!!!!!!!
data = {
    'Tarea': [
        'Documentación e investigación',
        'Decisión del tema y herramientas',
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
        '2024-09-30', 
        '2024-10-07', 
        '2024-10-14', 
        '2024-10-21', 
        '2024-10-28', 
        '2024-11-04', 
        '2024-11-13', 
        '2024-11-20', 
        '2024-11-27', 
        '2024-12-09'
    ],
    'Fin': [
        '2024-09-29', 
        '2024-10-06', 
        '2024-10-13', 
        '2024-10-20', 
        '2024-10-27', 
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
    ax.barh(row['Tarea'], (row['Fin'] - row['Inicio']).days, left=row['Inicio'], height=0.5, align='center')

ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1)) # esto hay q hacerlo para las fechas
ax.xaxis.set_major_formatter(DateFormatter("%d-%b"))


ax.set_yticks(range(len(df)))
ax.set_yticklabels(df['Tarea'])
ax.set_xlabel('Fecha')
ax.set_title('Planificación del Proyecto - Diagrama de Gantt')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
