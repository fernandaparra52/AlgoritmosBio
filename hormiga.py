import numpy as np

# Parámetros del problema
class AntColonyOptimization:
    def __init__(self, distances, num_ants, num_iterations, decay, alpha=1, beta=1):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)  # Inicializar las feromonas
        self.num_ants = num_ants  # Número de hormigas
        self.num_iterations = num_iterations  # Número de iteraciones
        self.decay = decay  # Tasa de decaimiento de las feromonas
        self.alpha = alpha  # Influencia de las feromonas
        self.beta = beta  # Influencia de la distancia

    def run(self):
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        
        for i in range(self.num_iterations):
            all_paths = self.generate_all_paths()  # Generar caminos para todas las hormigas
            self.spread_pheromones(all_paths)  # Esparcir feromonas basadas en los caminos generados
            shortest_path = min(all_paths, key=lambda x: x[1])  # Encontrar el camino más corto
            if shortest_path[1] < all_time_shortest_path[1]:
                all_time_shortest_path = shortest_path  # Actualizar el camino más corto encontrado
            self.pheromone *= self.decay  # Evaporación de feromonas
        
        # Convertir los valores a tipos estándar de Python (int)
        path = [(int(frm), int(to)) for frm, to in all_time_shortest_path[0]]
        return path, all_time_shortest_path[1]
    
    def generate_all_paths(self):
        all_paths = []
        for _ in range(self.num_ants):
            path = self.generate_path(0)  # Partimos desde la ciudad 0
            all_paths.append((path, self.path_distance(path)))  # Agregar camino y su distancia
        return all_paths

    def generate_path(self, start):
        path = []
        visited = set()
        visited.add(start)
        prev = start
        for _ in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append((prev, move))
            prev = move
            visited.add(move)
        path.append((prev, start))  # Volvemos al inicio
        return path
    
    def pick_move(self, pheromone, distances, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0  # Evitar visitar nodos ya visitados

        row = pheromone ** self.alpha * ((1.0 / distances) ** self.beta)  # Fórmula para la probabilidad
        norm_row = row / row.sum()  # Normalizar para obtener una distribución de probabilidad
        move = np.random.choice(range(len(distances)), 1, p=norm_row)[0]  # Selección del siguiente nodo
        return move

    def path_distance(self, path):
        total_distance = 0
        for (frm, to) in path:
            total_distance += self.distances[frm][to]  # Sumar la distancia entre las ciudades
        return total_distance

    def spread_pheromones(self, all_paths):
        for path, dist in all_paths:
            for move in path:
                self.pheromone[move] += 1.0 / dist  # Actualizar feromonas basado en la calidad del camino

# Ejemplo de matriz de distancias entre ciudades (5 ciudades)
distances = np.array([
    [np.inf, 2, 2, 5, 7],
    [2, np.inf, 4, 8, 2],
    [2, 4, np.inf, 1, 3],
    [5, 8, 1, np.inf, 2],
    [7, 2, 3, 2, np.inf]
])

# Parámetros del algoritmo
num_ants = 10  # Número de hormigas
num_iterations = 100  # Número de iteraciones
decay = 0.5  # Tasa de evaporación de feromonas
alpha = 1  # Influencia de las feromonas
beta = 2  # Influencia de la distancia

# Ejecutar ACO
aco = AntColonyOptimization(distances, num_ants, num_iterations, decay, alpha, beta)
shortest_path, shortest_distance = aco.run()

print(f"El camino más corto encontrado es: {shortest_path} con distancia {shortest_distance}")
