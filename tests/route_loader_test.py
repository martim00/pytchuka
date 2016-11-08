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
                'body': {
                    'hello': 'world'
                }
            }
        ]
        self.load_routes(route)
        self.assertEqual(1, len(self.loader.routes))
        self.assert_route(self.loader.get_route('/test'), '/test', 200, {'hello': 'world'})

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
                'body': {
                    'hello2': 'world'
                }
            },
            {
                'url': '/test3/sub-path',
                'status': 203,
                'body': {
                    'hello3': 'world'
                }
            }
        ]
        self.load_routes(route)
        self.assertEqual(2, len(self.loader.routes))
        self.assert_route(self.loader.get_route('/test2'), '/test2', 202, {'hello2': 'world'})
        self.assert_route(self.loader.get_route('/test3/sub-path'), '/test3/sub-path', 203, {'hello3': 'world'})

    def test_load_from_json(self):
        self.load_routes_from_file('test.json')
        self.assertEqual(2, len(self.loader.routes))
        self.assert_route(self.loader.get_route('/test2'), '/test2', 202, {'hello': 'world'})
        self.assert_route(self.loader.get_route('/test3/sub-path'), '/test3/sub-path', 203, {'hello': 'world3'})
