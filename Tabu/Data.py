import json
from copy import deepcopy

from Tableau import Tableau


class Data:
    PENALITE = 50
    PENALITE_FIXE = 100

    def __init__(self, nom_fichier):
        with open(nom_fichier, 'r') as f:
            data = json.load(f)

        self.nb_cellules = data['NbAntennas']
        self.nb_commutateurs = data['NbSwitches']
        self.tableau_releve = Tableau(data['HandoffCost'])
        self.tableau_cablage = Tableau(data['AntSwitchCost'])
        self.capacite_cellules = data['CallVolume'].copy()
        self.capacite_commutateurs = data['CallCapacity'].copy()
        self.capacite_residuelle = data['CallCapacity'].copy()

    def evaluation(self, objectif):
        capacite_residuelle = 0
        nombre_violations = 0
        quantite_violation = 0

        for i in range(self.nb_commutateurs):
            capacite_residuelle += self.capacite_residuelle[i]
            if self.capacite_residuelle[i] < 0:
                quantite_violation -= self.capacite_residuelle[i]
                nombre_violations += 1

        if capacite_residuelle < 0:
            return -1
        else:
            return objectif + quantite_violation * self.PENALITE + nombre_violations * self.PENALITE_FIXE

    def nouvelle_evaluation(self, objectif):
        nombre_violations = 0
        quantite_violation = 0

        for k in range(self.nb_commutateurs):
            if self.capacite_residuelle[k] < 0:
                quantite_violation -= self.capacite_residuelle[k]
                nombre_violations += 1

        return objectif + quantite_violation * self.PENALITE + nombre_violations * self.PENALITE_FIXE

    def respecte(self):
        for i in range(self.nb_commutateurs):
            if self.capacite_residuelle[i] < 0:
                return False
        return True

    def copy(self):
        return deepcopy(self)