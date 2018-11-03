def binary_search(target, item):
    # init variable
    first = 0
    last = len(target) - 1
    found = False
    count = 0
    mid = 0

    # search
    while first <= last and not found:
        mid = (first + last) // 2
        if target[mid] == item:
            found = True
        else:
            if item < target[mid]:
                last = mid - 1
            else:
                first = mid + 1
        count = count + 1

    return found, mid, count


def binary_search_re(target, item):
    if len(target) == 0:
        return False
    else:
        mid = len(target) // 2
        if target[mid] == item:
            return True
        else:
            if item < target[mid]:
                return binary_search_re(target[:mid], item)
            else:
                return binary_search_re(target[mid+1:], item)


def main():
    import random
    test_list = random.sample(range(0, 100), 10)
    test_list.sort()
    print(test_list)
    print(binary_search(test_list, random.choice(test_list)))
    print(binary_search(test_list, -1))
    print(binary_search_re(test_list, random.choice(test_list)))
    print(binary_search_re(test_list, -1))


if __name__ == '__main__':
    main()
