import people

class Teacher(people.People):
    def __init__(self, name, teacher_number):
        super().__init__(name)
        self.teacher_number = teacher_number
        self.lecture = None

    def print_info(self):
        super().print_info()
        print('Teacher {0}.'.format(self.teacher_number))

    def set_lecture(self, lecture):
        self.lecture = lecture

    def print_lecture(self):
        print('Teacher {0}.'.format(self.lecture))
