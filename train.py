#Space Discover: Genetic Algorithms - Training File 

#Importing the libraries
import numpy as np
from environment import Environment

#Defining the bots
#DNA: route sequence
#Fitness function: total distance travelled by bot

class Route ():
    
    def __init__(self, dnaLength):
        self.dnaLength = dnaLength
        self.dna = list()
        self.distance = 0
        
        #Initializing the DNA
        for i in range(self.dnaLength-1):
            #route traversed except planet 0 since it is always last
            #randomizing the path
            rnd = np.random.randint(1, self.dnaLength)
            #avoiding going over the same planet more than once
            while rnd in self.dna:
                rnd = np.random.randint(1, self.dnaLength)
            
            self.dna.append(rnd)
        #adding planet 0 at the end of the route
        self.dna.append(0)

    #Crossover to create offspring
    #How it works: takes entire dna of first parent, and inherits genes with random probability from the second parent
    def cross(self, dna1, dna2):
        self.dna = dna1.copy()
        
        for i in range(self.dnaLength-1):
            #randomizing the chance to inherit the genes from dna2
            if np.random.rand() <= 0.5:
                #storing the gene that we are changing
                previous = self.dna[i]
                #finding the index of the new gene in the current dna
                index = self.dna.index(dna2[i])
                #swapping the two genes
                self.dna[index] = previous
                self.dna[i] = dna2[i]
        
        #Mutating the DNA to improve the offspring's result
        
        #First mutation: randomly replacing a gene with another
        for i in range(self.dnaLength-1):
            if np.random.rand() <= 0.1:
                previous = self.dna[i]
                new = np.random.randint(1, self.dnaLength)
                index = self.dna.index(new)
                #replacing one gene randomly with another
                self.dna[i] = new
                self.dna[index] = previous
        
            #Second mutation: switch the place of a gene
            elif np.random.rand() <= 0.1:
                new = np.random.randint(1, self.dnaLength)
                #finding the index of the gene
                prevIndex = self.dna.index(new)
                #inserting the gene at its new position
                self.dna.insert(i, new)
                
                #deleting it from the old position
                if(prevIndex <= i):
                    self.dna.pop(prevIndex)
                #in case the element is in the RHS, then the previous index
                #increases after insertion
                else:
                    self.dna.pop(prevIndex + 1)
                    
#Initializing needed variables
populationSize = 50
#chance that a bot is a completely new one
mutationRate = 0.1
#number of bots that are selected from each generation
nSelected = 5 

env = Environment()
#getting the length of the path depending on the input
dnaLength = len(env.planets)
population = list()

#First population
for i in range(populationSize):
    agent = Route(dnaLength)    
    population.append(agent)

#keeps track of the number of generations
generation = 0
#initializing the optimal distance to infinity
bestDist = np.inf

#iterate for an undetermined duration
#to ensure the best path is found
while (True):
    #increasing generation when we iterate
    generation += 1
    
    for agent in population:
        env.reset()
        
        for i in range(dnaLength):
            #determining next planet
            action = agent.dna[i]
            
            #not interested in seeing every single bot so view is none
            agent.distance += env.step(action, 'none') #distance travelled to reach a planet
            
    #sorting the population based on the distance descendeing order
    sortedPopulation = sorted(population, key = lambda x: x.distance)
    population.clear()
     
     #modify the minimum distance if a more optimal one is found
    if sortedPopulation[0].distance < bestDist:
        bestDist = sortedPopulation[0].distance
     
    #adding the best bots to the new population
    #to preserve their genes and even if we have a crossover
    #with worse results we do not lose the best ones     
    for i in range(nSelected):
         best = sortedPopulation[i]
         #distance travelled by the bot is reset to 0
         best.distance = 0
         #appending the best bots to the new population
         population.append(best)
        
    #filling the rest of the population
    #subtracting the number of bots we added
    left = populationSize - nSelected
    
    for i in range(left):
        agent = Route(dnaLength)
        
        #deciding if it is a mutant or offspring
        if np.random.rand() <= mutationRate:
            population.append(agent)
        else:
            #cross the best bots 
            index1 = np.random.randint(0, nSelected)
            index2 = np.random.randint(0, nSelected)
            
            while index1==index2:
                index2 = np.random.randint(0, nSelected)
         
            dna1 = sortedPopulation[index1].dna
            dna2 = sortedPopulation[index2].dna
            
            agent.cross(dna1, dna2)
            
            population.append(agent)
     
    #displaying the results
    env.reset()
    
    for i in range(dnaLength):
        action = sortedPopulation[0].dna[i]
        _ = env.step(action, "normal")
    
    if generation % 500 == 0:
        env.reset()
    
        for i in range(dnaLength):
            action = sortedPopulation[0].dna[i]
            #display the rocket
            _ = env.step(action, "beautiful")
        
    print('Generation: ' + str(generation) + ' Shortest distance: {:.2f}'.format(bestDist) + ' light years')
        
            
    

    
        
                