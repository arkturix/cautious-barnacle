"""Player class"""
from blackjack.common import Wallet
from blackjack.dealer import Dealer

class Player:

    def __init__(self, starting_balance: int = 100, num_of_decks: int = 1) -> None:
        self.wallet = Wallet(starting_amount=starting_balance)
        self.dealer = Dealer(num_decks=num_of_decks)
        self.hand = []
        self._is_standing = False
        self._is_split = False
        self.split_hand = []
        self.current_bet = 0

    def deal(self, init_bet = 10):
        """Deal the initial cards"""
        self.hand = self.dealer.deal()
        self.current_bet = init_bet

    def hit(self):
        """Take another card from the dealer"""
        self.hand.append(self.dealer.deck.draw())

    def stand(self):
        """Stand when done drawing and betting"""
        self._is_standing = True

    def surrender(self):
        """Surrender the hand"""
        self.current_bet = int(self.current_bet / 2)

    def split(self):
        pass

    def double(self):
        """Double bet and draw one card"""
        self.current_bet *= 2
        self.hit()

    def resolve_round(self):
        """Resolve the round"""
        pass
