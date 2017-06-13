from controller.bus_arrival import BusArrivalController
from controller.bus_station import BusStationController


class ControllerHelper(object):
    _station_controller = BusStationController()
    _arrival_controller = BusArrivalController()

    @classmethod
    def station_controller(cls):
        return cls._station_controller

    @classmethod
    def arrival_controller(cls):
        return cls._arrival_controller
