import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("zN5Iy7Il6/sI8+F23sdopzWaWW/+PHsEGci9seuvObt0dB49EF8p7/3q3legaZ+gAqSldhMzdd2tLjeot4/9VzEJ+UghJU9Wspjx09PMRobhcPskg1jg6KhOCl6own1Ke4K4kX078ZNrIQWhUjKtZwdB04t89/1O/w1cDnyilFU="))
handler = WebhookHandler(os.environ.get("13c23864d56dc3b5970a0bcc0d9da1a2"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text

    # Send To Line
    reply = TextSendMessage(text=f"{get_message}")
    line_bot_api.reply_message(event.reply_token, reply)
