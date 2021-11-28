#Space Discover: Genetic Algorithms - Training File 

#Importing the libraries
import numpy as np
from environemnt import Environment

#Defining the bots
#DNA: route sequence
#Fitness function: total distance travelled by bot

class Route ():
    
    def __init__(self, dnaLength):
        self.dnaLenghth = dnaLength
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
                    
        
        
                