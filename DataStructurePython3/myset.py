from mynode import Node
from myinterface import InterfaceSet


class MySet(InterfaceSet):

    def __init__(self):
        self.head = None

    def size(self):
        cnt = 0
        ptr = self.head
        while ptr is not None:
            cnt = cnt + 1
            ptr = ptr.next_node
        return cnt

    def add(self, data):
        ptr = self.head
        prev = None
        isin = False
        while ptr is not None:
            if ptr.data == data:
                isin = True
                break
            prev = ptr
            ptr = ptr.next_node
        if not isin:
            node = Node(data=data)
            if prev is not None:
                prev.next_node = node
            if self.head is None:
                self.head = node
            return node.data
        return ptr.data

    def remove(self, data):
        ptr = self.head
        prev = None
        while ptr is not None:
            if ptr.data == data:
                break
            prev = ptr
            ptr = ptr.next_node
        if prev is not None:
            if ptr is None:
                prev.next_node = None
            else:
                prev.next_node = ptr.next_node

        if ptr == self.head:
            self.head = self.head.next_node
        return ptr.data

    def isin(self, data):
        isin = False
        ptr = self.head
        while ptr is not None:
            if ptr.data == data:
                isin = True
                break
            ptr = ptr.next_node
        return isin


def main():

    print('Example execution')
    print('[Create MySet(InterfaceSet)')
    s = MySet()
    print(s)
    print('[size() of MySet(InterfaceSet)')
    print(s.size())
    print('[Add object to MySet(InterfaceSet)')
    for i in range(20):
        s.add(i)
    print('[size() of MySet(InterfaceSet)')
    print(s.size())
    print('[Add object to MySet(InterfaceSet)')
    for i in range(20):
        s.add(i)
    print('[size() of MySet(InterfaceSet)')
    print(s.size())
    print('[remove() of MySet(InterfaceSet) by value 0->4->1->10->8->5')
    print(s.remove(0))
    print(s.remove(4))
    print(s.remove(1))
    print(s.remove(10))
    print(s.remove(8))
    print(s.remove(5))
    print('[size() of MySet(InterfaceSet)')
    print(s.size())
    print('[isin() of MyList(InterfaceSet)')
    for i in range(s.size()):
        print(f'> {i} - {s.isin(i)}')


if __name__ == '__main__':
    main()

