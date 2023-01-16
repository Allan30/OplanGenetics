import math
import random
from objects import *


class GA:

    def __init__(self, scheduleManager):
        self.scheduleManager = scheduleManager
        self.mutation1Percent = 0.8
        self.mutation2Percent = 0.8
        self.tournamentSize = 5
        self.elitism = True
        self.elitismOffset = 0

    def evolvePopulation(self, population):
        
        
        newPopulation = self.crossoverV2(population)
        
        for i in range(self.elitismOffset, newPopulation.populationSize()):
            self.mutate(newPopulation.getSchedule(i))
        
        return newPopulation

    def crossoverV2(self, population):
        newPopulation = Population(self.scheduleManager, population.populationSize(), False)
        if self.elitism:
            newPopulation.saveSchedule(0, population.getBestScore())
            self.elitismOffset = 1

        links = population.likenessBetweenSchedules()
        index = self.elitismOffset
        for parent1, parent2, likenesses in links:
            child1 = Schedule(self.scheduleManager)
            child2 = Schedule(self.scheduleManager)

            for i in range(self.scheduleManager.getNumberSlots()):
                child1.setSlot(i, self.scheduleManager.getSlot(i))
                child2.setSlot(i, self.scheduleManager.getSlot(i))

                period = self.scheduleManager.getPeriod(i)
                if period.day in likenesses or period.hour in likenesses:
                    child1.setSlot(i, parent1.copySlot(i))
                    child2.setSlot(i, parent2.copySlot(i))
                
                else: 
                    child1.setSlot(i, parent2.copySlot(i))
                    child2.setSlot(i, parent1.copySlot(i))

            newPopulation.saveSchedule(index, child1)
            index += 1
            if index >= population.populationSize(): break
            newPopulation.saveSchedule(index, child2)
            index += 1
            if index >= population.populationSize(): break

        return newPopulation

    def mutate(self, schedule):
        for schedulePos1 in range(schedule.getLenSchedule()):
            slot1 = schedule.getSlot(schedulePos1)
            #première mutation est l'échange de deux slots
            if random.random() < self.mutation1Percent:
                schedulePos2 = random.randint(0, schedule.getLenSchedule()-1)

                #verifier si l'echange est possible
                
                slot2 = schedule.getSlot(schedulePos2)

                slot1.switchADefenseWithTheSlot(slot2)

            #deuxième mutation est l'échange de professeur pour un groupe
            for indexDefense in range(len(slot1.defenses)):
                if random.random() < self.mutation2Percent:
                    #verifier que les creneaux du nouveau professeur concorde et que le professeur est différent du tuteur
                    slot1.switchTeacher(indexDefense, self.scheduleManager.getRandomTeacher(slot1))



    def selectionTournament(self, population):
        tournament = Population(self.scheduleManager, self.tournamentSize, False)
        for i in range(self.tournamentSize):
            randomId = random.randint(0, population.populationSize()-1)
            tournament.saveSchedule(i, population.getSchedule(randomId))
        return tournament.getBestScore()


if __name__ == '__main__':
    
    sm = ScheduleManager()


        
    import names

    students = list()
    for i in range(10):
        students.append(Person(names.get_first_name(), names.get_last_name(), i))

    import copy

    teachers = list()
    for i in range(10):
        contraintes = set()
        for j in range(random.randint(0, len(PERIODS)-1)):
            contraintes.add(random.choice(PERIODS))
        teachers.append(Teacher(names.get_first_name(), names.get_last_name(), i+10, list(contraintes)))

    apms = list()
    for i in range(10):
        apms.append(Apm(names.get_first_name(), names.get_last_name(), i+20))
    
    groups = list()
    for i in range(10):
        groups.append(Group(teachers[random.randint(0, 9)], apms[random.randint(0, 9)], students[i]))

    for period in PERIODS:
        sm.addPeriod(Period(period[0], period[1], len(CLASSES)))

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
        print(pop.getBestScore().isCorrect(), pop.getBestScore().getScore())

    bestPop = pop.getBestScore()
    bestPop._toString()
    print(bestPop.isCorrect())

    
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot(years, bestScores)

    plt.show()