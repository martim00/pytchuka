import argparse
import json
from wsgiref import simple_server

import falcon
from deepdiff import DeepDiff
from falcon_multipart.middleware import MultipartMiddleware
from falcon_multipart.parser import Parser

import re

from marshmallow import Schema, ValidationError
from marshmallow import fields


class RequestSchema(Schema):
    url = fields.Str(required=True)
    method = fields.Str(required=True)
    body = fields.Dict(required=False)
    query_string = fields.Str(required=False)
    file_upload = fields.Dict(required=False)


class ResponseSchema(Schema):
    status = fields.Int(required=True)
    body = fields.Dict(required=False, allow_none=True)


class RouteSchema(Schema):
    request = fields.Nested(RequestSchema(), required=True)
    response = fields.Nested(ResponseSchema(), required=True)


class RouteLoader:
    def __init__(self, spec="", live_reload=False):
        self.routes = {}
        self.live_reload = live_reload
        self.spec = spec
        self.reload()

    def load_from_file(self, filename):
        assert filename

        with open(filename, 'r') as file:
            self.load_routes(json.load(file))

    def load_routes(self, routes):
        try:
            self.routes = RouteSchema(many=True).load(routes)
            self.routes = [route for route in self.routes if route]
        except ValidationError as e:
            print('Unexpected errors loading routes. \nFields: {0}\nMessages: {1}'.format(e.fields, e.messages))

    def reload(self):
        if self.spec:
            self.load_from_file(self.spec)

    def match_response(self, url, method, body, query_string, file_upload):
        # we are reloading to improve usability (we know the performance degradation here)
        if self.live_reload:
            self.reload()

        for route in self.routes:
            request = route['request']
            if re.match(request['url'], url) and \
                    request['method'] == method and \
                    request.get('query_string', '') == query_string and \
                    self.is_body_equals(request.get('body', {}), body) and \
                    request.get('file_upload', {}) == file_upload:
                return route['response']

        # default route
        return {'status': 200, 'body': {}}

    @staticmethod
    def is_body_equals(r_body, body):
        if not r_body:
            return True
        diff = DeepDiff(r_body, body, verbose_level=1, ignore_order=True)
        if not diff:
            return True
        if diff.get('dictionary_item_added', []):
            return False
        if diff.get('dictionary_item_removed', []):
            return False
        for _, v in diff.get('values_changed', {}).items():
            if v.get('old_value', '') != '*':
                return False
        return True


class BlackHoleMiddleware(object):

    def __init__(self, loader):
        self.route_loader = loader

    def process_response(self, req, resp, resource, req_succeeded):
        file_upload = {}
        for key, value in req.params.items():
            if type(value) is Parser:
                file_upload = dict(key=key, filename=value.filename)
                break

        req_body = req.media if req.content_length and req.content_type == 'application/json' else {}
        response = self.route_loader.match_response(req.path, req.method, req_body,
                                                    req.query_string, file_upload)
        assert response is not None
        resp.body = json.dumps(response.get('body', ''))
        resp.status = falcon.get_http_status(response['status'])


def create_app(loader):
    return falcon.API(middleware=[MultipartMiddleware(), BlackHoleMiddleware(loader)])


def create_app_from_file(spec, live_reload):
    route_loader = RouteLoader(spec, live_reload)
    return create_app(route_loader)


def run_server(port, spec, live_reload):
    live_reload = live_reload if live_reload else True
    app = create_app_from_file(spec, live_reload)
    httpd = simple_server.make_server('', port, app)

    if not spec:
        print('Spec file not found. Accepting all routes (blackhole mode on).')
    else:
        print('Spec file: {}'.format(spec))

    address, port = httpd.server_address
    print(f'Pytchuka is running\nServer address: http://{address}:{port}\n')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


def main():
    parser = argparse.ArgumentParser(description='Very simple python mock server')
    parser.add_argument('port', type=int, help='The port to run.')
    parser.add_argument('--spec', type=str, help='The json file with the spec of paths to mock. '
                                                 'If not passed will accept any path.')
    parser.add_argument('--live', type=bool, help='Live reload mode. By default is enabled')

    args = parser.parse_args()
    run_server(args.port, args.spec, args.live)


if __name__ == '__main__':
    main()
