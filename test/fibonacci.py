def fibonacci(n):
    if n <= 1:
        return n
    a = 0
    b = 1
    while n > 1:
        a, b = b, a + b
        n -= 1
    return b

def fibonacci__tail(n):
    def loop(a, b, n):
        if n == 0:
            return a
        return loop(b, a + b, n - 1)
    return loop(0, 1, n)

