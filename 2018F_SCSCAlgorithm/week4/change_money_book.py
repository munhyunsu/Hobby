import time
import random


counter = 0


def make_change(coin_value_list, coin_change):
    """
    잔돈
    """
    global counter
    counter = counter + 1
    min_coins = coin_change

    if coin_change in coin_value_list:
        return 1, [coin_change]
    else:
        coins = list()
        for coin in coin_value_list:
            if coin <= coin_change:
                coins.append(coin)
        for coin in coins:
            num_coins = 1 + make_change(coin_value_list, coin_change - coin)
            if num_coins < min_coins:
                min_coins = num_coins
    return min_coins


def main():
    """
    잔돈 거스르기
    """
    coin_value_list = [1, 5, 10, 21, 25]  # 동전의 종류
    # coin_value_list = [1, 5, 10, 25]  # 동전의 종류
    random.shuffle(coin_value_list)
    coin_change = input('거스름돈: ') # 거스름돈
    coin_change = int(coin_change) # 인트형으로 바꾸자!

    start = time.time()
    print(make_change(coin_value_list, coin_change))
    end = time.time()
    print(counter)
    return_time = end-start
    print('Time: {0:7.3f}'.format(return_time))


if __name__ == '__main__':
    main()