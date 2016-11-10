import argparse
import json
from wsgiref.simple_server import make_server

import falcon
from pytchuka.route_loader import RouteLoader


class BlackHoleMiddleware(object):

    def __init__(self, loader):
        self.route_loader = loader

    def process_response(self, req, resp, resource, req_succeeded):
        route = self.route_loader.match_route(req.path, req.method)
        assert route is not None
        resp.body = json.dumps(route['body'])
        resp.status = falcon.get_http_status(route['status'])


def create_app(loader):
    return falcon.API(middleware=[BlackHoleMiddleware(loader)])


def create_app_from_file(spec, live_reload):
    route_loader = RouteLoader(spec, live_reload)
    return create_app(route_loader)


def run_server(port, spec, live_reload):
    live_reload = live_reload if live_reload else True
    app = create_app_from_file(spec, live_reload)
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
    parser = argparse.ArgumentParser(description='Very simple python mock server')
    parser.add_argument('port', type=int, help='The port to run.')
    parser.add_argument('--spec', type=str, help='The json file with the spec of paths to mock. '
                                                 'If not passed will accept any path.')
    parser.add_argument('--live', type=bool, help='Live reload mode. By default is enabled')

    args = parser.parse_args()
    run_server(args.port, args.spec, args.live)

if __name__ == '__main__':
    main()
