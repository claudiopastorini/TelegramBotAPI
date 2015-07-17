#!/usr/bin/env python
"""Little example for usage of TelegramBotAPI

In this example I show tha basic usage of TelegramBotAPI creating a bot that reply only with "Hi! " on "Hello".
"""

from lib import TelegramBotAPI

__author__ = "Claudio Pastorini (pincopallino93)"

__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Development"

TOKEN = "YOUR_TOKEN_HERE"

api = TelegramBotAPI(TOKEN)


@api.respond_to("Hello")
def respond(message):
    api.sendMessage(message.chat.id, "Hi!")


if __name__ == '__main__':
    api.debug = True
    api.run()