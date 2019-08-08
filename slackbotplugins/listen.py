from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

import os
import sys
import re
import datetime
import time

from db.bot_dictionary import BotDictionary

import slackbot_settings

@listen_to(r'\A辞書登録')
def register_opendb(message):
    try:
        texts = re.split(r'\s', message.body['text'], 2)
        message.send(f"{texts[1]}を辞書登録するよ")

        bot_dict = BotDictionary()
        res = bot_dict.insert_word(texts[1], texts[2])
        bot_dict.release()

        message.reply(res)   # メンション
    except:
        message.reply("なんかエラー出たわ")

@listen_to(r'\Aおしえて.* .+')
def get_opendb(message):
    texts = message.body['text'].split(' ')

    bot_dict = BotDictionary()
    res = bot_dict.get_word(texts[1])
    bot_dict.release()

    lfcount = res.count('\n')
    if lfcount > 3:
        message.reply(f"{texts[1]}は・・・", in_thread=True)
        message.reply(res, in_thread=True)
    else:
        message.send(f"{texts[1]}は・・・")
        message.send(res)

@listen_to('辞書リスト')
def get_list(message):
    bot_dict = BotDictionary()
    res = bot_dict.get_list()
    bot_dict.release()
    message.send(res)

