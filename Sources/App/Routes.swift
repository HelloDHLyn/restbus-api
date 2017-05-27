import Vapor

final class Routes: RouteCollection {
    let drop: Droplet
    init (droplet: Droplet) {
        drop = droplet
    }

    func build(_ builder: RouteBuilder) throws {
        builder.group("v1") { v1 in
            v1.get("hello") { req in
                return "Hello, world!"
            }

            // GET /v1/routes
            v1.group("routes") { routes in
                let controller = BusRouteController()
                routes.get("") { req in
                    return try controller.search(req)
                }
            }

            // GET /v1/stations
            v1.group("stations") { stations in
                let controller = BusStationController(droplet: drop)
                stations.get("") { req in
                    return try controller.get(req)
                }
            }
        }
    }
}
