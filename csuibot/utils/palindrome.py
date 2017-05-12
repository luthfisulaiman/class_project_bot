class Palindrome:
    def __init__(self, text):
        self.text = text

    def is_palindrome(self):
        if self.text == self.text[::-1]:
            return "Yes, it is a palindrome"
        return "No, it is not a palindrome"
