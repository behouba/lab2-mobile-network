from Data import Data


class Diverse:
    def __init__(self, data: Data, nb_start=3):
        self.nb_start = nb_start
        self.statistiques = [[0 for j in range(data.nb_commutateurs)] for i in range(data.nb_cellules)]

    def __getitem__(self, item):
        return self.statistiques[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.statistiques[key[0]][key[1]] = value

    def compte(self, solution):
        for i in range(solution.nb_cellules):
            for j in range(solution.nb_commutateurs):
                self[i, j] += solution[i, j]
