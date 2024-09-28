import os
import sys
import logging # debug, info, warning, error, critical
import time
import csv

import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score


FLAGS = _ = None


def main():
    logging.debug(f'Parsed arguments: {FLAGS}')
    logging.debug(f'Unparsed arguments: {_}')

    df = pd.read_csv(FLAGS.input)
    X = df[['latitude', 'longitude']]
    y = df[['cluster']]

    silhouette_avg = silhouette_score(dataset, cluster_labels)
    print(f'{FLAGS.input} analysis result: ')


if __name__ == '__main__':
    os.chdir(sys.path[0])
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', default='WARNING',
                        choices=logging._nameToLevel.keys(),
                        help='Set log level (default: WARNING)')
    parser.add_argument('--input', required=True,
                        help='CSV input (latitude, longitude)')

    FLAGS, _ = parser.parse_known_args()
    logging.basicConfig(level=FLAGS.logging)

    main()

