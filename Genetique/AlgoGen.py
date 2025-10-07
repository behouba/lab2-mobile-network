from Chromosome import Chromosome
from Data import Data
from Population import Population
from config import INTBIG


class AlgoGen:
    @classmethod
    def run(cls, nom_fichier, nb_generations=50, nb_cycles=5, prob_croisement=0.9, prob_mutation=0.08):
        data = Data(nom_fichier, nb_generations, nb_cycles, prob_croisement, prob_mutation)

        topologie_initiale = Chromosome(data)
        cout_initial = topologie_initiale.calculer_cout(data)

        topologie_best = cls.genetique(topologie_initiale, data)
        cout_best = topologie_best.calculer_cout(data)

        return topologie_best, cout_best

    @classmethod
    def genetique(cls, chromosome: Chromosome, data: Data):
        population = Population(data)
        objectif_best = INTBIG
        for cycle in range(data.nb_cycles):
            population.population_initiale(data)

            if 0 == cycle:
                chrom_best_cycle = Chromosome(data)
            else:
                chrom_best_cycle = chromosome.copy()

            objectif_best_cycle = INTBIG

            for generation in range(data.nb_generations):
                population.evaluer_population(data, population.nouvelle_population)
                cls.alteration(data, population)

                if population.nb_violations < 2 * data.taille_max:
                    population.repechage(data)

                if 0 == cycle:
                    chromosome = population.population_triee[0].copy()
                    chrom_best_cycle = population.population_triee[0].copy()
                    objectif_best = population.tableau_valeurs[0]
                    objectif_best_cycle = population.tableau_valeurs[0]
                    cycle_best = cycle
                    generation_best = generation
                else:
                    if population.population_triee[0].faisabilite(data):
                        if population.tableau_valeurs[0] < objectif_best:
                            objectif_best = population.tableau_valeurs[0]
                            chromosome = population.population_triee[0].copy()
                            cycle_best = cycle
                            generation_best = generation
                        if population.tableau_valeurs[0] < objectif_best_cycle:
                            objectif_best_cycle = population.tableau_valeurs[0]
                            chrom_best_cycle = population.population_triee[0].copy()

                        if population.tableau_valeurs[0] > objectif_best and not chromosome.faisabilite(data):
                            objectif_best = population.tableau_valeurs[0]
                            chromosome = population.population_triee[0].copy()
                            cycle_best = cycle
                            generation_best = generation

                        if population.tableau_valeurs[0] > objectif_best_cycle and not chrom_best_cycle.faisabilite(data):
                            objectif_best_cycle = population.tableau_valeurs[0]
                            chrom_best_cycle = population.population_triee[0].copy()
                    else:
                        if population.tableau_valeurs[0] < objectif_best and not chromosome.faisabilite(data):
                            objectif_best = population.tableau_valeurs[0]
                            chromosome = population.population_triee[0].copy()
                            cycle_best = cycle
                            generation_best = generation

                        if population.tableau_valeurs[0] < objectif_best_cycle and not chrom_best_cycle.faisabilite(
                                data):
                            objectif_best_cycle = population.tableau_valeurs[0]
                            chrom_best_cycle = population.population_triee[0].copy()

        return chromosome

    @classmethod
    def alteration(cls, data: Data, population: Population):
        population.croisement(data)
        population.mutation(data)
        population.evaluer_population(data, population.population_en_attente)

        population.copier_populations()
        population.trier_populations(data)
        population.evaluer_capacite_population(data)
