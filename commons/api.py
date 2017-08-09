from os import abort
from xml.etree import ElementTree

import certifi
import urllib3

from config.const import TOPIS_AUTH_TOKEN


class Api:
    def __init__(self):
        self._http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    def get_stations(self, route_id):
        def get_text(item, tag):
            return item.find(tag).text

        def get_int(item, tag):
            try:
                return int(get_text(item, tag))
            except ValueError:
                return -1

        url = f"http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?" \
              f"serviceKey={TOPIS_AUTH_TOKEN}&busRouteId={route_id}"
        req = self._http.request('GET', url)

        root = ElementTree.fromstring(req.data)

        return list(map(lambda item: {
            'sequence': get_int(item, 'seq'),
            'station_id': get_int(item, 'station'),
            'station_num': get_int(item, 'stationNo'),
            'station_name': get_text(item, 'stationNm'),
            'direction': get_text(item, 'direction'),
            'is_turn_station': (get_text(item, 'transYn') == 'Y'),
        }, root.iter('itemList')))

    def get_arrivals(self, route_id, station_id, sequence):
        def get_text(tag):
            return root.find(tag).text

        url = f"http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRoute?" \
              f"serviceKey={TOPIS_AUTH_TOKEN}&stId={station_id}&busRouteId={route_id}&ord={sequence}"
        req = self._http.request('GET', url)

        try:
            root = list(ElementTree.fromstring(req.data).iter('itemList'))[0]
        except IndexError:
            abort(400)

        return [
            {
                'bus_number': get_text('plainNo1'),
                'before': sequence - int(get_text('sectOrd1')),
                'station_name': get_text('stationNm1'),
                'waiting_time': int(get_text('exps1')),
                'people_count': int(get_text('reride_Num1')),
                'is_full': True if get_text('full1') == '1' else False,
                'is_last': True if get_text('isLast1') == '1' else False
            },
            {
                'bus_number': get_text('plainNo2'),
                'before': sequence - int(get_text('sectOrd2')),
                'station_name': get_text('stationNm2'),
                'waiting_time': int(get_text('exps2')),
                'people_count': int(get_text('reride_Num2')),
                'is_full': True if get_text('full2') == '1' else False,
                'is_last': True if get_text('isLast2') == '1' else False
            }
        ]
