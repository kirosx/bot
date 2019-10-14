from abstract_handler import AbstractHandler
from time import asctime as time
from basket import Basket
from config import BASKET_BUTTONS, CATEGORY_NAME, CLEARED
from utils import obj_id_checker, buy_button_checker


class HandlerCommands(AbstractHandler):
    def __init__(self, bot):
        super(HandlerCommands, self).__init__(bot)

    def run_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start_handler(message):
            client = self.bd.users.find_one({'tgid': message.from_user.id})
            if not client:
                self.bd.users.insert_one(dict(tgid=message.from_user.id, tgusername=message.from_user.username,
                                              tgfirstname=message.from_user.first_name, is_auth=False, time=time(),
                                              basket={}))
            self.bot.send_message(message.from_user.id, 'Choose category', reply_markup=self.buttons.set_categories())


class HandlerCategories(AbstractHandler):
    def __init__(self, bot):
        super(HandlerCategories, self).__init__(bot)

    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: m.text in self.bd.show_categories)
        def return_products_handler(message):
            self.bot.send_message(message.from_user.id, message.text,
                                  reply_markup=self.buttons.show_products_from_category(message.text))


class HandlerInline(AbstractHandler):
    def __init__(self, bot):
        super(HandlerInline, self).__init__(bot)

    @staticmethod
    def make_modal_message(product: dict):
        message = f'''
        Added to basket
        {product["name"]}
        price: {product["price"]}
        now at store: {product["qty"] - 1}
        '''
        return message

    @staticmethod
    def make_description_message(product: dict):
        message = f'''{product[CATEGORY_NAME]} {product['name']}
        price - {product['price']}'''
        return message

    def run_handlers(self):
        @self.bot.callback_query_handler(func=lambda call: obj_id_checker(call.data))
        def replay_info_about_product(call):
            product = self.bd.find_product_by_str_obj_id(call.data)
            self.bot.send_message(call.from_user.id,
                                  self.make_description_message(product),
                                  reply_markup=self.buttons.make_button_to_order(product))

        @self.bot.callback_query_handler(func=lambda call: buy_button_checker(call.data))
        def order_button_handler(call):
            obj_id = str.split(call.data)[1]
            product = self.bd.find_product_by_str_obj_id(obj_id)
            if product['qty'] < 1:
                message = 'No product at store'
                self.bot.answer_callback_query(call.id, message, show_alert=True)
            else:
                basket = Basket(call.from_user.id)
                basket.add_product(product)
                message = self.make_modal_message(product)
                self.bot.answer_callback_query(call.id, message, show_alert=True)
                self.bot.send_message(call.from_user.id, product[CATEGORY_NAME],
                                      reply_markup=self.buttons.show_products_from_category(product[CATEGORY_NAME]))


class HandlerBasket(AbstractHandler):
    def __init__(self, bot):
        super(HandlerBasket, self).__init__(bot)

    def run_handlers(self):
        @self.bot.message_handler(func=lambda m: m.text == '$ BASKET $' or (m.text in BASKET_BUTTONS))
        def show_basket(message):
            basket = Basket(message.from_user.id)
            if message.text == '$ BASKET $':
                show = 'Empty' if not basket.products else basket.show_basket_items()
                boolean = False if show == 'Empty' else True
                self.bot.send_message(message.from_user.id, show, reply_markup=self.buttons.show_basket_menu(boolean))
            elif message.text == 'CLEAR':
                basket.clear_basket()
                self.bot.send_message(message.from_user.id, CLEARED, reply_markup=self.buttons.show_basket_menu(False))
            elif message.text == '<<BACK':
                self.bot.send_message(message.from_user.id, message.text, reply_markup=self.buttons.set_categories())
