# TelegramBotAPI
Python client for the Telegram Bot API (https://core.telegram.org/bots/)


## Installation
Run in order to install all requirements with pip:
```
    pip install -r requirements.txt
```
And after downloading the whole repo, extract, open the folder and run:
```
    python setup.py install
```

## Usage

Create an instance of Telegram Bot API with your Token:
``` python
    api = TelegramBotAPI(YOUR_TOKEN_HERE)
```
Defines your functions that respond to some text input:
``` python
    @api.respond_to("YOUR_WORD_TO_CATCH_HERE")
    def respond(message):
        # YOUR_CODE_HERE
```
For now you can only send message using sendMessage API.
``` python
    api.sendMessage(message.chat.id, "YOUR_RESPONSE_HERE")
```

## Contribution

Feel free to contribute!!

## License

    The MIT License (MIT)

    Copyright (c) 2015 Claudio Pastorini
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.