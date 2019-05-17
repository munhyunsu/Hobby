
def check_equal(a, b):
    a1 = ord(a[0])
    a2 = int(a[1])
    b1 = ord(b[0])
    b2 = int(b[1])

    if (a1 + a2)%2 == 0:
        aa = True
    else:
        aa = False

    if (b1 + b2)%2 == 0:
        bb = True
    else:
        bb= False

    if aa and bb:
        return True
    else:
        return False


def main():
    print(check_equal('A4', 'B2')) # False
    print(check_equal('E5', 'H8')) # True
    print(check_equal('C2', 'F7')) # True


if __name__ == '__main__':
    main()

