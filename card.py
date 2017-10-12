

class Card:

    def __init__(self,
                 name,
                 island=False,
                 forest=False,
                 mountain=False,
                 plain=False,
                 swamp=False,
                 engaged=False):
        self.name = name
        self.island = island
        self.forest = forest
        self.mountain = mountain
        self.plain = plain
        self.swamp = swamp
        self.engaged = engaged
