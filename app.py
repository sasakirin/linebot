from flask import Flask, request, abort
import os
import sys
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

ACCESS_TOKEN= os.environ['ACCESS_TOKEN']
SECRET= os.environ['CHANNEL_SECRET']

# Channel Access Token
line_bot_api = LineBotApi(ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(SECRET)


@app.route("/")
def hello_world():
    return "hello world!"


# 監聽所有來自 /callback 的 Post Request
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

#傳送圖片給自己
image_message = ImageSendMessage(
original_content_url='https://cdn.vox-cdn.com/thumbor/Dy9wnuaxjdrgn11DCQc5f-8BEi8=/535x0:4171x2904/1200x800/filters:focal(1963x1079:2709x1825)/cdn.vox-cdn.com/uploads/chorus_image/image/59944749/usa_today_10872796.0.jpg', 
preview_image_url='https://cdn.vox-cdn.com/thumbor/Dy9wnuaxjdrgn11DCQc5f-8BEi8=/535x0:4171x2904/1200x800/filters:focal(1963x1079:2709x1825)/cdn.vox-cdn.com/uploads/chorus_image/image/59944749/usa_today_10872796.0.jpg'
) 
line_bot_api.push_message(to, image_message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
