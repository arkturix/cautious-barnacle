"""Player class"""
from blackjack.common import Wallet
from blackjack.common import Hand
from blackjack.common.exceptions import IllegalBet, IllegalSplit
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
        self.bet(init_bet)

    def bet(self, amount):
        """Add to bet"""
        if amount < 10:
            raise IllegalBet("Bet must be larger than $10!")
        elif self.wallet.balance - amount < 0:
            raise IllegalBet("Cannot bet more than you have!")
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
        self.current_bet = int(self.current_bet // 2)
        self._is_standing = True

    def split(self, init_bet = 10):
        """Split the hand"""
        card_vals=[]
        for card in self.hand.cards:
            if card[0] == 'A':
                card_vals.append(1)
            elif card[0] in ['K', 'Q', 'J']:
                card_vals.append(11)
            else:
                card_vals.append(card[0])
        if not card_vals[0] == card_vals[1]:  # Split cards must have the same value
            raise IllegalSplit("Split cards must be the same value!")
        self._is_split = True
        self.split_hand = self.hand.split()
        self.split_bet = init_bet

    def hit_split(self):
        """Take another card and put it into split hand"""
        self.split_hand + self.dealer.deck.draw()

    def bet_split(self, amount):
        """Add to split bet"""
        if not self._is_split:
            raise IllegalBet("That bet is not available (no split)!")
        if amount % 10 != 0:
            raise IllegalBet("Must bet in multiples of 10!")
        elif amount < 10:
            raise IllegalBet("Bet must be larger than 0!")
        elif self.wallet.balance - amount < 0:
            raise IllegalBet("Cannot bet more than you have!")
        else:
            self.split_bet += amount

    def double(self):
        """Double bet and draw one card"""
        self.current_bet *= 2
        self.hit()
        self._is_standing = True

    def resolve_round(self):
        """Resolve the round"""
        self.current_bet = 0
        self._is_standing = False
        self.hand.reset()
        self._is_split = False
        self.split_hand = None
        self.split_bet = 0
