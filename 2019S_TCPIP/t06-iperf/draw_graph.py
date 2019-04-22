import matplotlib.pyplot as plt
import pandas as pd

FLAGS = None


def main(_):
    print(FLAGS)
    data = pd.read_csv(FLAGS.input, header=None)
    plt.plot(data[0], data[3], '.-')
    plt.title(FLAGS.input)
    plt.xlabel('Time (s)')
    plt.ylabel('Congestion window size')
    if FLAGS.output is not None:
        plt.savefig(FLAGS.output)
    else:
        plt.show()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='draw target csv file')
    parser.add_argument('-o', '--output', type=str,
                        help='output plot file (png)')
    FLAGS, _ = parser.parse_known_args()

    main(_)

