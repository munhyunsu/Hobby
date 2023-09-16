import unittest

from mylist import MyList
from myinterface import InterfaceList


class TestMyList(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(MyList, InterfaceList))
        l = MyList()
        self.assertIsInstance(l, MyList)

    def test_size1(self):
        l = MyList()
        self.assertEqual(l.size(), 0)
    
    def test_add1(self):
        l = MyList()
        for i in range(100):
            l.add(i, f'{i}')
        self.assertEqual(l.size(), 100)
        for i in range(100):
            self.assertEqual(l.get(i), f'{i}')
    
    def test_add2(self):
        l = MyList()
        for i in range(100):
            l.add(0, float(i))
        expected = 99.0
        for i in range(l.size()):
            self.assertEqual(l.get(i), expected)
            expected = expected - 1

    def test_add3(self):
        l = MyList()
        l.add(0, 4)
        l.add(0, 7)
        l.add(1, 1)
        l.add(3, 9)
        l.add(l.size(), 10)
        l.add(2, 3)
        l.add(4, 8)
        self.assertEqual(l.get(0), 7)
        self.assertEqual(l.get(1), 1)
        self.assertEqual(l.get(2), 3)
        self.assertEqual(l.get(3), 4)
        self.assertEqual(l.get(4), 8)
        self.assertEqual(l.get(5), 9)
        self.assertEqual(l.get(6), 10)

    def test_remove1(self):
        l = MyList()
        for i in range(10):
            l.add(l.size(), i)
        self.assertEqual(l.remove(l.size()-1), 9)
        self.assertEqual(l.remove(0), 0)
        expected = 1
        for i in range(l.size()):
            self.assertEqual(l.get(i), expected)
            expected = expected + 1

    def test_remove2(self):
        l = MyList()
        for i in range(200, 210):
            l.add(0, float(i))
        self.assertEqual(l.remove(1), 208.0)
        self.assertEqual(l.remove(7), 201.0)
        self.assertEqual(l.remove(5), 203.0)
        self.assertEqual(l.remove(2), 206.0)
        self.assertEqual(l.remove(5), 200.0)
        self.assertEqual(l.remove(0), 209.0)
        self.assertEqual(l.get(0), 207.0)
        self.assertEqual(l.get(1), 205.0)
        self.assertEqual(l.get(2), 204.0)
        self.assertEqual(l.get(3), 202.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)

