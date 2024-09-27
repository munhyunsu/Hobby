import os
import sys
import logging # debug, info, warning, error, critical
import time
import csv

import numpy as np
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

    base_latitude = abs(90) + abs(-90)
    base_longitude = abs(180) + abs(-180)

    size_latitude = base_latitude / 2**FLAGS.level
    size_longitude = base_longitude / 2**FLAGS.level

    cluster_labels = []
    stime = time.time()
    for latitude, longitude in dataset:
        index_latitude = latitude//size_latitude
        position_latitude = latitude%size_latitude
        index_longitude = longitude//size_longitude
        position_longitude = longitude%size_longitude
        
        #start_geoid = (1-4**FLAGS.level)//-3
        ## 0
        ## 1 2 3 4
        ## 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
        ## 21

        division = 2**FLAGS.level
        locid = int(division*index_latitude + index_longitude)
        cluster_labels.append(locid)
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
    parser.add_argument('--output', default=f'ours_{int(time.time())}.csv',
                        help='CSV output')
    parser.add_argument('--level', default=16, type=int,
                        help='Clustering zoom level')

    FLAGS, _ = parser.parse_known_args()
    logging.basicConfig(level=FLAGS.logging)

    main()

