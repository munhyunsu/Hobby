from mynode import Node
from myinterface import InterfaceStack
from mylist import MyList


class MyStack(InterfaceStack):

    def __init__(self):
        self.l = MyList()

    def size(self):
        return self.l.size()

    def push(self, data):
        self.l.add(self.l.size(), data)
        return data

    def pop(self):
        return self.l.remove(self.l.size()-1)


def main():
    print('Example execution')
    print('[Create MyStack(InterfaceStack)')
    s = MyStack()
    print(s)
    print('[size() of MyStack(InterfaceStack)')
    print(s.size())
    print('[Add object to MyStack(InterfaceStack)')
    for i in range(20):
        s.push(f'{i}')
    print('[size() of MyStack(InterfaceStack)')
    print(s.size())
    print('[pop() of MyStack(InterfaceStack) 6 times')
    print(s.pop())
    print(s.pop())
    print(s.pop())
    print(s.pop())
    print(s.pop())
    print(s.pop())
    print('[size() of MyStack(InterfaceStack)')
    print(s.size())
    print('[get() of MyStack(InterfaceStack)')
    for i in range(s.size()):
        print(f'> {i} - {s.pop()}')


if __name__ == '__main__':
    main()

