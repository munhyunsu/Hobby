import os
import shlex
import subprocess

from file_handler import get_files


def main(_):
    # make output directory
    os.makedirs(FLAGS.output, exist_ok=True)

    print('Start unzip')
    for ipath in get_files(FLAGS.input, ext='.zip'):
        filename = os.path.basename(ipath)[:-4]
        opath = os.path.join(FLAGS.output, filename)
        command_line = 'unzip -O {0} -d \'{1}\' \'{2}\''.format(
          FLAGS.encoding, opath, ipath)
        command = shlex.split(command_line)
        print(command)
        subprocess.run(command)
    print('Complete unzip')


if __name__ == '__main__':
    import argparse

    # Set arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='directory zip files are stored')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='directory unzip files will be stored')
    parser.add_argument('-e', '--encoding', type=str, default='CP949',
                        help='zip file encoding')
    FLAGS, _ = parser.parse_known_args()

    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))

    main(_)

