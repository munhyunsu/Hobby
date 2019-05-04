import unittest

from char_removed import equalsWhenOneCharRemoved


class CharRemovedTests(unittest.TestCase):
    def test_case1(self):
        self.assertFalse(equalsWhenOneCharRemoved('x', 'y'))

    def test_case2(self):
        self.assertFalse(equalsWhenOneCharRemoved('x', 'XX'))

    def test_case3(self):
        self.assertFalse(equalsWhenOneCharRemoved('yy', 'yx'))

    def test_case4(self):
        self.assertTrue(equalsWhenOneCharRemoved('abcd', 'abxcd'))

    def test_case5(self):
        self.assertTrue(equalsWhenOneCharRemoved('xyz', 'xz'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

