import unittest

from myqueue import MyQueue
from myinterface import InterfaceQueue


class TestMyQueue(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(MyQueue, InterfaceQueue))
        q = MyQueue()
        self.assertIsInstance(q, MyQueue)

    def test_size1(self):
        q = MyQueue()
        self.assertEqual(q.size(), 0)
    
    def test_endequeue1(self):
        q = MyQueue()
        for i in range(100):
            q.enqueue(f'{i}')
        self.assertEqual(q.size(), 100)
        for i in range(100):
            self.assertEqual(q.dequeue(), f'{i}')
    
    def test_endequeue2(self):
        q = MyQueue()
        for i in range(100):
            q.enqueue(f'{i}')
        self.assertEqual(q.size(), 100)
        for i in range(100):
            self.assertEqual(q.dequeue(), f'{i}')
        for i in range(99, -1, -1):
            q.enqueue(f'{i}')
        self.assertEqual(q.size(), 100)
        for i in range(99, -1, -1):
            self.assertEqual(q.dequeue(), f'{i}')

    def test_endequeue3(self):
        q = MyQueue()
        for i in range(100):
            q.enqueue(f'{i}')
        self.assertEqual(q.size(), 100)
        for i in range(100):
            self.assertEqual(q.dequeue(), f'{i}')
        for i in range(99, -1, -1):
            q.enqueue(f'{i}')
        for i in range(99, -1, -1):
            q.enqueue(f'{i}')
        self.assertEqual(q.size(), 200)
        for i in range(99, -1, -1):
            self.assertEqual(q.dequeue(), f'{i}')


if __name__ == '__main__':
    unittest.main(verbosity=2)

