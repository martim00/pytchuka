import json
import unittest
from unittest.mock import MagicMock, call, ANY

from pytchuka.route_loader import RouteLoader


class RouteLoaderTest(unittest.TestCase):

    def setUp(self):
        self.mock_api = MagicMock()
        self.loader = RouteLoader(self.mock_api)

    def load_routes(self, routes):
        json_input = json.dumps(routes)
        self.loader.load(json_input)

    def load_routes_from_file(self, json_file):
        self.loader.load_from_file(json_file)

    def test_load_route(self):
        route = [
            {
                'url': '/test',
                'status': 200,
                'body': 'hello'
            }
        ]
        self.load_routes(route)
        self.mock_api.add_route.assert_called_once_with('/test', ANY)

    def test_configure_response(self):
        route = [
            {
                'url': '/test',
                'status': 200,
                'body': 'hello'
            }
        ]
        self.load_routes(route)
        self.assertEqual(1, self.mock_api.add_route.call_count)

        actual_path = self.mock_api.add_route.call_args_list[0][0][0]
        actual_resource = self.mock_api.add_route.call_args_list[0][0][1]

        self.assertEqual('/test', actual_path)
        self.assertEqual('hello', actual_resource.body)
        self.assertEqual(200, actual_resource.status)

    def test_load_many_routes(self):
        route = [
            {
                'url': '/test2',
                'status': 202,
                'body': 'hello2'
            },
            {
                'url': '/test3/sub-path',
                'status': 203,
                'body': 'hello3'
            }
        ]
        self.load_routes(route)
        self.assertEqual([call('/test2', ANY), call('/test3/sub-path', ANY)], self.mock_api.add_route.call_args_list)

    def test_load_from_json(self):
        self.load_routes_from_file('test.json')
