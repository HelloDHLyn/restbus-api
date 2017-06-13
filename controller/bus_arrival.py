from xml.etree import ElementTree

from flask import abort

from config.const import TOPIS_AUTH_TOKEN
from helper.http import HttpHelper


class BusArrivalController(object):
    @classmethod
    def get(cls, route_id, station_id, order):
        def get_text(tag):
            return root.find(tag).text

        http = HttpHelper().pool()

        url = f"http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRoute?" \
              f"serviceKey={TOPIS_AUTH_TOKEN}&stId={station_id}&busRouteId={route_id}&ord={order}"
        req = http.request('GET', url)

        try:
            root = list(ElementTree.fromstring(req.data).iter('itemList'))[0]
        except IndexError:
            abort(400)

        return [
            {
                'bus_number': get_text('plainNo1'),
                'before': order - int(get_text('sectOrd1')),
                'station_name': get_text('stationNm1'),
                'waiting_time': int(get_text('exps1')),
                'people_count': int(get_text('reride_Num1')),
                'is_full': True if get_text('full1') == '1' else False,
                'is_last': True if get_text('isLast1') == '1' else False
            },
            {
                'bus_number': get_text('plainNo2'),
                'before': order - int(get_text('sectOrd2')),
                'station_name': get_text('stationNm2'),
                'waiting_time': int(get_text('exps2')),
                'people_count': int(get_text('reride_Num2')),
                'is_full': True if get_text('full2') == '1' else False,
                'is_last': True if get_text('isLast2') == '1' else False
            }
        ]
