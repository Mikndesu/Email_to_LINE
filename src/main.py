from flask import Flask, request, abort
import os
from os.path import join, dirname
from dotenv import load_dotenv

from linebot import (
    LineBotApi, WebhookHandler
)

from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-LINE-SIGNATURES']

    body = request.get_data(as_text=True)
    app.logger.info("Request Body: " + body)

    try:
        handler.handle(body, signature)
    except: InvalidSignatureError
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_tpken,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = os.getenv("PORT")
    app.run(host="0.0.0.0", port=port)


