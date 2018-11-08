import copy

from binary_search_tree import BinarySearchTree, is_bst


def main():
    target_list = [
        (8, '여덟'),
        (2, '둘'),
        (9, '아홉'),
        (3, '셋'),
        (6, '여섯'),
        (5, '다섯'),
        (4, '넷'),
        (1, '하나'),
        (7, '일곱')
    ]
    print(target_list)

    bst = BinarySearchTree()
    for key, value in target_list:
        bst.insert_node(key, value)
    bst.print_bst()

    for key, value in target_list:
        copied_bst = copy.deepcopy(bst)
        print('Delete {0}'.format(key))
        copied_bst.delete_node(key)
        copied_bst.print_bst()
        print('Is Binary Search Tree? {0}'.format(is_bst(copied_bst.get_root())))


if __name__ == '__main__':
    main()
