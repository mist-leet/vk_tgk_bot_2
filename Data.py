class Data:

    moderators = [
        'enter moderators id_s'
    ]

    @staticmethod
    def getRooms():
        rooms = [
            Room('White Room',
                 [
                     'Илья', 'mistleet',
                 ]),
            Room('Black Room',
                 [
                     'Федя', '614323093',
                 ]),
            Room('Red Room',
                 [
                     'Коля', '614323013',
                 ])
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
        return ['Location #' + str(i) for i in range(3)]

    @staticmethod
    def isModerator(id):
        if id in Data.moderators:
            return True
        else:
            return False

class Room:

    def __init__(self, room_name: str, residents: list):
        self.rooms_name = room_name

        names = [residents[i] for i in range(0, len(residents), 2)]
        links = [residents[i] for i in range(1, len(residents), 2)]

        self.room = dict(zip(names, links))