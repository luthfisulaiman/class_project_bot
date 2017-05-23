from random import randint


def checkPossib(function):
    def wrapper(*args, **kwargs):
        hasil = function(*args, **kwargs)
        if(args[1] > args[3]):
            hasil = "Your luck number is Bad"
            hasil += "(Bigger thAn the siDe)"
        return hasil
    return wrapper


class diceSim:

    def __init__(self):
        self.post = "dice"

    def coin(self):
        possib = ["head", "tail"]
        return possib[randint(0, 1)]

    def roll(self, x, y):
        hasil = "Result: " + str(x) + "d" + str(y)
        hasil += " ("
        hasil += str(randint(1, int(y)))
        for i in range(x-1):
            hasil += ", " + str(randint(1, int(y)))
            hasil += ")"
            return hasil

    def multiroll(self, x, y, z):
        hasil = ""
        for i in range(z):
            hasil += str(x) + "d" + str(y)
            hasil += " ("
            hasil += str(randint(1, int(y)))
            for q in range(x-1):
                hasil += ", "+str(randint(1, int(y)))
                hasil += ")\n"
        return hasil

    @checkPossib
    def is_lucky(self, n, x, y):
        arr = []
        flag = False
        counter = 0
        for i in range(x):
            arr.append(randint(1, y))
            for a in range(len(arr)):
                if(arr[a] == n):
                    flag = True
                    counter = counter + 1
        if(flag):
            hasil = str(n) + " appears " + str(counter)
        else:
            hasil = "I'm not lucky"
        return hasil
