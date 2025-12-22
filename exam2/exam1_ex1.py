import enum

class TaskStatus(enum.Enum):
    IN_PROCESS = ('В процессе')
    DONE = ('Завершено')


class Employee:
    def __init__(self, name, position, salary, hours_worked=0):
        self.name = name
        self.position = position
        self.salary = salary
        self.hours_worked = hours_worked

    def add_hours(self, hours):
        self.hours_worked += hours

    def calculate_pay(self):
        working_hours_in_month = 20 * 8  # кол-во раб. дней в месяце * кол-во раб. часов в 1 раб. дне
        value_of_one_hour = self.salary / working_hours_in_month  # стоимость 1 раб. часа
        return value_of_one_hour * self.hours_worked


class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.status = TaskStatus.IN_PROCESS
        self.assigned_employee = None

    def assign_employee(self, employee):
        self.assigned_employee = employee

    def mark_complete(self):
        self.status = TaskStatus.DONE

    def is_complete(self):
        return self.status == TaskStatus.DONE


class Project:
    def __init__(self, title, tasks=None):
        self.title = title
        if tasks is None:
            self.tasks = []
        else:
            self.tasks = tasks

    def add_task(self, task):
        self.tasks.append(task)

    def project_progress(self):
        count_of_completed_tasks = sum(1 for task in self.tasks if task.is_complete())
        return count_of_completed_tasks * 100 / len(self.tasks)


if __name__ == '__main__':
    harry = Employee('Harry', 'Middle', 100)
    hermione = Employee('Hermione', 'Middle+', 110)
    ron = Employee('Ron', 'Middle-', 90)
    dumbledore = Employee('Dumbledore', 'Senior+', 220, 20)
    mc_gonagall = Employee('McGonagall', 'Senior', 200, 30)
    hagrid = Employee('Hagrid', 'Senior-', 180, 15)

    kill_evil = Task('Kill evil', 'Kill all evil')
    pass_exams = Task('Pass exams', 'Pass all exams with excellent marks')
    do_not_disturb_others = Task('Do not disturb others', 'Do not disturb others in their tasks')
    protect_hogwarts = Task('Protect Hogwarts', 'Protect Hogwarts against evil')
    teach = Task('Teach', 'Teach students')
    raise_creatures = Task('Raise creatures', 'Raise all sorts of creatures')

    main_project = Project('Main Project')
    sub_project = Project('Sub Project')
    minor_project = Project('Minor Project', [do_not_disturb_others, raise_creatures])

    kill_evil.assign_employee(harry)
    pass_exams.assign_employee(hermione)
    do_not_disturb_others.assign_employee(ron)
    protect_hogwarts.assign_employee(dumbledore)
    teach.assign_employee(mc_gonagall)
    raise_creatures.assign_employee(hagrid)

    employees = [harry, hermione, ron, dumbledore, mc_gonagall, hagrid]
    tasks = [kill_evil, pass_exams, do_not_disturb_others, protect_hogwarts, teach, raise_creatures]
    projects = [main_project, sub_project, minor_project]

    main_project.add_task(kill_evil)
    main_project.add_task(protect_hogwarts)
    sub_project.add_task(pass_exams)
    sub_project.add_task(teach)

    print("Init pay:")
    for employee in employees:
        print(f'{employee.name} - {employee.calculate_pay()}')

    print()
    print("Init project progress:")
    for project in projects:
        print(f'{project.title} - {project.project_progress()}')

    harry.add_hours(160)
    hermione.add_hours(160)
    ron.add_hours(160)
    dumbledore.add_hours(140)
    mc_gonagall.add_hours(130)
    hagrid.add_hours(145)

    kill_evil.mark_complete()
    pass_exams.mark_complete()
    do_not_disturb_others.mark_complete()
    protect_hogwarts.mark_complete()
    teach.mark_complete()
    raise_creatures.mark_complete()

    print()
    print("Final pay:")
    for employee in employees:
        print(f'{employee.name} - {employee.calculate_pay()}')

    print()
    print("Final project progress:")
    for project in projects:
        print(f'{project.title} - {project.project_progress()}')


