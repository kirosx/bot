from telebot import TeleBot
from handler import HandlerBuilder
from config import TOKEN


class Bot:
    def __init__(self, token: str):
        self.bot = TeleBot(token)
        self.handler = HandlerBuilder(self.bot)

    def run_bot(self):
        self.handler.run_handlers()
        self.bot.polling(none_stop=True)


if __name__ == '__main__':
    bot = Bot(TOKEN)
    bot.run_bot()