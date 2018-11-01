import unittest
import random

from change_money_dp_list import make_change


class TestMakechange(unittest.TestCase):
    def test_makechange(self):
        coin_value_list = [1, 5, 10, 21, 25]
        for change in range(0, 101, 1):
            random.shuffle(coin_value_list)
            known_result = list()
            for index in range(0, change + 1):
                known_result.append([])
            result = make_change(coin_value_list, change, known_result)
            print(sum(known_result[change]) == change, known_result[change], change)
            self.assertEqual(sum(known_result[change]), change)

    def test_63(self):
        coin_value_list = [1, 5, 10, 21, 25]
        random.shuffle(coin_value_list)
        known_result = list()
        for index in range(0, 63 + 1):
            known_result.append([])
        make_change(coin_value_list, 63, known_result)
        self.assertEqual([21, 21, 21], known_result[63])

    def test_12(self):
        coin_value_list = [1, 2, 3, 5, 7]
        random.shuffle(coin_value_list)
        known_result = list()
        for index in range(0, 12 + 1):
            known_result.append([])
        make_change(coin_value_list, 12, known_result)
        known_result[12].sort()
        self.assertEqual([5, 7], known_result[12])


if __name__ == '__main__':
    unittest.main(verbosity=2)
