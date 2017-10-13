#!/bin/usr/env python3

# exit, argv
import sys
# csv
import csv

HEADER = ['BallSprite', 'Number', 'Species', 'Nature', 'Ability',
          'Move1', 'Move2', 'Move3', 'Move4', 'Ball']
NUMDATA = None

def main(argv):
    """
    main function
    """
    # for arguments
    if len(argv) > 1:
        target = argv[1]
    else:
        target = 'input.csv'

    # reader, writer
    input_file = open(target, 'r')
    reader = csv.DictReader(input_file)
    output_file = open('output.csv', 'w')
    writer = csv.DictWriter(output_file, fieldnames = HEADER,
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

    # loop and write
    for row in reader:
        output_data = get_row_dict(row)
        writer.writerow(output_data)

    # reader, writer close
    input_file.close()
    output_file.close()



def get_row_dict(box):
    # result variable initialize
    # copy data from box report based on HEADER
    result = dict()
    for key in HEADER:
        if key in box:
            result[key] = box[key]
        else:
            result[key] = ''

    # fill the new data
    result['BallSprite'] = ''
    result['Number'] = get_pokemon_number(result['Species'])

    # return row dict
    return result



def get_pokemon_number(species):
    global NUMDATA
    # initialize data
    if NUMDATA == None:
        NUMDATA = dict()
        with open('data_name_number', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                NUMDATA[row['species']] = row['number']

    # return number of species
    if species in NUMDATA:
        return NUMDATA[species]
    else:
        0




if __name__ == '__main__':
    sys.exit(main(sys.argv))
