import sys


def main(argv):
    src = argv[1]
    src_file = open(src, 'r')
    dst_file = open('output', 'w')
    dst_file.write('OOoUserDict1\n')
    dst_file.write('lang: <none>\n')
    dst_file.write('type: positive\n')
    dst_file.write('---\n')
    
    for line in src_file:
        if len(line.split('/')) < 2:
            continue
        dst_file.write(line.split('/')[0]+'\n')

    src_file.close()
    dst_file.close()


if __name__ == '__main__':
    ys.exit(main(sys.argv))

