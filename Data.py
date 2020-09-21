# coding=utf-8
from Duty import Duty


class Data:
    moderators = [
        'enter moderators id_s'
    ]

    @staticmethod
    def getRooms():
        rooms = [
            Room('Красная комната',
                 [
                     'Кристина Ботнарь', '152220652',
                     'Татьяна Дамрина', 'tdamrina',
                 ]),
            Room('ГЕСТ 8',
                 [
                     'Борис', 'shtormnamore',
                 ]),
            Room('Голубая лагуна',
                 [
                     'Илья', 'mistleet',
                     'Арсен', 'emshv_arsn',
                 ]),
            Room('Гнездышко',
                 [
                     'Серафима', 'avolzok_se',
                     'Женя', 'evgenysergeevich90',
                 ]),
            Room('Нора',
                 [
                     'Жанна', '529306038',
                 ]),
            Room('ГЕСТ 4',
                 [
                     'Арзу', '198886807',
                     'Мира', 'mirokkg',
                     'Наташа', 'natalie_noymann',
                 ]),
            Room('Белая комната',
                 [
                     'Софа', '133687981',
                     'Настя', 'ebeniesexom',
                 ]),
            Room('Аня & Юля',
                 [
                     'Юля', '16144866',
                     'Аня', 'n_mori_an',
                 ]),
            Room('Настя & Маша',
                 [
                     'Настя Маркова', 'mindalllka',
                     'Маша', 'mashasergeeva98',
                 ]),
            Room('Алексеи',
                 [
                     'Алексей Мазырин', 'lampowl',
                     'Алексей Бахмет', '109997707',
                 ]),
            # Room('',
            #      [
            #          '', '',
            #          '', '',
            #      ]),
        ]
        for i in range(7):
            rooms.append(Room(
                'room # {}'.format(str(i)),
                [
                    '{}'.format(str(j)) * 10 for j in range(4)
                ])
            )
        return rooms

    @staticmethod
    def getLocations():
        return [
            'Красный ковер',
            'Раздельный сбор',
            'Кухня',
            'Ванная'
        ]

    @staticmethod
    def isModerator(id):
        if id in Data.moderators:
            return True
        else:
            return False

    @staticmethod
    def getTmpDuty():
        rooms = Data.getRooms()
        locations = Data.getLocations()

        return Duty([
            next(filter(lambda x: x.room_name == 'Настя & Маша', rooms)),
            next(filter(lambda x: x.room_name == 'Нора', rooms)),
            next(filter(lambda x: x.room_name == 'ГЕСТ 4', rooms)),
            next(filter(lambda x: x.room_name == 'Белая комната', rooms)),
        ],
            Data.getLocations()
        )


class Room:

    def __init__(self, room_name: str, residents: list):
        self.rooms_name = room_name

        names = [residents[i] for i in range(0, len(residents), 2)]
        links = [residents[i] for i in range(1, len(residents), 2)]

        self.room = dict(zip(names, links))
