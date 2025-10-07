import json
from copy import deepcopy

from Hardware.Antenna import Antenna
from Hardware.Switch import Switch


class Base:
    _cls_antenna_list = None
    _cls_switch_list = None

    def __init__(self):
        self._antenna_list = deepcopy(self._cls_antenna_list)
        self._switch_list = deepcopy(self._cls_switch_list)

    @classmethod
    def read(cls, filename):
        with open(filename, "r") as data:
            data = json.load(data)

            nb_antennas = data['NbAntennas']
            nb_switches = data['NbSwitches']

        ant_switch_cost = data['AntSwitchCost']
        handoff_cost = data['HandoffCost']
        call_volume = data['CallVolume']
        call_capacity = data['CallCapacity']

        switch_ant_cost = [[ant_switch_cost[i][j] for i in range(len(ant_switch_cost))] for j in
                           range(len(ant_switch_cost[0]))]

        cls._cls_antenna_list = [Antenna(pid=i, call_volume=call_volume[i],
                                         ant_switch_cost=ant_switch_cost,
                                         handoff_cost=handoff_cost[i]) for i in
                                 range(nb_antennas)]

        cls._cls_switch_list = [Switch(pid=i, call_capacity=call_capacity[i], antenna_cost=switch_ant_cost[i]) for i in
                                range(nb_switches)]

    def start(self, *args, **kwargs):
        return self._start(*args, **kwargs)

    def _start(self, *args, **kwargs):
        raise NotImplementedError()
