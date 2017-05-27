import Vapor
import HTTP
import Kanna

final class BusStationController {
    let drop: Droplet
    init (droplet: Droplet) {
        drop = droplet
    }

    func get(_ req: Request) throws -> ResponseRepresentable {
        // 파라미터 값을 가져온다.
        guard let routeId = req.query?["routeId"]?.string else {
            throw Abort(.badRequest)
        }
        guard let authToken = drop.config["secrets", "bus_auth_token"]?.string else {
            throw Abort(.internalServerError)
        }

        // 버스정보시스템 API로부터 경로를 불러온다.
        // TODO: 하루 단위의 캐싱 적용
        let url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?serviceKey=\(authToken)&busRouteId=\(routeId)"
        let remoteReq = Request(method: .get, uri: url)

        let res = try drop.client.respond(to: remoteReq)

        // 모델을 변환하여 응답을 반환한다.
        // TODO: nil 체크
        if let doc = Kanna.XML(xml: String(bytes: res.body.bytes!), encoding: .utf8) {
            return try doc.xpath("//msgBody//itemList").map { item -> BusStation in
                func getNodeText(_ node: String) -> String { return (item.xpath(node).first?.text)! }

                return BusStation(
                    sequence: Int(getNodeText("seq"))!,
                    stationId: Int(getNodeText("stationNo"))!,
                    stationName: getNodeText("stationNm"),
                    direction: getNodeText("direction"),
                    isTurnStation: (getNodeText("transYn") == "Y")
                )
            }.makeJSON()
        } else {
            return JSON()
        }
    }
}
