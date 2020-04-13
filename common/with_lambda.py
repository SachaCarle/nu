class WithLambda():
    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
    def __enter__(self):
        return self.l1()
    def __exit__(self, type, value, traceback):
        return self.l2()
