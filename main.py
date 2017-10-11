#!/usr/bin/env python3
import json
from random import shuffle


bi_color_lands = {
    ('I','F')  : 2,
    ('I','P')   : 2,
    ('I','M')   : 2,
    ('I','S')   : 2,
    ('F','P')   : 2,
    ('F','M')   : 3,
    ('F','S')   : 2,
    ('P','M')    : 2,
    ('P','S')    : 2,
    ('M','S')    : 2
}

# https://mtg.gamepedia.com/TaPand#TriPe_taPands
# In the order of the web site left to right
tri_color_lands = {
    ('F','P','I'): 1,
    ('P','I','S') : 1,
    ('I','S','M') : 1,
    ('S','M','F') : 1,
    ('M','F','P') : 1,
    ('P','S','F') : 1,
    ('I','M','P') : 1,
    ('S','F','I'): 1,
    ('M','P','S')  : 1,
    ('F','I','M'): 1,
}

any_color_lands = {
    ('F', 'P', 'I', 'S', 'M') : 6
}
caverns = {
    'cavern' : 2
}

all_lands = {
    **bi_color_lands,
    **tri_color_lands,
    **any_color_lands,
    **caverns,
}

# all_lands = {
#     ('A', 'B') : 1,
#     ('C', 'D', 'E') : 1,
#     ('D', 'E') : 1,
#     'E' : 1,
#     'cavern' : 0
# }

nb_lands = sum(all_lands.values())

deck_size = 100
draw_hand_size = 7
nb_diff_land_to_collect = 5
deck = []
hand = []
board = []
decision_tree = {}
compute_tree = []
stats = {
    'cavern' : 0,
    'nb_turns' : 0
}
nb_turns_simulation = 1000
mulligan_enabled = True


def init():
    global deck, hand, board
    deck.clear()
    hand.clear()
    board.clear()


# Create deck
def game_set_up():
    for land_type in all_lands:
        deck.extend([land_type] * all_lands[land_type])
    # Fill now the deck with 'useless' cards
    deck.extend(['useless'] * (deck_size - nb_lands))
    shuffle(deck)
    # Because we draw with pop(), so reverse for better visibility
    # print('This is the deck shuffled -> %s' % list(reversed(deck)))


def is_hand_improvable(hand_size):
    if hand_size < 2:
        return False
    theory_chance_land_hand = nb_lands / deck_size
    nb_land_hand = 0
    for card in hand:
        if card != 'useless':
            nb_land_hand += 1
    # print('Hand size %i ; nb_land %i (%f |%f)' % (hand_size,nb_land_hand,theory_chance_land_hand,nb_land_hand / (hand_size-1)))
    return theory_chance_land_hand > nb_land_hand / (hand_size-1)


# If we enable mulligans
def mulligan_phase(hand_size):
    deck.extend(hand)
    hand.clear()
    shuffle(deck)
    for i in range(hand_size):
        hand.append(deck.pop())
    # print("%(hand_size)i cards hand -> %(hand)s " % {
    #     'hand_size' : hand_size,
    #     'hand'      : hand
    # })
    if not mulligan_enabled or hand_size == 0 or not is_hand_improvable(hand_size):
        return
    mulligan_phase(hand_size - 1)

# ABCDE
# -----
# AB -> CDE -> AB -> ED
# ACBE -> D
# ACBD -> E
# ADBE -> C
# AEBD -> C
# BCAE -> D
# BDAE -> C
# BCAD -> E
# BEAD -> C
# 2 D
# 4 C
# 2 E

# A -> 6
# B -> 6
# C -> 16
# D -> 8
# E -> 8


# ACD
# ACE
# ACBD
# ACBE
# AD
# ADE
# ADB
# ADBE
# AED
# AE
# AEBD
# AEB
# BCAD
# BCAE
# BCD
# BCE
# BDA
# BDAE
# BD
# BDE
# BEAD
# BEA
# BED
# BE


def place_element_tree(tree, elem):
    if not tree:
        if type(elem) != tuple:
            elem = tuple(elem)
        for e in elem:
            tree[e] = {}
        return
    for key,val in tree.items():
        place_element_tree(val,elem)


def construct_decision_tree():
    for card in board:
        if card == 'cavern':
            continue
        place_element_tree(decision_tree,card)


def do_compute_tree(next_elem, path=''):
    if not next_elem:
        return compute_tree.append(path)
    for key,val in next_elem.items():
        if key in path:
            do_compute_tree(val, path)
        else:
            do_compute_tree(val, path+key)


def check_succeed():
    if 'cavern' in board and len(board) > 5:
        return True
    construct_decision_tree()
    # print(json.dumps(decision_tree, indent=1))
    do_compute_tree(decision_tree)
    # print(json.dumps(compute_tree, indent=1))

    for elem in compute_tree:
        if len(elem) == nb_diff_land_to_collect:
            return True
    return False


def place_land_board():
    weight_matrix = {}
    card_to_add = None
    for card in hand:
        if card == 'useless':
            continue
        if card == 'cavern':
            if len(board) == 5:
                weight_matrix[card] = 100
            else:
                weight_matrix[card] = 0.5
        if card in board:
            weight_matrix[card] = 0
        weight_matrix[card] = len(card) if type(card) == tuple else 1

    if not weight_matrix:
        return
    card_to_add = max(weight_matrix, key=weight_matrix.get)

    hand.remove(card_to_add)
    board.append(card_to_add)
    # print('%s added to the board...' % (card_to_add,))
    # print('%s is the new board...' % board)


def game():
    global decision_tree,compute_tree
    while len(deck) > 0:

        decision_tree = {}
        compute_tree = []

        card_drawn = deck.pop()
        # print("Draw %s" % (card_drawn,))
        hand.append(card_drawn)
        place_land_board()
        if check_succeed():
            return 1
    return 0


def game_result(ret):
    if ret:
        nb_turns_win = (deck_size-draw_hand_size) - len(deck)
        stats['nb_turns'] += nb_turns_win
        if 'cavern' in board and len(board) > 5:
            stats['cavern'] += 1
            # print('You have done it (CAVERN) in %i turns !' % nb_turns_win)
        # else:
            # print('You have done it in %i turns !' % nb_turns_win)
    elif len(deck) <= 0:
        print('Deck empty... you lost')
    else:
        print("Something wrong occured?")


if __name__ == "__main__":
    print("Number of bi color lands -> %i" % sum(bi_color_lands.values()))
    print("Number of tri color lands -> %i" % sum(tri_color_lands.values()))
    print("Number of any color lands -> %i" % sum(any_color_lands.values()))
    print("Number of caverns -> %i" % sum(caverns.values()))
    print("Number of total lands -> %i" % nb_lands)
    for i in range(nb_turns_simulation):
        init()
        game_set_up()
        mulligan_phase(draw_hand_size)
        ret = game()
        game_result(ret)
    print('Win in avg %f turns' % (stats['nb_turns']/nb_turns_simulation))
    print('Nb cavern win %i ' % (stats['cavern']))
