from math import exp

from Base import Base
from copy import deepcopy
from random import choice, random


class Recuit(Base):
    init_temp = None
    t_factor = None
    t_palier = None

    def _start(self, initial_solution, init_temp, t_factor, t_palier):
        acceptance_threshold = 0.005
        acceptance_counter = 0
        acceptance_max = 10

        temp = init_temp

        best_solution = deepcopy(initial_solution)
        solution = deepcopy(initial_solution)

        if solution.is_partial():
            raise RuntimeError("Solution initiale partielle, recuit simulé impossible")

        if not solution.is_valid():
            raise RuntimeError("Solution initiale non valide.")

        done = False
        while not done:
            best_cost = solution.cost
            acceptance_rate = 0
            nb_moves = 0

            for k in range(t_palier):
                i = choice(self._antenna_list).id
                j = choice(self._switch_list).id
                old_switch_id = solution.get_assignment(i)

                if j != old_switch_id:
                    if solution.assign(i, j):
                        delta_cost = solution.cost - best_cost
                        if self.metropolis(delta_cost, temp):
                            best_cost = solution.cost
                            nb_moves += 1
                            if best_cost < best_solution.cost:
                                best_solution = deepcopy(solution)
                        else:
                            solution.assign(i, old_switch_id)

                acceptance_rate = nb_moves/(k+1)

            if acceptance_rate <= acceptance_threshold:
                acceptance_counter += 1
            else:
                acceptance_counter = 0

            if acceptance_counter == acceptance_max:
                done = True

            temp *= t_factor

        return best_solution

    def metropolis(self, delta_cost, temp):
        if delta_cost <= 0:
            return True

        prob = exp(-delta_cost/temp)
        return random() <= prob
