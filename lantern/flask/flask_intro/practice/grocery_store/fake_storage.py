from itertools import count
from .store_app import NoSuchUserError, NoSuchUserID, NoSuchStoreID, NoSuchManagerID


class FakeStorage:
    def __init__(self):
        self._users = FakeUsers()
        self._goods = FakeGoods()
        self._stores = FakeStores()

    @property
    def users(self):
        return self._users

    @property
    def goods(self):
        return self._goods

    @property
    def stores(self):
        return self._stores


class FakeUsers:
    def __init__(self):
        self._users = {}
        self._id_counter = count(1)

    def add(self, user):
        user_id = next(self._id_counter)
        self._users[user_id] = user
        return user_id

    def get_user_by_id(self, user_id):
        try:
            return self._users[user_id]
        except KeyError:
            raise NoSuchUserError(user_id)

    def update_user_by_id(self, user_id, user):
        if user_id in self._users:
            self._users[user_id] = user
        else:
            raise NoSuchUserError(user_id)


class FakeGoods:
    def __init__(self):
        self._goods = {}
        self._id_counter = count(1)

    def add(self, goods):
        count_of_new_goods = 0
        for i in goods:
            goods_id = next(self._id_counter)
            self._goods[goods_id] = i
            count_of_new_goods += 1
        return count_of_new_goods

    def get_goods(self):
        # import pdb;pdb.set_trace()
        list_goods = []
        for key, values in self._goods.items():  # self._goods возвращает {1: {'name': 'Chocolate_bar', 'price': 10} а нам нужно только значение {'name': 'Chocolate_bar', 'price': 10}
            list_goods.append({**values, "id": key})  # делаем распаковку values потому что у нас там лежит {'name': 'Chocolate_bar', 'price': 10}
            # "id": key делаем потому что по условию у нас должен возвращать метод сами продукты и их id
        return list_goods

    def update_goods(self, goods):
        number_update_goods = 0
        list_goods_id_error = []
        for key in goods:
            if key["id"] in self._goods:
                # import pdb;pdb.set_trace()
                self._goods[key['id']] = {**goods[key['id']], **key}
                number_update_goods += 1
            else:
                list_goods_id_error.append(key["id"])
        return number_update_goods, list_goods_id_error


class FakeStores:
    def __init__(self):
        self._stores = {}
        self._id_counter = count(1)

    def add_new_store(self, store):
        store_id = next(self._id_counter)
        user_id = store_id
        try:
            self._stores[store_id] = store
            return store_id
        except KeyError:
            raise NoSuchUserID(user_id)

    def get_store(self, store_id):
        # import pdb;pdb.set_trace()
        try:
            return self._stores[store_id]
        except KeyError:
            raise NoSuchStoreID(store_id)

    def update_store_data_by_id(self, store_id, store):
        manager_id = store_id
        if store_id in self._stores:
            self._stores[store_id] = store
        else:
            raise (NoSuchStoreID(store_id), NoSuchManagerID(manager_id))