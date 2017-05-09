class Compute:
    def __init__(self, text):
        self.text = text

    def calculate(self):
        return eval(self.text)
