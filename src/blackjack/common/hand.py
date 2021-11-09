"""Hand class"""


class Hand:

    def __init__(self, cards = []) -> None:
        self.cards = cards

    def __add__(self, card: tuple):
        self.cards.append(card)

    def split(self):
        """Split the hand"""
        return Hand(cards=[self.cards.pop()])

    def total(self):
        """Get the total value of the hand"""
        hand_value = 0
        aces = []
        for card in self.cards:
            card_value = 0
            if card[0] == 'A':
                aces.append(self.cards.pop(card))
            elif card[0] in ['K', 'Q', 'J']:
                card_value = 10
            else:
                card_value = card[0]
            hand_value += card_value
            if hand_value > 21:
                break
        for card in aces:
            if (hand_value + 11) <= 21:
                hand_value += 11
            else:
                hand_value += 1
            self.cards.pop(card)
        return hand_value
    
    def reset(self):
        """Empty the hand at the end of a round"""
        self.cards = []
