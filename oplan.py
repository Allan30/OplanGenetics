import math
import random
from objects import *


class GA:

    def __init__(self, scheduleManager):
        self.scheduleManager = scheduleManager
        self.mutation1Percent = 1
        self.mutation2Percent = 1
        self.tournamentSize = 5
        self.elitism = True

    def evolvePopulation(self, population):
        newPopulation = Population(self.scheduleManager, population.populationSize(), False)
        elitismOffset = 0
        if self.elitism:
            newPopulation.saveSchedule(0, population.getBestScore())
            elitismOffset = 1
        
        for i in range(elitismOffset, newPopulation.populationSize()):
            parent1 = self.selectionTournament(population)
            parent2 = self.selectionTournament(population)
            child = self.crossover(parent1, parent2)
            newPopulation.saveSchedule(i, child)
        
        for i in range(elitismOffset, newPopulation.populationSize()):
            self.mutate(newPopulation.getSchedule(i))
        
        return newPopulation

    def crossover(self, parent1, parent2):
        child = Schedule(self.scheduleManager)

        splitPos = random.randint(0, self.scheduleManager.getNumberGroups()-1)

        for i in range(child.getLenSchedule()):
            child.setSlot(i, Slot(self.scheduleManager.getSlot(i), None, None))

        slots1 = parent1.getSlotsOfGroups()
        slots2 = parent2.getSlotsOfGroups()

        random.shuffle(slots1)
        random.shuffle(slots2)

        for i in range(splitPos):
            index, currentSlot = slots1[i]
            child.getSlot(index).setGroup(currentSlot.getGroup())
            child.getSlot(index).setTeacher(currentSlot.getTeacher())

        for index, slot in slots2:
            if not child.contains(slot.getGroup()):
                if child.getSlot(index).getGroup():
                    j = random.randint(0, child.getLenSchedule()-1)
                    while child.getSlot(j).getTeacher() != None: #ajout vérification dispo enseignant, tuteur et maitre de stage
                        j = random.randint(0, child.getLenSchedule()-1)
                    child.getSlot(j).setGroup(slot.getGroup())
                    child.getSlot(j).setTeacher(slot.getTeacher())
                else:
                    child.getSlot(index).setGroup(slot.getGroup())
                    child.getSlot(index).setTeacher(slot.getTeacher())
        
        return child

    def crossoverV2(self):
        pass

    def likenessBetweenSchedules(self): 
        parents = list() #p1, p2, indiceRessemblance
        for i in range(len(self.population)):
            bestLikeness = 0
            bestJ = i+1
            for j in range(i+1, len(self.population)):
                currentLikeness = self.population[i].getLikeness(self.population[j])
                if currentLikeness > bestLikeness:
                    bestLikeness = currentLikeness
                    bestJ = j
            parents.append([self.population[i], self.population[bestJ], bestLikeness])
        return sorted(parents, key=lambda x: x[2], reverse=True)

    def mutate(self, schedule):
        for schedulePos1 in range(schedule.getLenSchedule()):
            #première mutation est l'échange de deux slots
            if random.random() < self.mutation1Percent:
                schedulePos2 = random.randint(0, schedule.getLenSchedule()-1)

                #verifier si l'echange est possible
                slot1 = schedule.getSlot(schedulePos1)
                slot2 = schedule.getSlot(schedulePos2)

                if slot1.canISwitchTheSlotWith(slot2):

                    group1 = slot1.getGroup()
                    group2 = slot2.getGroup()

                    teacher1 = slot1.getTeacher()
                    teacher2 = slot2.getTeacher()

                    slot1.setGroup(group1)
                    slot2.setGroup(group2)

                    slot1.setTeacher(teacher1)
                    slot2.setTeacher(teacher2)

            #deuxième mutation est l'échange de professeur pour un groupe
            if random.random() < self.mutation2Percent:
                slot = schedule.getSlot(schedulePos1)
                if slot.getTeacher() != None:
                    #verifier que les creneaux du nouveau professeur concorde et que le professeur est différent du tuteur
                    slot.setTeacher(self.scheduleManager.getRandomTeacherWithout(slot.getGroup().getTutor()))
                    schedule.setSlot(schedulePos1, slot)



    def selectionTournament(self, population):
        tournament = Population(self.scheduleManager, self.tournamentSize, False)
        for i in range(self.tournamentSize):
            randomId = random.randint(0, population.populationSize()-1)
            tournament.saveSchedule(i, population.getSchedule(randomId))
        return tournament.getBestScore()


if __name__ == '__main__':
    
    sm = ScheduleManager()

    slots = slotsGenerator()
        
    import names

    students = list()
    for i in range(10):
        students.append(Person(names.get_first_name(), names.get_last_name(), i))

    import copy

    teachers = list()
    for i in range(10):
        contraintes = list()
        for j in range(random.randint(0, len(slots)-1)):
            contraintes.append(slots[random.randint(0, len(slots)-1)])
        teachers.append(Teacher(names.get_first_name(), names.get_last_name(), i+10, contraintes))

    apms = list()
    for i in range(10):
        apms.append(Apm(names.get_first_name(), names.get_last_name(), i+20))
    
    groups = list()
    for i in range(10):
        groups.append(Group(teachers[random.randint(0, 9)], apms[random.randint(0, 9)], students[i]))

    for slot in slots:
        sm.addSlot(slot)

    for i in range(10):
        sm.addGroup(groups[i])
        sm.addTeacher(teachers[i])



    pop = Population(sm, 100, True)
    #pop.schedules[random.randint(0, 49)]._toString()
    #pop.getBestScore()._toString()

    ga = GA(sm)
    bestScores = list()
    years = list()
    pop = ga.evolvePopulation(pop)
    years.append(0)
    bestScores.append((pop.getBestScore().getScore()))
    for i in range(0, 100):
        pop = ga.evolvePopulation(pop)
        years.append(i+1)
        bestScores.append(pop.getBestScore().getScore())
        print(pop.getBestScore().isCorrect())

    bestPop = pop.getBestScore()
    bestPop._toString()
    print(bestPop.isCorrect())

    
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot(years, bestScores)

    plt.show()