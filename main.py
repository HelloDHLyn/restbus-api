from flask import Flask, request, jsonify

from helper.controller import ControllerHelper
from helper.database import DatabaseHelper
from helper.json import CustomJSONEncoder
from model.bus_route import BusRoute

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

session = DatabaseHelper().session()


@app.route('/v1/hello')
def hello():
    return "Hello, world!"


@app.route('/v1/routes', methods=['GET'])
def bus_routes():
    query_string = request.args.get('query')

    routes = session.query(BusRoute).filter(BusRoute.route_name.like(f"%{query_string}%")).all()
    session.close()

    return jsonify(list(map(lambda i: i.as_dict(), routes)))


@app.route('/v1/stations', methods=['GET'])
def bus_stations():
    route_id = request.args.get('route_id')

    controller = ControllerHelper().station_controller()
    return jsonify(controller.get(route_id))


@app.route('/v1/arrivals', methods=['GET'])
def arrivals():
    route_id = request.args.get('route_id')
    station_id = request.args.get('station_id')
    order = int(request.args.get('order'))

    controller = ControllerHelper().arrival_controller()
    return jsonify(controller.get(route_id, station_id, order))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
