import numpy as np
import random
import math

# Función objetivo a minimizar (en este caso es la función de rastrigin)
def objective_function(x):
    return x**2 + 10 * math.cos(2 * math.pi * x)

# Genera una solución vecina perturbando la actual ligeramente
def neighbor_solution(current_solution):
    return current_solution + random.uniform(-1, 1)

# Recocido Simulado
def simulated_annealing(initial_solution, temperature, cooling_rate, min_temperature):
    current_solution = initial_solution
    best_solution = current_solution
    current_cost = objective_function(current_solution)
    best_cost = current_cost
    
    while temperature > min_temperature:
        # Generar una solución vecina
        new_solution = neighbor_solution(current_solution)
        new_cost = objective_function(new_solution)
        
        # Si la nueva solución es mejor, se acepta
        if new_cost < current_cost:
            current_solution = new_solution
            current_cost = new_cost
            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost
        # Si es peor, se acepta con una probabilidad basada en la temperatura
        else:
            prob = math.exp(-(new_cost - current_cost) / temperature)
            if random.random() < prob:
                current_solution = new_solution
                current_cost = new_cost
        
        # Enfriar la temperatura
        temperature *= cooling_rate

    return best_solution, best_cost

# Parámetros del algoritmo
initial_solution = random.uniform(-10, 10)  # Solución inicial aleatoria
temperature = 1000  # Temperatura inicial
cooling_rate = 0.99  # Tasa de enfriamiento
min_temperature = 0.01  # Temperatura mínima

# Ejecutar el Recocido Simulado
best_solution, best_cost = simulated_annealing(initial_solution, temperature, cooling_rate, min_temperature)

print(f"La mejor solución encontrada es: {best_solution} con costo {best_cost}")
