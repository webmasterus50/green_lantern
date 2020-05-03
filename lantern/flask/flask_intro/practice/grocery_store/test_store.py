import inject

from .store_app import app
from .fake_storage import FakeStorage


def configure_test(binder):
    db = FakeStorage()
    binder.bind('DB', db)


class Initializer:
    def setup(self):
        inject.clear_and_configure(configure_test)

        app.config['TESTING'] = True
        with app.test_client() as client:
            self.client = client


class TestUsers(Initializer):
    def test_create_new(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        assert resp.status_code == 201
        assert resp.json == {'user_id': 1}

        resp = self.client.post(
            '/users',
            json={'name': 'Andrew Derkach'}
        )
        assert resp.json == {'user_id': 2}

    def test_successful_get_user(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        user_id = resp.json['user_id']
        resp = self.client.get(f'/users/{user_id}')
        assert resp.status_code == 200
        assert resp.json == {'name': 'John Doe'}

    def test_get_unexistent_user(self):
        resp = self.client.get(f'/users/1')
        assert resp.status_code == 404
        assert resp.json == {'error': 'No such user_id 1'}

    def test_successful_update_user(self):
        resp = self.client.post(
            '/users',
            json={'name': 'John Doe'}
        )
        user_id = resp.json['user_id']
        resp = self.client.put(
            f'/users/{user_id}',
            json={'name': 'Johnna Doe'}
        )
        assert resp.status_code == 200
        assert resp.json == {'status': 'success'}


class TestGoods(Initializer):
    # super().setup()
    # self.input_goods =

    # self.get_goods =

    def test_add_new_goods(self):
        resp = self.client.post(
            '/goods',
            json=[{'name': 'Chocolate_bar', 'price': 10},
                  {'name': 'Apricots', 'price': 25},
                  {'name': 'Blackberries', 'price': 55},
                  {'name': 'Avocado', 'price': 100},
                  {'name': 'Breadfruit', 'price': 130},
                  {'name': 'Cherries', 'price': 70},
                  ]
        )
        assert resp.status_code == 201
        assert resp.json == {'numbers of items created': 6}

    def test_get_goods(self):
        self.client.post(
            '/goods',
            json=[{'name': 'Chocolate_bar', 'price': 10, 'id': 1},
                  {'name': 'Apricots', 'price': 25, 'id': 2},
                  {'name': 'Blackberries', 'price': 55, 'id': 3},
                  {'name': 'Avocado', 'price': 100, 'id': 4},
                  {'name': 'Breadfruit', 'price': 130, 'id': 5},
                  {'name': 'Cherries', 'price': 70, 'id': 6},
                  ]
        )
        resp = self.client.get(f'/goods')
        assert resp.status_code == 200
        assert resp.json == [{'name': 'Chocolate_bar', 'price': 10, 'id': 1},
                             {'name': 'Apricots', 'price': 25, 'id': 2},
                             {'name': 'Blackberries', 'price': 55, 'id': 3},
                             {'name': 'Avocado', 'price': 100, 'id': 4},
                             {'name': 'Breadfruit', 'price': 130, 'id': 5},
                             {'name': 'Cherries', 'price': 70, 'id': 6},
                             ]

    def test_successful_update_goods(self):
        self.client.post(
            '/goods',
            json=[{'name': 'Chocolate_bar', 'price': 10, 'id': 1},
                  {'name': 'Apricots', 'price': 25, 'id': 2},
                  {'name': 'Blackberries', 'price': 55, 'id': 3},
                  {'name': 'Avocado', 'price': 100, 'id': 4},
                  {'name': 'Breadfruit', 'price': 130, 'id': 5},
                  {'name': 'Cherries', 'price': 70, 'id': 6},
                  ]
        )
        resp = self.client.put(
            '/goods',
            json=[{'name': 'Chocolate_bar', 'price': 12, 'id': 1},
                  {'name': 'Apricots', 'price': 28, 'id': 2},
                  {'name': 'Blackberries', 'price': 60, 'id': 3},
                  {'name': 'Apples', 'price': 90, 'id': 12},
                  {'name': 'Banana', 'price': 120, 'id': 7},
                  {'name': 'Bread', 'price': 55, 'id': 8},
                  ]
        )
        assert resp.status_code == 200
        assert resp.json == {'successfully_updated': 3, 'errors': {'no such id in goods': [12, 7, 8]}}


class TestStores(Initializer):
    def test_create_new_store(self):
        resp = self.client.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}
        )
        assert resp.status_code == 201
        assert resp.json == {'store_id': 1}

    def test_get_store(self):
        sent_store_data = self.client.post(
             '/store',
             json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}
        )
        store_id = sent_store_data.json['store_id']
        resp = self.client.get(f'/store/{store_id}')
        assert resp.status_code == 200
        assert resp.json == {'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}

    def test_successful_update_store(self):
        sent_store_data = self.client.post(
            '/store',
            json={'name': 'Mad Cow', 'location': 'Lviv', 'manager_id': 2}
        )
        store_id = sent_store_data.json['store_id']
        resp = self.client.put(
            f'/store/{store_id}',
            json={'name': 'Local Taste', 'location': 'Lviv', 'manager_id': 2}
        )
        assert resp.status_code == 200
        assert resp.json == {'status': 'success'}
