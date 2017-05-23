import Vapor
import FluentProvider
import HTTP

final class BusRoute: Model {
    let storage = Storage()

    /// 노선 ID
    var routeId: Int

    /// 노선 이름
    var routeName: String

    /// 유형
    /// (1:공항, 3:간선, 4:지선, 5:순환, 6:광역, 7:인천, 8:경기, 9:폐지, 0:공용)
    var routeType: Int

    /// 기점 이름
    var firstStationName: String

    /// 종점 이름
    var lastStationName: String

    /// 첫차 시간 (yyyyMMddhhmmss)
    var firstBusTime: Date

    /// 막차 시간 (yyyyMMddhhmmss)
    var lastBusTime: Date

    /// 배차간격
    var term: Int

    init(routeId: Int, routeName: String, routeType: Int, firstStationName: String,
         lastStationName: String, firstBusTime: Date, lastBusTime: Date, term: Int) throws{
        self.routeId = routeId
        self.routeName = routeName
        self.routeType = routeType
        self.firstStationName = firstStationName
        self.lastStationName = lastStationName
        self.firstBusTime = firstBusTime
        self.lastBusTime = lastBusTime
        self.term = term
    }

    init(row: Row) throws {
        routeId = try row.get("route_id")
        routeName = try row.get("route_name")
        routeType = try row.get("route_type")
        firstStationName = try row.get("first_station_name")
        lastStationName = try row.get("last_station_name")
        firstBusTime = try row.get("first_bus_time")
        lastBusTime = try row.get("last_bus_time")
        term = try row.get("term")
    }

    func makeRow() throws -> Row {
        var row = Row()
        try row.set("routeId", routeId)
        try row.set("routeName", routeName)
        try row.set("routeType", routeType)
        try row.set("firstStationName", firstStationName)
        try row.set("lastStationName", lastStationName)
        try row.set("firstBusTime", firstBusTime)
        try row.set("lastBusTime", lastBusTime)
        try row.set("term", term)
        return row
    }
}

extension BusRoute: Timestampable { }

extension BusRoute: Preparation {
    static func prepare(_ database: Database) throws {
        try database.create(self) { builder in
            builder.id()
            builder.int("route_id")
            builder.string("route_name")
            builder.int("route_type")
            builder.string("first_station_name")
            builder.string("last_station_name")
            builder.date("first_bus_time")
            builder.date("last_bus_time")
            builder.int("term")
        }
    }

    static func revert(_ database: Database) throws {
        try database.delete(self)
    }
}

extension BusRoute: JSONConvertible {
    convenience init(json: JSON) throws {
        try self.init(
            routeId: json.get("routeId"),
            routeName: json.get("routeName"),
            routeType: json.get("routeType"),
            firstStationName: json.get("firstStationName"),
            lastStationName: json.get("lastStationName"),
            firstBusTime: json.get("firstBusTime"),
            lastBusTime: json.get("lastBusTime"),
            term: json.get("term")
        )
    }

    func makeJSON() throws -> JSON {
        var json = JSON()
        try json.set("routeId", routeId)
        try json.set("routeName", routeName)
        try json.set("routeType", routeType)
        try json.set("firstStationName", firstStationName)
        try json.set("lastStationName", lastStationName)
        try json.set("firstBusTime", firstBusTime)
        try json.set("lastBusTime", lastBusTime)
        try json.set("term", term)
        return json
    }
}

extension BusRoute: ResponseRepresentable { }
