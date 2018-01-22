import unittest
from unittest.mock import MagicMock

import os
from pytchuka.route_loader import RouteLoader


class RouteLoaderTest(unittest.TestCase):

    def load_routes(self, routes):
        self.loader = RouteLoader()
        self.loader.load_routes(routes)

    def load_routes_from_file(self, json_file, live_reload=False):
        self.loader = RouteLoader(live_reload=live_reload)
        self.loader.load_from_file(json_file)

    def test_load_route(self):
        route = [
            {
                'request': {
                    'url': '/test',
                    'method': 'GET',
                },
                'response': {
                    'status': 200,
                    'body': {
                        'hello': 'world'
                    }
                }
            }
        ]
        self.load_routes(route)
        self.assertEqual(1, len(self.loader.routes))
        self.assert_route(self.loader.match_response('/test', 'GET', {}, '', {}), 200, {'hello': 'world'})

    def assert_route(self, response, expected_status, expected_body):
        self.assertIsNotNone(response)
        self.assertEqual(expected_status, response['status'])
        self.assertEqual(expected_body, response['body'])

    def test_load_many_routes(self):
        route = [
            {
                'request': {
                    'url': '/test2',
                    'method': 'GET',
                },
                'response': {
                    'status': 202,
                    'body': {
                        'hello2': 'world'
                    }
                }
            },
            {
                'request': {
                    'url': '/test3/sub-path',
                    'method': 'GET',
                },
                'response': {
                    'status': 203,
                    'body': {
                        'hello3': 'world'
                    }
                }
            }
        ]
        self.load_routes(route)
        self.assertEqual(2, len(self.loader.routes))
        self.assert_route(self.loader.match_response('/test2', 'GET', {}, '', {}), 202, {'hello2': 'world'})
        self.assert_route(self.loader.match_response('/test3/sub-path', 'GET', {}, '', {}),
                          203, {'hello3': 'world'})

    def test_load_from_json(self):
        filename = os.path.join(os.path.dirname(__file__), 'test.json')
        self.load_routes_from_file(filename)
        self.assertEqual(5, len(self.loader.routes))
        self.assert_route(self.loader.match_response('/test2', 'GET', {}, '', {}), 202, {'hello': 'world'})
        self.assert_route(self.loader.match_response('/test3/sub-path', 'POST', {}, '', {}),
                          203, {'hello': 'world3'})
        self.assert_route(self.loader.match_response('/test3/sub-path', 'POST', {}, 'id=1234&file=C:%5CTmp%5Cblue.txt', {}),
                          200, {'hello': 'Test Quey Param'})

        file_upload = dict(key='key name', filename='my personal file_tabajara')
        self.assert_route(self.loader.match_response('/test3/sub-path', 'POST', {}, '', file_upload),
                          201, {'hello': 'Test File Upload'})
        self.assert_route(self.loader.match_response('/test3/sub-path', 'POST', {"name": "Baltazar"}, '', {}),
                          201, {'hello': 'Hello Baltazar!!'})

    def test_router_return_default_value_if_none_is_matched(self):
        self.load_routes({})
        self.assert_route(self.loader.match_response('/skjandkasn', 'GET', {}, '', {}), 200, {})

    def test_should_be_able_to_pass_regex_as_urls(self):
        route = [
            {
                'request': {
                    'url': '/test/*',
                    'method': 'GET',
                },
                'response': {
                    'status': 200,
                    'body': {
                        'hello': 'world'
                    }
                }
            }
        ]
        self.load_routes(route)
        self.assert_route(self.loader.match_response('/test/', 'GET', {}, '', {}), 200, {'hello': 'world'})
        self.assert_route(self.loader.match_response('/test/saa', 'GET', {}, '', {}), 200, {'hello': 'world'})
        self.assert_route(self.loader.match_response('/test', 'GET', {}, '', {}), 200, {'hello': 'world'})
        self.assert_route(self.loader.match_response('/test/3211/321', 'GET', {}, '', {}), 200, {'hello': 'world'})

    def test_should_be_able_to_define_routes_with_http_methods(self):
        route = [
            {
                'request': {
                    'url': '/test/*',
                    'method': 'GET',
                },
                'response': {
                    'status': 200,
                    'body': {
                        'method': 'get'
                    }
                }
            },
            {
                'request': {
                    'url': '/test/*',
                    'method': 'POST',
                },
                'response': {
                    'status': 201,
                    'body': {
                        'method': 'post'
                    }
                }
            }
        ]
        self.load_routes(route)
        self.assert_route(self.loader.match_response('/test/', 'GET', {}, '', {}), 200, {'method': 'get'})
        self.assert_route(self.loader.match_response('/test/', 'POST', {}, '', {}), 201, {'method': 'post'})

    def test_on_live_reload_mode_the_routes_are_dinamically_loaded(self):
        filename = os.path.join(os.path.dirname(__file__), 'test.json')
        self.load_routes_from_file(filename, True)
        self.loader.reload = MagicMock()
        self.loader.match_response('/test', 'GET', {}, '', {})

        self.assertEqual(1, self.loader.reload.call_count)

    def test_query_string_and_file_upload_must_to_be_not_none(self):
        filename = os.path.join(os.path.dirname(__file__), 'test.json')
        self.load_routes_from_file(filename)
        self.assert_route(self.loader.match_response('/test3/sub-path', 'POST', {}, 'id=1234&file=C:%5CTmp%5Cblue.txt', None),
                          200, {})

        file_upload = dict(key='key name', filename='my personal file_tabajara')
        self.assert_route(self.loader.match_response('/test3/sub-path', 'POST', {}, None, file_upload),
                          200, {})