import unittest

from node import Node
from tree_travelsal import print_pre2, print_in2, print_post2, print_level


class TreeTravelTests(unittest.TestCase):
    tree = Node(key=2)

    tree.set_left(Node(key=7))
    tree.set_right(Node(key=5))

    tree.get_left().set_left(Node(key=2))
    tree.get_left().set_right(Node(key=6))
    tree.get_right().set_right(Node(key=9))

    tree.get_left().get_right().set_left(Node(key=5))
    tree.get_left().get_right().set_right(Node(key=11))
    tree.get_right().get_right().set_left(Node(key=4))

    def test_pre_order(self):
        result = print_pre2(self.tree)
        self.assertEqual(result, [2, 7, 2, 6, 5, 11, 5, 9, 4])

    def test_in_order(self):
        result = print_in2(self.tree)
        self.assertEqual(result, [2, 7, 5, 6, 11, 2, 5, 4, 9])

    def test_post_order(self):
        result = print_post2(self.tree)
        self.assertEqual(result, [2, 5, 11, 6, 7, 4, 9, 5, 2])

    def test_level_order(self):
        result = print_level(self.tree)
        self.assertEqual(result, [2, 7, 5, 2, 6, 9, 5, 11, 4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
