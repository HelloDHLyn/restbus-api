from controller.bus_station import BusStationController


class ControllerHelper(object):
    _station_controller = BusStationController()

    @classmethod
    def station_controller(cls):
        return cls._station_controller
