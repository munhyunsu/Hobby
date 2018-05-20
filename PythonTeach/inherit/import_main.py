import sys
import people

def main(argv = sys.argv):
    name = argv[1]

    user = people.People(name)

    user.print_name()


if __name__ == '__main__':
    sys.exit(main())
