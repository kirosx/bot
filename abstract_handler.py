from abc import ABCMeta, abstractmethod
from keyboard import Buttons
from dbclass import Database


class AbstractHandler(metaclass=ABCMeta):
    def __init__(self, bot):
        self.bot = bot
        self.buttons = Buttons()
        self.bd = Database()

    @abstractmethod
    def run_handlers(self):
        pass
