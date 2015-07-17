# http://www.expobrain.net/2010/07/31/simple-event-dispatcher-in-python/
class MessageDispatcher(object):
    """
    Message dispatcher which listen for text message and dispatch it.
    """

    def __init__(self):
        self._events = dict()

    def __del__(self):
        """
        Remove all listener references at destruction time.
        """
        self._events = None

    def has_listener(self, listener):
        """
        Return true if listener is already registered.
        :param listener: Dict, Listener to check.
        """
        return listener in self._events

    def dispatch_message(self, message):
        """
        Dispatch message to right function watching the text attribute.
        :param message: Message, Message to dispatch.
        """
        if message.text in self._events.keys():
            listener = self._events[message.text]
            listener(message)

    def add_message_listener(self, word, listener):
        """
        Add a message listener for a word.
        :param word: String, Word which the MessageDispatcher has to check.
        :param listener: Function, Function that MessageDispatcher has to call when word comes.
        """
        if not self.has_listener(listener):
            self._events.update({word: listener})

    def remove_message_listener(self, listener):
        """
        Remove message listener.
        :param listener: Dict, Listener to remove.
        """
        if self.has_listener(listener):
            del self._events[listener]

    def respond_to(self, word):
        """
        A decorator useful in order to add listener for a message.
        Example:
            @api.respond_to("Hello")
            def respond(message):
                api.sendMessage(message.chat.id, "Hi!")

        :param word: String, Word.
        """

        def decorator(function):
            self.add_message_listener(word, function)
            return function

        return decorator