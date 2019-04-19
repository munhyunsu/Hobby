import webbrowser
import requests
import hashlib

FLAGS = None


def main(_):
    # args to dict
    flag_var = vars(FLAGS)

    # get initial code
    url = 'https://api.meethue.com/oauth2/auth?clientid={clientid}&appid=remoteapp&deviceid={deviceid}&devicename=&state=&response_type=code'.format_map(flag_var)
    r = webbrowser.open_new(url)
    print('If error occured, open {0} manually'.format(url))
    print('Do login, and grant access')
    res_url = input('Input the responsed URL: ')
    flag_var['code'] = res_url.split('=')[-1]

    # get realm, nonce
    url = 'https://api.meethue.com/oauth2/token?code={code}&grant_type=authorization_code'.format_map(flag_var)
    r = requests.post(url)
    flag_var['realm'] = r.headers['WWW-Authenticate'].split('"')[1]
    flag_var['nonce'] = r.headers['WWW-Authenticate'].split('"')[3]

    # calculate md5
    m = hashlib.md5()
    m.update('{clientid}:{realm}:{clientsecret}'.format_map(flag_var).encode('utf-8'))
    hash1 = m.hexdigest()
    m = hashlib.md5()
    m.update('POST:/oauth2/token'.encode('utf-8'))
    hash2 = m.hexdigest()
    m = hashlib.md5()
    m.update('{0}:{1}:{2}'.format(hash1, flag_var['nonce'], hash2).encode('utf-8'))
    flag_var['response'] = m.hexdigest()

    # making autorization
    auth = ('Digest username="{clientid}", '
            'realm="{realm}", '
            'nonce="{nonce}", '
            'uri="/oauth2/token", '
            'response="{response}"').format_map(flag_var)
    header = {'Authorization': auth}

    # get token
    url = 'https://api.meethue.com/oauth2/token?code={code}&grant_type=authorization_code'.format_map(flag_var)
    r = requests.post(url, headers = header)

    print(r.headers)
    print(r.content.encode('utf-8'))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clientid', required=True,
                        help='client id')
    parser.add_argument('-s', '--clientsecret', required=True,
                        help='client secret')
    parser.add_argument('-a', '--appid', required=True,
                        help='app id')
    parser.add_argument('-d', '--deviceid', required=True,
                        help='device id')

    FLAGS, _ = parser.parse_known_args()


    main(_)

