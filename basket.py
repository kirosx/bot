from dbclass import Database


class Basket:
    def __init__(self, user_tgid: int):
        self.db = Database()
        self.user = self.db.users.find_one({'tgid': user_tgid})
        self.products = self.user['basket']

    def total_price(self):
        default = 0
        if self.products:
            for k, v in self.products.items():
                default += self.db.products.find_one({'name': k})['price'] * v
        return default

    def show_basket_items(self):
        items = ''
        for k, v in self.products.items():
            items += f'Name: {k}\nquantity: {v}\n\n\n'
        items += f'TOTAL PRICE: {self.total_price()}'
        return items

    def clear_basket(self):
        for k, v in self.products.items():
            self.db.products.find_one_and_update({'name': k}, {'$inc': {'qty': v}})
        self.products.clear()
        self.db.users.find_one_and_update({'tgid': self.user['tgid']},
                                          {'$set': {'basket': self.products}})

    def add_product(self, product: dict):
        product_in_db = self.db.products.find_one(product)
        if product_in_db and not (product_in_db['qty'] < 1):
            self.db.products.find_one_and_update(product, {'$set': {'qty': product_in_db['qty']-1}})
            if product_in_db['name'] not in self.products:
                self.products[product_in_db['name']] = 1
            else:
                self.products[product_in_db['name']] += 1
            self.db.users.find_one_and_update({'tgid': self.user['tgid']},
                                              {'$set': {'basket': self.products}})


