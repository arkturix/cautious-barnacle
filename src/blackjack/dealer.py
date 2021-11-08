"""Dealer class"""
from blackjack.common import Deck


class Dealer:

    def __init__(self, num_decks: int = 1) -> None:
        self.deck = Deck(num_of_decks=num_decks)
        self.display_card = None
        self.hole_card = None
        self.hand = []

    def deal(self) -> list:
        """Deal the initial cards for the game"""
        self.display_card = self.deck.draw()
        self.hole_card = self.deck.draw()
        player_hand = [self.deck.draw() for i in range(2)]
        return player_hand

    def resolve(self):
        """Resolve the dealer's hand"""
        pass
