

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

    def __repr__(self):
        return "{name} -> ({mana_color}){engaged}".format(
            name=self.name,
            mana_color=",".join(self.get_mana_colors()),
            engaged=" - engaged" if self.engaged else ""
        )

    def get_mana_colors(self):
        mana_colors = []
        if self.island:
            mana_colors.append("Island")
        if self.forest:
            mana_colors.append("Forest")
        if self.mountain:
            mana_colors.append("Mountain")
        if self.plain:
            mana_colors.append("Plain")
        if self.swamp:
            mana_colors.append("Swamp")
        return mana_colors

    def get_binary_color_matrix(self):
        mana_colors = []
        if self.island:
            mana_colors.append(0b10000)
        if self.forest:
            mana_colors.append(0b01000)
        if self.mountain:
            mana_colors.append(0b00100)
        if self.plain:
            mana_colors.append(0b00010)
        if self.swamp:
            mana_colors.append(0b00001)
        return mana_colors
