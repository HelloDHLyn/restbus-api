import Vapor
import Console
import Kanna

import Foundation

final class GetRoutesBatchCommand: Command {
    public let id = "batch-get-routes"
    public let console: ConsoleProtocol
    public let client: ClientFactoryProtocol

    public let authToken: String

    public init(_ config: Config, authToken: String) throws {
        self.console = try! config.resolveConsole()
        self.client = try! config.resolveClient()

        self.authToken = authToken
    }

    public func run(arguments: [String]) throws {
        let url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getBusRouteList?serviceKey=\(authToken)"
        let remoteReq = Request(method: .get, uri: url)

        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyyMMddHHmm"
        dateFormatter.timeZone = TimeZone(abbreviation: "Asia/Seoul")

        let res = try client.respond(to: remoteReq)
        if let doc = Kanna.XML(xml: String(bytes: res.body.bytes!), encoding: .utf8) {
            let routes = try doc.xpath("//msgBody//itemList").map { item -> BusRoute in
                func getNodeString(_ node: String) -> String? {
                    return item.xpath(node).first?.text
                }

                func getNodeInt(_ node: String) -> Int {
                    return Int(getNodeString(node)!)!
                }

                func getNodeDate(_ node: String) -> Date {
                    let string = getNodeString(node)!

                    dateFormatter.dateFormat = "yyyyMMddHHmmss"
                    if let date = dateFormatter.date(from: string) {
                        return date
                    } else {
                        dateFormatter.dateFormat = "yyyyMMddHHmm"
                        return dateFormatter.date(from: string)!
                    }
                }

                let routeId = getNodeInt("busRouteId")
                let routeName = getNodeString("busRouteNm")!
                let routeType = getNodeInt("routeType")
                let firstStationName = getNodeString("stStationNm")
                let lastStationName = getNodeString("edStationNm")
                let firstBusTime = getNodeDate("firstBusTm")
                let lastBusTime = getNodeDate("lastBusTm")
                let term = getNodeInt("term")

                if let route = try BusRoute.makeQuery().filter("route_id", .equals, routeId).first() {
                    route.routeName = routeName
                    route.routeType = routeType
                    route.firstStationName = firstStationName
                    route.lastStationName = lastStationName
                    route.firstBusTime = firstBusTime
                    route.lastBusTime = lastBusTime
                    route.term = term
                    return route
                } else {
                    return try BusRoute(
                            routeId: routeId, routeName: routeName, routeType: routeType,
                            firstStationName: firstStationName, lastStationName: lastStationName,
                            firstBusTime: firstBusTime, lastBusTime: lastBusTime, term: term
                    )
                }
            }.forEach { route in
                try route.save()
            }
        } else {
            print("Error!")
        }

    }
}

extension GetRoutesBatchCommand: ConfigInitializable {
    public convenience init(config: Config) throws {
        guard let authToken = config["secrets", "bus_auth_token"]?.string else {
            throw ConfigError.missing(key: ["bus_auth_token"], file: "secrets.json", desiredType: String.Type.self)
        }

        try self.init(config, authToken: authToken)
    }
}