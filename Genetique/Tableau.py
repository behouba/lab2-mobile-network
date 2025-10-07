from copy import deepcopy


class Tableau:
    def __init__(self, tableau=None):
        if tableau is None:
            self.tableau = [[]]
        else:
            self.tableau = deepcopy(tableau)

    def __getitem__(self, item):
        return self.tableau[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.tableau[key[0]][key[1]] = value
