import numpy as np

FLAGS = None

def get_levenshtein_table(x, y):
    # Create table for dynamic programming
    len_x = len(x) # for multiple usage
    len_y = len(y)
    table = np.zeros((len_x+1, len_y+1), dtype=int) 
    # Initialize variable for Levenshtein distance
    for index in range(1, len_x+1):
        table[index, 0] = index
    for index in range(1, len_y+1):
        table[0, index] = index
    
    for index_x in range(1, len_x+1):
        for index_y in range(1, len_y+1):
            if x[index_x-1] == y[index_y-1]:
                distance = 0
            else:
                distance = 1
            table[index_x, index_y] = \
              min(table[index_x-1, index_y]+1, # deletion
                  table[index_x, index_y-1]+1, # addition
                  table[index_x-1, index_y-1]+distance) # subtitution
    return table




def equalsWhenOneCharRemoved(x, y, life=1):
    # get Levenshtein distance table
    table = get_levenshtein_table(x, y)

    # Go backtracking
    # for easy understanding
    #[[0 1 2 3]
    # [1 0 1 2]
    # [2 1 0 1]
    # [3 2 1 1]]
    path_queue = list() # Use like queue
    path_queue.append((len(x), len(y), life)) # initial life 1
    while len(path_queue) != 0:
        index_x, index_y, life = path_queue.pop(0)
        if table[index_x, index_y] == 0: # Check is it goal?
            return True
        # get all pathes and minimum path
        left = table[index_x, index_y-1]
        top_left = table[index_x-1, index_y-1]
        top = table[index_x-1, index_y]
        min_path = min(left, top_left, top)
        # number of cases
        if min_path == left: # addition
            next_life = life-1
            if next_life >= 0:
                path_queue.append((index_x, index_y-1, next_life))
        if min_path == top: # deletion
            next_life = life-1
            if next_life >= 0:
                path_queue.append((index_x-1, index_y, next_life))
        if min_path == top_left: 
            if x[index_x-1] == y[index_y-1]: # equal
                path_queue.append((index_x-1, index_y-1, life))

    return False


def main(_):
    print(equalsWhenOneCharRemoved(FLAGS.str_x, FLAGS.str_y, FLAGS.life))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-x', '--str_x', required=True, type=str,
                        help='String X')
    parser.add_argument('-y', '--str_y', required=True, type=str,
                        help='String Y')
    parser.add_argument('-l', '--life', default=1, type=int,
                        help='Allowed maximum string distance')
    FLAGS, _ = parser.parse_known_args()

    main(_)

