# coding=utf-8

from vk_api.longpoll import VkLongPoll, VkEventType

import requests
import vk_api

from Data import Data
from Duty import Duty
from Bot import Bot
from private import private_key
from User import User


class MyLongPoll(VkLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print(e)


session = requests.Session()
vk_session = vk_api.VkApi(token=private_key)

longpoll = MyLongPoll(vk_session)
vk = vk_session.get_api()


users = []
current_user = 0
current_duty = Data.getTmpDuty()

# bot.send()
print('starting...')
for event in longpoll.listen():

    current_user = User.isInUsers(event.peer_id, users)
    if current_user == 0:
        users.append(User(vk, '', event.peer_id))
        users[-1].updateDuty(current_duty)
        current_user = users[-1]

    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        current_user.Bot.send(event.text)