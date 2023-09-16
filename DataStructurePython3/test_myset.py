import unittest

from myset import MySet
from myinterface import InterfaceSet


class TestMySet(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(MySet, InterfaceSet))
        s = MySet()
        self.assertIsInstance(s, MySet)

    def test_size1(self):
        s = MySet()
        self.assertEqual(s.size(), 0)
    
    def test_add1(self):
        s = MySet()
        for i in range(100):
            s.add(f'{i}')
        self.assertEqual(s.size(), 100)
        for i in range(100):
            s.add(f'{i}')
        self.assertEqual(s.size(), 100)
    
    def test_add2(self):
        s = MySet()
        for i in range(100):
            s.add(float(i))
        self.assertEqual(s.size(), 100)
        for i in range(99, -1, -1):
            s.add(float(i))
        self.assertEqual(s.size(), 100)
        for i in range(100):
            self.assertTrue(s.isin(float(i)))

    def test_remove1(self):
        s = MySet()
        s.add(4)
        s.add(7)
        s.add(1)
        s.add(9)
        s.add(10)
        s.add(3)
        s.add(8)
        self.assertTrue(s.isin(7))
        self.assertEqual(s.remove(7), 7)
        self.assertFalse(s.isin(7))
        self.assertTrue(s.isin(4))
        self.assertEqual(s.remove(4), 4)
        self.assertFalse(s.isin(4))
        self.assertTrue(s.isin(3))
        self.assertEqual(s.remove(3), 3)
        self.assertFalse(s.isin(3))
        self.assertTrue(s.isin(8))
        self.assertEqual(s.remove(8), 8)
        self.assertFalse(s.isin(8))
        self.assertEqual(s.size(), 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)

