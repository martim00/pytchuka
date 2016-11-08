import argparse
import json
from wsgiref.simple_server import make_server

import falcon
from pytchuka.route_loader import RouteLoader


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
    if spec:
        route_loader.load_from_file(spec)
    app = falcon.API(middleware=[BlackHoleMiddleware(route_loader)])

    httpd = make_server('', port, app)

    if not spec:
        print("Spec file not found. Accepting all routes (blackhole mode on).")
    else:
        print("Spec file: {}".format(spec))
    print("Running pytchuka on {}".format(port))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()


def main():
    parser = argparse.ArgumentParser(description='Very very simple python mock server')
    parser.add_argument('port', type=int, help='The port to run.')
    parser.add_argument('--spec', type=str, help='The json file with the spec of paths to mock. '
                                                 'If not passed will accept any path')

    args = parser.parse_args()
    run_server(args.port, args.spec)

if __name__ == '__main__':
    main()
