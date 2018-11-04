class Node(object):
    def __init__(self, key=None, value=None, left=None, right=None):
        self._key = key
        self._value = value
        self._left = left
        self._right = right

    def set_key(self, key):
        self._key = key

    def get_key(self):
        return self._key

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def set_left(self, left):
        self._left = left

    def get_left(self):
        return self._left

    def set_right(self, right):
        self._right = right

    def get_right(self):
        return self._right

    def __str__(self):
        return str({'key': self._key, 'value': self._value,
                    'left': self._left, 'right': self._right})


def main():
    tree = Node(key=2)

    tree.set_left(Node(key=7))
    tree.set_right(Node(key=5))

    tree.get_left().set_left(Node(key=2))
    tree.get_left().set_right(Node(key=6))
    tree.get_right().set_right(Node(key=9))

    tree.get_left().get_right().set_left(Node(key=5))
    tree.get_left().get_right().set_right(Node(key=11))
    tree.get_right().get_right().set_left(Node(key=4))

    print(tree)


if __name__ == '__main__':
    main()
