#!/bin/usr/env python3

# exit, argv
import sys
# csv
import csv

def main(argv):
    input_file = open('input.csv', 'r')
    reader = csv.DictReader(input_file)

    output_file = open('output.csv', 'w')
    fieldnames = ['A',
                  'B'
                 ]
    writer = csv.DictWriter(output_file, fieldnames = fieldnames,
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

    for row in reader:
        name = row['name']
        if name == 'a':
            name = '나몰뺴미'
        writer.writerow({'A': name, 
                         'B': row['abi1']}
                       )


    input_file.close()
    output_file.close()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
