# coding=utf-8
import unittest
import api
import json


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()

    def test_hello_world(self):
        rv = self.app.get('/')
        assert u"Hej, världen!" in rv.data.decode('utf8')

    def test_default_todos(self):
        rv = self.app.get('/api/todos/')
        with open('fixtures.json') as todos_file:
            expected_todos = json.load(todos_file)
        api_todos = json.loads(rv.data.decode('utf8'))['todos']
        assert expected_todos == api_todos

    def test_get_todo(self):
        rv = self.app.get('/api/todos/1')
        with open('fixtures.json') as todos_file:
            expected_todo = json.load(todos_file)[0]
        api_todo = json.loads(rv.data.decode('utf8'))
        assert expected_todo == api_todo

    # TODO: Stop depending on test case execution order
    def test_new_todo(self):
        data = {'title': 'Test'}
        rv = self.app.post('/api/todos/',
                           data=json.dumps(data),
                           content_type='application/json')
        api_todo = json.loads(rv.data.decode('utf8'))
        assert 'Test' == api_todo['title']
        assert 4 == api_todo['id']

    def test_put_todo(self):
        data = {'title': 'Test2'}
        rv = self.app.put('/api/todos/3',
                          data=json.dumps(data),
                          content_type='application/json')
        api_todo = json.loads(rv.data.decode('utf8'))
        assert 'Test2' == api_todo['title']

    def test_put_todo_index(self):
        # Check the current order of ids
        rv = self.app.get('/api/todos/')
        api_todos = json.loads(rv.data.decode('utf8'))['todos']
        api_ids = [t['id'] for t in api_todos]
        expected_ids = [1,3,2,4]
        assert api_ids == expected_ids

        # Move from current index to index 1
        data = {'$index': 1}
        rv = self.app.put('/api/todos/4',
                          data=json.dumps(data),
                          content_type='application/json')
        api_todo = json.loads(rv.data.decode('utf8'))
        # We got the right todo back
        assert 4 == api_todo['id']
        assert 200 == rv.status_code

        # Check the new order of ids
        rv = self.app.get('/api/todos/')
        api_todos = json.loads(rv.data.decode('utf8'))['todos']
        api_ids = [t['id'] for t in api_todos]
        expected_ids = [1,4,3,2]
        assert api_ids == expected_ids

    def test_put_todo_index_invalid(self):
        # Move from current index to index -1
        data = {'$index': -1}
        rv = self.app.put('/api/todos/4',
                          data=json.dumps(data),
                          content_type='application/json')
        # We got the right status code
        assert 400 == rv.status_code

        # Move from current index to index larger than list
        data = {'$index': 4}
        rv = self.app.put('/api/todos/4',
                          data=json.dumps(data),
                          content_type='application/json')
        # We got the right status code
        assert 400 == rv.status_code

    def test_remove_todo(self):
        rv = self.app.delete('/api/todos/3')
        assert u'OK' == rv.data.decode('utf8')

    def test_remove_todos_and_add(self):
        # Remove remaining
        rv = self.app.delete('/api/todos/1')
        assert u'OK' == rv.data.decode('utf8')
        rv = self.app.delete('/api/todos/2')
        assert u'OK' == rv.data.decode('utf8')
        rv = self.app.delete('/api/todos/4')
        assert u'OK' == rv.data.decode('utf8')

        # Create new one
        # Id should reset to 1
        data = {'title': 'Test'}
        rv = self.app.post('/api/todos/',
                           data=json.dumps(data),
                           content_type='application/json')
        api_todo = json.loads(rv.data.decode('utf8'))
        assert 'Test' == api_todo['title']
        assert 1 == api_todo['id']



if __name__ == '__main__':
    unittest.main()
