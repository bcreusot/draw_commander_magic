

class Hand:

    def __init__(self):
        self.cards = []

    def clear(self):
        self.cards.clear()

    def is_improvable(self, nb_lands, deck_size):
        if len(self.cards) < 2:
            return False
        theory_chance_land_hand = nb_lands / deck_size
        nb_land_hand = 0
        for card in self.cards:
            if card.name != 'useless':
                nb_land_hand += 1
        return theory_chance_land_hand > nb_land_hand / (len(self.cards)-1)

    def add_cards(self, cards_drawn):
        for card in cards_drawn:
            self.add_card(card)

    def add_card(self, card):
        self.cards.append(card)

    def get_size(self):
        return len(self.cards)

    def get_cards(self):
        return self.cards

