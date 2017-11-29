from flask import Flask, request, abort

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

line_bot_api = LineBotApi('b7HhK/E1hT5d5y9K9WirtFg0CM7kJRHr33FP3Nawh4w8uplHuebpyW6XMHpPm1PlX28cOViqx3O1+TgrduSmvlnopdYQ0/TaA/N1CRRPEavTa6TZ7DsLOasTlX6Ga8KdUx13i/qulCWzM0QLp1Mb8wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0ac66f9744963c85314748d1b12bc319')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()