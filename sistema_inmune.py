import numpy as np

# Función objetivo a minimizar (ejemplo simple)
def objective_function(x):
    return np.sum(x ** 2)

# Inicializar la población de soluciones
def initialize_population(size, dim, lower_bound, upper_bound):
    return np.random.uniform(lower_bound, upper_bound, (size, dim))

# Proceso clonal: selecciona, clona y muta las mejores soluciones
def clonal_selection(population, fitness, clone_factor, mutation_rate):
    num_clones = int(clone_factor * len(population))
    clones = []
    for idx, individual in enumerate(population):
        # Clonar y mutar
        for _ in range(num_clones):
            clone = individual + mutation_rate * np.random.randn(*individual.shape)
            clones.append(clone)
    return np.array(clones)

# Ejecutar el Algoritmo Clonal
def clonal_algorithm(pop_size, dim, lower_bound, upper_bound, generations, clone_factor, mutation_rate):
    population = initialize_population(pop_size, dim, lower_bound, upper_bound)
    
    for gen in range(generations):
        fitness = np.array([objective_function(ind) for ind in population])
        
        # Seleccionar los mejores individuos (menor fitness)
        best_indices = np.argsort(fitness)[:int(pop_size / 2)]
        best_population = population[best_indices]
        
        # Aplicar clonal selection
        clones = clonal_selection(best_population, fitness, clone_factor, mutation_rate)
        
        # Evaluar fitness de los clones y seleccionar los mejores
        clone_fitness = np.array([objective_function(clone) for clone in clones])
        best_clones_indices = np.argsort(clone_fitness)[:pop_size]
        population = clones[best_clones_indices]
    
    # Devolver la mejor solución encontrada
    best_individual = population[np.argmin(fitness)]
    best_fitness = np.min(fitness)
    return best_individual, best_fitness

# Parámetros del algoritmo
pop_size = 20
dim = 5
lower_bound = -10
upper_bound = 10
generations = 100
clone_factor = 0.1
mutation_rate = 0.1

# Ejecutar el algoritmo clonal
best_solution, best_fitness = clonal_algorithm(pop_size, dim, lower_bound, upper_bound, generations, clone_factor, mutation_rate)

print(f"La mejor solución encontrada es: {best_solution} con un costo de: {best_fitness}")
