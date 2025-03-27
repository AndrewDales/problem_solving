from functools import lru_cache

lru_cache(maxsize=2000)
def coins(n, coin_list):
    if len(coin_list) == 1:
        if n % coin_list[0] == 0:
            num_partitions = 1
        else:
            num_partitions = 0
    else:
        new_coin_list = coin_list.copy()
        coin = new_coin_list.pop()
        num_partitions = sum(coins(n - coin * i, new_coin_list) for i in range(n // coin))
    return num_partitions


if __name__ == '__main__':
    uk_coins = [1, 2, 5, 10, 20, 50, 100, 200]
    num_parts = coins(200, uk_coins)
    print(num_parts)