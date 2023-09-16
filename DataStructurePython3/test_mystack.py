import unittest

from mystack import MyStack
from myinterface import InterfaceStack


class TestMyStack(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(MyStack, InterfaceStack))
        s = MyStack()
        self.assertIsInstance(s, MyStack)

    def test_size1(self):
        s = MyStack()
        self.assertEqual(s.size(), 0)
    
    def test_pushpop1(self):
        s = MyStack()
        for i in range(100):
            s.push(f'{i}')
        self.assertEqual(s.size(), 100)
        for i in range(99, -1, -1):
            self.assertEqual(s.pop(), f'{i}')
    
    def test_pushpop2(self):
        s = MyStack()
        for i in range(100):
            s.push(f'{i}')
        self.assertEqual(s.size(), 100)
        for i in range(99, -1, -1):
            self.assertEqual(s.pop(), f'{i}')
        for i in range(99, -1, -1):
            s.push(f'{i}')
        self.assertEqual(s.size(), 100)
        for i in range(100):
            self.assertEqual(s.pop(), f'{i}')

    def test_pushpop3(self):
        s = MyStack()
        for i in range(100):
            s.push(f'{i}')
        self.assertEqual(s.size(), 100)
        for i in range(99, -1, -1):
            self.assertEqual(s.pop(), f'{i}')
        for i in range(100):
            s.push(f'{i}')
        for i in range(99, -1, -1):
            s.push(f'{i}')
        self.assertEqual(s.size(), 200)
        for i in range(100):
            self.assertEqual(s.pop(), f'{i}')


if __name__ == '__main__':
    unittest.main(verbosity=2)

