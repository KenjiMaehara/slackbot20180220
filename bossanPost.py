# -*- coding: utf-8 -*-

from slacker import Slacker
import slackbot_settings
from plugins import my_mention

if __name__ == '__main__':
    slack = Slacker(slackbot_settings.API_TOKEN)
    slack.chat.post_message('general','こんにちわー')
    if my_mention.securityMode == 0:
        slack.chat.post_message('general','現在、防犯解除中です')
    else:
        slack.chat.post_message('general','現在、防犯開始中です')
