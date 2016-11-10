import json
import re

from marshmallow import Schema
from marshmallow import fields


class RouteSchema(Schema):
    url = fields.Str(required=True)
    method = fields.Str(required=True)
    status = fields.Int(required=True)
    body = fields.Dict(required=True)


class RouteLoader:
    def __init__(self):
        self.routes = {}

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.load_routes(json.load(file))

    def load_routes(self, routes):
        self.routes = RouteSchema(many=True).load(routes).data

    def match_route(self, url, method):
        for route in self.routes:
            if re.match(route['url'], url) and route['method'] == method:
                return route

        # default route
        return {'url': url, 'status': 200, 'method': method, 'body': {}}

