from mynode import Node
from myinterface import InterfaceQueue
from mylist import MyList


class MyQueue(InterfaceQueue):

    def __init__(self):
        self.l = MyList()

    def size(self):
        return self.l.size()

    def enqueue(self, data):
        self.l.add(0, data)
        return data

    def dequeue(self):
        return self.l.remove(self.l.size()-1)


def main():
    print('Example execution')
    print('[Create MyQueue(InterfaceQueue)')
    q = MyQueue()
    print(q)
    print('[size() of MyQueue(InterfaceQueue)')
    print(q.size())
    print('[Add object to MyQueue(InterfaceQueue)')
    for i in range(20):
        q.enqueue(f'{i}')
    print('[size() of MyQueue(InterfaceQueue)')
    print(q.size())
    print('[dequeue() of MyQueue(InterfaceQueue) 6 times')
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print('[size() of MyQueue(InterfaceQueue)')
    print(q.size())
    print('[get() of MyQueue(InterfaceQueue)')
    for i in range(q.size()):
        print(f'> {i} - {q.dequeue()}')


if __name__ == '__main__':
    main()

