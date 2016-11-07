import argparse
import json
from wsgiref.simple_server import make_server

import falcon
from marshmallow import Schema
from marshmallow import fields


class RouteSchema(Schema):
    url = fields.Str(required=True)
    status = fields.Int(required=True)
    body = fields.Dict(required=True)


class RouteLoader:
    def __init__(self):
        self.routes = {}

    def load(self, filename):
        with open(filename, 'r') as file:
            json_info = json.load(file)
            routes_list = RouteSchema(many=True).load(json_info)
            for route in routes_list.data:
                self.routes[route['url']] = route

    def get_route(self, url):
        return self.routes.get(url, None)


class BlackHoleMiddleware(object):

    def __init__(self, loader):
        self.route_loader = loader

    def process_response(self, req, resp, resource, req_succeeded):
        route = self.route_loader.get_route(req.path)
        req_succeeded = True
        if route:
            resp.body = json.dumps(route['body'])
            resp.status = falcon.get_http_status(route['status'])
        else:
            resp.body = ''
            resp.status = falcon.get_http_status(200)


def run_server(port, spec):
    route_loader = RouteLoader()
    route_loader.load(spec)
    app = falcon.API(middleware=[BlackHoleMiddleware(route_loader)])

    httpd = make_server('', port, app)
    httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description='Very very simple python mock server')
    parser.add_argument('port', type=int, help='The port to run')
    parser.add_argument('spec', type=str, help='The json file with the spec of paths to mock')

    args = parser.parse_args()
    print(args.port)
    print(args.spec)

    run_server(args.port, args.spec)

if __name__ == '__main__':
    main()
