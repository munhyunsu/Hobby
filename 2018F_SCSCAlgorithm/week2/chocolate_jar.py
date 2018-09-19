class ChocolateJar(object):
    def __init__(self, chocolates=13):
        self.chocolates = chocolates+1

    def take_chocolate(self, hands):
        self.chocolates = self.chocolates - hands

