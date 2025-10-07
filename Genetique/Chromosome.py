from copy import deepcopy
from random import randint, random

from Data import Data
from FixedList import FixedList
from config import PENALITE, INTBIG


class Chromosome:
    def __init__(self, data: Data):
        self.chromosomes = FixedList(content=[randint(0, data.nb_commutateurs - 1) for _ in range(data.nb_cellules)])
        self.capacites_commutateurs = FixedList(content=[0 for _ in range(data.nb_commutateurs)])

    @classmethod
    def from_parents(cls, chromosome1, chromosome2, mixing_index):
        enfant1 = chromosome1.copy()
        enfant2 = chromosome2.copy()

        enfant1.chromosomes[mixing_index + 1:] = chromosome2.chromosomes[mixing_index + 1:]
        enfant2.chromosomes[mixing_index + 1:] = chromosome1.chromosomes[mixing_index + 1:]

        return enfant1, enfant2

    @classmethod
    def from_inversion(cls, chromosome):
        enfant = chromosome.copy()
        enfant.chromosomes.reverse()
        return enfant

    def evaluer_liaison(self, data):
        valeur_objective = 0.0
        for j in range(data.nb_cellules):
            valeur_objective += data.tableau_cablage[j, self.chromosomes[j]]

        return valeur_objective

    def evaluer_releve(self, data):
        valeur_objective = 0.0
        for j in range(data.nb_cellules):
            for k in range(data.nb_cellules):
                if self.chromosomes[j] != self.chromosomes[k]:
                    valeur_objective += data.tableau_releve[j, k]

        return valeur_objective

    def evaluer_penalite(self, data):
        valeur_objective = 0.0
        for j in range(data.nb_commutateurs):
            if data.capacite_commutateurs[j] < self.capacites_commutateurs[j]:
                valeur_objective += (data.capacite_commutateurs[j] - self.capacites_commutateurs[j]) * PENALITE

        return valeur_objective

    def evaluer_capacite_chromosome(self, data):
        for i in range(data.nb_commutateurs):
            self.capacites_commutateurs[i] = 0

        for i in range(data.nb_cellules):
            commutateur = self.chromosomes[i]
            self.capacites_commutateurs[commutateur] += data.capacite_cellules[i]

    def calculer_cout(self, data):
        return self.evaluer_liaison(data) + self.evaluer_releve(data) + self.evaluer_penalite(data)

    # def remplir_chromosome(self, index, value):
    #     self.chromosomes[index] = value
    #
    # def remplir_capacite(self, index, value):
    #     self.capacites_commutateurs[index] = value

    def plus_courte_distance(self, data):
        for i in range(data.nb_cellules):
            cout_minimal = INTBIG
            indice = 0
            for j in range(data.nb_commutateurs):
                if data.tableau_cablage[i, j] < cout_minimal:
                    cout_minimal = data.tableau_cablage[i, j]
                    indice = j
            self.chromosomes[i] = indice

    def muter_chromosome(self, data):
        prob = random()
        if prob <= data.probabilite_mutation:
            indice = randint(0, data.nb_cellules - 1)
            value = randint(0, data.nb_commutateurs - 1)

            self.chromosomes[indice] = value

    def faisabilite(self, data: Data):
        for i in range(data.nb_commutateurs):
            if self.capacites_commutateurs[i] > data.capacite_commutateurs[i]:
                return False
        return True

    def copy(self):
        return deepcopy(self)

    def __repr__(self):
        msg = ""
        for i in range(len(self.chromosomes)):
            msg += f"Cellule: {i} MSC {self.chromosomes[i]}\n"
        return msg
