from flask import Flask, request, jsonify

from helper.controller import ControllerHelper
from helper.database import DatabaseHelper
from model.bus_route import BusRoute

app = Flask(__name__)
session = DatabaseHelper().session()


@app.route('/v1/hello')
def hello():
    return "Hello, world!"


@app.route('/v1/routes', methods=['GET'])
def bus_route():
    query_string = request.args.get('query')
    routes = session.query(BusRoute).filter(BusRoute.route_name.like(f"%{query_string}%")).all()

    return jsonify(list(map(lambda i: i.as_dict(), routes)))


@app.route('/v1/stations', methods=['GET'])
def bus_routes():
    controller = ControllerHelper().station_controller()

    route_id = request.args.get('route_id')
    return jsonify(controller.get(route_id))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
