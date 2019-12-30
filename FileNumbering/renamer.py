import os

from file_obj import File

FLAGS = None



def main():
    print(f'Args: {FLAGS}')
    
    with os.scandir(FLAGS.input_dir) as it:
        for entry in it:
            if entry.is_file():
                fpath = entry.path
                fobj = File(fpath)
                head, tail = os.path.split(fpath)
                _, ext = os.path.splitext(tail)
                dst = os.path.join(head, f'{fobj.sha256}{ext}')
                fobj.move(dst)
                print(f'{fpath}\n->{dst}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', type=str, required=True)
    
    FLAGS, _ = parser.parse_known_args()

    FLAGS.input_dir = os.path.abspath(os.path.expanduser(FLAGS.input_dir))

    main()

