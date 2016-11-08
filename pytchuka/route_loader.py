import json

from marshmallow import Schema
from marshmallow import fields


class RouteSchema(Schema):
    url = fields.Str(required=True)
    status = fields.Int(required=True)
    body = fields.Dict(required=True)


class RouteLoader:
    def __init__(self):
        self.routes = {}

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            json_info = json.load(file)
            self.load_routes(json_info)

    def load_routes(self, routes):
        routes_list = RouteSchema(many=True).load(routes)
        for route in routes_list.data:
            self.routes[route['url']] = route

    def get_route(self, url):
        return self.routes.get(url, None)

