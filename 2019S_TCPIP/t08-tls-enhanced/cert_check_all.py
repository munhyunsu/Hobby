import socket
import ssl
import json
import hashlib

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
            bcert = ssock.getpeercert(binary_form=True)
            cert_sha256 = hashlib.sha256(bcert).hexdigest().upper()
            if FLAGS.input not in pin.keys():
                print('{0} is not in pin file'.format(FLAGS.input))
                return
            pin_sha256 = ''.join(pin[FLAGS.input].split(':')).upper()
            if cert_sha256 == pin_sha256:
                print('Valid Certificate!')
            else:
                print('Invalid Certificate!')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Target server name')
    parser.add_argument('-p', '--pin', type=str,
                        help='Pinning information')

    FLAGS, _ = parser.parse_known_args()
    main(_)

