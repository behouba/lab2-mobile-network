from random import randint, random

from Chromosome import Chromosome
from Data import Data
from FixedList import FixedList


class Population:
    def __init__(self, data: Data):
        self.nouvelle_population = FixedList(content=[Chromosome(data) for _ in range(data.taille_max)])
        self.population_en_attente = FixedList(size=2 * data.taille_max)
        self.population_triee = FixedList(content=[Chromosome(data) for _ in range(2 * data.taille_max)])

        self.viol_capacite = FixedList(content=[Chromosome(data) for _ in range(2 * data.taille_max)])
        self.tableau_valeurs = FixedList(content=[0 for _ in range(2 * data.taille_max)])
        self.tableau_viol = FixedList(content=[0 for _ in range(2 * data.taille_max)])

        self.nb_violations = 0

    def population_initiale(self, data):
        self.nouvelle_population = FixedList(content=[Chromosome(data) for _ in range(data.taille_max)])
        self.nouvelle_population[0].plus_courte_distance(data)
        self.nb_violations = 0

    def evaluer_population(self, data, population):
        for i, chromosome in enumerate(population):
            self.tableau_valeurs[i] = chromosome.evaluer_liaison(data) + chromosome.evaluer_releve(data)

    def croisement(self, data: Data):
        taille_max = data.taille_max
        for j in range(taille_max, 0, -2):
            select1 = randint(0, taille_max - 1)
            temp1 = self.nouvelle_population[select1].copy()

            select2 = randint(0, taille_max - 1)
            temp2 = self.nouvelle_population[select2].copy()

            self.population_en_attente.append(temp1.copy())
            self.population_en_attente.append(temp2.copy())

            prob = random()
            if prob <= data.probabilite_croisement:
                lieu_croisement = randint(0, data.nb_cellules - 1)
                enfant1, enfant2 = Chromosome.from_parents(temp1, temp2, lieu_croisement)
            else:
                enfant1 = Chromosome.from_inversion(temp1)
                enfant2 = Chromosome.from_inversion(temp2)

            self.population_en_attente.append(enfant1)
            self.population_en_attente.append(enfant2)

    def mutation(self, data: Data):
        for i in range(data.taille_max):
            self.population_en_attente[i].muter_chromosome(data)

    def copier_populations(self):
        self.population_triee = self.population_en_attente.copy()

    def trier_populations(self, data: Data):
        for i in range(len(self.population_triee) - 1):
            minimum = i
            for j in range(i + 1, len(self.population_triee)):
                if self.tableau_valeurs[j] < self.tableau_valeurs[minimum]:
                    minimum = j

            self.tableau_valeurs[i], self.tableau_valeurs[minimum] = self.tableau_valeurs[minimum], \
                                                                     self.tableau_valeurs[i]
            self.population_triee[i], self.population_triee[minimum] = self.population_triee[minimum], \
                                                                       self.population_triee[i]

    def evaluer_capacite_population(self, data):
        for i in range(2 * data.taille_max):
            self.population_triee[i].evaluer_capacite_chromosome(data)

        i, fin = 0, 2 * data.taille_max
        while i < fin:
            buffer_chrom = self.population_triee[i].copy()
            if not buffer_chrom.faisabilite(data):
                buffer_value = self.tableau_valeurs[i]
                for l in range(i + 1, fin):
                    self.tableau_valeurs[l - 1] = self.tableau_valeurs[l]
                    self.population_triee[l - 1] = self.population_triee[l]

                self.population_triee[fin - 1] = buffer_chrom
                self.tableau_valeurs[fin - 1] = buffer_value

                fin -= 1
            else:
                i += 1

    def repechage(self, data):
        i, fin = 0, data.taille_max
        while i < fin and self.population_triee[i].faisabilite(data):
            i += 1

        if i < fin:
            for j in range(data.nb_commutateurs):
                if self.population_triee[i].capacites_commutateurs[j] / data.capacite_commutateurs[j] > 1.10:
                    break
            else:
                self.viol_capacite[self.nb_violations] = self.population_triee[i]
                self.tableau_viol[self.nb_violations] = self.tableau_valeurs[i]
                self.nb_violations += 1

    def roulette_nouvelle_population(self, data):
        for i in range(data.taille_max):
            self.nouvelle_population[i] = self.population_triee[i].copy()
