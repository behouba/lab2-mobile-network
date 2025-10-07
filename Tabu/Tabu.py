from Data import Data
from Diverse import Diverse
from FixedList import FixedList
from Gain import Gain
from Intense import Intense
from Mouvement import Mouvement
from Solution import Solution
from config import KMAX, LIMITE_RESPECT, LIMITE_SEVERITE, INTBIG, PRIME_CAPACITE_FIXE, PRIME_CAPACITE, EPSILON


class Tabu:
    def __init__(self, nom_fichier, taille_tabu=9, moyen_terme=False, long_terme=False):
        self.data = Data(nom_fichier)
        self.solution = Solution(self.data)
        self.solution_initiale = None
        self.gain = Gain(self.data)

        self.liste_tabu = FixedList(taille_tabu)

        if moyen_terme:
            self.intensification = Intense(self.data)
        else:
            self.intensification = None
        if long_terme:
            self.diversification = Diverse(self.data)
        else:
            self.diversification = None

    def tabu_court_moyen(self, solution: Solution):
        severite = 0
        type_gain = 1
        non_respect = 0

        objectif = solution.objectif(self.data)

        solution_best = solution.copy()
        evaluation_best = evaluation_actuelle = self.data.evaluation(objectif)

        iteration_actuelle = iteration_best = 0

        gain_penalite = Gain(self.data)
        self.gain.generer(self.data, solution)

        if self.intensification is not None:
            self.intensification.append(self.data, solution, self.gain, evaluation_actuelle, objectif)

        if self.diversification is not None:
            self.diversification.compte(solution)

        while True:
            if iteration_actuelle - iteration_best < KMAX:
                if not self.data.respecte():
                    non_respect += 1
                else:
                    non_respect = 0
                    severite = 0
                    type_gain = 1

                if non_respect >= LIMITE_RESPECT:
                    if severite < LIMITE_SEVERITE:
                        severite += 1
                    type_gain = 2

                # On prend en compte les contraintes de capacite dans le calcul du gain
                if type_gain == 2:
                    for j in range(self.gain.nb_cellules):
                        for k in range(self.gain.nb_commutateurs):
                            # Il faut pénaliser la solution car elle ne respecte pas les contraintes
                            if self.data.capacite_residuelle[k] < 0:
                                if self.gain[j, k] != INTBIG:
                                    gain_penalite[j, k] = self.gain[j, k] + severite * (
                                            PRIME_CAPACITE_FIXE + PRIME_CAPACITE * (
                                            self.data.capacite_cellules[j] - self.data.capacite_residuelle[k]))
                                else:
                                    gain_penalite[j, k] = INTBIG
                            else:
                                gain_penalite[j, k] = self.gain[j, k]
                    mouvement = self.choisit_mouvement(
                        evaluation_best, objectif, gain_penalite, solution
                    )
                else:
                    mouvement = self.choisit_mouvement(
                        evaluation_best, objectif, self.gain, solution
                    )

                if mouvement is not None:
                    iteration_actuelle += 1

                    cellule, nouveau_comm = mouvement.cellule, mouvement.commutateur
                    ancien_comm = solution.recherche_commutateur(cellule)

                    solution[cellule, ancien_comm] = 0
                    solution[cellule, nouveau_comm] = 1

                    if self.diversification is not None:
                        self.diversification.compte(solution)

                    self.data.capacite_residuelle[ancien_comm] += self.data.capacite_cellules[cellule]
                    self.data.capacite_residuelle[nouveau_comm] -= self.data.capacite_cellules[cellule]

                    objectif += self.gain[cellule, nouveau_comm]
                    evaluation_actuelle = self.data.nouvelle_evaluation(objectif)

                    self.gain.mise_a_jour(self.data, solution, cellule, nouveau_comm, ancien_comm)

                    mouvement_inverse = Mouvement(cellule, ancien_comm)
                    self.liste_tabu.append(mouvement_inverse)

                    if (evaluation_best - evaluation_actuelle) > EPSILON:
                        solution_best = solution.copy()
                        iteration_best = iteration_actuelle
                        evaluation_best = evaluation_actuelle

                        if self.intensification is not None:
                            self.intensification.append(self.data, solution_best, self.gain, evaluation_best, objectif)
                else:
                    break
            else:
                break

        if self.intensification is not None:
            evaluation_intense, solution_intense = self.intensification.intensifie(self.data, evaluation_best)
            if solution_intense is not None:
                return evaluation_intense, solution_intense

        return evaluation_best, solution_best

    def choisit_mouvement(self, evaluation_best: float, objectif: float, gain: Gain, solution: Solution):
        mouvement = Mouvement()
        meilleur = INTBIG
        local_data = self.data.copy()
        local_best = evaluation_best

        for i in range(self.data.nb_cellules):
            for k in range(self.data.nb_commutateurs):
                if gain[i, k] < meilleur:
                    mouvement_temporaire = Mouvement(i, k)
                    if mouvement_temporaire not in self.liste_tabu:
                        mouvement = mouvement_temporaire
                        meilleur = gain[i, k]
                    else:
                        cellule = i
                        nouveau_comm = k
                        ancien_comm = solution.recherche_commutateur(cellule)

                        local_data.capacite_residuelle[ancien_comm] += self.data.capacite_cellules[cellule]
                        local_data.capacite_residuelle[nouveau_comm] -= self.data.capacite_cellules[cellule]

                        nouveau_objectif = objectif + self.gain[cellule, nouveau_comm]
                        best_temporaire = local_data.nouvelle_evaluation(nouveau_objectif)
                        if best_temporaire < local_best:
                            mouvement = mouvement_temporaire
                            break
                        else:
                            local_data.capacite_residuelle[ancien_comm] -= self.data.capacite_cellules[cellule]
                            local_data.capacite_residuelle[nouveau_comm] += self.data.capacite_cellules[cellule]
            else:
                continue
            break

        return mouvement if mouvement != Mouvement() else None

    def run(self):
        self.solution.initialiser(self.data)
        solution_temporaire: Solution = self.solution.copy()

        evaluation_temporaire, solution_temporaire = self.tabu_court_moyen(solution_temporaire)
        self.solution_initiale = solution_temporaire.copy()
        evaluation_best = evaluation_temporaire
        self.solution = solution_temporaire.copy()

        if self.diversification:
            for i in range(self.diversification.nb_start):
                self.gain = Gain(self.data)
                solution_temporaire.initialiser(self.data, self.diversification)
                if self.intensification is not None:
                    self.intensification = Intense(self.data)

                evaluation_temporaire, solution_temporaire = self.tabu_court_moyen(solution_temporaire)

                if evaluation_best - evaluation_temporaire > EPSILON:
                    self.solution = solution_temporaire.copy()
                    evaluation_best = evaluation_temporaire

        return evaluation_best

    def respecte_conditions(self):
        for j in range(self.data.nb_commutateurs):
            somme = self.data.capacite_commutateurs[j]
            for i in range(self.data.nb_cellules):
                somme -= self.solution[i, j] * self.data.capacite_cellules[i]
            if somme < 0:
                return False
        return True

    def affiche_resultats(self, best_cout):
        msg = ""
        msg += f"COUT MEILLEURE SOLUTION: {best_cout:.2f}\n"
        msg += f"RESPECTE CONDITION: {self.respecte_conditions()}"
        print(msg)

    def affiche_solution(self):
        for i in range(len(self.solution)):
            print(f"Cellule: {i} MSC: {self.solution.tableau[i].index(1)}")