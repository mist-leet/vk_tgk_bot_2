# coding=utf-8

from Bot import Task, Bot
from Duty import Duty


class User:

    def __init__(self, vk, name, peer, tasks: Task = None):
        self.name = name
        self.peer = peer
        if tasks is not None:
            self.tasks = [t for t in tasks]
        self.Bot = Bot(vk, peer)

    def Push(self, task):
        self.tasks.append(task)

    def Pop(self, task):
        task.Log()
        self.tasks.remove(task)

    @staticmethod
    def isInUsers(peer_to_check, users):
        for user in users:
            if user.peer == peer_to_check:
                return user
        return 0

    def updateDuty(self, duty : Duty):
        self.Bot.updateDuty(duty)