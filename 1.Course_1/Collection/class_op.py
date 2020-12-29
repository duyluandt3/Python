# Override

class Operation:
    def __init__(self, n1, n2):
        self._n1 = n1
        self._n2 = n2
    def sum(self):
        return self._n1 + self._n2
    def div(self):
        return self._n1/ self._n2

class Multi(Operation):
    def __init__(self, n1, n2):
        self._n1 = n1
        self._n2 = n2
    def Mul(self):
        return self._n1 * self._n2
    # Override sum method
    def sum(self):
        return (self._n1 + self._n2)*2
