def factorial(n):
    r = 1
    while n > 1:
        r *= n
        n -= 1
    return r

def factorial__tail(n):
    def loop(n, r):
        if n <= 1:
            return r
        return loop(n - 1, r * n)
    return loop(n, 1)
