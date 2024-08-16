import json
import numpy as np

# Cargar los datos desde el archivo JSON
with open('data_global.json', 'r') as file:
    data_global = json.load(file)

# Función para calcular las estadísticas
def calculate_statistics(data):
    max_value = int(np.max(data))
    min_value = int(np.min(data))
    mean_value = float(np.mean(data))
    median_value = float(np.median(data))
    std_dev = float(np.std(data))
    iqr = float(np.percentile(data, 75) - np.percentile(data, 25))
    
    return {
        'Maximo': max_value,
        'Minimo': min_value,
        'Promedio': mean_value,
        'Mediana': median_value,
        'Desviacion_Estandar': std_dev,
        'Rango_Intercuartilico': iqr
    }

# Calcular estadísticas para cada iteración
statistics = {}
for iteration in data_global:
    # Convertir los valores de la iteración a una lista de enteros
    data_list = list(map(int, data_global[iteration].values()))
    statistics[iteration] = calculate_statistics(data_list)

# Exportar las estadísticas a un archivo JSON
with open('statistics.json', 'w') as file:
    json.dump(statistics, file, indent=4)