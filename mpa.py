import numpy as np
import json


# Definición de la matriz de costos (tiempos)
cost_matrix = np.array([
    [0, 5, 10, 15, 7, 12, 20, 8, 14, 10, 9],
    [5, 0, 6, 9, 5, 8, 14, 4, 7, 5, 6],
    [10, 6, 0, 8, 4, 6, 13, 7, 5, 8, 9],
    [15, 9, 8, 0, 7, 4, 10, 5, 3, 6, 12],
    [7, 5, 4, 7, 0, 3, 9, 6, 4, 5, 8],
    [12, 8, 6, 4, 3, 0, 7, 3, 5, 6, 9],
    [20, 14, 13, 10, 9, 7, 0, 6, 5, 8, 10],
    [8, 4, 7, 5, 6, 3, 6, 0, 2, 5, 7],
    [14, 7, 5, 3, 4, 5, 5, 2, 0, 3, 8],
    [10, 5, 8, 6, 5, 6, 8, 5, 3, 0, 4],
    [9, 6, 9, 12, 8, 9, 10, 7, 8, 4, 0]
])

"""
# Matriz de costos (tiempos) para 16 clientes incluyendo el origen
matriz_costos_16_clientes = np.array([
    # Origen, C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16
    [0, 5, 10, 15, 7, 12, 20, 8, 14, 10, 9, 11, 13, 12, 10, 14, 9],   # Origen
    [5, 0, 6, 9, 5, 8, 14, 4, 7, 5, 6, 8, 7, 9, 11, 13, 12],          # C1 Plaza Sotomayor
    [10, 6, 0, 8, 4, 6, 13, 7, 5, 8, 9, 10, 12, 11, 10, 15, 13],      # C2 Facultad de Ingeniería UV
    [15, 9, 8, 0, 7, 4, 10, 5, 3, 6, 12, 14, 13, 12, 11, 17, 14],     # C3 Paseo 21 de Mayo
    [7, 5, 4, 7, 0, 3, 9, 6, 4, 5, 8, 10, 9, 8, 7, 12, 10],           # C4 Hospital Carlos van Buren
    [12, 8, 6, 4, 3, 0, 7, 3, 5, 6, 9, 11, 10, 9, 8, 14, 11],         # C5 Museo La Sebastiana
    [20, 14, 13, 10, 9, 7, 0, 6, 5, 8, 10, 15, 14, 13, 12, 18, 16],   # C6 Complejo Penitenciario
    [8, 4, 7, 5, 6, 3, 6, 0, 2, 5, 7, 9, 8, 7, 9, 11, 10],            # C7 Mirador Portales
    [14, 7, 5, 3, 4, 5, 5, 2, 0, 3, 8, 10, 9, 8, 7, 13, 11],          # C8 Cerro Concepción
    [10, 5, 8, 6, 5, 6, 8, 5, 3, 0, 4, 6, 7, 6, 9, 12, 10],           # C9 Terminal de Buses de Valparaíso
    [9, 6, 9, 12, 8, 9, 10, 7, 8, 4, 0, 7, 8, 6, 11, 13, 12],         # C10 Estadio Elías Figueroa
    [11, 8, 10, 14, 10, 11, 15, 9, 10, 6, 7, 0, 5, 9, 12, 14, 10],    # C11 (nuevo cliente)
    [13, 7, 12, 13, 9, 10, 14, 8, 9, 7, 8, 5, 0, 6, 9, 13, 11],       # C12 (nuevo cliente)
    [12, 9, 11, 12, 8, 9, 13, 7, 8, 6, 6, 9, 6, 0, 8, 12, 10],        # C13 (nuevo cliente)
    [10, 11, 10, 11, 7, 8, 12, 9, 7, 9, 11, 12, 9, 8, 0, 11, 13],     # C14 (nuevo cliente)
    [14, 13, 15, 17, 12, 14, 18, 11, 13, 12, 13, 14, 13, 12, 11, 0, 16],  # C15 (nuevo cliente)
    [9, 12, 13, 14, 10, 11, 16, 10, 11, 10, 12, 10, 11, 10, 13, 16, 0]   # C16 (nuevo cliente)
])
"""

# Algoritmo de Marine Predators (MPA) para VRP
class MPA_VRP:
    def __init__(self, cost_matrix, num_predators=30, max_iter=100):
        self.cost_matrix = cost_matrix
        self.num_predators = num_predators
        self.max_iter = max_iter
        self.num_locations = cost_matrix.shape[0]
        self.best_global_route = None
        self.best_global_cost = float('inf')

        # Inicialización de depredadores (soluciones)
        self.predators = [self.random_route() for _ in range(num_predators)]
        self.best_predator_routes = list(self.predators)
        self.best_predator_costs = [self.route_cost(
            route) for route in self.predators]

        self.update_global_best()

    def random_route(self):
        route = list(range(1, self.num_locations))
        np.random.shuffle(route)
        return [0] + route + [0]

    def route_cost(self, route):
        cost = 0
        for i in range(len(route) - 1):
            cost += self.cost_matrix[route[i], route[i+1]]
        return cost

    def update_global_best(self):
        for i in range(self.num_predators):
            if self.best_predator_costs[i] < self.best_global_cost:
                self.best_global_cost = self.best_predator_costs[i]
                self.best_global_route = self.best_predator_routes[i]

    def optimize(self):
        for _ in range(self.max_iter):
            for i in range(self.num_predators):
                # Fase de exploitation
                self.predators[i] = self.exploit(self.predators[i])

                # Evaluar costo
                current_cost = self.route_cost(self.predators[i])
                if current_cost < self.best_predator_costs[i]:
                    self.best_predator_costs[i] = current_cost
                    self.best_predator_routes[i] = self.predators[i]

            # Actualizar mejor global
            self.update_global_best()

    def exploit(self, predator):
        # Exploitation básica: seguir al mejor depredador
        new_predator = predator[:]
        swap_idx = np.random.randint(1, len(new_predator) - 2, 2)
        new_predator[swap_idx[0]], new_predator[swap_idx[1]] = (
            new_predator[swap_idx[1]], new_predator[swap_idx[0]]
        )
        if self.route_cost(new_predator) < self.route_cost(predator):
            return new_predator
        return predator


max_iter = [200, 200, 200 , 200, 200]
num_predators = [20, 70, 100, 120, 150]

data_global = {}
for i in range(5):
    data = {}
    for j in range(50):
        # Crear instancia del MPA para VRP
        mpa_vrp = MPA_VRP(matriz_costos_16_clientes, max_iter[i], num_predators[i])

        # Optimizar la ruta
        mpa_vrp.optimize()

        data[str(j)] = int(mpa_vrp.best_global_cost)
    
    data_global[str(i)] = data


# Exportar a archivo JSON
with open('data_global.json', 'w') as file:
    json.dump(data_global, file, indent=4)


# Crear instancia del MPA para VRP
mpa_vrp = MPA_VRP(matriz_costos_16_clientes)

# Optimizar la ruta
mpa_vrp.optimize()

# Mejor solución encontrada
print("Mejor ruta:", mpa_vrp.best_global_route)
print("Costo total de la ruta:", mpa_vrp.best_global_cost)
