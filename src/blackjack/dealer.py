"""Dealer class"""
from blackjack.common import Deck
from blackjack.common import Hand


class Dealer:

    def __init__(self, num_decks: int = 1) -> None:
        self.deck = Deck(num_of_decks=num_decks)
        self.hand = Hand()
        self.resolve()

    def deal(self) -> list:
        """Deal the initial cards for the game"""
        self.display_card = self.deck.draw()
        self.hole_card = self.deck.draw()
        self.hand + self.display_card
        self.hand + self.hole_card
        player_hand = [self.deck.draw() for i in range(2)]
        return player_hand

    def draw(self):
        """Draw card"""
        self.hand + self.deck.draw()

    def resolve(self):
        """Resolve the dealer's hand"""
        self.display_card = None
        self.hole_card = None
        self.hand.reset()
        self.deck.shuffle()
