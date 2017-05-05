class Compute:
    def __init__(self, text):
        self.text = text

    def compute(self):
        return eval(self.text)
