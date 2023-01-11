import random

CLASSROOMS = False

days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
hours = ["08:50", "09:40", "10:30", "11:20", "14:00", "14:50", "15:40", "16:30"]
classes = ["salle 01", "salle 02", "salle 03"]

def slotsGenerator():
    slots = list()
    for day in days:
        for hour in hours: 
            for classe in classes: slots.append(EmptySlot(day, hour, classe)) 
    return slots

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

    def getSlot(self): return self.emptySlot

    def getGroup(self): return self.group

    def getTeacher(self): return self.teacher

    def setGroup(self, group): self.group = group

    def setTeacher(self, teacher): self.teacher = teacher

    def canISwitchTheSlotWith(self, slot):
        if slot.getGroup() == None and self.group == None: return False
        if slot.getGroup() == None: return self.teacher.isFree(slot.getSlot()) and self.group.getTutor().isFree(slot.getSlot()) 
        if self.group == None: return slot.getGroup().getTutor().isFree(self.getSlot()) and slot.getTeacher().isFree(self.getSlot())
        return self.group.getTutor().isFree(slot.getSlot()) and self.teacher.isFree(slot.getSlot()) and slot.getGroup().getTutor().isFree(self.getSlot()) and slot.getTeacher().isFree(self.getSlot())
    

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

    def getLikness(self, otherSchedule):
        for index in range(len(self.schedule)):
            pass
            
        
    def getScore(self):
        """
        suivi des soutenances de meme Map : 100
        jour complet : 10
        suivi des soutenances de meme tuteur : 2
        contrainte pas respecte : -1
        """
        score = 0
        prevDay = "None"
        prevHour = "None"
        emptySlot = False
        teachersOfTheHour = list()
        for index, slot in enumerate(self.schedule):
            currentDay = slot.getSlot().day
            currentHour = slot.getSlot().dayPeriod
            if not slot.getTeacher(): emptySlot = True
            else: 
                if currentHour != prevHour: 
                    teachersOfTheHour = [slot.getTeacher(), slot.getGroup().getTutor(), slot.getGroup().getApm()]
                else: 
                    if slot.getTeacher() in teachersOfTheHour or slot.getGroup().getTutor() in teachersOfTheHour or slot.getGroup().getApm() in teachersOfTheHour: score -= 100
                    teachersOfTheHour.append(slot.getTeacher())
                    teachersOfTheHour.append(slot.getGroup().getTutor())
                    teachersOfTheHour.append(slot.getGroup().getApm())
                if currentDay == prevDay and currentHour != prevHour:
                    if index > 0 and self.schedule[index-1].getTeacher() and self.schedule[index-1].getGroup().getApm() == slot.getGroup().getApm(): score += 100

                    if index > 0 and self.schedule[index-1].getTeacher() and self.schedule[index-1].getGroup().getTutor() == slot.getGroup().getTutor(): score += 2

                    if index > 0 and self.schedule[index-1].getTeacher() and self.schedule[index-1].getTeacher() == slot.getTeacher(): score += 10
                
                elif currentDay != prevDay: 
                    if not emptySlot: score += 10
                    emptySlot = False
                
                if slot.getGroup().getTutor().isFree(slot.getSlot()): score += 50
                if slot.getTeacher().isFree(slot.getSlot()): score += 50

            prevDay = currentDay
            prevHour = currentHour

        self.score = score
        return score

    def isCorrect(self):
        teachersOfTheHour = list()
        prevHour = "None"
        for slot in self.schedule:
            currentHour = slot.getSlot().dayPeriod
            if slot.getTeacher():
                if not slot.getGroup().getTutor().isFree(slot.getSlot()): return False
                if not slot.getTeacher().isFree(slot.getSlot()): return False
                if currentHour != prevHour: 
                    teachersOfTheHour = [slot.getTeacher(), slot.getGroup().getTutor(), slot.getGroup().getApm()]
                else: 
                    if slot.getTeacher() in teachersOfTheHour or slot.getGroup().getTutor() in teachersOfTheHour or slot.getGroup().getApm() in teachersOfTheHour: return False
                    teachersOfTheHour.append(slot.getTeacher())
                    teachersOfTheHour.append(slot.getGroup().getTutor())
                    teachersOfTheHour.append(slot.getGroup().getApm())
            prevHour = currentHour
        return True

    def getErrors(self):
        errors = list()
        teachersOfTheHour = list()
        prevHour = "None"
        for slot in self.schedule:
            currentHour = slot.getSlot().dayPeriod
            if slot.getTeacher():
                if not slot.getGroup().getTutor().isFree(slot.getSlot()): errors.append(f"{slot.getGroup().getTutor().id} Tutor not free")
                if not slot.getTeacher().isFree(slot.getSlot()): errors.append(f"{slot.getTeacher().id} Teacher not free")
                if currentHour != prevHour: 
                    teachersOfTheHour = [slot.getTeacher(), slot.getGroup().getTutor(), slot.getGroup().getApm()]
                else: 
                    if slot.getTeacher() in teachersOfTheHour or slot.getGroup().getTutor() in teachersOfTheHour or slot.getGroup().getApm() in teachersOfTheHour: errors.append("Teacher already in the classes")
                    teachersOfTheHour.append(slot.getTeacher())
                    teachersOfTheHour.append(slot.getGroup().getTutor())
                    teachersOfTheHour.append(slot.getGroup().getApm())
            prevHour = currentHour
        return errors

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