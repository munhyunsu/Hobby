import os
import csv
import datetime
from operator import itemgetter

FLAGS = None


def get_second_item_size(item):
    return item[0], len(item[1])


def main(_):
    with open(FLAGS.input, 'r') as f:
        reader = csv.DictReader(f)
        # declare variable area
        if FLAGS.question == 1: # Q1
            count = 0
            site_dict = dict()
        elif FLAGS.question == 2: # Q2
            pivot1 = datetime.datetime(2019, 2, 3,
                                       hour=0, minute=0, second=0)
            pivot2 = datetime.datetime(2019, 2, 4,
                                       hour=23, minute=59, second=59)
            user_dict = dict()
            answer_dict = dict()
        elif FLAGS.question == 3:
            default_datetime = datetime.datetime(1989, 6, 8,
                                                 hour=0, minute=0, second=0)
            user_dict = dict()
            site_dict = dict()
        elif FLAGS.question == 4:
            default_datetime1 = datetime.datetime(1989, 6, 8,
                                                  hour=0, minute=0, second=0)
            default_datetime2 = datetime.datetime(2189, 6, 8,
                                                  hour=0, minute=0, second=0)
            user_dict = dict()
            

        # process data area
        for row in reader:
            ts = datetime.datetime.strptime(row['ts'],
                                            '%Y-%m-%d %H:%M:%S')
            user_id = row['user_id']
            country_id = row['country_id']
            site_id = row['site_id']
            if FLAGS.question == 1: # Q1
                if country_id != 'BDV': # condition
                    continue
                count = count+1 # Maybe it is 844
                # Add user_id to site_id dict
                user_set = site_dict.get(site_id, set())
                user_set.add(user_id)
                site_dict[site_id] = user_set
            elif FLAGS.question == 2: # Q2
                if not (pivot1 < ts and ts < pivot2): # condition
                    continue
                site_dict = user_dict.get(user_id, dict())
                visit_num = site_dict.get(site_id, 0) + 1
                site_dict[site_id] = visit_num
                user_dict[user_id] = site_dict
                if visit_num >= 10:
                    answer_dict[user_id] = (site_id, visit_num)
            elif FLAGS.question == 3: # Q3
                last_ts = user_dict.get(user_id, (default_datetime, None))[0]
                if last_ts < ts:
                    user_dict[user_id] = (ts, site_id)
            elif FLAGS.question == 4: # Q4
                user_data = user_dict.get(user_id, [default_datetime2, None,
                                                    default_datetime1, None])
                if ts < user_data[0]:
                    user_data[0] = ts
                    user_data[1] = site_id
                if ts > user_data[2]:
                    user_data[2] = ts
                    user_data[3] = site_id
                user_dict[user_id] = user_data

        # analysis or print data area
        if FLAGS.question == 1: # Q1
            # get largest unique user
            site_list = list(map(get_second_item_size, site_dict.items()))
            site_list.sort(key=itemgetter(1), reverse=True)
            msg = ('The site which has '
                   'largest number of unique users is \'{0}\' '
                   'and the number is {1}')
            print(msg.format(site_list[0][0], site_list[0][1]))
        elif FLAGS.question == 2: # Q2
            print('UserId,SiteId,NumberOfVisits')
            for key, value in answer_dict.items():
                print(key, value[0], value[1], sep=',')
        elif FLAGS.question == 3: # Q3
            for key in user_dict.keys():
                site_id = user_dict[key][1]
                site_dict[site_id] = site_dict.get(site_id, 0) + 1
            site_list = list(site_dict.items())
            site_list.sort(key=itemgetter(1), reverse=True)
            print('SiteId,NumberOfVisits')
            for site_id, visit_num in site_list[:3]:
                print(site_id, visit_num, sep=',')
        elif FLAGS.question == 4: # Q4
            first_last_same = 0
            for key in user_dict.keys():
                user_data = user_dict[key]
                if user_data[1] == user_data[3]:
                    first_last_same = first_last_same + 1
            msg = ('The number of users whose first/last visits are '
                   'to the same website is {0}')
            print(msg.format(first_last_same))
            first_last_same = 0
            for key in user_dict.keys():
                user_data = user_dict[key]
                if (user_data[0] != user_data[2] and 
                        user_data[1] == user_data[3]):
                    first_last_same = first_last_same + 1
            msg = ('If the user who has only one connection is removed, '
                   'then the number of users is {0}')
            print(msg.format(first_last_same))
            

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str,
                        help='Input file path')
    parser.add_argument('-q', '--question', required=True, type=int,
                        help='Question number')
    FLAGS, _ = parser.parse_known_args()

    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))

    main(_)

