import random
from collections import OrderedDict

CLASSROOMS = False

DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
HOURS = ["08:50", "09:40", "10:30", "11:20", "14:00", "14:50", "15:40", "16:30"]
CLASSES = ["salle 01", "salle 02", "salle 03"]
PERIODS = [(day, hour) for day in DAYS for hour in HOURS]
        

class Slot:

    def __init__(self, period):
        self.period = period
        self.defenses = list()

    def add(self, group, teacher): self.defenses.append((group, teacher))

    def addDefense(self, defense): self.defenses.append(defense)

    def getCopy(self): 
        newSlot = Slot(self.period)
        for defense in self.defenses: newSlot.addDefense(defense)
        return newSlot

    def popRandomDefense(self): 
        if len(self.defenses) == 0: return None
        return self.defenses.pop(random.randint(0, len(self.defenses)-1))

    def getApms(self): return [group.getApm() for group, _ in self.defenses]

    def getAllTeachers(self): 
        teachers = list()
        for group, teacher in self.defenses:
            teachers.append(teacher)
            teachers.append(group.getTutor())
        
        return teachers

    def isFull(self): 
        return len(self.defenses) >= self.period.nbClassrooms

    def isEmpty(self): return len(self.defenses) == 0

    def isWrong(self):
        for index, defense in enumerate(self.defenses):
            group, teacher = defense
            tutor = group.getTutor()
            apm = group.getApm()
            if not teacher.isFree(self.period): return True
            if not group.getTutor().isFree(self.period): return True
            for g, t in self.defenses[index+1:]:
                if t == teacher or t == tutor or g.getTutor() == teacher or g.getTutor() == tutor or apm == g.getApm(): return True
        return False

    def teachersOrTutorsInSlot(self, teachers):
        numberOfTeachers = 0
        myTeachers = self.getAllTeachers()
        for t in teachers:
            if t in myTeachers: numberOfTeachers += 1
        return numberOfTeachers

    def apmInSlot(self, apms):
        numberOfApm = 0
        myApm = self.getApms()
        for a in apms:
            if a in myApm: numberOfApm += 1
        return numberOfApm

    def switchTeacher(self, indexDefense, newTeacher):
        if newTeacher.isFree(self.period):
            self.defenses[indexDefense] = (self.defenses[indexDefense][0], newTeacher)
            return True
        return False

    def switchADefenseWithTheSlot(self, slot):
        defenseExt = slot.popRandomDefense()
        defenseInt = self.popRandomDefense()
        GROUP = 0
        TEACHER = 1

        switched = True

        if defenseExt: 
            if not defenseInt:
                if defenseExt[GROUP].getTutor().isFree(self.period) and defenseExt[TEACHER].isFree(self.period): 
                    self.addDefense(defenseExt)
                    switched = True
                else: switched = False
            else:
                if self.apmInSlot([defenseExt[GROUP].getApm()]) > 0: switched = False
                elif slot.apmInSlot([defenseInt[GROUP].getApm()]) > 0: switched = False
                elif self.teachersOrTutorsInSlot([defenseExt[GROUP].getTutor(), defenseExt[TEACHER]]) > 0: switched = False
                elif slot.teachersOrTutorsInSlot([defenseInt[GROUP].getTutor(), defenseInt[TEACHER]]) > 0: switched = False
                elif not (defenseExt[GROUP].getTutor().isFree(self.period) and defenseExt[TEACHER].isFree(self.period)): switched = False
                elif not (defenseInt[GROUP].getTutor().isFree(slot.period) and defenseInt[TEACHER].isFree(slot.period)): switched = False
                else:
                    self.addDefense(defenseExt)
                    slot.addDefense(defenseInt)
                    switched = True
        
        else:
            if defenseInt:
                if defenseInt[GROUP].getTutor().isFree(slot.period) and defenseInt[TEACHER].isFree(slot.period): 
                    slot.addDefense(defenseInt)
                    switched = True
                else: switched = False
            else:
                switched = True

        if not switched: 
            if defenseExt: slot.addDefense(defenseExt)
            if defenseInt: self.addDefense(defenseInt)

        return switched

    def isEqual(self, slot): 
        if not self.period.isEqual(slot.period): return False
        if len(self.defenses) != len(slot.defenses): return False

        for defense in self.defenses:
            if defense not in slot.defenses: return False


        return True

class Period:

    def __init__(self, day, hour, nbClassrooms):
        self.day = day
        self.hour = hour
        self.nbClassrooms = nbClassrooms

    def isEqual(self, period):
        return self.day == period.day and self.hour == period.hour

class Person:

    def __init__(self, name, surname, id):
        self.name = name
        self.surname = surname
        self.id = id

class Teacher(Person):

    def __init__(self, name, surname, id, constraints):
        super().__init__(name, surname, id)
        self.constraints = constraints

    def isFree(self, period): 
        return (period.day, period.hour) not in self.constraints

    def isFreeTuple(self, period):
        return period not in self.constraints

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
        self.periods = list()
        self.groups = list()
        self.teachers = list()

    def addPeriod(self, period): self.periods.append(period)

    def addGroup(self, group): self.groups.append(group)

    def addTeacher(self, teacher): self.teachers.append(teacher)

    def getSlot(self, index): return Slot(self.periods[index])

    def getPeriod(self, index): return self.periods[index]

    def getGroup(self, index): return self.groups[index]

    def getGroups(self): return self.groups

    def getTeacher(self, index): return self.teachers[index]

    def getRandomTeacher(self, slot, noTeacher=None): 
        if noTeacher:
            return random.choice([i for i in self.teachers if i.isFree(slot.period) and i != noTeacher])
        return random.choice([i for i in self.teachers if i.isFree(slot.period)])

    def getNumberSlots(self): return len(self.periods)

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

    def copySlot(self, index): return self.schedule[index].getCopy()

    def setSlot(self, index, slot): 
        self.schedule[index] = slot
        self.score = 0

    def generateIndividual(self):
        for index in range(self.scheduleManager.getNumberSlots()): 
            slot = self.scheduleManager.getSlot(index)
            self.setSlot(index, slot)

        constraints = dict()
        dictConstraints = dict()
        for index, period in enumerate(PERIODS): constraints[period] = 0; dictConstraints[period] = index
        for teacher in self.scheduleManager.teachers:
            for constraint in teacher.constraints:
                constraints[constraint] += 1

        constraints = OrderedDict(sorted(constraints.items(), key=lambda c: c[1]))  

        for group in self.scheduleManager.getGroups():
            for period, _ in constraints.items():   
                slot = self.schedule[dictConstraints[period]]
                if group.getTutor().isFreeTuple(period) and not slot.isFull():
                    teacher = self.scheduleManager.getRandomTeacher(slot, group.getTutor())
                    slot.add(group, teacher)
                    break
                

    def getLikeness(self, otherSchedule):
        likeness = list()
        for i in range(len(DAYS)):
            allSlotInDayExist = True
            for j in range(len(HOURS)):
                index = i*len(HOURS)+j
                slotInDayExist = False
                for j2 in range(len(HOURS)):
                    index2 = i*len(HOURS)+j2
                    if self.getSlot(index).isEqual(otherSchedule.getSlot(index2)): slotInDayExist = True; break
                if not slotInDayExist: allSlotInDayExist = False; break
            if allSlotInDayExist: likeness.append(DAYS[i])

        for j in range(len(HOURS)):
            allSlotInHourExist = True
            for i in range(len(DAYS)):
                index = i*len(HOURS)+j
                slotInHourExist = False
                for i2 in range(len(DAYS)):
                    index2 = i2*len(HOURS)+j
                    if self.getSlot(index).isEqual(otherSchedule.getSlot(index2)): slotInHourExist = True; break
                if not slotInHourExist: allSlotInHourExist = False; break
            if allSlotInHourExist: likeness.append(HOURS[j])

        return likeness
            
        
    def getScore(self):
        score = 0
        prevDay = self.schedule[0].period.day
        slotStrik = 0
        for index, slot in enumerate(self.schedule):
            currentDay = slot.period.day
            if not slot.isEmpty():
                slotStrik += len(slot.defenses)
            if currentDay == prevDay:
                if index > 0:
                    score += 10*self.schedule[index-1].teachersOrTutorsInSlot(slot.getAllTeachers())
                    score += 1000*self.schedule[index-1].apmInSlot(slot.getApms())
            
            elif currentDay != prevDay: 
                score += slotStrik*30
                slotStrik = 0
            
            if slot.isWrong(): score -= 100

            prevDay = currentDay

        self.score = score
        return score

    def isCorrect(self):
        for slot in self.schedule:
            if slot.isWrong(): return False
        return True

    def getErrors(self):
        errors = list()
        return errors

    def getLenSchedule(self): return len(self.schedule)

    def _toString(self):
        pass

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

    def getSchedule(self, index): 
        try:
            return self.schedules[index]
        except:
            return None

    def getBestScore(self): 
        bestScore = self.schedules[0]

        for schedule in self.schedules[1:]:
            if schedule.getScore() > bestScore.getScore(): bestScore = schedule

        return bestScore

    def populationSize(self): return len(self.schedules)

    def likenessBetweenSchedules(self): 
        parents = list() #p1, p2, indiceRessemblance
        for i in range(self.populationSize()-1):
            bestLikeness = list()
            bestJ = i
            scheduleI = self.getSchedule(i)
            for j in range(i+1, self.populationSize()):
                currentLikeness = scheduleI.getLikeness(self.getSchedule(j))
                if len(currentLikeness) > len(bestLikeness) and len(currentLikeness) < len(DAYS)+len(HOURS):
                    bestLikeness = currentLikeness
                    bestJ = j
            parents.append([scheduleI, self.getSchedule(bestJ), bestLikeness])
        return sorted(parents, key=lambda x: len(x[2]), reverse=True)
