import random

class Duty:

    def __init__(self, rooms, locations):
        self.rooms = rooms
        self.locations = locations
        self.duty = self.Create()

    def Create(self):

        tmp_rooms = random.shuffle(self.rooms)
        duty = dict(zip(tmp_rooms, self.locations[0:len(self.rooms)]))