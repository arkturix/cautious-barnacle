"""Player class"""
from blackjack.common import Wallet
from blackjack.common import Hand
from blackjack.common.exceptions import IllegalBet
from blackjack.dealer import Dealer

class Player:

    def __init__(self, starting_balance: int = 100, num_of_decks: int = 1) -> None:
        self.wallet = Wallet(starting_amount=starting_balance)
        self.dealer = Dealer(num_decks=num_of_decks)
        self.hand = Hand()
        self.resolve_round()

    def deal(self, init_bet = 10):
        """Deal the initial cards"""
        initial_deal = self.dealer.deal()
        self.hand + initial_deal[0]
        self.hand + initial_deal[1]
        self.current_bet = init_bet

    def bet(self, amount):
        """Add to bet"""
        if amount % 10 != 0:
            raise IllegalBet("Must bet in multiples of 10!")
        else:
            self.current_bet += amount

    def hit(self):
        """Take another card from the dealer"""
        self.hand + self.dealer.deck.draw()

    def stand(self):
        """Stand when done drawing"""
        self._is_standing = True

    def surrender(self):
        """Surrender the hand"""
        self.current_bet = int(self.current_bet / 2)

    def split(self, init_bet = 10):
        """Split the hand"""
        self._is_split = True
        self.split_hand = self.hand.split()
        self.split_bet = init_bet

    def double(self):
        """Double bet and draw one card"""
        self.current_bet *= 2
        self.hit()

    def resolve_round(self):
        """Resolve the round"""
        # TODO: Figure out winning/losing bet
        self.current_bet = 0
        self._is_standing = False
        self.hand.reset()
        self._is_split = False
        self.split_hand = None
        self.split_bet = 0
