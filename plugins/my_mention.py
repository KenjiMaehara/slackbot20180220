# coding: utf-8

from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

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

securityMode = 0

@respond_to('警備状況')
def mention_func(message):
    if securityMode == 1:
        message.reply('現在警備中です') # メンション
    else:
        message.reply('現在警備解除中です') # メンション

@respond_to('警備を開始')
def mention_func(message):
    message.reply('警備を開始します') # メンション
    global securityMode
    securityMode = 1

@respond_to('警備を解除')
def mention_func(message):
    message.reply('警備を解除します') # メンション
    global securityMode
    securityMode = 0
