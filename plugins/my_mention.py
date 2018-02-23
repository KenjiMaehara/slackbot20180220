# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

from slacker import Slacker
import slackbot_settings
import time
import threading
# GPIOを制御するライブラリ
import wiringpi2 as w

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
@respond_to('メンション')
def mention_func(message):
    message.reply('私にメンションと言ってどうするのだ') # メンション

@listen_to('リッスン')
def listen_func(message):
    message.send('誰かがリッスンと投稿したようだ')      # ただの投稿
    message.reply('君だね？')                           # メンション

@respond_to('かっこいい')
def cool_func(message):
    message.reply('ありがとう。スタンプ押しとくね')     # メンション
    message.react('+1')     # リアクション

count = 0

@default_reply()
def default_func(message):
    global count        # 外で定義した変数の値を変えられるようにする
    count += 1
    message.reply('%d 回目のデフォルトの返事です' % count)  # メンション


@respond_to('警備状況')
@respond_to('警備の状況')
@respond_to('防犯状況')
@respond_to('防犯の状況')
@respond_to('状況')
def mention_func(message):
    if timeCountSecurityOn > -1:
        message.reply('現在警備中です') # メンション
    else:
        message.reply('現在警備解除中です') # メンション

@respond_to('警備を開始')
@respond_to('警備開始')
@respond_to('防犯を開始')
@respond_to('防犯開始')
def mention_func(message):
    message.reply('警備を開始します') # メンション
    #message.send('警備を開始します')
    slack = Slacker(slackbot_settings.API_TOKEN)
    slack.chat.post_message('general','防犯を開始します。')
    global timeCountSecurityOn
    timeCountSecurityOn = 0

@respond_to('警備を解除')
@respond_to('警備解除')
@respond_to('防犯を解除')
@respond_to('防犯解除')
def mention_func(message):
    message.reply('警備を解除します') # メンション
    slack = Slacker(slackbot_settings.API_TOKEN)
    slack.chat.post_message('general','防犯を解除します。')
    global timeCountSecurityOn
    timeCountSecurityOn = -1

@respond_to('使い方')
def mention_func(message):
    message.reply('”警備開始して”')
    message.reply('”警備解除して”')
    message.reply('”状況を教えて”')
    message.reply('このように話しかけてみてください')



timeCountSecurityOn = -1
sensorCheck = 0
sensorCheckOld = 0

def hello():
    global timeCountSecurityOn

    if timeCountSecurityOn > -1:
            timeCountSecurityOn+=1
            if timeCountSecurityOn > 300:
                slack = Slacker(slackbot_settings.API_TOKEN)
                slack.chat.post_message('general','現在警備中であります　特に異常なし　(`・ω・́)ゝ　')
                timeCountSecurityOn = 0
    else:
        timeCountSecurityOn = -1


    buttonPin = 4
    # GPIO初期化
    w.wiringPiSetupGpio()
    # GPIOを出力モード（1）に設定
    w.pinMode(buttonPin,0)
    # 端子に何も接続されていない場合の状態を設定
    # 3.3Vの場合には「2」（プルアップ）
    # 0Vの場合は「1」と設定する（プルダウン）
    w.pullUpDnControl(buttonPin,2)

    if( w.digitalRead(buttonPin) == 0 ):
        print ("Switch ON")
        sensorCheck = 0
    else:
        print ("Switch OFF ACTIVE ACTIVE")
        sensorCheck = 1

    if timeCountSecurityOn > -1 and sensorCheckOld not sensorCheck and sensorCheck == 1:
        slack = Slacker(slackbot_settings.API_TOKEN)
        slack.chat.post_message('general','センサー検知発生')

    sensorCheckOld = sensorCheck


    print("現在のスレッドの数: " + str(threading.activeCount()))
    print("[%s] helohelo!!" % threading.currentThread().getName())
    t=threading.Timer(1,hello)
    t.start()
