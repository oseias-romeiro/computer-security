import random

# TODO: review test
def test_MillerRabin(n,k) -> bool:

    if(n == 2): return True
    elif(n <= 1 or n%2 == 0): return False

    # let s > 0 and d odd > 0 | n - 1 != (2**s)*d
    s, d = 0, n - 1
    while d % 2 == 0:
        s += 1
        d //= 2

    for _ in range(0,k+1):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            for _ in range(0, s-1):
                y = pow(x, 2, n)
                if y == n - 1:
                    break
        else:
            return False
    return True

def genPrimes(keySize:int, k:int=20) -> int:
    """
    params:
        - keySize : minimu size of key in bits
        - k: determines the accuracy of test
    """

    while True:
        prime = random.randrange(2**(keySize-1)+1, 2**keySize-1)
        if(test_MillerRabin(prime, k)):
            return prime
