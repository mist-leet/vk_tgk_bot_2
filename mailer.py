import requests
from vk_api import vk_api

from Data import Data, Room
from Bot import Bot
from main import MyLongPoll
from private import private_key

MESSAGE_FILE = 'message.txt'


# targets = Data.getRooms()

rooms = Data.getRooms()

message = ''.join(open(MESSAGE_FILE).readlines())


session = requests.Session()
vk_session = vk_api.VkApi(token=private_key)

longpoll = MyLongPoll(vk_session)
vk = vk_session.get_api()

print('start mailing...')
bot = Bot(vk, 'mistleet')
for room in rooms:
    for name, link in room.room.items():
        if bot.send_message(link, message, name=name):
            print(name+ ' получил сообщение')
        else:
            print('error with user: ' + name + ' : ' + link)