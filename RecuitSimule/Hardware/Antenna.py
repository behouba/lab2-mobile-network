class Antenna:
    def __init__(self, pid=None, call_volume=None, ant_switch_cost=None, handoff_cost=None):
        self.__id = pid
        self.__call_volume = call_volume
        self.__handoff_cost = handoff_cost
        self.__score = None
        self.__switch_id = None
        self.__ant_switch_cost = ant_switch_cost

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, pid):
        self.__id = pid

    @property
    def call_volume(self):
        return self.__call_volume

    @call_volume.setter
    def call_volume(self, pcall_volume):
        self.__call_volume = pcall_volume

    @property
    def handoff_cost(self):
        return self.__handoff_cost

    @handoff_cost.setter
    def handoff_cost(self, handoff_cost_list):
        self.__handoff_cost = handoff_cost_list

    def get_handoff_cost(self, antenna_id):
        return self.__handoff_cost[antenna_id]

    @property
    def ant_switch_cost(self):
        return self.__ant_switch_cost

    @ant_switch_cost.setter
    def ant_switch_cost(self, ant_switch_cost_list):
        self.__ant_switch_cost = ant_switch_cost_list

    def get_ant_switch_cost(self, switch_id):
        return self.__ant_switch_cost[switch_id]

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, pscore):
        self.__score = pscore

    @property
    def switch_id(self):
        return self.__switch_id

    @switch_id.setter
    def switch_id(self, pswitch):
        self.__switch_id = pswitch

    def __lt__(self, other):
        return self.__score < other.__score

    def __gt__(self, other):
        return self.__score > other.__score
