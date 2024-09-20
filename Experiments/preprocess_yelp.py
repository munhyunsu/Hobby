import os
import sys
import json


os.chdir(sys.path[0])

data_path = os.path.join('rawdata/yelp_dataset', 'yelp_academic_dataset_business.json')

output_file = open('data/yelp.csv', 'w')
output_csv = csv.DictWriter(
    output_file,
    fieldnames=['latitude', 'longitude'],
    quoting=csv.QUOTE_MINIMAL,
    lineterminator=os.linesep
)
output_csv.writeheader()

with open(data_path, 'r') as f:
    for line in f:
        line_json = json.loads(line)
        output_csv.writerow({'latitude': line_json['latitude'],
                             'longitude': line_json['longitude']})
output_file.close()

