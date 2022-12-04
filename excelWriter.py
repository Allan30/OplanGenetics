import openpyxl
from oplan import *

class WriterExcel:

    def __init__(self, path):
        self.path = path
        self.wb = openpyxl.Workbook()
        self.sheets = list()

    def writeData(self, sheet, row, column, data, color=None):
        sheet.cell(row=row, column=column).value = data
        sheet.cell(row=row, column=column).alignment = openpyxl.styles.Alignment(horizontal='center', vertical='center')
        if color != None:
            sheet.cell(row=row, column=column).fill = openpyxl.styles.PatternFill(start_color=color, end_color=color, fill_type='solid')
        self.wb.save(self.path)

    def writeConstraintes(self, teachers, schedule):
        sheet = self.wb.create_sheet(index = len(self.sheets) , title = "constraints")
        self.sheets.append(sheet)

        hours = sorted(list(set([slot.getSlot().dayPeriod for slot in schedule.schedule])))
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        classes = sorted(list(set([slot.getSlot().classroom for slot in schedule.schedule])))
        dictDays = {day: i+2 for i, day in enumerate(days)}
        dictHours = {hour: i+2 for i, hour in enumerate(hours)}
        dictClasses = {classroom: i+2 for i, classroom in enumerate(classes)}

        

        index = 0
        for teacher in teachers:
            for hour, column  in dictHours.items():
                self.writeData(sheet, 1 + index, column, hour)
            for day, row in dictDays.items():
                for classroom, row2 in dictClasses.items():
                    self.writeData(sheet, len(dictClasses)*(row-2) + row2 + index , 1, f"{day} / {classroom}")
            self.writeData(sheet, index+1, 1, teacher.name)
            for constraint in teacher.constraints:
                
                self.writeData(sheet, len(dictClasses)*(dictDays[constraint.day]-2) + dictClasses[constraint.classroom] + index, dictHours[constraint.dayPeriod], "X", "000000")
                    
            index += len(dictDays)*len(dictClasses)+2



    def writeSchedule(self, schedule):
        sheet = self.wb.create_sheet(index = len(self.sheets) , title = "schedule")
        self.sheets.append(sheet)
        self.writeData(sheet, 1, 1, schedule.getScore())

        hours = sorted(list(set([slot.getSlot().dayPeriod for slot in schedule.schedule])))
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        classes = sorted(list(set([slot.getSlot().classroom for slot in schedule.schedule])))

        dictDays = {day: i+2 for i, day in enumerate(days)}
        dictHours = {hour: i+2 for i, hour in enumerate(hours)}
        dictClasses = {classroom: i+2 for i, classroom in enumerate(classes)}
        for hour, column  in dictHours.items():
            self.writeData(sheet, 1, column, hour)
        for day, row in dictDays.items():
            for classroom, row2 in dictClasses.items():
                self.writeData(sheet, len(dictClasses)*(row-2) + row2, 1, f"{day} / {classroom}")

        for slot in schedule.schedule:
            if slot.getGroup() != None:
                self.writeData(sheet, len(dictClasses)*(dictDays[slot.getSlot().day]-2) + dictClasses[slot.getSlot().classroom], dictHours[slot.getSlot().dayPeriod], f"{slot.getTeacher().name}  / {slot.getGroup().getStudent().name} / {slot.getGroup().getTutor().name} / {slot.getGroup().getApm().name}")



if __name__ == "__main__":
    sm = ScheduleManager()

    slots = list()
    days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
    hours = ["08:50", "09:40", "10:30", "11:20", "14:00", "14:50", "15:40", "16:30"]
    classes = ["salle 01", "salle 02", "salle 03"]

    for day in days:
        for hour in hours: 
            for classe in classes: slots.append(EmptySlot(day, hour, classe))  

    # student1 = Person("Allan", "Des Courtils", 1)
    # student2 = Person("Thibault", "Thomas", 2)
    # student3 = Person("Emilie", "Vey", 3)
    # student4 = Person("Nathan", "Peyronnet", 4)
    # student5 = Person("Benoit", "Kezel", 5)

    # teacher1 = Teacher("Moahammed", "Haddad", 6, [slots[random.randint(0, len(slots)-1)] for i in range(random.randint(0, len(slots)-1))])
    # teacher2 = Teacher("Bastien", "Jerome", 7, [slots[random.randint(0, len(slots)-1)] for i in range(random.randint(0, len(slots)-1))])
    # teacher3 = Teacher("Valerie", "James", 8, [slots[random.randint(0, len(slots)-1)] for i in range(random.randint(0, len(slots)-1))])
    # teacher4 = Teacher("Florence", "Perraud", 9, [slots[random.randint(0, len(slots)-1)] for i in range(random.randint(0, len(slots)-1))])
    # teacher5 = Teacher("Stephane", "Bonnevay", 10, [slots[random.randint(0, len(slots)-1)] for i in range(random.randint(0, len(slots)-1))])

    # apm1 = Apm("Eric", "Judor", 11)
    # apm2 = Apm("Anne", "Hathaway", 12)
    # apm3 = Apm("Jonathan", "Coen", 13)
    # apm4 = Apm("Robert", "De Nirot", 14)

    # group1 = Group(teacher1, apm2, student1)
    # group2 = Group(teacher1, apm1, student2)
    # group3 = Group(teacher2, apm3, student3)
    # group4 = Group(teacher2, apm4, student4)
    # group5 = Group(teacher3, apm4, student5)

    # for slot in slots:
    #     sm.addSlot(slot)

    # sm.addGroup(group1)
    # sm.addGroup(group2)
    # sm.addGroup(group3)
    # sm.addGroup(group4)
    # sm.addGroup(group5)

    # sm.addTeacher(teacher1)
    # sm.addTeacher(teacher2)
    # sm.addTeacher(teacher3)
    # sm.addTeacher(teacher4)
    # sm.addTeacher(teacher5)

    import names

    nb_students = 24
    nb_teachers = 10
    nb_apms = 24

    students = list()
    for i in range(nb_students):
        students.append(Person(names.get_first_name(), names.get_last_name(), i))

    teachers = list()
    for i in range(nb_teachers):
        contraintes = list()
        for j in range(random.randint(0, len(slots)-1)):
            contraintes.append(slots[random.randint(0, len(slots)-1)])
        teachers.append(Teacher(names.get_first_name(), names.get_last_name(), i+nb_students, contraintes))

    apms = list()
    for i in range(nb_apms):
        apms.append(Apm(names.get_first_name(), names.get_last_name(), i+nb_students+nb_teachers))
    
    groups = list()
    for i in range(nb_students):
        groups.append(Group(teachers[random.randint(0, 9)], apms[random.randint(0, 9)], students[i]))

    for slot in slots:
        sm.addSlot(slot)

    for i in range(nb_students):
        sm.addGroup(groups[i])

    for i in range(nb_teachers):
        sm.addTeacher(teachers[i])

    


    
    pop = Population(sm, 100, True)
    #pop.schedules[random.randint(0, 49)]._toString()
    #pop.getBestScore()._toString()

    ga = GA(sm)
    for i in range(0, 100):
        pop = ga.evolvePopulation(pop)

    print(pop.getBestScore().isCorrect())
    writer = WriterExcel("test.xlsx")
    writer.writeSchedule(pop.getBestScore())
    writer.writeConstraintes(sm.teachers, pop.getBestScore())
