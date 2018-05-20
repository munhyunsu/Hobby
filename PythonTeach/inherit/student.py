import people

class Student(people.People):
    def __init__(self, name, student_number):
        super().__init__(name)
        self.student_number = student_number

    def print_info(self):
        print('Student {0}, {1}.'.format(self.name, self.student_number))
