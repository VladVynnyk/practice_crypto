import unittest
from unittest.mock import patch, Mock


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_add_user_request(self):
        # requests = Mock()
        # requests.Response()
        # requests.Response.assert_called()
        # print(requests.Response({"some": "here"}))
        # requests.Response.assert_called_with({"some": "here"})

        TestClient = Mock()
        client = TestClient
        response = client.get("/")
        print(response)
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

if __name__ == '__main__':
    unittest.main()