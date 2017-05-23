import Vapor
import HTTP

final class BusRouteController {
    func search(_ req: Request) throws -> ResponseRepresentable {
        let query = req.query?["query"]
        let routes = try BusRoute
            .makeQuery()
            .filter("route_name", .contains, query)
            .all()

        return try routes.makeJSON()
    }
}
