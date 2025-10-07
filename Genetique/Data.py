import json

from Tableau import Tableau


class Data:
    def __init__(self, nom_fichier, nb_generations, nb_cycles, prob_croisement, prob_mutation):
        with open(nom_fichier, 'r') as f:
            data = json.load(f)

            self.nb_cellules = data['NbAntennas']
            self.nb_commutateurs = data['NbSwitches']
            self.tableau_releve = Tableau(data['HandoffCost'])
            self.tableau_cablage = Tableau(data['AntSwitchCost'])
            self.capacite_cellules = data['CallVolume'].copy()
            self.capacite_commutateurs = data['CallCapacity'].copy()

            self.taille_max = data['NbAntennas']
            self.nb_generations = nb_generations
            self.nb_cycles = nb_cycles

            if not 0 <= prob_croisement <= 1:
                raise ArithmeticError("Probabilité de croisement doit être entre 0 et 1.")
            else:
                self.probabilite_croisement = prob_croisement

            if not 0 <= prob_mutation <= 1:
                raise ArithmeticError("Probabilité de mutation doit être entre 0 et 1.")
            else:
                self.probabilite_mutation = prob_mutation
