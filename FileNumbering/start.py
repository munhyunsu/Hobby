import sys

from file_handler import get_files_by_mtime

def main(argv = sys.argv):
    '''
    Main function
    :param argv:
    :return:
    '''
    if len(argv) < 2:
        print('Need input path')
        sys.exit(0)

    for path in get_files_by_mtime(argv[1]):
        print(path)



if __name__ == '__main__':
    sys.exit(main())