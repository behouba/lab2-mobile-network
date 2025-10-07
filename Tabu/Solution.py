from copy import deepcopy

from Data import Data
from Diverse import Diverse
from config import INTBIG


class Solution:
    def __init__(self, data):
        self.nb_cellules = data.nb_cellules
        self.nb_commutateurs = data.nb_commutateurs
        self.tableau = [[0 for j in range(self.nb_commutateurs)] for i in range(self.nb_cellules)]

    def __getitem__(self, item):
        return self.tableau[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.tableau[key[0]][key[1]] = value

    def __len__(self):
        return len(self.tableau)

    def _solution_initiale(self, data: Data):
        for i in range(self.nb_cellules):
            cout_minimum = INTBIG
            comm_minimum = None
            for j in range(self.nb_commutateurs):
                if data.tableau_cablage[i, j] < cout_minimum:
                    cout_minimum = data.tableau_cablage[i, j]
                    comm_minimum = j
            self[i, comm_minimum] = 1
            data.capacite_residuelle[comm_minimum] -= data.capacite_cellules[i]

    def _solution_initiale_long_terme(self, data: Data, diversification: Diverse):
        # Désaffecte toutes les cellules et reset les capacités résiduelles
        for j in range(self.nb_commutateurs):
            data.capacite_residuelle[j] = data.capacite_commutateurs[j]
            for i in range(self.nb_cellules):
                self[i, j] = 0

        for i in range(self.nb_cellules):
            # Selection du commutateur avec les plus petites statistiques de diversification pour chaque cellule
            comm_select = 0
            for j in range(self.nb_commutateurs):
                if diversification[i, j] < diversification[i, comm_select]:
                    comm_select = j
            self[i, comm_select] = 1
            data.capacite_residuelle[comm_select] -= data.capacite_cellules[i]

    def initialiser(self, data: Data, diversification=None):
        if diversification is not None:
            self._solution_initiale_long_terme(data, diversification)
        else:
            self._solution_initiale(data)

    def copy(self):
        return deepcopy(self)

    def objectif(self, data: Data):
        resultat = 0
        for i in range(self.nb_cellules):
            for k in range(self.nb_commutateurs):
                for j in range(self.nb_cellules):
                    if self[i, k] == 1:
                        resultat += data.tableau_releve[i, j] * (1 - self[j, k])
                resultat += data.tableau_cablage[i, k] * self[i, k]
        return resultat

    def recherche_commutateur(self, cellule):
        for commutateur in range(self.nb_commutateurs):
            if self[cellule, commutateur] == 1:
                return commutateur
