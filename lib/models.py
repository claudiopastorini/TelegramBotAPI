import json


def as_json(dictionary):
    """
    Object hook used in order to create the right object reading a JSON.
    :param dictionary: Dict, Dictionary to analyze.
    :return: The right object represented in the JSON.
    """
    if "first_name" in dictionary:
        return User(**dictionary)
    elif "update_id" in dictionary:
        return Update(**dictionary)
    elif "result" in dictionary:
        return Response(**dictionary)
    else:
        dictionary["message_from"] = dictionary["from"]
        del dictionary["from"]
        return Message(**dictionary)


class JSONEncoder(json.JSONEncoder):
    """
    JSONEncoder extension useful in order to return dict with right keys and not private ones.
    """

    def default(self, obj):
        dictionary = dict()
        for key in obj.__dict__.keys():
            dictionary.update({key[1:]: obj.__dict__[key]})
        return dictionary


class Jsonable():
    """
    Father class for all object that can serialized/deserialized from/to JSON.
    """

    @staticmethod
    def to_json(obj):
        """
        Static method that return the JSON of the object.
        :param obj: Object, The object to serialize.
        :return: The JSON of the serialized Object.
        """
        return json.dumps(obj, cls=JSONEncoder)

    @staticmethod
    def from_text(text):
        """
        Static method that return the Object from a JSON.
        :param text: String, The JSON to deserialize.
        :return: The Object of the deserialized JSON.
        """
        return json.loads(text, object_hook=as_json)


class Response(Jsonable):
    """
    This object represents a Telegram server's response.
    """

    def __init__(self, ok, result=None, description=None, error_code=None):
        """
        :param ok: Boolean, Response status.
        :param result: List of Object, The result of the query.
        :param description: String, Human-readable description of the result.
        :param error_code: Integer, Integer for error but its contents are subject to change in the future.
        """
        if not result:
            result = []
        self._ok = ok
        self._result = result
        self._description = description
        self._error_code = error_code

    @property
    def ok(self):
        """
        Response status.
        """
        return self._ok

    @property
    def result(self):
        """
        The result of the query.
        """
        return self._result

    @property
    def description(self):
        """
        Human-readable description of the result.
        """
        return self._description

    @property
    def error_code(self):
        """
        Integer for error but its contents are subject to change in the future.
        """
        return self._error_code


class User(Jsonable):
    """
    This object represents a Telegram user or bot.
    """

    def __init__(self, id, first_name, last_name=None, username=None):
        """
        :param id: Integer, Unique identifier for this user or bot.
        :param first_name: String, User‘s or bot’s first name.
        :param last_name: String, Optional. User‘s or bot’s last name.
        :param username: String, Optional. User‘s or bot’s username.
        """
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._username = username

    @property
    def id(self):
        """
        Unique identifier for this user or bot.
        """
        return self._id

    @property
    def first_name(self):
        """
        User‘s or bot’s first name.
        """
        return self._first_name

    @property
    def last_name(self):
        """
        User‘s or bot’s last name.
        """
        return self._last_name

    @property
    def username(self):
        """
        User‘s or bot’s username.
        """
        return self._username


class GroupChat(Jsonable):
    """
    This object represents a group chat.
    """

    def __init__(self, id, title):
        """
        :param id: Integer, Unique identifier for this group chat.
        :param title: String, Group name.
        """
        self._id = id
        self._title = title

    @property
    def id(self):
        """
        Unique identifier for this group chat.
        """
        return self._id

    @property
    def title(self):
        """
        Group name.
        """
        return self._title


class Message(Jsonable):
    """
    This object represents a message.
    """

    def __init__(self, message_id, message_from, date, chat, forward_from=None, forward_date=None,
                 reply_to_message=None, text=None, audio=None, document=None, photo=None, sticker=None, video=None,
                 contact=None, location=None, new_chat_participant=None, left_chat_participant=None,
                 new_chat_title=None, new_chat_photo=None, delete_chat_photo=None, group_chat_created=None):
        """
        :param message_id: Integer, Unique message identifier.
        :param message_from: User, Sender.
        :param date: Integer, Date the message was sent in Unix time.
        :param chat: User or GroupChat, Conversation the message belongs to — user in case of a private message,
            GroupChat in case of a group.
        :param forward_from: User, Optional. For forwarded messages, sender of the original message.
        :param forward_date: Integer, Optional. For forwarded messages, date the original message was sent in Unix time.
        :param reply_to_message: Message, Optional. For replies, the original message. Note that the Message object in
            this field will not contain further reply_to_message fields even if it itself is a reply.
        :param text: String, Optional. For text messages, the actual UTF-8 text of the message.
        :param audio: Audio, Optional. Message is an audio file, information about the file.
        :param document: Document, Optional. Message is a general file, information about the file.
        :param photo: Array of PhotoSize, Optional. Message is a photo, available sizes of the photo.
        :param sticker: Sticker, Optional. Message is a sticker, information about the sticker.
        :param video: Video, Optional. Message is a video, information about the video.
        :param contact: Contact, Optional. Message is a shared contact, information about the contact.
        :param location: Location, Optional. Message is a shared location, information about the location.
        :param new_chat_participant: User, Optional. A new member was added to the group, information about them (this
            member may be bot itself).
        :param left_chat_participant: User, Optional. A member was removed from the group, information about them (this
            member may be bot itself).
        :param new_chat_title: String, Optional. A group title was changed to this value.
        :param new_chat_photo: Array of PhotoSize, Optional. A group photo was change to this value.
        :param delete_chat_photo: Boolean, Optional. Informs that the group photo was deleted.
        :param group_chat_created: Boolean, Optional. Informs that the group has been created.
        """
        self._message_id = message_id
        self._from = message_from
        self._chat = chat
        self._date = date
        self._forward_from = forward_from
        self._forward_date = forward_date
        self._reply_to_message = reply_to_message
        self._text = text
        self._audio = audio
        self._document = document
        self._photo = photo
        self._sticker = sticker
        self._video = video
        self._contact = contact
        self._location = location
        self._new_chat_participant = new_chat_participant
        self._left_chat_participant = left_chat_participant
        self._new_chat_title = new_chat_title
        self._new_chat_photo = new_chat_photo
        self._delete_chat_photo = delete_chat_photo
        self._group_chat_created = group_chat_created

    @property
    def message_id(self):
        """
        Unique message identifier.
        """
        return self._message_id

    @property
    def message_from(self):
        """
        Sender.
        """
        return self._from

    @property
    def chat(self):
        """
        Conversation the message belongs to — user in case of a private message, GroupChat in case of a group.
        """
        return self._chat

    @property
    def date(self):
        """
        Date the message was sent in Unix time.
        """
        return self._date

    @property
    def forward_from(self):
        """
        For forwarded messages, sender of the original message.
        """
        return self._forward_from

    @property
    def forward_date(self):
        """
        For forwarded messages, date the original message was sent in Unix time.
        """
        return self._forward_date

    @property
    def reply_to_message(self):
        """
        For replies, the original message. Note that the Message object in this field will not contain further
        reply_to_message fields even if it itself is a reply.
        """
        return self._reply_to_message

    @property
    def text(self):
        """
        For text messages, the actual UTF-8 text of the message.
        """
        return self._text

    @property
    def audio(self):
        """
        Message is an audio file, information about the file.
        """
        return self._audio

    @property
    def document(self):
        """
        Message is a general file, information about the file.
        """
        return self._document

    @property
    def photo(self):
        """
        Message is a photo, available sizes of the photo.
        """
        return self._photo

    @property
    def sticker(self):
        """
        Message is a sticker, information about the sticker.
        """
        return self._sticker

    @property
    def video(self):
        """
        Message is a video, information about the video.
        """
        return self._video

    @property
    def contact(self):
        """
        Message is a shared contact, information about the contact.
        """
        return self._contact

    @property
    def location(self):
        """
        Message is a shared location, information about the location.
        """
        return self._location

    @property
    def new_chat_participant(self):
        """
        A new member was added to the group, information about them (this member may be bot itself).
        """
        return self._new_chat_participant

    @property
    def left_chat_participant(self):
        """
        A member was removed from the group, information about them (this member may be bot itself).
        """
        return self._left_chat_participant

    @property
    def new_chat_title(self):
        """
        A group title was changed to this value.
        """
        return self._new_chat_title

    @property
    def new_chat_photo(self):
        """
        A group photo was change to this value.
        """
        return self._new_chat_photo

    @property
    def delete_chat_photo(self):
        """
         Informs that the group photo was deleted.
        """
        return self._delete_chat_photo

    @property
    def group_chat_created(self):
        """
        Informs that the group has been created.
        """
        return self._group_chat_created


class PhotoSize(Jsonable):
    """
    This object represents one size of a photo or a file / sticker thumbnail.
    """

    def __init__(self, file_id, width, height, file_size=None):
        """
        :param file_id: String, Unique identifier for this file.
        :param width: Integer, Photo width.
        :param height: Integer, Photo height.
        :param file_size: Integer, Optional. File size.
        """
        self._file_id = file_id
        self._width = width
        self._height = height
        self._file_size = file_size

    @property
    def file_id(self):
        """
        Unique identifier for this file.
        """
        return self._file_id

    @property
    def width(self):
        """
        Photo width.
        """
        return self._width

    @property
    def height(self):
        """
        Photo height.
        """
        return self._height

    @property
    def file_size(self):
        """
        File size.
        """
        return self._file_size


class Audio(Jsonable):
    """
    This object represents an audio file (voice note).
    """

    def __init__(self, file_id, duration, mime_type=None, file_size=None):
        """
        :param file_id: String, Unique identifier for this file.
        :param duration: Integer, Duration of the audio in seconds as defined by sender.
        :param mime_type: String, Optional. MIME type of the file as defined by sender.
        :param file_size: Integer, Optional. File size.
        """
        self._file_id = file_id
        self._duration = duration
        self._mime_type = mime_type
        self._file_size = file_size

    @property
    def file_id(self):
        """
        Unique identifier for this file.
        """
        return self._file_id

    @property
    def duration(self):
        """
        Duration of the audio in seconds as defined by sender.
        """
        return self._duration

    @property
    def mime_type(self):
        """
        MIME type of the file as defined by sender.
        """
        return self._mime_type

    @property
    def file_size(self):
        """
        File size.
        """
        return self._file_size


class Document(Jsonable):
    """
    This object represents a general file (as opposed to photos and audio files).
    """

    def __init__(self, file_id, thumb, file_name=None, mime_type=None, file_size=None):
        """
        :param file_id: String, Unique file identifier.
        :param thumb: PhotoSize, Document thumbnail as defined by sender.
        :param file_name: String, Optional. Original filename as defined by sender.
        :param mime_type: String, Optional. MIME type of the file as defined by sender.
        :param file_size: Integer, Optional. File size.
        """
        self._file_id = file_id
        self._thumb = thumb
        self._file_name = file_name
        self._mime_type = mime_type
        self._file_size = file_size

    @property
    def file_id(self):
        """
        Unique file identifier.
        """
        return self._file_id

    @property
    def thumb(self):
        """
        Document thumbnail as defined by sender.
        """
        return self._thumb

    @property
    def file_name(self):
        """
        Original filename as defined by sender.
        """
        return self._file_name

    @property
    def mime_type(self):
        """
        MIME type of the file as defined by sender.
        """
        return self._mime_type

    @property
    def file_size(self):
        """
        File size.
        """
        return self._file_size


class Sticker(Jsonable):
    """
    This object represents a sticker.
    """

    def __init__(self, file_id, width, height, thumb, file_size=None):
        """
        :param file_id: String, Unique identifier for this file.
        :param width: Integer, Sticker width.
        :param height: Integer, Sticker height.
        :param thumb: PhotoSize, Sticker thumbnail in .webp or .jpg format.
        :param file_size: Integer, Optional. File size.
        """
        self._file_id = file_id
        self._width = width
        self._height = height
        self._thumb = thumb
        self._file_size = file_size

    @property
    def file_id(self):
        """
        Unique identifier for this file.
        """
        return self._file_id

    @property
    def width(self):
        """
        Sticker width.
        """
        return self._width

    @property
    def height(self):
        """
        Sticker height.
        """
        return self._height

    @property
    def thumb(self):
        """
        Sticker thumbnail in .webp or .jpg format.
        """
        return self._thumb

    @property
    def file_size(self):
        """
        File size.
        """
        return self._file_size


class Video(Jsonable):
    """
    This object represents a video file.
    """

    def __init__(self, file_id, width, height, duration, thumb, mime_type, file_size=None, caption=None):
        """
        :param file_id: String, Unique identifier for this file.
        :param width: Integer, Video width as defined by sender.
        :param height: Integer, Video height as defined by sender.
        :param duration: Integer, Duration of the video in seconds as defined by sender.
        :param thumb: PhotoSize, Video thumbnail.
        :param mime_type: String, Optional. Mime type of a file as defined by sender.
        :param file_size: Integer, Optional. File size.
        :param caption: String, Optional. Text description of the video (usually empty).
        """
        self._file_id = file_id
        self._width = width
        self._height = height
        self._duration = duration
        self._thumb = thumb
        self._mime_type = mime_type
        self._file_size = file_size
        self._caption = caption

    @property
    def file_id(self):
        """
        Unique identifier for this file.
        """
        return self._file_id

    @property
    def width(self):
        """
        Video width as defined by sender.
        """
        return self._width

    @property
    def height(self):
        """
        Video height as defined by sender.
        """
        return self._height

    @property
    def duration(self):
        """
        Duration of the video in seconds as defined by sender.
        """
        return self._duration

    @property
    def thumb(self):
        """
        Video thumbnail.
        """
        return self._thumb

    @property
    def mime_type(self):
        """
        Mime type of a file as defined by sender.
        """
        return self._mime_type

    @property
    def file_size(self):
        """
        File size.
        """
        return self._file_size

    @property
    def caption(self):
        """
        Text description of the video (usually empty).
        """
        return self._caption


class Contact(Jsonable):
    """
    This object represents a phone contact.
    """

    def __init__(self, phone_number, first_name, last_name=None, user_id=None):
        """
        :param phone_number: String, Contact's phone number.
        :param first_name: String, Contact's first name.
        :param last_name: String, Optional. Contact's last name.
        :param user_id: String, Optional. Contact's user identifier in Telegram.
        :return:
        """
        self._phone_number = phone_number
        self._first_name = first_name
        self._last_name = last_name
        self._user_id = user_id

    @property
    def phone_number(self):
        """
        Contact's phone number.
        """
        return self._phone_number

    @property
    def first_name(self):
        """
        Contact's first name.
        """
        return self._first_name

    @property
    def last_name(self):
        """
        Contact's last name.
        """
        return self._last_name

    @property
    def user_id(self):
        """
        Contact's user identifier in Telegram.
        """
        return self._user_id


class Location(Jsonable):
    """
    This object represents a point on the map.
    """

    def __init__(self, longitude, latitude):
        """
        :param longitude: Float, Longitude as defined by sender.
        :param latitude: Float, Latitude as defined by sender.
        """
        self._longitude = longitude
        self._latitude = latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def latitude(self):
        return self._latitude


class UserProfilePhotos(Jsonable):
    """
    This object represent a user's profile pictures.
    """

    def __init__(self, total_count, photos):
        """
        :param total_count: Integer, Total number of profile pictures the target user has photos.
        :param photos: Array of Array of PhotoSize, Requested profile pictures (in up to 4 sizes each).
        """
        self._total_count = total_count
        self._photos = photos

    @property
    def total_count(self):
        """
        Total number of profile pictures the target user has photos.
        """
        return self._total_count

    @property
    def photos(self):
        """
        Requested profile pictures (in up to 4 sizes each).
        """
        return self._photos


class ReplyKeyboardMarkup(Jsonable):
    """
    This object represents a custom keyboard with reply options (see Introduction to bots for details and examples).
    """

    def __init__(self, keyboard, resize_keyboard=False, one_time_keyboard=False, selective=None):
        """
        :param keyboard: Array of Array of String, Array of button rows, each represented by an Array of Strings.
        :param resize_keyboard: Boolean, Optional. Requests clients to resize the keyboard vertically for optimal fit
            (e.g., make the keyboard smaller if there are just two rows of buttons). Defaults to false, in which case
            the custom keyboard is always of the same height as the app's standard keyboard.
        :param one_time_keyboard: Boolean, Optional. Requests clients to hide the keyboard as soon as it's been used.
            Defaults to false.
        :param selective: Boolean, Optional. Use this parameter if you want to show the keyboard to specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
        """
        self._keyboard = keyboard
        self._resize_keyboard = resize_keyboard
        self._one_time_keyboard = one_time_keyboard
        self._selective = selective

    @property
    def keyboard(self):
        """
        Array of button rows, each represented by an Array of Strings.
        """
        return self._keyboard

    @property
    def resize_keyboard(self):
        """
        Requests clients to resize the keyboard vertically for optimal fit.
        """
        return self._resize_keyboard

    @property
    def one_time_keyboard(self):
        """
        Requests clients to hide the keyboard as soon as it's been used.
        """
        return self._one_time_keyboard

    @property
    def selective(self):
        """
        Use this parameter if you want to show the keyboard to specific users only.
        """
        return self._selective


class ReplyKeyboardHide(Jsonable):
    """
    Upon receiving a message with this object, Telegram clients will hide the current custom keyboard and display the
    default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot.
    An exception is made for one-time keyboards that are hidden immediately after the user presses a button
    (see ReplyKeyboardMarkup).
    """

    def __init__(self, hide_keyboard, selective=None):
        """
        :param hide_keyboard: Boolean, Requests clients to hide the custom keyboard.
        :param selective: Boolean, Optional. Use this parameter if you want to hide keyboard for specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
        """
        self._hide_keyboard = hide_keyboard
        self._selective = selective

    @property
    def hide_keyboard(self):
        """
        Requests clients to hide the custom keyboard.
        """
        return self._hide_keyboard

    @property
    def selective(self):
        """
        Use this parameter if you want to hide keyboard for specific users only.
        """
        return self._selective


class ForceReply(Jsonable):
    """
    Upon receiving a message with this object, Telegram clients will display a reply interface to the user (act as if
    the user has selected the bot‘s message and tapped ’Reply'). This can be extremely useful if you want to create
    user-friendly step-by-step interfaces without having to sacrifice privacy mode.
    """

    def __init__(self, force_reply, selective=None):
        """
        :param force_reply: Boolean, Shows reply interface to the user, as if they manually selected the bot‘s message
            and tapped ’Reply'.
        :param selective: Boolean, Optional. Use this parameter if you want to force reply from specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
        """
        self._force_reply = force_reply
        self._selective = selective

    @property
    def force_reply(self):
        """
        Shows reply interface to the user, as if they manually selected the bot‘s message and tapped ’Reply'.
        """
        return self._force_reply

    @property
    def selective(self):
        """
        Use this parameter if you want to force reply from specific users only.
        """
        return self._selective


class Update(Jsonable):
    """
    This object represents an incoming update.
    """

    def __init__(self, update_id, message=None):
        """
        :param update_id: Integer, The update‘s unique identifier. Update identifiers start from a certain positive
            number and increase sequentially. This ID becomes especially handy if you’re using Webhooks, since it allows
            you to ignore repeated updates or to restore the correct update sequence, should they get out of order.
        :param message: Message, Optional. New incoming message of any kind — text, photo, sticker, etc.
        """
        self._update_id = update_id
        self._message = message

    @property
    def update_id(self):
        """
        The update‘s unique identifier. Update identifiers start from a certain positive number and increase
        sequentially. This ID becomes especially handy if you’re using Webhooks, since it allows you to ignore
        repeated updates or to restore the correct update sequence, should they get out of order.
        """
        return self._update_id

    @property
    def message(self):
        """
        New incoming message of any kind — text, photo, sticker, etc.
        :return:
        """
        return self._message