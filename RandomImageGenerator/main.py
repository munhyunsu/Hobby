import os
import csv
import random
import hashlib

from PIL import Image, ImageFont, ImageDraw

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    print(f'Salt: {FLAGS.salt}')

    os.makedirs(FLAGS.output, exist_ok=True)
    font = ImageFont.truetype('NanumGothic.ttf', size=int(FLAGS.width*FLAGS.height*0.00025))

    print('Number,Name,Salt,Code')
    with open(FLAGS.input, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            number = row['Number']
            name = row['Name']
            data = f'{FLAGS.salt}{number}{name}'.encode('utf-8')
            h = hashlib.sha256(data).hexdigest()
            print(f'{number},{name},{FLAGS.salt},{h}')
            
            image = Image.new('RGB', (FLAGS.width, FLAGS.height))
            draw = ImageDraw.Draw(image, 'RGB')
            draw.text((int(FLAGS.width*0.05), int(FLAGS.height*0.5)), h[:8], font=font)
            path = os.path.join(FLAGS.output, f'{number}.jpg')
            with open(path, 'wb') as f:
                image.save(f, 'JPEG')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--input', required=True,
                        help='The input csv file for members')
    parser.add_argument('--salt', default=random.getrandbits(64),
                        help='The salt number')
    parser.add_argument('--width', type=int, default=800,
                        help='The width')
    parser.add_argument('--height', type=int, default=600,
                        help='The height')
    parser.add_argument('--output', default='output',
                        help='The output directory')

    FLAGS, _ = parser.parse_known_args()
    FLAGS.input = os.path.abspath(os.path.expanduser(FLAGS.input))
    FLAGS.output = os.path.abspath(os.path.expanduser(FLAGS.output))
    DEBUG = FLAGS.debug

    main()
