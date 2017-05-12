class CalculateBinary:

    def __init__(self, binA, binB):
        self._numA = int(binA, 2)
        self._numB = int(binB, 2)

    def addition(self):
        return self._numA + self._numB

    def multiplication(self):
        return self._numA * self._numB

    def subtraction(self):
        return self._numA - self._numB

    def division(self):
        return int(self._numA / self._numB)
