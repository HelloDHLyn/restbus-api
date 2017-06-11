from flask import Flask, request, jsonify

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


if __name__ == "__main__":
    app.run()