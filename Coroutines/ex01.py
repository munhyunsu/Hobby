#/usr/bin/python

# This is Python 2 code, since this section discusses Python 2.
# For Python 3 replace range(...) with list(range(...)) and
# replace xrange(...) with range(...).
def primes(limit):
    "Yield all primes <= limit."

    sqrt_limit = int(round(limit**0.5))
    #print('sqrt_limit %d' % sqrt_limit)
    limit += 1
    sieve = range(limit)
    sieve[1] = 0
    for i in xrange(2, sqrt_limit + 1):
        #print('aaa')
        if sieve[i]:
            sieve[i*i:limit:i] = [0] * len(xrange(i*i, limit, i))
            yield i
    for i in xrange(sqrt_limit + 1, limit):
        #print('bbb')
        if sieve[i]:
            yield i


if __name__ == '__main__':
    for x in primes(121):
        print(x)
