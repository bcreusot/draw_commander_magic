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


binary_lands = {
    # Bi color lands
    0b11000: 2,
    0b10010: 2,
    0b10001: 2,
    0b01100: 2,
    0b01010: 2,
    0b01001: 2,
    0b00110: 2,
    0b00011: 2,

    # Tri color lands
    0b11100: 2,
    0b10101: 2,
    0b10011: 2,
    0b01011: 2,
    0b01110: 2,
    0b01101: 2,
    0b10110: 2,
    0b11001: 2,
    0b00111: 2,
    0b11010: 2,

    0b11111: 6
}

class GameController:

    CONST_ISLAND_MASK = 0b10000
    CONST_FOREST_MASK = 0b01000
    CONST_PLAIN_MASK = 0b00100
    CONST_MOUNTAIN_MASK = 0b00010
    CONST_SWAMP_MASK = 0b00001

    def __init__(self, deck_wanted_size,hand_init_size, enable_mulligan=True):
        self.deck = Deck()
        self.hand = Hand()
        self.board = Board()
        self.deck_wanted_size = deck_wanted_size
        self.hand_init_size = hand_init_size
        self.enable_mulligan = enable_mulligan

        self.decision_tree = {}
        self.compute_tree = []

    def init(self):
        self.deck.clear()
        self.hand.clear()
        self.board.clear()

    def insert_lands_in_deck(self):
        for land,quantity in binary_lands.items():
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
        self.deck.shuffle()
        self.hand.clear()
        self.mulligan_phase(hand_size - 1)

    def run(self):
        self.init()
        self.game_set_up()
        self.mulligan_phase(self.hand_init_size)
        print(self.hand)
        ret = self.game()
        # game_result(ret)

    def place_element_tree(self,tree, elem):
        if not tree:
            if type(elem) != tuple:
                elem = tuple(elem)
            for e in elem:
                tree[e] = {}
            return
        for key, val in tree.items():
            self.place_element_tree(val, elem)

    def construct_decision_tree(self):
        for card in self.board.get_cards():
            if card.name == 'cavern':
                continue
            self.place_element_tree(self.decision_tree, card)

    def do_compute_tree(self,next_elem, path=''):
        if not next_elem:
            return self.compute_tree.append(path)
        for key, val in next_elem.items():
            if key in path:
                self.do_compute_tree(val, path)
            else:
                self.do_compute_tree(val, path + key)

    def check_succeed(self):
        if self.board.get_size() > 5 and self.board.has_cavern():
            return True
        self.construct_decision_tree()
        # print(json.dumps(decision_tree, indent=1))
        self.do_compute_tree(self.decision_tree)
        # print(json.dumps(compute_tree, indent=1))

        for elem in self.compute_tree:
            if len(elem) == 5:#nb_diff_land_to_collect:
                return True
        return False

    def place_land_board(self):
        weight_matrix = {}
        for key,card in enumerate(self.hand.get_cards()):
            if card.name == 'useless':
                continue
            if card.name == 'cavern':
                if len(self.board.get_size()) == 5:
                    weight_matrix[key] = 100
                else:
                    weight_matrix[key] = 0.5
            if card in self.board.get_cards():
                weight_matrix[key] = 1
            weight_matrix[key] = len(card.get_mana_colors())

        if not weight_matrix:
            return
        key = max(weight_matrix, key=weight_matrix.get)

        card_to_add = self.hand.remove(key)
        self.board.add_card(card_to_add)
        # print('%s added to the board...' % (card_to_add))
        # print(self.board)

    def game(self):
        while self.deck.get_size() > 0:

            self.decision_tree = {}
            self.compute_tree = []

            card_drawn = self.deck.draw(1)
            # print("Draw %s" % (card_drawn,))
            self.hand.add_cards(card_drawn)
            self.place_land_board()
            if self.check_succeed():
                return 1
        return 0

    @staticmethod
    def get_land_quantity():
        return len(binary_lands)


if __name__ == "__main__":
    gc = GameController(100, 30)
    gc.run()
