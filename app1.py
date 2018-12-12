# -*- coding: UTF-8 -*-


from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# custom storage
session={}
did = 0

# Channel Access Token
line_bot_api = LineBotApi('NihKt9+egg2TErCu8+Ldnb1GNmDtaHXkzHlhgqJ3mhr2ecO5OVJoOFMkisyht5eWhq+9有S5ib8xPZL30psL+49ZLG/RIeXq2fOa7NvZma8d74nMsvKkC02p5kOq1xMMARxhGbS8kIDlouxhwCIcCAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('89ce7adaa644788a454a10324ee36ad3')

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

'''location = LocationSendMessage(
    title='National Cheng Kung University Hospital',
    address='Tainan',
    latitude=23.001673,
    longitude=120.220120
)
line_bot_api.reply_message(event.reply_token, message)'''

def medical(user,text):
    global session
    print(text)
    # try to retrieve session
    if user not in session:
        session[user]=1
    did = session[user]

    src=text
    Hello = ['Hello', '哈囉']
    End = ['Reset', "重新"]
    Confirm = ['有', '有喔', '有阿', '好', '好喔', '好阿', '可', '可以']
    Disable = ['沒有', '不']
    country = ['東京', '大阪', '曼谷', '首爾', '沖繩', '香港', '京都', '新加坡', '上海', '巴黎']
    location = LocationSendMessage(
    title='National Cheng Kung University Hospital',
    address='Tainan',
    latitude=23.001673,
    longitude=120.220120)
    if text in Hello:
        res = '您好，手環資料顯示您的體溫似乎比較高，請問您有咳嗽情形嗎？'
        did = 1
        
    if did==1:
        if text in Confirm:
            res = '請問您咳嗽有血痰嗎？'
            did = 2
        elif text in Disable:
            res ='請問您有肌肉痠痛情形嗎？'
            did = 3
    elif did==2:
        if text in Confirm:
            res = '建議您盡速至醫院急診就醫'
            did = 7
        elif text in Disable:
            res = '請問您有呼吸困難情形嗎？'
            did = 8
    elif did==3:
        if text in Confirm:
            res = '請問您有呼吸困難情形嗎？'
            did=8
        elif text in Disable:
            res = '請問您有喉嚨痛情形嗎？'
            did=4
    elif did==4:
        if text in Confirm:
            res = '請問您有呼吸困難情形嗎？'
            did = 8
        elif text in Disable:
            res = '請問您有流鼻水情形嗎？'
            did = 5
    elif did==5:
        if text in Confirm:
            res = '請問您有呼吸困難情形嗎？'
            did = 8
        elif text in Disable:
            res = '請問您有接觸流感病人嗎？'
            did = 6
    elif did==6:
        if text in Confirm:
            res = '請問您有呼吸困難情形嗎？'
            did =  8
        elif text in Disable:
            res = '請持續密切注意您的體溫變化，多休息多喝水，至公共場合時記得戴口罩，若有任何身體不適仍建議您至醫療院所就醫'
            did = 9
    elif did==7: # terminal
        res = ''
    elif did==8:
        if text in Confirm:
            res = '建議您盡速至醫院急診就醫'
            did = 7
        elif text in Disable:
            res = '請問最近這三個月有出國嗎？'
            did = 10
    elif did==9: # terminal
        res = ''           
    elif did==10:
        if text in Confirm:
            res = '請問去哪個國家？'
            did = 11
        elif text in Disable:
            res = '請問去年或今年有施打流感疫苗嗎？'
            did = 12 
    elif did==11: # if text in '國家'
        if text in country:
            res = '請問去年或今年有施打流感疫苗嗎？'
            did = 12
        else:
            res = ''        
    elif did==12:
        if text in Confirm:
            res = '請問有對藥物過敏嗎？'
            did = 13
        elif text in Disable:
            res = '請問有對藥物過敏嗎？'
            did = 13
        else:
            res = ''            
    elif did==13:
        if text in Confirm:
            res = '請問是否需要提供您附近醫療院所的資訊？'
            did = 14
        elif text in Disable:
            res = '請問是否需要提供您附近醫療院所的資訊？'
            did = 14
        else:
            res = ''            
    elif did==14:
        if text in Confirm:
            res = '請問您目前的位置？'
            did =  15 
        elif text in Disable:
            res = '請盡快至您熟悉方便的醫療院所就醫'
            did = 16
    elif did==15: # 不管輸入什麼都回復：'以下為您所在位置附近的醫療院所資訊，請盡快就醫'
        res = '以下為您所在位置附近的醫療院所資訊，請盡快就醫'
        did = 17         
    elif did==16: # terminal
        res = ''            
    elif did==17: # terminal
        res = ''         

    # save state to session
    session[user] = did

    return src, res, did

def highlight_printer(text,up=True,bot=True,highlight=True):
    if up and highlight:
        print("*"*30)
    print(text)
    if bot and highlight:
        print("*"*30)
    return text

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    uid = event.source.user_id
    src, res, did = medical(uid, event.message.text)
    highlight_printer("Received from: "+uid,bot=False)
    highlight_printer("Content: "+src,highlight=False)
    highlight_printer("In dialogue: "+str(did),highlight=False)
    highlight_printer("Respond: "+res,highlight=False)
    highlight_printer("Current user queue: "+str(len(session)),up=False)
    message = TextSendMessage(text="res")
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    highlight_printer("NCKU Medical Chatbot Started.")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
