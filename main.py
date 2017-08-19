from flask import Flask, request

from commons.api import Api
from commons.database import DatabaseHelper
from commons.decorators import json_response, transactional
from commons.json import CustomJSONEncoder
from model.bus_route import BusRoute

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

api = Api()

session = DatabaseHelper().session()


@app.route('/v1/hello')
def hello():
    return "Hello, world!"


@app.route('/v1/bus/routes', methods=['GET'])
@json_response
@transactional(session)
def bus_routes():
    query_string = request.args.get('query')
    routes = session.query(BusRoute).filter(BusRoute.route_name.like(f"%{query_string}%")).all()

    return list(map(lambda i: i.as_dict(), routes))


@app.route('/v1/bus/stations', methods=['GET'])
@json_response
def bus_stations():
    route_id = request.args.get('route_id')

    return api.get_stations(route_id)


@app.route('/v1/bus/arrivals', methods=['GET'])
@json_response
def arrivals():
    route_id = request.args.get('route_id')
    station_id = request.args.get('station_id')
    sequence = int(request.args.get('sequence'))

    return api.get_arrivals(route_id, station_id, sequence)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
