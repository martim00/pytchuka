
from falcon import testing
from pytchuka.pytchuka import create_app
from pytchuka.route_loader import RouteLoader


class ServerTest(testing.TestCase):

    def setUp(self):
        super(ServerTest, self).setUp()
        self.loader = RouteLoader()
        self.app = create_app(self.loader)

    def test_get_correct_body(self):
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
        self.loader.load_routes(route)
        result = self.simulate_get('/test')
        self.assertEqual({'hello': 'world'}, result.json)
        self.assertEqual(200, result.status_code)

    def test_return_empty_json_when_route_does_not_exist(self):
        self.loader.load_routes([])
        result = self.simulate_get('/iwqwkjwq')
        self.assertEqual({}, result.json)

    def test_define_route_regex(self):
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
        self.loader.load_routes(route)
        result = self.simulate_get('/test/dsakjnsa/snakn')
        self.assertEqual({'hello': 'world'}, result.json)
