"""Player's wallet class"""


class Wallet:

    def __init__(self, starting_amount: int = 100) -> None:
        self.balance = starting_amount

    def __add__(self, amount):
        self.balance += amount

    def __sub__(self, amount):
        self.balance -= amount
