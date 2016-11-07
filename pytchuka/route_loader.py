import json
from marshmallow import Schema, fields


class GenericResource:
    def __init__(self, body, status):
        self.body = body
        self.status = status

    def on_post(self, req, resp):
        resp.body = self.body
        resp.status = self.status

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.body = self.body
        resp.status = self.status


class RouteSchema(Schema):
    url = fields.Str(required=True)
    status = fields.Int(required=True)
    body = fields.Str(required=True)


class RouteLoader:

    def __init__(self, api):
        self.routes = []
        # self.api = api

    def load_from_file(self, json_file):
        with open(json_file, 'r') as file:
            json_info = json.load(file)
            self.load(json_info)

    def load(self, json_input):
        schema = RouteSchema(many=True)
        json_loaded = json.loads(json_input)
        self.routes = schema.load(json_loaded)
        # for route in routes.data:
        #     self.api.add_route(route['url'], GenericResource(route['body'], route['status']))

