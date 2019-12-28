class File(object):
    def __init__(self, src):
        self.path = src
        self.obj = open(src, 'r')
    
    def move(self, dst):
        # Check sha256
