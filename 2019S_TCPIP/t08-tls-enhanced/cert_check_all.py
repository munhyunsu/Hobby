import socket
import ssl
import json

FLAGS = None


def main(_):
    print('Unparsed args {0}'.format(_))

    if FLAGS.pin is not None:
        with open(FLAGS.pin, 'r') as f:
            pin = json.load(f)
    else:
        pin = dict()

    with socket.create_connection((FLAGS.input, 443)) as sock:
        context = ssl.create_default_context()
        with context.wrap_socket(sock, 
          server_hostname=FLAGS.input) as ssock:
            print(ssock)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Target server name')
    parser.add_argument('-p', '--pin', type=str,
                        help='Pinning information')

    FLAGS, _ = parser.parse_known_args()
    main(_)

