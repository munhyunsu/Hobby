import sys


DEBUG = True
MAXNUM = 2**31


def dprint(data):
    if DEBUG:
        print(data)


class BigInt(object):
    def __init__(self, num):
        if type(num) == list:
            self.data = num
        else:
            self.data = list()
            self.data.append(num%MAXNUM)

    def __str__(self):
        st = ''
        for index in range(0, len(self.data)):
            if len(st) > 0:
                st = st + ' + '
            st = st + '{0} * {1}^{2}'.format(self.data[index], MAXNUM, index)
        return st
    
    def __add__(self, o):
        nlst = list()
        midx = max(len(self.data), len(o.data))

        for index in range(0, midx):
            if index < len(self.data):
                a = self.data[index]
            else:
                a = 0
            if index < len(o.data):
                b = o.data[index]
            else:
                b = 0
            nlst.append(a+b)

        for index in range(0, len(nlst)):
            if nlst[index] >= MAXNUM:
                nlst[index] = nlst[index] - MAXNUM
                if index == len(nlst)-1:
                    nlst.append(1)
                else:
                    nlst[index+1] = nlst[index+1] + 1

        nobj = BigInt(0)
        nobj.data = nlst
        return nobj


def main(argv):
    print('Argv: ', argv)
    numlst = map(int, argv[1:])
    dprint(numlst)    
    blst = list(map(BigInt, numlst))
    for entry in blst:
        dprint(entry)

    result = BigInt(0)
    for entry in blst:
        result = result + entry

    print(result)
    





if __name__ == '__main__':
    main(sys.argv)

