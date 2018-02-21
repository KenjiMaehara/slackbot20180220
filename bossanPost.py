# -*- coding: utf-8 -*-

from slacker import Slacker
import slackbot_settings
from .plugins.my_mention import *

if __name__ == '__main__':
    slack = Slacker(slackbot_settings.API_TOKEN)
    slack.chat.post_message('general','こんにちわー')
