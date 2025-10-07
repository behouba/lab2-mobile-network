from Data import Data
from FixedList import FixedList
from Gain import Gain
from Mouvement import Mouvement
from Solution import Solution
from config import INTENSE_TAILLE_BEST, INTENSE_TAILLE_TABU, INTENSE_KMAX, INTENSE_LIMITE_RESPECT, INTBIG, EPSILON


class Intense:
    def __init__(self, data: Data):
        self.liste_taboue_1 = FixedList(INTENSE_TAILLE_TABU)
        self.liste_taboue_2 = FixedList(INTENSE_TAILLE_TABU)
        self.liste_best = FixedList(INTENSE_TAILLE_BEST)

        self.solution = Solution(data)
        self.gain = Gain(data)
        self.commutateurs = []

    def append(self, data: Data, solution: Solution, gain: Gain, evaluation: float, objectif: float):
        self.liste_best.append(dict(
            evaluation=evaluation,
            objectif=objectif,
            solution=solution,
            gain=gain,
            capacite_residuelle=data.capacite_residuelle[:]
        ))

    def set_commutateurs(self, solution: Solution):
        for i in range(solution.nb_cellules):
            self.commutateurs.append(solution.recherche_commutateur(i))

    def intensifie(self, data: Data, evaluation_best):
        compte_respect = 0
        solution_best = solution_locale = None

        for best in self.liste_best:
            self.liste_taboue_1 = FixedList(INTENSE_TAILLE_TABU)
            self.liste_taboue_2 = FixedList(INTENSE_TAILLE_TABU)

            self.solution: Solution = best['solution']
            self.gain: Gain = best['gain']
            objectif = best['objectif']
            evaluation_locale = best['evaluation']

            evaluation_courante = evaluation_locale

            self.set_commutateurs(self.solution)

            iteration_actuelle = 0
            iteration_best = 0

            data.capacite_residuelle = best['capacite_residuelle'].copy()
            if data.respecte():
                compte_respect += 1

            while True:
                if iteration_actuelle - iteration_best < INTENSE_KMAX:
                    mouvement1, mouvement2 = Mouvement(), Mouvement()
                    if compte_respect > INTENSE_LIMITE_RESPECT:
                        mouvement1 = self.mouvement_intense_2(self.gain, data)
                    else:
                        mouvement1, mouvement2 = self.mouvement_intense_1(objectif, evaluation_locale, self.gain, data)
                    if mouvement1 != Mouvement():
                        iteration_actuelle += 1
                        cell1 = mouvement1.cellule
                        cell2 = mouvement2.cellule

                        nouveau_commutateur1 = mouvement1.commutateur
                        self.solution[cell1, self.commutateurs[cell1]] = 0
                        self.solution[cell1, nouveau_commutateur1] = 1

                        data.capacite_residuelle[self.commutateurs[cell1]] += data.capacite_cellules[cell1]
                        data.capacite_residuelle[nouveau_commutateur1] -= data.capacite_cellules[cell1]

                        objectif += self.gain[cell1, nouveau_commutateur1]
                        self.gain.mise_a_jour(data, self.solution, cell1, nouveau_commutateur1, self.commutateurs[cell1])

                        mouvement_inverse = Mouvement(cell1, self.commutateurs[cell1])
                        if compte_respect > INTENSE_LIMITE_RESPECT:
                            self.liste_taboue_2.append(mouvement_inverse)
                        else:
                            self.liste_taboue_1.append(mouvement_inverse)

                        if cell2 != -1:
                            self.solution[cell2, self.commutateurs[cell2]] = 0
                            self.solution[cell2, self.commutateurs[cell1]] = 1
                            data.capacite_residuelle[self.commutateurs[cell2]] += data.capacite_cellules[cell2]
                            data.capacite_residuelle[self.commutateurs[cell1]] -= data.capacite_cellules[cell2]

                            objectif += self.gain[cell2, self.commutateurs[cell1]]
                            evaluation_courante = data.nouvelle_evaluation(objectif)

                            self.gain.mise_a_jour(data, self.solution, cell2, self.commutateurs[cell1], self.commutateurs[cell2])

                            mouvement_inverse = Mouvement(cell2, self.commutateurs[cell2])
                            self.liste_taboue_1.append(mouvement_inverse)

                            self.commutateurs[cell1], self.commutateurs[cell2] = self.commutateurs[cell2], self.commutateurs[cell1]
                        else:
                            self.commutateurs[cell1] = mouvement1.commutateur
                            evaluation_courante = data.nouvelle_evaluation(objectif)

                        if data.respecte():
                            compte_respect = 0
                        else:
                            compte_respect += 1

                        if evaluation_locale - evaluation_courante > EPSILON:
                            solution_locale = self.solution.copy()
                            iteration_best = iteration_actuelle
                            evaluation_locale = evaluation_courante
                    else:
                        break
                else:
                    break

            if evaluation_best - evaluation_locale > EPSILON:
                solution_best = solution_locale.copy()
                evaluation_best = evaluation_locale

        return evaluation_best, solution_best

    def mouvement_intense_1(self, objectif, evaluation_best, gain: Gain, data: Data):
        meilleur = INTBIG
        data_local = data.copy()
        evaluation_best_locale = evaluation_best

        solution_temporaire = self.solution.copy()
        mouvement1, mouvement2 = Mouvement(), Mouvement()

        for i in range(data.nb_cellules):
            for j in range(i + 1, data.nb_cellules):
                if gain[i, self.commutateurs[j]] != INTBIG \
                        and gain[i, self.commutateurs[j]] + gain[j, self.commutateurs[i]] < meilleur:
                    mouvement_temp1 = Mouvement(i, self.commutateurs[j])
                    mouvement_temp2 = Mouvement(j, self.commutateurs[i])

                    if mouvement_temp1 not in self.liste_taboue_1 and mouvement_temp2 not in self.liste_taboue_1:
                        mouvement1 = mouvement_temp1.copy()
                        mouvement2 = mouvement_temp2.copy()
                        meilleur = gain[i, self.commutateurs[j]] + gain[j, self.commutateurs[i]]
                    else:
                        gain_local = gain.copy()
                        objectif_nouveau = objectif
                        solution_temporaire[i, self.commutateurs[i]] = 0
                        solution_temporaire[i, self.commutateurs[j]] = 1

                        data_local.capacite_residuelle[self.commutateurs[i]] += data.capacite_cellules[i]
                        data_local.capacite_residuelle[self.commutateurs[j]] -= data.capacite_cellules[i]

                        objectif_nouveau += gain_local[i, self.commutateurs[j]]
                        gain_local.mise_a_jour(data, solution_temporaire, i, self.commutateurs[j], self.commutateurs[i])

                        data_local.capacite_residuelle[self.commutateurs[j]] += data.capacite_cellules[j]
                        data_local.capacite_residuelle[self.commutateurs[i]] -= data.capacite_cellules[j]

                        objectif_nouveau += gain_local[j, self.commutateurs[i]]
                        evaluation_best_temporaire = data_local.nouvelle_evaluation(objectif_nouveau)

                        if evaluation_best_temporaire < evaluation_best_locale:
                            evaluation_best_locale = evaluation_best_temporaire
                            mouvement1 = mouvement_temp1.copy()
                            mouvement2 = mouvement_temp2.copy()
                            return mouvement1, mouvement2
                        else:
                            solution_temporaire[i, self.commutateurs[i]] = 1
                            solution_temporaire[i, self.commutateurs[j]] = 0

                            data_local.capacite_residuelle[self.commutateurs[i]] -= data.capacite_cellules[i] - \
                                                                                    data.capacite_cellules[j]
                            data_local.capacite_residuelle[self.commutateurs[j]] -= data.capacite_cellules[j] - \
                                                                                    data.capacite_cellules[i]

        return mouvement1, mouvement2

    def mouvement_intense_2(self, gain: Gain, data: Data):
        min_resi = min_gain = min_cell = INTBIG
        comm_min = comm_max = cell_min = -1

        # Le commutateur avec la plus petite capacité résiduelle
        for i in range(data.nb_commutateurs):
            if data.capacite_residuelle[i] < min_resi:
                min_resi = data.capacite_residuelle[i]
                comm_min = i

        # La cellule du commutateur minimal qui a la plus faible capacité
        for j in range(data.nb_cellules):
            if self.commutateurs[j] == comm_min and data.capacite_cellules[j] < min_cell:
                min_cell = data.capacite_cellules[j]
                cell_min = j

        # Le commutateur auquel il faut affecter la cellule minimale
        for comm in range(data.nb_commutateurs):
            mouvement_temporaire = Mouvement(cell_min, comm)
            if gain[cell_min, comm] < min_gain and data.capacite_residuelle[comm] >= min_cell \
                    and mouvement_temporaire not in self.liste_taboue_2:
                min_gain = gain[cell_min, comm]
                comm_max = comm

        if comm_max != -1:
            return Mouvement(cell_min, comm_max)
        else:
            return Mouvement()
