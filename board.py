

class Board:

    def __init__(self):
        self.cards = []

    def clear(self):
        self.cards.clear()

    def get_size(self):
        return len(self.cards)

    def get_cards(self):
        return self.cards

    def add_card(self, card):
        self.cards.append(card)

    def __repr__(self):
        display = "----------- BOARD ({})-----------\n".format(self.get_size())
        for card in self.cards:
            display += str(card) + "\n"
        display += "-----------------------------"
        return display

    def has_cavern(self):
        for card in self.cards:
            if card.name == 'cavern':
                return True
