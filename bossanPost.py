# -*- coding: utf-8 -*-

from slacker import Slacker
import slackbot_settings
from plugins import my_mention

if __name__ == '__main__':
    slack = Slacker(slackbot_settings.API_TOKEN)
    slack.chat.post_message('general','こんにちわー')
