import sys

from file_handler import get_files_by_mtime, copy_files, move_copied_file


# TODO(LuHa): considering current working directory
def main(argv = sys.argv):
    '''
    Main function
    :param argv:
    :return:
    '''
    if len(argv) < 3:
        print('Need [SourcePath] [Prefix]')
        sys.exit(0)

    spath = argv[1]
    prefix = argv[2]

    # copy and sort files
    path = get_files_by_mtime(spath)
    fnums = copy_files(path, prefix)
    print('{0} files copied from {1}'.format(fnums, spath))

    # preserve or not
    print('Do you want move copied files to original files?')
    print('If you want to it, original files are deleted')
    print('This function is working in only linux')

    user_input = request_input('Yes(y) or No(n): ')
    if user_input == 'y':
        move_copied_file(spath)
        print('Move copied files to original one')

    print('Program ended')



def request_input(txt = ''):
    user_input = input(txt)
    user_input = user_input.strip()
    user_input = user_input.lower()

    return user_input



if __name__ == '__main__':
    sys.exit(main())
