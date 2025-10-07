from copy import deepcopy


class Mouvement:
    def __init__(self, cellule=-1, commutateur=-1):
        self.cellule = cellule
        self.commutateur = commutateur

    def __eq__(self, other):
        return self.cellule == other.cellule and self.commutateur == other.commutateur

    def copy(self):
        return deepcopy(self)

    def __repr__(self):
        return f"cell {self.cellule} -> comm {self.commutateur}"
