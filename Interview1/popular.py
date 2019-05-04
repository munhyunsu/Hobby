import os
import csv
import json
from operator import itemgetter

FLAGS = None


def get_uid_size(item):
    return item[0], len(item[1])


def get_pid_only(item):
    return item[0]


def data_reader(path):
    # prepare goal variable
    purchasers = dict()
    quantities = dict()
    # read data
    with open(FLAGS.input, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data = json.loads(row[0]) # load json
            uid = data['user_id']
            pid = data['product_id']
            quantity = data['quantity']
            # statistics
            user_set = purchasers.get(pid, set())
            user_set.add(uid)
            purchasers[pid] = user_set
            quantities[pid] = quantities.get(pid, 0) + quantity
    return purchasers, quantities


def get_top_tiers(item_list):
    # slice items when ties
    item_len = len(item_list)
    pivot = 1
    while pivot < item_len:
        if item_list[pivot-1][1] == item_list[pivot][1]:
            pivot = pivot + 1
        else:
            break
    return item_list[:pivot]


def main(_):
    # read data
    purchasers, quantities = data_reader(FLAGS.input)

    # calculate purchasers size and rank
    purchasers_list = list(map(get_uid_size, purchasers.items()))
    purchasers_list.sort(key=itemgetter(1), reverse=True)
    # calculate quantities size and rank
    quantities_list = list(quantities.items())
    quantities_list.sort(key=itemgetter(1), reverse=True)

    # get top tier list
    purchasers_list = get_top_tiers(purchasers_list)
    quantities_list = get_top_tiers(quantities_list)

    # export only pid
    purchasers_list = list(map(get_pid_only, purchasers_list))
    quantities_list = list(map(get_pid_only, quantities_list))

    # print    
    msg = 'Most popular product(s) based on the number of purchasers: {0}'
    print(msg.format(purchasers_list))
    msg = 'Most popular product(s) based on the quantity of goods sold: {0}'
    print(msg.format(quantities_list))
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str,
                        help='Input file path')
    FLAGS, _ = parser.parse_known_args()

    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))

    main(_)

