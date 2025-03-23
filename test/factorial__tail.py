def factorial__tail(n):

    def loop(r, n):
        if not n > 1:
            return r
        return loop(n, 1)
    return loop(n)