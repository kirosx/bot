from telebot.types import (InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from dbclass import Database
from config import BASKET_BUTTONS


class Buttons:
    def __init__(self):
        self.markup = None
        self.db = Database()

    def set_categories(self):
        self.markup = ReplyKeyboardMarkup(True, True)
        for i in self.db.show_categories:
            self.markup.row(i)
        self.markup.row('$ BASKET $')
        return self.markup

    def remove_buttons(self):
        return ReplyKeyboardRemove()

    def show_basket_menu(self, is_basket_full=True):
        self.remove_buttons()
        self.markup = ReplyKeyboardMarkup(True, True)
        if not is_basket_full:
            for i in BASKET_BUTTONS[:-2]:
                self.markup.row(i)
            return self.markup
        for i in BASKET_BUTTONS:
            self.markup.row(i)
        return self.markup

    def show_products_from_category(self, category: str):
        self.markup = InlineKeyboardMarkup(row_width=1)
        for i in self.db.show_products_in_category(category):
            self.markup.add(InlineKeyboardButton(f"{i['name']} {i['price']}$ ({i['qty']})",
                                                 callback_data=str(i['_id'])))
        return self.markup

    def make_button_to_order(self, product):
        self.markup = InlineKeyboardMarkup(row_width=1)
        self.markup.add(InlineKeyboardButton('ORDER', callback_data=f'buy {str(product["_id"])}'))
        return self.markup




