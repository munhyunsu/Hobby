import re
from operator import itemgetter, methodcaller


def split_head_number_tail(target):
    number = re.findall(r'(\d+)', target)[0]
    number_sindex = target.find(number)
    number_eindex = number_sindex + len(number)
    head = target[:number_sindex]
    number = target[number_sindex:number_eindex]
    tail = target[number_eindex:]

    return head, number, tail


def append_incase_int(target):
    return target[0], target[1], target[2], target[0].lower(), int(target[1])


def go_sort(target):
    nodes = list()
    for entry in target:
        result = split_head_number_tail(entry)
        result = append_incase_int(result)
        nodes.append(result)

    nodes.sort(key=itemgetter(3, 4))

    for index in range(0, len(nodes)):
        nodes[index] = ''.join(nodes[index][0:3])

    return nodes


def main():
    x = 'foo9.txt'
    print(split_head_number_tail(x))
    y = 'foo010bar020.zip'
    print(split_head_number_tail(y))
    z = 'F-15'
    print(split_head_number_tail(z))


if __name__ == '__main__':
    main()
