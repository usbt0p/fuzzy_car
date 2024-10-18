import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

# Actualización para reflejar los sprints ágiles extendidos (del 21 de octubre al 2 de diciembre)

## 3 dias antes + 2 dias

data = {
    'Tarea': [
        'Decisión del tema y herramientas',
        'Documentación e investigación',
        'Planificación detallada',
        'Sprint 1 - Requisitos',
        'Sprint 1 - Diseño',
        'Sprint 1 - Desarrollo',
        'Sprint 1 - Testing',
        'Sprint 1 - Revisión',
        'Sprint 2 - Requisitos',
        'Sprint 2 - Diseño',
        'Sprint 2 - Desarrollo',
        'Sprint 2 - Testing',
        'Sprint 2 - Revisión',
        'Pruebas finales',
        'Completar memoria y documentación',
        'Defensa del proyecto, Memoria final'
    ],
    'Inicio': [
        '2024-09-23',  # Sin cambios
        '2024-09-23',  # Sin cambios
        '2024-10-08',  # Sin cambios
        '2024-10-15',  # Sprint 1 - Requisitos sin cambios
        '2024-10-18',  # Sprint 1 - Diseño sin cambios (pero extendido luego)
        '2024-10-22',  # Sprint 1 - Desarrollo ajustado (comienza después del diseño)
        '2024-10-27',  # Sprint 1 - Testing ajustado
        '2024-11-01',  # Sprint 1 - Revisión ajustado
        '2024-11-02',  # Sprint 2 - Requisitos movido 5 días antes
        '2024-11-05',  # Sprint 2 - Diseño movido 5 días antes (extendido)
        '2024-11-09',  # Sprint 2 - Desarrollo ajustado para no solapar (comienza después del diseño)
        '2024-11-14',  # Sprint 2 - Testing ajustado para no solapar
        '2024-11-18',  # Sprint 2 - Revisión ajustado para no solapar
        '2024-11-20',  # Estructura Memoria sin cambios
        '2024-11-27',  # Pruebas finales sin cambios
        '2024-12-08'   # Sin cambios
    ],
    'Fin': [
        '2024-10-02',  # Sin cambios
        '2024-10-08',  # Sin cambios
        '2024-10-15',  # Sin cambios
        '2024-10-18',  # Sprint 1 - Requisitos sin cambios
        '2024-10-22',  # Sprint 1 - Diseño extendido 2 días (finaliza después)
        '2024-10-27',  # Sprint 1 - Desarrollo extendido 2 días (finaliza después)
        '2024-11-01',  # Sprint 1 - Testing ajustado para no solapar
        '2024-11-02',  # Sprint 1 - Revisión ajustado para no solapar
        '2024-11-05',  # Sprint 2 - Requisitos sin cambios
        '2024-11-09',  # Sprint 2 - Diseño extendido 2 días (finaliza después)
        '2024-11-14',  # Sprint 2 - Desarrollo extendido 2 días (finaliza después)
        '2024-11-18',  # Sprint 2 - Testing ajustado para no solapar
        '2024-11-20',  # Sprint 2 - Revisión ajustado para no solapar
        '2024-11-27',  # Sin cambios
        '2024-12-08',  # Sin cambios
        '2024-12-18'   # Sin cambios
    ]
}

# Convertir los datos en un DataFrame
df = pd.DataFrame(data)

# Convertir las fechas de inicio y fin a formato datetime
df['Inicio'] = pd.to_datetime(df['Inicio'])
df['Fin'] = pd.to_datetime(df['Fin'])

# Crear la figura y los ejes
fig, ax = plt.subplots(figsize=(10, 6))

# Crear barras para cada tarea
for idx, row in df.iterrows():
    ax.barh(row['Tarea'], (row['Fin'] - row['Inicio']).days, left=row['Inicio'], height=0.5, align='center')

# Configurar el formato de la fecha en el eje x
ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
ax.xaxis.set_major_formatter(DateFormatter("%d-%b"))

# Ajustar las etiquetas del eje y (tareas)
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df['Tarea'])

# Etiquetas de los ejes
ax.set_xlabel('Fecha')
ax.set_title('Planificación del Proyecto con Sprints Extendidos - Diagrama de Gantt')

# Rotar etiquetas del eje x
plt.xticks(rotation=45)
ax.grid(True, axis='x', linestyle='--')

# Mostrar el gráfico
plt.tight_layout()
plt.show()
