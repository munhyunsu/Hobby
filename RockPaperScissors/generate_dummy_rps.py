import csv
import time
import random


def main():
    with open('dummy.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['unixtime', 'userid', 'hand', 'score'])
        for users in range(0, 100):
            userid = random.randint(1000000000, 9999999999)
            for rounds in range(0, 1000):
                unixtime = random.randint(1514764800, 1546298639)
                hand = random.randint(1, 3)
                score = random.randint(1, 3)
                writer.writerow([unixtime, userid, hand, score])

if __name__ == '__main__':
    main()
