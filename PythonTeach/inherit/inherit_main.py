import sys
import people
import student
import teacher

def main(argv = sys.argv):
    user1 = people.People('쟁반통닭')
    user1.print_info()

    user2 = student.Student('Hyunsu', '201550320')
    user2.print_info()

    user3 = teacher.Teacher('정화', '133442')
    user3.print_info()
    user3.set_lecture('영어')
    user3.print_lecture()


if __name__ == '__main__':
    sys.exit(main())
