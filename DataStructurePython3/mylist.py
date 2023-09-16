from mynode import Node
from myinterface import InterfaceList


class MyList(InterfaceList):

    def __init__(self):
        self.head = None

    def size(self):
        cnt = 0
        ptr = self.head
        while ptr is not None:
            cnt = cnt + 1
            ptr = ptr.next_node
        return cnt

    def add(self, idx, data):
        node = Node(data=data)
        cnt = 0
        ptr = self.head
        prev = None
        while ptr is not None and cnt < idx:
            cnt = cnt + 1
            prev = ptr
            ptr = ptr.next_node
        if prev is not None:
            prev.next_node = node
        node.next_node = ptr
        if self.head is None or idx == 0:
            self.head = node
        return node.data

    def remove(self, idx):
        cnt = 0
        ptr = self.head
        prev = None
        while ptr is not None and cnt < idx:
            cnt = cnt + 1
            prev = ptr
            ptr = ptr.next_node
        if prev is not None:
            if ptr is None:
                prev.next_node = None
            else:
                prev.next_node = ptr.next_node
        if idx == 0:
            self.head = self.head.next_node
        return ptr.data

    def get(self, idx):
        """
        ptr = self.head
        for _ in range(idx):
            ptr = ptr.next_node
        return ptr.data
        """
        cnt = 0
        ptr = self.head
        while cnt < idx:
            cnt = cnt + 1
            ptr = ptr.next_node
        return ptr.data


def main():
    print('Example execution')
    print('[Create MyList(InterfaceList)')
    l = MyList()
    print(l)
    print('[size() of MyList(InterfaceList)')
    print(l.size())
    print('[Add object to MyList(InterfaceList)')
    for i in range(20):
        l.add(i, str(i))
    print('[size() of MyList(InterfaceList)')
    print(l.size())
    print('[remove() of MyList(InterfaceList) by index 0->4->1->10->8->5')
    print(l.remove(0))
    print(l.remove(4))
    print(l.remove(1))
    print(l.remove(10))
    print(l.remove(8))
    print(l.remove(5))
    print('[size() of MyList(InterfaceList)')
    print(l.size())
    print('[get() of MyList(InterfaceList)')
    for i in range(l.size()):
        print(f'> {i} - {l.get(i)}')


if __name__ == '__main__':
    main()

