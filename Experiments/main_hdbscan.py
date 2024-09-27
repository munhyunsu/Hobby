import os
import sys
import logging # debug, info, warning, error, critical
import time
import csv

import numpy as np
from sklearn.cluster import HDBSCAN
from sklearn.metrics import silhouette_score


FLAGS = _ = None


def main():
    logging.debug(f'Parsed arguments: {FLAGS}')
    logging.debug(f'Unparsed arguments: {_}')

    dataset = []
    with open(FLAGS.input, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append((float(row['latitude']), float(row['longitude'])))
    stime = time.time()
    clusterer = HDBSCAN()
    cluster_labels = clusterer.fit_predict(dataset)
    etime = time.time()
    silhouette_avg = silhouette_score(dataset, cluster_labels)
    print(f'{len(np.unique(cluster_labels))} {silhouette_avg} via {(etime-stime)*1000}')
    with open(FLAGS.output, 'w') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['latitude', 'longitude', 'cluster'],
            quoting=csv.QUOTE_MINIMAL,
            lineterminator=os.linesep
        )
        writer.writeheader()
        for (latitude, longitude), cluster in zip(dataset, cluster_labels):
            writer.writerow({
                'latitude': latitude,
                'longitude': longitude,
                'cluster': cluster
            })


if __name__ == '__main__':
    os.chdir(sys.path[0])
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', default='WARNING',
                        choices=logging._nameToLevel.keys(),
                        help='Set log level (default: WARNING)')
    parser.add_argument('--input', required=True,
                        help='CSV input (latitude, longitude)')
    parser.add_argument('--output', default=f'hdbscan_{int(time.time())}.csv',
                        help='CSV output')

    FLAGS, _ = parser.parse_known_args()
    logging.basicConfig(level=FLAGS.logging)

    main()

