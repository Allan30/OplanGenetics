import random
import math
import matplotlib.pyplot as plt
import mpl_toolkits.basemap

class City:

    def __init__(self, x, y, name):
        self.name = name
        self.x = x
        self.y = y

    def getDistance(self, city):
        distanceX = (city.x-self.x)*40000*math.cos((self.y+city.y)*math.pi/360)/360
        distanceY = (self.y-city.y)*40000/360
        distance = math.sqrt( (distanceX*distanceX) + (distanceY*distanceY) )
        return distance

class CircuitManager:

    def __init__(self):
        self.cities = list()

    def addCity(self, city): self.cities.append(city)

    def getCity(self, index): return self.cities[index]

    def getNumberCities(self): return len(self.cities)

class Circuit:

    def __init__(self, circuitManager, circuit=None):
        self.circuit = list()
        self.circuitManager = circuitManager
        self.fitness = 0.0
        self.distance = 0.0
        if circuit != None: self.circuit = circuit
        else: 
            for _ in range(circuitManager.getNumberCities()): self.circuit.append(None)

    def __len__(self): return len(self.circuit)

    def getCity(self, index): return self.circuit[index]

    def setCity(self, index, city): 
        self.circuit[index] = city
        self.fitness = 0.0
        self.distance = 0.0

    def generateIndividual(self):
        for index in range(self.circuitManager.getNumberCities()): self.setCity(index, self.circuitManager.getCity(index))
        random.shuffle(self.circuit)

    def getFitness(self):
        if self.fitness == 0.0: self.fitness = 1/self.getDistance()
        return self.fitness

    def getDistance(self):
        if self.distance == 0.0:
            currentDistance = 0.0
            for index, city in enumerate(self.circuit[:-1]): currentDistance += city.getDistance(self.circuit[index+1])
            currentDistance += city.getDistance(self.circuit[0])
            self.distance = currentDistance
        return self.distance

    def getLenCircuit(self): return len(self.circuit)

    def contains(self, city): return city in self.circuit


class Population:

    def __init__(self, circuitManager, populationSize, init):
        self.circuits = list()
        for i in range(populationSize): self.circuits.append(None)

        if init:
            for i in range(populationSize):
                newCircuit = Circuit(circuitManager)
                newCircuit.generateIndividual()
                self.saveCircuit(i, newCircuit)

    def saveCircuit(self, index, circuit): self.circuits[index] = circuit

    def getCircuit(self, index): return self.circuits[index]

    def getFittest(self): 
        fittest = self.circuits[0]

        for circuit in self.circuits[1:]:
            if circuit.getFitness() > fittest.getFitness(): fittest = circuit

        return fittest

    def populationSize(self): return len(self.circuits)


class GA:

    def __init__(self, circuitManager):
        self.circuitManager = circuitManager
        self.mutationPercent = 0.015
        self.tournamentSize = 5
        self.elitism = True

    def evolvPopulation(self, population):
        newPopulation = Population(self.circuitManager, population.populationSize(), False)
        elitismeOffset = 0
        if self.elitism:
            newPopulation.saveCircuit(0, population.getFittest())
            elitismeOffset = 1
        
        for i in range(elitismeOffset, newPopulation.populationSize()):
            parent1 = self.selectionTournament(population)
            parent2 = self.selectionTournament(population)
            enfant = self.crossover(parent1, parent2)
            newPopulation.saveCircuit(i, enfant)
        
        for i in range(elitismeOffset, newPopulation.populationSize()):
            self.mutate(newPopulation.getCircuit(i))
        
        return newPopulation

    def crossover(self, parent1, parent2):
        child = Circuit(self.circuitManager)

        startPos = int(random.random() * parent1.getLenCircuit())
        endPos = int(random.random() * parent1.getLenCircuit())

        for i in range(child.getLenCircuit()):
            if startPos < endPos and i > startPos and i < endPos:
                child.setCity(i, parent1.getCity(i))
            elif startPos > endPos:
                if not (i < startPos and i > endPos):
                    child.setCity(i, parent1.getCity(i))
        
        for i in range(0, parent2.getLenCircuit()):
            if not child.contains(parent2.getCity(i)):
                for ii in range(0, child.getLenCircuit()):
                    if child.getCity(ii) == None:
                        child.setCity(ii, parent2.getCity(i))
                        break
        
        return child

    def mutate(self, circuit):
        for circuitPos1 in range(circuit.getLenCircuit()):
            if random.random() < self.mutationPercent:
                circuitPos2 = int(circuit.getLenCircuit() * random.random())

                city1 = circuit.getCity(circuitPos1)
                city2 = circuit.getCity(circuitPos2)

                circuit.setCity(circuitPos2, city1)
                circuit.setCity(circuitPos1, city2)

    def selectionTournament(self, population):
        tournament = Population(self.circuitManager, self.tournamentSize, False)
        for i in range(self.tournamentSize):
            randomId = int(random.random() * population.populationSize())
            tournament.saveCircuit(i, population.getCircuit(randomId))
        return tournament.getFittest()


if __name__ == '__main__':
   
   gc = CircuitManager()   

   #on cree nos villes
   ville1 = City(3.002556, 45.846117, 'Clermont-Ferrand')
   gc.addCity(ville1)
   ville2 = City(-0.644905, 44.896839, 'Bordeaux')
   gc.addCity(ville2)
   ville3 = City(-1.380989, 43.470961, 'Bayonne')
   gc.addCity(ville3)
   ville4 = City(1.376579, 43.662010, 'Toulouse')
   gc.addCity(ville4)
   ville5 = City(5.337151, 43.327276, 'Marseille')
   gc.addCity(ville5)
   ville6 = City(7.265252, 43.745404, 'Nice')
   gc.addCity(ville6)
   ville7 = City(-1.650154, 47.385427, 'Nantes')
   gc.addCity(ville7)
   ville8 = City(-1.430427, 48.197310, 'Rennes')
   gc.addCity(ville8)
   ville9 = City(2.414787, 48.953260, 'Paris')
   gc.addCity(ville9)
   ville10 = City(3.090447, 50.612962, 'Lille')
   gc.addCity(ville10)
   ville11 = City(5.013054, 47.370547, 'Dijon')
   gc.addCity(ville11)
   ville12 = City(4.793327, 44.990153, 'Valence')
   gc.addCity(ville12)
   ville13 = City(2.447746, 44.966838, 'Aurillac')
   gc.addCity(ville13)
   ville14 = City(1.750115, 47.980822, 'Orleans')
   gc.addCity(ville14)
   ville15 = City(4.134148, 49.323421, 'Reims')
   gc.addCity(ville15)
   ville16 = City(7.506950, 48.580332, 'Strasbourg')
   gc.addCity(ville16)
   ville17 = City(1.233757, 45.865246, 'Limoges')
   gc.addCity(ville17)
   ville18 = City(4.047255,48.370925, 'Troyes')
   gc.addCity(ville18)
   ville19 = City(0.103163,49.532415, 'Le Havre')
   gc.addCity(ville19)
   ville20 = City(-1.495348, 49.667704, 'Cherbourg')
   gc.addCity(ville20)
   ville21 = City(-4.494615, 48.447500, 'Brest')
   gc.addCity(ville21)
   ville22 = City(-0.457140, 46.373545, 'Niort')
   gc.addCity(ville22)


   #on initialise la population avec 50 circuits
   pop = Population(gc, 50, True)
   print("Distance initiale : " + str(pop.getFittest().getDistance()))
   
   # On fait evoluer notre population sur 100 generations
   ga = GA(gc)
   pop = ga.evolvPopulation(pop)
   for i in range(0, 100):
      pop = ga.evolvPopulation(pop)
      #print("Distance : " + str(pop.getFittest().getDistance()))
   
   print("Distance finale : " + str(pop.getFittest().getDistance()))
   meilleurePopulation = pop.getFittest()


   #on genere une carte représentant notre solution
   lons = []
   lats = []
   noms = []
   for ville in meilleurePopulation.circuit:
      lons.append(ville.x)
      lats.append(ville.y)
      noms.append(ville.name)

   lons.append(lons[0])
   lats.append(lats[0])
   noms.append(noms[0])

   map = mpl_toolkits.basemap.Basemap(llcrnrlon=-5.5,llcrnrlat=42.3,urcrnrlon=9.3,urcrnrlat=51.,
             resolution='i', projection='tmerc', lat_0 = 45.5, lon_0 = -3.25)

   map.drawmapboundary(fill_color='aqua')
   map.fillcontinents(color='coral',lake_color='aqua')
   map.drawcoastlines()
   map.drawcountries()
   x,y = map(lons,lats)
   map.plot(x,y,'bo', markersize=12)
   for nom,xpt,ypt in zip(noms,x,y):
       plt.text(xpt+5000,ypt+25000,nom)

   map.plot(x, y, 'D-', markersize=10, linewidth=2, color='k', markerfacecolor='b') 
   plt.show()