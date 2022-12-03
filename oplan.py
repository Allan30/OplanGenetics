import math
import random

CLASSROOMS = False

class EmptySlot:

    def __init__(self, day, dayPeriod, classroom=None):
        self.day = day
        self.dayPeriod = dayPeriod
        self.classroom = classroom

class Slot:

    def __init__(self, emptySlot, group, teacher):
        self.emptySlot = emptySlot
        self.group = group
        self.teacher = teacher

    def setGroup(self, group): self.group = group

    def setTeacher(self, teacher): self.teacher = teacher

    def getSlot(self): return self.emptySlot

    def getGroup(self): return self.group

    def getTeacher(self): return self.teacher

    

class Person:

    def __init__(self, name, surname, id):
        self.name = name
        self.surname = surname
        self.id = id

class Teacher(Person):

    def __init__(self, name, surname, id, constraints):
        super().__init__(name, surname, id)
        self.constraints = constraints

    def isFree(self, slot): return slot not in self.constraints

    def getRandomSlot(self, constraints):
        try:
            return random.choice(list(set(self.constraints)&set(constraints)))
        except:
            return None

class Apm(Person):

    def __init__(self, name, surname, id):
        super().__init__(name, surname, id)

class Group:

    def __init__(self, tutor, apm, student):
        self.tutor = tutor
        self.apm = apm
        self.student = student

    def getTutor(self): return self.tutor

    def getApm(self): return self.apm

    def getStudent(self): return self.student

    def writeIn(self, file):
        file.write(self.tutor.name + " " + self.tutor.surname + " " + self.tutor.id)
        # "┌──────────────────────────────┬───────┬───────┬───────┬───────┬───────┐\n"\
        # "│       │ 08:00 │ 09:45 │ 11:30 │ 14:00 │ 15:45 │\n"\
        # "├──────────────────────────────┼───────┼───────┼───────┼───────┼───────┤\n"\
        print("┌──────────────────────────────┬───────┬───────┬───────┬───────┬───────┐")
        print("│ Lundi │ 08:00 │ 08:50 │ 09:40 │ 10:30 │ 11:20 │ 12:10 │ 14:00 │ 14:50 │ 15:40 │ 16:30 │ 17:20 |")
        print("├──────────────────────────────┼───────┼───────┼───────┼───────┼───────┤")

class ScheduleManager:

    def __init__(self):
        self.slots = list()
        self.groups = list()
        self.teachers = list()

    def addSlot(self, slot): self.slots.append(slot)

    def addGroup(self, group): self.groups.append(group)

    def addTeacher(self, teacher): self.teachers.append(teacher)

    def getSlot(self, index): return self.slots[index]

    def getGroup(self, index): return self.groups[index]

    def getTeacher(self, index): return self.teachers[index]

    def getRandomTeacherWithout(self, teacher): return random.choice([i for i in self.teachers if i != teacher])

    def getNumberSlots(self): return len(self.slots)

    def getNumberGroups(self): return len(self.groups)

    def getNumberTeachers(self): return len(self.teachers)

class Schedule:

    def __init__(self, scheduleManager, schedule=None):
        self.schedule = list()
        self.scheduleManager = scheduleManager
        self.score = 0

        if schedule != None: self.schedule = schedule
        else: 
            for _ in range(scheduleManager.getNumberSlots()): self.schedule.append(None)

    def getSlot(self, index): return self.schedule[index]

    def setSlot(self, index, slot): 
        self.schedule[index] = slot
        self.score = 0

    def generateIndividual(self):
        #génére le planning de façon aléatoire, sans tenir compte des contraintes professeurs
        for index in range(self.scheduleManager.getNumberSlots()): 
            slot = self.scheduleManager.getSlot(index)
            self.setSlot(index, Slot(slot, None, None))
        
        alreadyChooseIndex = list()
        for index in range(self.scheduleManager.getNumberGroups()):
            scheduleIndex = random.choice([i for i in range(self.scheduleManager.getNumberSlots()) if i not in alreadyChooseIndex])
            teacher = self.scheduleManager.getRandomTeacherWithout(self.scheduleManager.getGroup(index).getTutor())
            self.setSlot(scheduleIndex, Slot(self.getSlot(scheduleIndex).getSlot(), self.scheduleManager.getGroup(index), teacher))
            alreadyChooseIndex.append(scheduleIndex)
        
    def getScore(self):
        """
        suivi des soutenances de meme Map : 100
        jour complet : 10
        suivi des soutenances de meme tuteur : 2
        contrainte pas respecte : -1
        """
        score = 0
        prevDay = "None"
        emptySlot = False
        for index, slot in enumerate(self.schedule):
            currentDay = slot.getSlot().day
            if not slot.getTeacher(): emptySlot = True
            else: 
                if currentDay == prevDay:
                    if index > 0 and self.schedule[index-1].getTeacher() and self.schedule[index-1].getGroup().getApm() == slot.getGroup().getApm(): score += 500

                    if index > 0 and self.schedule[index-1].getTeacher() and self.schedule[index-1].getGroup().getTutor() == slot.getGroup().getTutor(): score += 2

                    if index > 0 and self.schedule[index-1].getTeacher() and self.schedule[index-1].getTeacher() == slot.getTeacher(): score += 10
                
                else: 
                    if not emptySlot: score += 10
                    emptySlot = False
                
                if slot.getGroup().getTutor().isFree(slot.getSlot()): score += 50
                if slot.getTeacher().isFree(slot.getSlot()): score += 50

            prevDay = currentDay

        # nextIndex = 1
        # for index, slot in enumerate(self.schedule):
        #     if index%4 == 0: completDay = 0
        #     if slot.getTeacher() != None:
        #         completDay += 1
        #         if index%4 < nextIndex%4 and index < len(self.schedule)-2 and self.schedule[index+1].getTeacher() != None and self.schedule[index+1].getGroup().getApm() == slot.getGroup().getApm(): score += 100

        #         if index%4 < nextIndex%4 and index < len(self.schedule)-2 and self.schedule[index+1].getTeacher() != None and self.schedule[index+1].getGroup().getTutor() == slot.getGroup().getTutor(): score += 2

        #         if index%4 < nextIndex%4 and index < len(self.schedule)-2 and self.schedule[index+1].getTeacher() != None and self.schedule[index+1].getTeacher() == slot.getTeacher(): score += 10

        #         if slot.getGroup().getTutor().isFree(slot.getSlot()): score += 50
        #         if slot.getTeacher().isFree(slot.getSlot()): score += 20
        #     if completDay == 4: score += 10
        #     nextIndex+=1
        self.score = score
        return score

    def isCorrect(self):
        for slot in self.schedule:
            if slot.getTeacher():
                if not slot.getGroup().getTutor().isFree(slot.getSlot()): return False
                if not slot.getTeacher().isFree(slot.getSlot()): return False
        return True

    def getLenSchedule(self): return len(self.schedule)

    def contains(self, group):
        for slot in self.schedule:
            if slot != None and slot.getGroup() == group: return True
        return False

    def getSlotsOfGroups(self):
        groups = list()
        for index, slot in enumerate(self.schedule):
            if slot.getTeacher():
                groups.append((index, slot))

        return groups

    def _toString(self):
        print("==============Score : ", self.getScore(), "====================")
        prevDay = "None"
        prevPeriod = "None"
        for slot in self.schedule:
            currentDay = slot.getSlot().day
            currentPeriod = slot.getSlot().dayPeriod
            if currentDay != prevDay:
                print(slot.getSlot().day, " : ")
            if CLASSROOMS:
                if currentPeriod != prevPeriod: 
                    print("    ", slot.getSlot().dayPeriod, " : ")
                    continue
                else:
                    if slot.getTeacher() != None:
                        print("     > ", slot.getSlot().classroom, " : ", slot.getTeacher().id, " / ", slot.getGroup().student.id)
                    if slot.getTeacher() == None: 
                        print("     > ", slot.getSlot().classroom, " : None")
            else:
                if slot.getTeacher() != None:
                    print("     > ", slot.getSlot().dayPeriod, " : ", slot.getTeacher().id, " / ", slot.getGroup().student.id)
                if slot.getTeacher() == None: 
                    print("     > ", slot.getSlot().dayPeriod, " : None")
            prevDay = slot.getSlot().day
            prevPeriod = slot.getSlot().dayPeriod

class Population:

    def __init__(self, scheduleManager, populationSize, init):
        self.schedules = list()
        for i in range(populationSize): self.schedules.append(None)

        if init:
            for i in range(populationSize):
                newShedule = Schedule(scheduleManager)
                newShedule.generateIndividual()
                self.saveSchedule(i, newShedule)

    def saveSchedule(self, index, schedule): self.schedules[index] = schedule

    def getSchedule(self, index): return self.schedules[index]

    def getBestScore(self): 
        bestScore = self.schedules[0]

        for schedule in self.schedules[1:]:
            if schedule.getScore() > bestScore.getScore(): bestScore = schedule

        return bestScore

    def populationSize(self): return len(self.schedules)

class GA:

    def __init__(self, scheduleManager):
        self.scheduleManager = scheduleManager
        self.mutation1Percent = 0.5
        self.mutation2Percent = 0.5
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

        for i in range(splitPos):
            index, currentSlot = slots1[i]
            child.getSlot(index).setGroup(currentSlot.getGroup())
            child.getSlot(index).setTeacher(currentSlot.getTeacher())

        for index, slot in slots2:
            if not child.contains(slot.getGroup()):
                if child.getSlot(index).getGroup():
                    j = random.randint(0, child.getLenSchedule()-1)
                    while child.getSlot(j).getTeacher() != None:
                        j = random.randint(0, child.getLenSchedule()-1)
                    child.getSlot(j).setGroup(slot.getGroup())
                    child.getSlot(j).setTeacher(slot.getTeacher())
                else:
                    child.getSlot(index).setGroup(slot.getGroup())
                    child.getSlot(index).setTeacher(slot.getTeacher())
        
        return child

    def mutate(self, schedule):
        for schedulePos1 in range(schedule.getLenSchedule()):
            #première mutation est l'échange de deux slots
            if random.random() < self.mutation1Percent:
                schedulePos2 = random.randint(0, schedule.getLenSchedule()-1)

                #verifier si l'echange est possible
                slot1 = schedule.getSlot(schedulePos1)
                slot2 = schedule.getSlot(schedulePos2)

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

    slots = list()
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    hours = ["08:50", "09:40", "10:30", "11:20", "14:00", "14:50", "15:40", "16:30"]

    for day in days:
        for hour in hours: slots.append(EmptySlot(day, hour))  
        
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
        groups.append(Group(teachers[i], apms[i], students[i]))

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