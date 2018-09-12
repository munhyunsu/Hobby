import sys
import copy

from table_utils import print_table_dict
from table import TimeTable


def main(argv=sys.argv):
    if len(argv) < 2:
        sys.exit(0)
    target = argv[1]
    print('reading... {0}'.format(target))

    timetable = TimeTable(target)
    # print(timetable.get_slot())
    print('----+ 변경가능한 선생 ----+')
    print_table_dict(timetable.get_slot())
    print(len(timetable.get_slot().keys()))
    print('----+ 변경해야하는 선생 ----+')
    print_table_dict(timetable.get_target())
    print(len(timetable.get_target().keys()))


if __name__ == '__main__':
    main()
