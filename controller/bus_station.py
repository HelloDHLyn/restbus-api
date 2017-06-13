from xml.etree import ElementTree

from config.const import TOPIS_AUTH_TOKEN
from helper.http import HttpHelper


class BusStationController(object):
    @classmethod
    def get(cls, route_id):
        def get_text(item, tag):
            return item.find(tag).text

        def get_int(item, tag):
            try:
                return int(get_text(item, tag))
            except ValueError:
                return -1

        http = HttpHelper().pool()

        url = f"http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?" \
              f"serviceKey={TOPIS_AUTH_TOKEN}&busRouteId={route_id}"
        req = http.request('GET', url)

        root = ElementTree.fromstring(req.data)

        return list(map(lambda item: {
            'sequence': get_int(item, 'seq'),
            'station_id': get_int(item, 'station'),
            'station_num': get_int(item, 'stationNo'),
            'station_name': get_text(item, 'stationNm'),
            'direction': get_text(item, 'direction'),
            'is_turn_station': (get_text(item, 'transYn') == 'Y'),
        }, root.iter('itemList')))
