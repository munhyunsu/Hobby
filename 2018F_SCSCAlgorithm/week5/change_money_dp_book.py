def make_change(coin_value_list, coin_change, min_coins, coins_used):
    global counter
    for cents in range(0, coin_change+1):
        coin_count = cents
        new_coin = 1
        coins = list()
        for coin in coin_value_list:
            if coin <= cents:
                coins.append(coin)
        for coin in coins:
            counter = counter + 1
            if min_coins[cents - coin] + 1 < coin_count:
                coin_count = min_coins[cents - coin] + 1
                new_coin = coin
        min_coins[cents] = coin_count
        coins_used[cents] = new_coin
    return min_coins[coin_change]


def print_coins(coins_used, coin_change):
    coin = coin_change
    while coin > 0:
        this_coin = coins_used[coin]
        print(this_coin)
        coin = coin - this_coin


counter = 0


def main():
    """
    잔돈 거스르기
    """
    coin_value_list = [1, 5, 10, 21, 25]  # 동전의 종류
    coin_change = input('Change: ')  # 거스름돈
    coin_change = int(coin_change)  # 인트형으로 바꾸자!
    coins_used = [0] * (coin_change + 1)
    coin_count = [0] * (coin_change + 1)

    print('Making change for', coin_change, 'requires')
    print(make_change(coin_value_list, coin_change, coin_count, coins_used), 'coins')
    print('They are:')
    print_coins(coins_used, coin_change)
    print('The used list is as follows:')
    print(coins_used)
    print(counter)


if __name__ == '__main__':
    main()
