from binary_search_tree import BinarySearchTree
import unittest
import copy


def is_bst(root):
    isit = True
    queue = list()
    queue.append(root)

    while len(queue) != 0:
        current = queue.pop(0)
        if current.get_left() is not None:
            queue.append(current.get_left())
            if current.get_key() < current.get_left().get_key():
                isit = False
                break
        if current.get_right() is not None:
            queue.append(current.get_right())
            if current.get_key() > current.get_right().get_key():
                isit = False
                break

    return isit


class BSTTest(unittest.TestCase):
    # test01
    def test_key01(self):
        key_list = [8, 3, 10, 1, 6, 4, 7, 14, 13]
        bst = BinarySearchTree()
        for key in key_list:
            bst.insert_node(key, None)
        self.assertTrue(is_bst(bst.get_root()))
        for key in key_list:
            temp_bst = copy.deepcopy(bst)
            temp_bst.delete_node(key)
            self.assertTrue(is_bst(bst.get_root()))

    # test02
    def test_key02(self):
        key_list = [
            (90, '이상해씨'),
            (50, '이상해풀'),
            (150, '이상해꽃'),
            (20, '파이리'),
            (75, '리자드'),
            (95, '리자몽'),
            (175, '꼬부기'),
            (5, '어니부기'),
            (25, '거북왕'),
            (66, '캐터피'),
            (80, '단데기'),
            (92, '버터플'),
            (111, '뿔충이'),
            (166, '딱충이'),
            (200, '독침붕')
        ]
        bst = BinarySearchTree()
        for key, value in key_list:
            bst.insert_node(key, value)
        self.assertTrue(is_bst(bst.get_root()))
        for key, value in key_list:
            temp_bst = copy.deepcopy(bst)
            temp_bst.delete_node(key)
            self.assertTrue(is_bst(bst.get_root()))

    # test03
    def test_key03(self):
        key_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bst = BinarySearchTree()
        for key in key_list:
            bst.insert_node(key, None)
        self.assertTrue(is_bst(bst.get_root()))
        for key in key_list:
            temp_bst = copy.deepcopy(bst)
            temp_bst.delete_node(key)
            self.assertTrue(is_bst(bst.get_root()))

    # test04
    def test_key04(self):
        key_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        bst = BinarySearchTree()
        for key in key_list:
            bst.insert_node(key, None)
        self.assertTrue(is_bst(bst.get_root()))
        for key in key_list:
            temp_bst = copy.deepcopy(bst)
            temp_bst.delete_node(key)
            self.assertTrue(is_bst(bst.get_root()))


if __name__ == '__main__':
    unittest.main()
