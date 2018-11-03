def sequential_search(target, item):
    # init variable
    position = 0
    found = False
    count = 0

    # search
    while position < len(target) and not found:
        if target[position] == item:
            found = True
        else:
            position = position + 1
        count = count + 1

    # return
    return found, position, count


def main():
    import random
    test_list = random.sample(range(0, 100), 10)
    print(test_list)
    print(sequential_search(test_list, random.choice(test_list)))
    print(sequential_search(test_list, -1))


if __name__ == '__main__':
    main()
