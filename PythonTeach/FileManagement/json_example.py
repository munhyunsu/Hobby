import json

def main():
    with open('sample1.json') as f:
        json_data = json.load(f)

    print(json_data['firstName'], json_data['lastName'], json_data['age'])
    print(json_data['address']['city'])
    print(json_data['phoneNumber'][0]['number'])


if __name__ == '__main__':
    main()