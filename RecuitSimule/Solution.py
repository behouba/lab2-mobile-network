class Solution:
    def __init__(self, antenna_list=None, switch_list=None):
        self.__cost = 0

        if antenna_list is None or switch_list is None:
            self.__antenna_list = []
            self.__switch_list = []
        else:
            self.__antenna_list = antenna_list
            self.__switch_list = switch_list
            self.__assignment = [None for i in range(len(antenna_list))]

    @property
    def antenna_list(self):
        return self.__antenna_list

    @antenna_list.setter
    def antenna_list(self, pantenna_list):
        self.__antenna_list = pantenna_list

    @property
    def switch_list(self):
        return self.__switch_list

    @switch_list.setter
    def switch_list(self, pswitch_list):
        self.__switch_list = pswitch_list

    def is_valid(self):
        for switch in self.__switch_list:
            if switch.call_capacity < 0:
                return False
        return True

    def is_partial(self):
        for value in self.__assignment:
            if value is None:
                return True
        return False

    @property
    def cost(self):
        return self.__cost

    def __update_cost(self, antenna_id, switch_id=None):
        if self.__assignment[antenna_id] is not None:
            self.__cost -= self.__switch_list[self.__assignment[antenna_id]].get_antenna_cost(antenna_id)

        if switch_id is not None:
            self.__cost += self.__switch_list[switch_id].get_antenna_cost(antenna_id)

        for i in range(len(self.__antenna_list)):
            if self.__assignment[antenna_id] is not None:
                if self.__assignment[i] is not None:
                    if self.__assignment[antenna_id] != self.__assignment[i]:
                        self.__cost -= self.__antenna_list[antenna_id].get_handoff_cost(i)
                        self.__cost -= self.__antenna_list[i].get_handoff_cost(antenna_id)

            if switch_id is not None:
                if self.__assignment[i] is not None:
                    if switch_id != self.__assignment[i]:
                        self.__cost += self.__antenna_list[antenna_id].get_handoff_cost(i)
                        self.__cost += self.__antenna_list[i].get_handoff_cost(antenna_id)

    def can_assign(self, antenna_id, switch_id):
        return self.__switch_list[switch_id].call_capacity >= self.__antenna_list[antenna_id].call_volume

    def assign(self, antenna_id, switch_id):
        if not self.can_assign(antenna_id, switch_id):
            return False

        self.unassign(antenna_id)
        self.__update_cost(antenna_id, switch_id)

        self.__switch_list[switch_id].call_capacity = self.__switch_list[switch_id].call_capacity - self.__antenna_list[
            antenna_id].call_volume

        self.__assignment[antenna_id] = switch_id
        return True

    def unassign(self, antenna_id):
        if not self.is_assigned(antenna_id):
            return False

        self.__update_cost(antenna_id, None)
        self.__switch_list[self.__assignment[antenna_id]].call_capacity = self.__switch_list[self.__assignment[
            antenna_id]].call_capacity + self.__antenna_list[antenna_id].call_volume

        self.__assignment[antenna_id] = None

    def is_assigned(self, antenna_id):
        return self.__assignment[antenna_id] is not None

    def get_assignment(self, antenna_id):
        return self.__assignment[antenna_id]

    def __repr__(self):
        value = []
        for i in range(len(self.__antenna_list)):
            value.append(f"L'antenne {i} est raccordée au commutateur {self.__assignment[i]}")

        value.append(f"Le cout total est de {self.cost}")
        value.append(f"La solution est {'partielle' if self.is_partial() else 'complète'}")
        if self.is_partial():
            for i in range(len(self.__antenna_list)):
                if self.__assignment[i] is None:
                    value.append(f"L'antenne {i} n'est pas asignée!")

        value.append(f"La solution est {'valide' if self.is_valid() else 'invalide'}")
        return '\n'.join(value)
