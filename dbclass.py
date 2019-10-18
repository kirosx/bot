from pymongo import MongoClient
from config import DATABASE, DB_NAME, DB_PWD, DB_USER, CATEGORY_NAME
from json import loads
from bson.objectid import ObjectId
from time import asctime as time


class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = None

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Database(metaclass=Singleton):
    def __init__(self):
        self.db = MongoClient(DATABASE, username=DB_USER, password=DB_PWD)[DB_NAME]
        self.users = self.db['users']
        self.products = self.db['products']

    def load_test_collection(self, collection_name: str):
        self.db.create_collection(collection_name)
        with open('test_collection.js') as test_db:
            for i in test_db:
                self.db[collection_name].insert_one(loads(i))

    def count_users(self):
        return self.users.find().count()

    def add_new_user(self, message):
        self.users.insert_one(dict(tgid=message.from_user.id, tgusername=message.from_user.username,
                                   tgfirstname=message.from_user.first_name, is_auth=False, time=time(),
                                   basket={}))

    @property
    def show_categories(self):
        return {i[CATEGORY_NAME] for i in self.db.products.find()}

    def show_products_in_category(self, category: str):
        return self.products.find({CATEGORY_NAME: category})

    def find_product_by_str_obj_id(self, object_id: str):
        return self.products.find_one({'_id': ObjectId(object_id)})




