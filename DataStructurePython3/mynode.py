class Node():

    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
    
    def __repr__(self):
        return f'repr: {self.data} - {self.next_node}'

    def __str__(self):
        return f'str: {self.data} - {self.next_node}'

