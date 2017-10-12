from board import Board
from card import Card
from deck import Deck
from hand import Hand

# Island | Forest | Plain | Mountain | Swamp

binary_lands = {
    # Bi color lands
    0b11000: 2,
    0b10010: 1,
    0b10001: 2,
    0b01100: 1,
    0b01010: 1,
    0b01001: 1,
    0b00110: 1,
    0b00011: 1,

    # Tri color lands
    0b11100: 1,
    0b10101: 1,
    0b10011: 1,
    0b01011: 1,
    0b01110: 1,
    0b01101: 1,
    0b10110: 1,
    0b11001: 1,
    0b00111: 1,
    0b11010: 1,

    0b11111: 6
}

class GameController:

    CONST_ISLAND_MASK = 0b10000
    CONST_FOREST_MASK = 0b01000
    CONST_PLAIN_MASK = 0b00100
    CONST_MOUNTAIN_MASK = 0b00010
    CONST_SWAMP_MASK = 0b00001

    def __init__(self, deck_wanted_size,hand_init_size):
        self.deck = Deck()
        self.hand = Hand()
        self.board = Board()
        self.deck_wanted_size = deck_wanted_size
        self.hand_init_size = hand_init_size
        self.enable_mulligan = True

    def init(self):
        self.deck.clear()
        self.hand.clear()
        self.board.clear()

    def insert_lands_in_deck(self):
        for land,quantity in binary_lands:
            card = Card(
                'terrain',
                land & self.CONST_ISLAND_MASK,
                land & self.CONST_FOREST_MASK,
                land & self.CONST_PLAIN_MASK,
                land & self.CONST_MOUNTAIN_MASK,
                land & self.CONST_SWAMP_MASK,
            )
            self.deck.add_card(card)

    def fill_deck(self):
        for i in range(self.deck_wanted_size - self.get_land_quantity()):
            self.deck.add_card(Card('useless'))


    def game_set_up(self):
        self.insert_lands_in_deck()
        self.fill_deck()
        self.deck.shuffle()

    # If we enable mulligans
    def mulligan_phase(self, hand_size):
        cards_drawn = self.deck.draw(hand_size)
        self.hand.clear()
        self.hand.add_cards(cards_drawn)
        if not self.enable_mulligan or \
           hand_size == 0 or \
           not self.hand.is_improvable(self.get_land_quantity(), self.deck.get_size()):
            return

        # Put card back into the deck and redraw
        self.deck.add_cards(self.hand.get_cards())
        self.hand.clear()
        self.mulligan_phase(hand_size - 1)

    def run(self):
        self.init()
        self.game_set_up()
        self.mulligan_phase(self.hand_init_size)
        ret = game()
        game_result(ret)

    def get_land_quantity(self):
        return len(binary_lands)
