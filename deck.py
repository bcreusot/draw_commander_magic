from random import shuffle


class Deck:

    def __init__(self):
        self.cards = []

    def clear(self):
        self.cards.clear()

    def add_cards(self, cards):
        for card in cards:
            self.add_card(card)

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        shuffle(self.cards)

    def get_size(self):
        return len(self.cards)

    def draw(self, quantity):
        cards_drawn = []
        for i in range(quantity):
            cards_drawn.append(self.cards.pop())
        return cards_drawn
