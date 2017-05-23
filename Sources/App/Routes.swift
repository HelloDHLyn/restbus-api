import Vapor

final class Routes: RouteCollection {
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
        }
    }
}

/// Since Routes doesn't depend on anything
/// to be initialized, we can conform it to EmptyInitializable
///
/// This will allow it to be passed by type.
extension Routes: EmptyInitializable { }
