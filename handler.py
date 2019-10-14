from handlers import HandlerCommands, HandlerCategories, HandlerInline, HandlerBasket


class HandlerBuilder:
    def __init__(self, bot):
        self.handler_commands = HandlerCommands(bot)
        self.handler_categories = HandlerCategories(bot)
        self.handler_inline = HandlerInline(bot)
        self.handler_basket = HandlerBasket(bot)

    def run_handlers(self):
        for i in self.__dict__.values():
            i.run_handlers()
