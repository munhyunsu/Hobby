import unittest
import random

from change_money_list import make_change


class TestMakechange(unittest.TestCase):
    def test_makechange(self):
        coin_value_list = [1, 5, 10, 21, 25]
        for change in range(0, 51, 1):
            random.shuffle(coin_value_list)
            result = make_change(coin_value_list, change)
            print(sum(result[2]) == change, result[2], change)
            self.assertEqual(change, sum(result[2]))

    def test_63(self):
        coin_value_list = [1, 5, 10, 21, 25]
        random.shuffle(coin_value_list)
        result = make_change(coin_value_list, 63)[2]
        self.assertEqual([21, 21, 21], result)

    def test_12(self):
        coin_value_list = [1, 2, 3, 5, 7]
        random.shuffle(coin_value_list)
        result = make_change(coin_value_list, 12)[2]
        result.sort()
        self.assertEqual([5, 7], result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
