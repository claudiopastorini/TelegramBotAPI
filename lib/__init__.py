import requests

from lib.dispatcher import MessageDispatcher
from lib.models import *



# noinspection PyPep8Naming
class TelegramBotAPI(MessageDispatcher):  # TODO Use singleton?
    """
    Client for Telegram Bot API.
    You can simply use it in this way:

        api = TelegramBotAPI(YOUR_TOKEN_HERE)


        @api.respond_to("Hello")
        def respond(message):
            api.sendMessage(message.chat.id, "Hi!")


    For more examples see the examples package.
    """
    METHOD_LIST = ["getMe", "getUpdates", "setWebhook", "sendMessage", "forwardMessage", "sendPhoto", "sendAudio",
                   "sendDocument", "sendSticker", "sendVideo", "sendLocation", "sendChatAction", "getUserProfilePhotos",
                   "getUpdates", "setWebhook"]

    def __init__(self, token=None, bot=None, debug=False):
        """
        :param token: String, It is a string along the lines of 110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw that will
            be required to authorize the bot and send requests to the Bot API.
        :param bot: User, User that represent the  bot.
        """
        super().__init__()
        self._token = token
        self._bot = bot
        self._debug = debug
        self._offset = 0  # Default value for specification
        self._limit = 100  # Default value for specification
        self._timeout = 0  # Default value for specification
        self._base_url = ""

        if bot is None:
            self._refresh_base_url()  # Refresh base url
            self.getMe()  # Get the bot

    @property
    def token(self):
        """
        It is a string along the lines of 110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw that will be required to
        authorize the bot and send requests to the Bot API.
        """
        return "You are not allowed to get token!"

    @token.setter
    def token(self, value):
        self._token = value
        self._refresh_base_url()  # TODO: Use observable?

    @property
    def bot(self):
        """
        User that represent the bot.
        """
        return self._bot

    @property
    def debug(self):
        """
        Debug Boolean.
        """
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    @property
    def offset(self):
        """
        Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of
        previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An
        update is considered confirmed as soon as getUpdates is called with an offset higher than its update_id.
        """
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value

    @property
    def limit(self):
        """
        Limits the number of updates to be retrieved. Values between 1—100 are accepted.
        """
        return self._limit

    @limit.setter
    def limit(self, value):
        if 0 < value < 101:
            self._limit = value
        else:
            raise Exception("Not valid range")

    @property
    def timeout(self):
        """
        Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        self._timeout = value

    def _refresh_base_url(self):
        """
        Private method useful in order to refresh base URL using the token.
        """
        self._base_url = "https://api.telegram.org/bot" + self._token + "/"

    def getMe(self):
        """
        A simple method for testing your bot's auth token. Requires no parameters.
        :Returns basic information about the bot in form of a User object.
        """
        url = self._base_url + self.METHOD_LIST[0]
        response_text = requests.get(url).text
        response = Response.from_text(response_text)
        self._bot = response.result

    def getUpdates(self, offset=None, limit=None, timeout=None):
        """
        Use this method to receive incoming updates using long polling (wiki). An Array of Update objects is returned.
        :param offset: Integer, Optional. Identifier of the first update to be returned. Must be greater by one than the highest
            among the identifiers of previously received updates. By default, updates starting with the earliest
            unconfirmed update are returned. An update is considered confirmed as soon as getUpdates is called with
            an offset higher than its update_id.
        :param limit: Integer, Optional. Limits the number of updates to be retrieved. Values between 1—100 are
            accepted. Defaults to 100.
        :param timeout: Integer, Optional. Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling.
        :return: An Array of Update objects is returned.
        """
        if offset is None:
            offset = self._offset
        if limit is None:
            limit = self._limit
        if timeout is None:
            timeout = self._timeout

        data = {"offset": offset, "limit": limit, "timeout": timeout}

        url = self._base_url + self.METHOD_LIST[1]
        response_text = requests.get(url, params=data).text

        if self._debug:  # If in debug mode, print all response
            print(response_text)

        response = Response.from_text(response_text)
        try:
            self._offset = response.result[0].update_id
        except IndexError:
            self._offset = 0

        return response.result

    def sendMessage(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None):
        """
        Use this method to send text messages.
        :param chat_id: Integer, Unique identifier for the message recipient — User or GroupChat id.
        :param text: String, Text of the message to be sent.
        :param disable_web_page_preview: Boolean, Optional. Disables link previews for links in this message.
        :param reply_to_message_id: Integer, Optional. If the message is a reply, ID of the original message.
        :param reply_markup: ReplyKeyboardMarkup or ReplyKeyboardHide or ForceReply, Optional. Additional interface
            options. A JSON-serialized object for a custom reply keyboard, instructions to hide keyboard or to force a
            reply from the user.
        :return: On success, the sent Message is returned.
        """
        if chat_id is not "" and text is not "":
            data = {"chat_id": chat_id,
                    "text": text,
                    "disable_web_page_preview": disable_web_page_preview,
                    "reply_to_message_id": reply_to_message_id,
                    "reply_markup": reply_markup}

            url = self._base_url + self.METHOD_LIST[3]
            response = json.loads(requests.post(url, data=data).text)
            return response

    def dispatch_message(self, message):
        """
        Override of dispatch_message in order to increase also message offset.
        """
        super().dispatch_message(message)
        self._offset += 1

    def run(self):
        """
        This method starts the client.
        """
        while True:
            updates = self.getUpdates()

            for update in updates:
                self.dispatch_message(update.message)
