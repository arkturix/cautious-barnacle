"""Custom exceptions"""


class IllegalBet(Exception):
    pass


class InvalidInput(Exception):

    def __init__(self, message):
        self.message = message
        print(f"Invalid input! {self.message}")
        super().__init__(self.message)


class IllegalSplit(Exception):
    pass
