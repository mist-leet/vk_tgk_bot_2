from vk_api.longpoll import VkLongPoll, VkEventType

import requests
import vk_api
from Bot import Bot
from private import private_key


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

my_peer = '119568994'
bot = Bot(vk, my_peer)

bot.send()
for event in longpoll.listen():

    #if once == 0:
    #    once -= 1
    #    bot.send()
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            bot.send(event.text)
