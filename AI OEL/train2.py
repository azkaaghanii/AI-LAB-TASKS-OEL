import numpy as np
from environment import Environment

# Creating the bots
# dna = 3,1,2,0
# fitness = total distance travelled
class Route():
    
    def __init__(self, dnaLength):
        self.dnaLength = dnaLength
        self.dna = list()
        self.distance = 0
        
        for i in range(self.dnaLength - 1):
            # dna = 3,1,2
            rnd = np.random.randint(1, self.dnaLength)
            while rnd in self.dna:
                rnd = np.random.randint(1, self.dnaLength)
            self.dna.append(rnd)
        self.dna.append(0)
        
    # Building cross over method
    def mix(self, dna1, dna2):
        # dna1 = 1,2,3,4,0
        # dna2 = 4,3,2,1,0
        
        self.dna = dna1.copy()
        
        for i in range(self.dnaLength - 1):
            if np.random.rand() <= 0.5:
                previous = self.dna[i]
                inx = self.dna.index(dna2[i])
                self.dna[inx] = previous
                self.dna[i] = dna2[i]
                
        # Random partial mutation
        for i in range(self.dnaLength - 1):
            if np.random.rand() <= 0.1:
                previous = self.dna[i]
                rnd = np.random.randint(1, self.dnaLength)
                inx = self.dna.index(rnd)
                self.dna[inx] = previous
                self.dna[i] = rnd
                
            elif np.random.rand() <= 0.1:
                rnd = np.random.randint(1, self.dnaLength)
                prevInx = self.dna.index(rnd)
                self.dna.insert(i, rnd)
                
                if i >= prevInx:
                    self.dna.pop(prevInx)
                else:
                    self.dna.pop(prevInx + 1)

# Initializing the main code
population_size = 50
mutation_rate = 0.1
n_selected = 5

env = Environment()
dnaLength = len(env.cities)
population = list()

# Creating the first population
for i in range(population_size):
    route = Route(dnaLength)
    population.append(route)
    
# Starting main loop
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
            
    # Sorting the population
    sortedPop = sorted(population, key=lambda x: x.distance)
    population.clear()
    
    if sortedPop[0].distance < bestDist:
        bestDist = sortedPop[0].distance
    
    # Adding best previous routes to the population
    for i in range(n_selected):
        best = sortedPop[i]
        best.distance = 0
        population.append(best)
        
    # Filling the rest of the population
    left = population_size - n_selected
    
    for i in range(left):
        new_route = Route(dnaLength)
        if np.random.rand() <= mutation_rate:
            population.append(new_route)
        else:
            inx1 = np.random.randint(0, n_selected)
            inx2 = np.random.randint(0, n_selected)
            
            while inx1 == inx2:
                inx2 = np.random.randint(0, n_selected)
            
            dna1 = sortedPop[inx1].dna
            dna2 = sortedPop[inx2].dna
            
            new_route.mix(dna1, dna2)
            population.append(new_route)
            
    # Display the results
    env.reset()
    
    for i in range(dnaLength):
        action = sortedPop[0].dna[i]
        _ = env.step(action, 'normal')
        
    if generation % 100 == 0:
        env.reset()
        for i in range(dnaLength):
            action = sortedPop[0].dna[i]
            _ = env.step(action, 'beautiful')
            
    print("Generation: " + str(generation) + ' Shortest distance: {:.2f}'.format(bestDist) + ' units')
