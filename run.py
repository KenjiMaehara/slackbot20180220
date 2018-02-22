# coding: utf-8

from slackbot.bot import Bot
from plugins import my_mention
import time
import threading

def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('start slackbot')
    t=threading.Thread(target=my_mention.hello)
    t.start()

    main()
