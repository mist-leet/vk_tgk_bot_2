# coding=utf-8

import random

class Duty:

    def __init__(self, rooms, locations):
        self.rooms = rooms
        self.locations = locations
        self.duty = self.Create()

    def Create(self):
        #tmp_rooms = random.shuffle(self.rooms)[0:len(self.locations)]
        return dict(zip(self.locations, self.rooms[0:len(self.locations)]))

    def Clear(self):
        self.duty.clear()

    def Update(self, key, value):
        self.duty.update(key, value)
