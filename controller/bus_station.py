from xml.etree import ElementTree

from config.const import TOPIS_AUTH_TOKEN
from helper.http import HttpHelper


class BusStationController(object):
    @classmethod
    def get(cls, route_id):
        http = HttpHelper().pool()

        url = f"http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?" \
              f"serviceKey={TOPIS_AUTH_TOKEN}&busRouteId={route_id}"
        req = http.request('GET', url)

        root = ElementTree.fromstring(req.data)

        return list(map(lambda item: {
            'sequence': int(item.find('seq').text),
            'station_id': int(item.find('stationNo').text),
            'station_name': item.find('stationNm').text,
            'direction': item.find('direction').text,
            'is_turn_station': (item.find('transYn').text == 'Y'),
        }, root.iter('itemList')))
