import socket
import ssl
import json
import hashlib
import base64

import OpenSSL

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
            x509 = OpenSSL.crypto.load_certificate(
              OpenSSL.crypto.FILETYPE_ASN1, bcert)
            pubkey = x509.get_pubkey()
            bpubkey = OpenSSL.crypto.dump_publickey(
              OpenSSL.crypto.FILETYPE_ASN1, pubkey)
            b64sha256_pubkey = base64.b64encode(
              hashlib.sha256(bpubkey).digest()).decode('utf-8')
            if FLAGS.input not in pin.keys():
                print('{0} is not in pin file'.format(FLAGS.input))
                return
            pin_sha256 = pin[FLAGS.input]
            if b64sha256_pubkey == pin_sha256:
                import pprint
                pprint.pprint(ssock.getpeercert())
                
                print('Valid Certificate!')
            else:
                print('Invalid Certificate!')
                print('B64SHA256', b64sha256_pubkey)
                print('PIN', pin_sha256)
                print('Pubkey', OpenSSL.crypto.dump_publickey(
                  OpenSSL.crypto.FILETYPE_PEM, pubkey))
                import pprint
                pprint.pprint(ssock.getpeercert())


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='Target server name')
    parser.add_argument('-p', '--pin', type=str,
                        help='Pinning information')

    FLAGS, _ = parser.parse_known_args()
    main(_)

