class People(object):
    def __init__(self, name):
        self.name = name

    def print_info(self):
        print('People name: {0}.'.format(self.name))
