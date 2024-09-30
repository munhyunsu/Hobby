import os
import sys
import logging # debug, info, warning, error, critical
import time
import csv

import numpy as np
import pandas as pd
from geopy.distance import great_circle
from sklearn.metrics import pairwise_distances
from sklearn.metrics import silhouette_score


FLAGS = _ = None


def compute_cluster_centers(df):
    cluster_centers = df.groupby('cluster')[['latitude', 'longitude']].mean()
    return cluster_centers


def average_distance_to_center(df, cluster_centers):
    distances = []
    for _, row in df.iterrows():
        cluster_center = cluster_centers.loc[row['cluster']]
        dist = great_circle((row['latitude'], row['longitude']), (cluster_center['latitude'], cluster_center['longitude'])).kilometers
        distances.append(dist)
    return np.mean(distances)


def average_distance_between_centers(cluster_centers):
    center_coords = cluster_centers[['latitude', 'longitude']].values
    distances = pairwise_distances(center_coords, metric=lambda u, v: great_circle(u, v).kilometers)
    return np.mean(distances[np.triu_indices(len(cluster_centers), k=1)])


def main():
    logging.debug(f'Parsed arguments: {FLAGS}')
    logging.debug(f'Unparsed arguments: {_}')

    df = pd.read_csv(FLAGS.input)
    X = df[['latitude', 'longitude']]
    y = df['cluster']

    print(f'{FLAGS.input} analysis result: ')
    print(f'The number of cluster: {y.nunique()}')
    cluster_centers = compute_cluster_centers(df)
    avg_distance_to_center = average_distance_to_center(df, cluster_centers)
    print(f'The average distance within cluster: {avg_distance_to_center}km')
    avg_distance_between_centers = average_distance_between_centers(cluster_centers)
    print(f'The average distance between each cluster: {avg_distance_between_centers}km')
    silhouette_avg = silhouette_score(X, y)
    print(f'The average of Silhouette score: {silhouette_avg}')
    
    



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

