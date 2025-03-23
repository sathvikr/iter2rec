def factorial__tail(n):

    def loop(r, n):
        if not n > 1:
            return r
        return loop(n * r, n - 1)
    return loop(1, n)