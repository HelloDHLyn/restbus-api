import Vapor
import HTTP

final class BusStation {
    /// 순번 (1, 2, 3, ...)
    var sequence: Int

    /// 정류장 ID
    var stationId: Int

    /// 정류장 이름
    var stationName: String

    /// 정류장 방향
    var direction: String

    /// 회차지 여부
    var isTurnStation: Bool

    init(sequence: Int, stationId: Int, stationName: String, direction: String, isTurnStation: Bool) {
        self.sequence = sequence
        self.stationId = stationId
        self.stationName = stationName
        self.direction = direction
        self.isTurnStation = isTurnStation
    }
}

extension BusStation: JSONConvertible {
    convenience init(json: JSON) throws {
        try self.init(
            sequence: json.get("sequence"),
            stationId: json.get("stationId"),
            stationName: json.get("stationName"),
            direction: json.get("dircetion"),
            isTurnStation: json.get("isTurnStation")
        )
    }

    func makeJSON() throws -> JSON {
        var json = JSON()
        try json.set("sequence", sequence)
        try json.set("stationId", stationId)
        try json.set("stationName", stationName)
        try json.set("direction", direction)
        try json.set("isTurnStation", isTurnStation)
        return json
    }
}

extension BusStation: ResponseRepresentable { }
