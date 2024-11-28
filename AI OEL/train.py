# This file implements a genetic algorithm to optimize the path between cities.

# Importing the libraries
import numpy as np
from environment import Environment

# This class represents a candidate solution (route between cities).
class Route():

    # Defines a route's DNA (sequence of cities) and tracks the total distance traveled.
    def __init__(self, dnaLength):
        self.dnaLength = dnaLength
        self.dna = list()

        # Fitness score (total distance).
        self.distance = 0
        
        # Initializing the random DNA generates a sequence of cities to visit, avoiding duplicates.
        # Ensures the sequence ends with the starting city (0).
        for i in range(self.dnaLength - 1):
            rnd = np.random.randint(1, self.dnaLength)
            while rnd in self.dna:
                rnd = np.random.randint(1, self.dnaLength)
            self.dna.append(rnd)
        self.dna.append(0)
    
    # Building the Crossover method: Creates new DNA by combining two parent routes.
    def mix(self, dna1, dna2):     
        self.dna = dna1.copy()
        
        # With 50% probability, swaps genes from dna2 into dna1.
        for i in range(self.dnaLength - 1):
            if np.random.rand() <= 0.5:
                previous = self.dna[i]
                inx = self.dna.index(dna2[i])
                self.dna[inx] = previous
                self.dna[i] = dna2[i]
        
        # Randomly introduces variations in DNA to maintain diversity

        # Random Partial Mutations 1: Exchanges two genes.
        for i in range(self.dnaLength - 1):
            if np.random.rand() <= 0.1:
                previous = self.dna[i]
                rnd = np.random.randint(1, self.dnaLength)
                inx = self.dna.index(rnd)
                self.dna[inx] = previous
                self.dna[i] = rnd
            
            # Random Partial Mutations 2: Moves a random gene to a new position
            elif np.random.rand() <= 0.1:
                rnd = np.random.randint(1, self.dnaLength)
                prevInx = self.dna.index(rnd)
                self.dna.insert(i, rnd)
            
                if i >= prevInx:
                    self.dna.pop(prevInx)
                else:
                    self.dna.pop(prevInx + 1)

# Initializing the main code
# Total number of routes in the population.
populationSize = 50

# Likelihood of applying a mutation.
mutationRate = 0.1

# Number of top-performing routes retained for the next generation.
nSelected = 5

# Stopping Conditions
max_generations = 1000  # Stop after this many generations
distance_threshold = 10.0  # Stop if the best distance is below this value

# Environment Initialization
# Creates an environment instance 
env = Environment()

# Number of cities in the environment
dnaLength = len(env.cities)

# List of Route objects 
population = list()

# Creating the first population: Generates the initial population of routes with random DNA.
for i in range(populationSize):
    route = Route(dnaLength)
    population.append(route)

# Tracks the generation count and the shortest distance found so far
generation = 0
bestDist = np.inf
while True:
    generation += 1
    
    # Evaluating the population
    for route in population:
        env.reset()
        for i in range(dnaLength):
            action = route.dna[i]
            route.distance += env.step(action, 'none')
    
    # Sorting the population: Sorts routes by their total distance (shortest first) and updates the bestDist if a new shortest route is found.
    sortedPop = sorted(population, key=lambda x: x.distance)
    population.clear()
    if sortedPop[0].distance < bestDist:
        bestDist = sortedPop[0].distance
    
    # Add stopping conditions here
    if generation >= max_generations:
        print(f"Stopping: Reached maximum generations: {max_generations}")
        break
    if bestDist <= distance_threshold:
        print(f"Stopping: Reached desired distance threshold: {distance_threshold}")
        break
    
    # Adding best previous routes to the population: Keeps the top-performing nSelected routes in the next generation.
    for i in range(nSelected):
        best = sortedPop[i]
        best.distance = 0
        population.append(best)
    
    # Filling in the rest of the population:
    # Some are replaced by random routes (based on mutationRate).
    # Others are offspring of the top-performing routes (via crossover).
    left = populationSize - nSelected
    for i in range(left):
        newRoute = Route(dnaLength)
        if np.random.rand() <= mutationRate:
            population.append(newRoute)
        else:
            inx1 = np.random.randint(0, nSelected)
            inx2 = np.random.randint(0, nSelected)
            while inx1 == inx2:
                inx2 = np.random.randint(0, nSelected)
            dna1 = sortedPop[inx1].dna
            dna2 = sortedPop[inx2].dna
            newRoute.mix(dna1, dna2)
            population.append(newRoute)
    
    # Displaying the results
    env.reset()  
    for i in range(dnaLength):
        action = sortedPop[0].dna[i]
        _ = env.step(action, 'normal')

        # Every 100 generations, a more detailed animation is shown in "beautiful" mode.
    if generation % 100 == 0:
        env.reset()
        for i in range(dnaLength):
            action = sortedPop[0].dna[i]
            _ = env.step(action, 'beautiful')
    print(f"Generation: {generation} Shortest distance: {bestDist:.2f} units")
