class Switch:
    def __init__(self, pid=None, call_capacity=None, antenna_cost=None):
        self.__id = pid
        self.__call_capacity = call_capacity
        self.__antenna_cost = antenna_cost

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, pid):
        self.__id = pid

    @property
    def call_capacity(self):
        return self.__call_capacity

    @call_capacity.setter
    def call_capacity(self, pcall_capacity):
        self.__call_capacity = pcall_capacity

    @property
    def antenna_cost(self):
        return self.__antenna_cost

    @antenna_cost.setter
    def antenna_cost(self, pantenna_cost):
        self.__antenna_cost = pantenna_cost

    def get_antenna_cost(self, antenna_id):
        return self.__antenna_cost[antenna_id]
