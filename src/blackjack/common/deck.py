"""Deck(s) of cards class"""
import random
import time


class Deck:

    def __init__(self, num_of_decks: int = 1) -> None:
        self.num_decks = num_of_decks
        suits = ['spades', 'clubs', 'hearts', 'diamonds']
        one_deck = []
        for suit in suits:
            for card in range(1, 14):
                if card == 1: card = 'A'
                if card == 11: card = 'J'
                if card == 12: card = 'Q'
                if card == 13: card = 'K'
                one_deck.append((card, suit))
        self._deck = self._starting_deck = one_deck * self.num_decks
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck"""
        random.shuffle(self._deck)

    def draw(self):
        """Draw a card from the deck"""
        if len(self._deck) == 0:
            print(f"Shuffling {self.num_decks} before drawing next card...")
            time.sleep(2)
            self._deck = self._starting_deck  # Back fill deck when out of cards
            self.shuffle()
        return self._deck.pop()
