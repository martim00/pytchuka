import unittest

from pytchuka.route_loader import RouteLoader


class RouteLoaderTest(unittest.TestCase):

    def setUp(self):
        self.loader = RouteLoader()

    def load_routes(self, routes):
        self.loader.load_routes(routes)

    def load_routes_from_file(self, json_file):
        self.loader.load_from_file(json_file)

    def test_load_route(self):
        route = [
            {
                'url': '/test',
                'status': 200,
                'method': 'GET',
                'body': {
                    'hello': 'world'
                }
            }
        ]
        self.load_routes(route)
        self.assertEqual(1, len(self.loader.routes))
        self.assert_route(self.loader.match_route('/test', 'GET'), '/test', 200, {'hello': 'world'})

    def assert_route(self, route, expected_url, expected_status, expected_body):
        self.assertIsNotNone(route)
        self.assertEqual(expected_url, route['url'])
        self.assertEqual(expected_status, route['status'])
        self.assertEqual(expected_body, route['body'])

    def test_load_many_routes(self):
        route = [
            {
                'url': '/test2',
                'status': 202,
                'method': 'GET',
                'body': {
                    'hello2': 'world'
                }
            },
            {
                'url': '/test3/sub-path',
                'status': 203,
                'method': 'GET',
                'body': {
                    'hello3': 'world'
                }
            }
        ]
        self.load_routes(route)
        self.assertEqual(2, len(self.loader.routes))
        self.assert_route(self.loader.match_route('/test2', 'GET'), '/test2', 202, {'hello2': 'world'})
        self.assert_route(self.loader.match_route('/test3/sub-path', 'GET'),
                          '/test3/sub-path', 203, {'hello3': 'world'})

    def test_load_from_json(self):
        self.load_routes_from_file('./tests/test.json')
        self.assertEqual(2, len(self.loader.routes))
        self.assert_route(self.loader.match_route('/test2', 'GET'), '/test2', 202, {'hello': 'world'})
        self.assert_route(self.loader.match_route('/test3/sub-path', 'POST'),
                          '/test3/sub-path', 203, {'hello': 'world3'})

    def test_router_return_default_value_if_none_is_matched(self):
        self.assert_route(self.loader.match_route('/skjandkasn', 'GET'), '/skjandkasn', 200, {})

    def test_should_be_able_to_pass_regex_as_urls(self):
        route = [
            {
                'url': '/test/*',
                'status': 200,
                'method': 'GET',
                'body': {
                    'hello': 'world'
                }
            }
        ]
        self.load_routes(route)
        self.assert_route(self.loader.match_route('/test/', 'GET'), '/test/*', 200, {'hello': 'world'})
        self.assert_route(self.loader.match_route('/test/saa', 'GET'), '/test/*', 200, {'hello': 'world'})
        self.assert_route(self.loader.match_route('/test', 'GET'), '/test/*', 200, {'hello': 'world'})
        self.assert_route(self.loader.match_route('/test/3211/321', 'GET'), '/test/*', 200, {'hello': 'world'})

    def test_should_be_able_to_define_routes_with_http_methods(self):
        route = [
            {
                'url': '/test/*',
                'status': 200,
                'method': 'GET',
                'body': {
                    'method': 'get'
                }
            },
            {
                'url': '/test/*',
                'status': 201,
                'method': 'POST',
                'body': {
                    'method': 'post'
                }
            }
        ]
        self.load_routes(route)
        self.assert_route(self.loader.match_route('/test/', 'GET'), '/test/*', 200, {'method': 'get'})
        self.assert_route(self.loader.match_route('/test/', 'POST'), '/test/*', 201, {'method': 'post'})
