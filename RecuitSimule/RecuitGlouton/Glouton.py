from Base import Base
from Solution import Solution
from copy import deepcopy
from random import randint, choice


class Glouton(Base):
    rand_factor = None

    def _start(self, rand_factor):
        self.rand_factor = rand_factor
        solution = Solution(self._antenna_list, self._switch_list)

        for i in range(len(self._antenna_list)):
            k = self.get_next_antenna(solution)
            best_antennas = []

            for j in range(len(self._switch_list)):
                temp = solution.cost
                if solution.assign(k, j):
                    self._antenna_list[k].score = solution.cost
                    self._antenna_list[k].switch_id = j
                    best_antennas.append(deepcopy(self._antenna_list[k]))
                    solution.unassign(k)
                if abs(temp - solution.cost > 0.0000000001):
                    raise RuntimeError(
                        f"Erreur de remise en place de la solution: {temp} != {solution.cost}, k={k}, j={j}"
                    )

            best_antennas.sort()
            antenna = self.choose_index(best_antennas)

            solution.assign(antenna.id, antenna.switch_id)

        return solution

    def get_next_antenna(self, solution):
        best_antennas = []

        for i in range(len(self._antenna_list)):
            if solution.is_assigned(i):
                continue

            average, minimum, nb_switches = 0, -1, 0
            for j in range(len(self._switch_list)):
                if (not solution.is_assigned(i)) and solution.can_assign(i, j):
                    average += self._switch_list[j].get_antenna_cost(i)
                    if minimum == -1 or minimum > self._switch_list[j].get_antenna_cost(i):
                        minimum = self._switch_list[j].get_antenna_cost(i)
                    nb_switches += 1
            if nb_switches == 0:
                pass
            self._antenna_list[i].score = average / nb_switches - minimum
            best_antennas.append(deepcopy(self._antenna_list[i]))

        best_antennas.sort(reverse=True)
        antenna = self.choose_index(best_antennas)

        return antenna.id

    def choose_index(self, best_antennas):
        nb_intervals = 1
        for j in range(len(best_antennas) - 1):
            if best_antennas[j].score != best_antennas[j + 1].score:
                nb_intervals += 1

        interval_index = randint(0, int(self.rand_factor * nb_intervals))
        min_index = 0
        max_index = len(best_antennas)
        for j in range(len(best_antennas) - 1):
            if interval_index == 0:
                min_index = j
            if interval_index < 0:
                max_index = j
                break
            if best_antennas[j].score != best_antennas[j + 1].score:
                interval_index -= 1

        antenna = choice(best_antennas[min_index:max_index])
        return antenna
