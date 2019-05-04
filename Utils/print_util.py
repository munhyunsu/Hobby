def pprint(data, style=0):
    """
    """
    if style == 0:
        print('\x1B[33m\x1B[100m{0}\x1B[0m'.format(data))

def pinput(data, style=0):
    """
    """
    if style == 0:
        value = input('\x1B[33m\x1B[100m{0}\x1B[0m'.format(data))

    return value
        
