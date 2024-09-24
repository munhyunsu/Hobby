import os
import sys
import logging # debug, info, warning, error, critical
import time
import csv

from sklearn.cluster import KMeans
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
    max_n_cluster = -1
    max_silhouette_avg = 0
    for i in range(2, 100, 1):
        stime = time.time()
        clusterer = KMeans(n_clusters=i)
        cluster_labels = clusterer.fit_predict(dataset)
        silhouette_avg = silhouette_score(dataset, cluster_labels)
        if max_silhouette_avg <= silhouette_avg:
            max_n_cluster = i
            max_silhouette_avg = silhouette_avg
            print(f'[Updated] {max_n_cluster}, {max_silhouette_avg}')
        etime = time.time()
        print(f'[{i}] {silhouette_avg} via {(etime-stime)*1000}')


if __name__ == '__main__':
    os.chdir(sys.path[0])
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--logging', default='WARNING',
                        choices=logging._nameToLevel.keys(),
                        help='Set log level (default: WARNING)')
    parser.add_argument('--input', required=True,
                        help='CSV input (latitude, longitude)')
    parser.add_argument('--output', default=f'kmeans_{int(time.time())}.csv',
                        help='CSV output')

    FLAGS, _ = parser.parse_known_args()
    logging.basicConfig(level=FLAGS.logging)

    main()

