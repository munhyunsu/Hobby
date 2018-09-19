import unittest

from chocolate_jar import ChocolateJar


class ChocolateJarTest(unittest.TestCase):
    def test_create(self):
        jar = ChocolateJar(13)
        self.assertEqual(14, jar.chocolates)

    def test_take(self):
        jar = ChocolateJar(13)
        jar.take_chocolate(3)
        self.assertEqual(11, jar.chocolates)
        jar.take_chocolate(2)
        self.assertEqual(9, jar.chocolates)
        jar.take_chocolate(1)
        self.assertEqual(8, jar.chocolates)


if __name__ == '__main__':
    unittest.main(verbosity=2)
