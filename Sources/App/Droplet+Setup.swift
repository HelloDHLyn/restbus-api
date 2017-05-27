@_exported import Vapor

extension Droplet {
    public func setup() throws {
        let route = Routes(droplet: self)
        try collection(route)
    }
}
