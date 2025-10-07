from copy import deepcopy

from Data import Data
from Solution import Solution
from config import INTBIG


class Gain:
    def __init__(self, data: Data):
        self.nb_cellules = data.nb_cellules
        self.nb_commutateurs = data.nb_commutateurs
        self.tableau = [[0 for j in range(self.nb_commutateurs)] for i in range(self.nb_cellules)]

    def __getitem__(self, item):
        return self.tableau[item[0]][item[1]]

    def __setitem__(self, key, value):
        self.tableau[key[0]][key[1]] = value

    def generer(self, data: Data, solution: Solution):
        for cell_id in range(self.nb_cellules):
            comm_id = solution.recherche_commutateur(cell_id)

            for calc_comm_id in range(self.nb_commutateurs):
                if calc_comm_id != comm_id:
                    for calc_cell_id in range(self.nb_cellules):
                        self[cell_id, calc_comm_id] += (
                                (data.tableau_releve[cell_id, calc_cell_id] + data.tableau_releve[
                                    calc_cell_id, cell_id]) *
                                (solution[calc_cell_id, comm_id] - solution[calc_cell_id, calc_comm_id])
                        )

                    self[cell_id, calc_comm_id] += (
                            data.tableau_cablage[cell_id, calc_comm_id] - data.tableau_cablage[cell_id, comm_id]
                    )
                else:
                    self[cell_id, comm_id] = INTBIG

    def mise_a_jour(self, data: Data, solution: Solution, cellule, nouveau_commutateur, ancien_commutateur):
        for p in range(self.nb_cellules):
            if p != cellule:
                commutateur_de_p = solution.recherche_commutateur(p)
                if commutateur_de_p == ancien_commutateur:
                    for q in range(self.nb_commutateurs):
                        if q != ancien_commutateur and q != nouveau_commutateur:
                            self[p, q] -= data.tableau_releve[p, cellule] + data.tableau_releve[cellule, p]
                    self[p, nouveau_commutateur] -= 2 * (
                                data.tableau_releve[p, cellule] + data.tableau_releve[cellule, p])
                elif commutateur_de_p == nouveau_commutateur:
                    for q in range(self.nb_commutateurs):
                        if q != ancien_commutateur and q != nouveau_commutateur:
                            self[p, q] += data.tableau_releve[p, cellule] + data.tableau_releve[cellule, p]
                    self[p, ancien_commutateur] += 2 * (
                                data.tableau_releve[p, cellule] + data.tableau_releve[cellule, p])
                else:
                    self[p, ancien_commutateur] += (data.tableau_releve[p, cellule] + data.tableau_releve[cellule, p])
                    self[p, nouveau_commutateur] -= (data.tableau_releve[p, cellule] + data.tableau_releve[cellule, p])
            else:
                for q in range(self.nb_commutateurs):
                    if q != ancien_commutateur and q != nouveau_commutateur:
                        self[p, q] -= self[cellule, nouveau_commutateur]
                self[p, ancien_commutateur] = -self[cellule, nouveau_commutateur]
                self[p, nouveau_commutateur] = INTBIG

    def copy(self):
        return deepcopy(self)