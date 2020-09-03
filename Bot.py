from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id

from StateMachine import State, States
from Data import Data
from datetime import datetime, date, time


class Bot:
    def __init__(self, vk, peer):
        self.state = State()

        self.rooms = Data.getRooms()
        self.locations = Data.getLocations()

        self.peer = peer
        self.vk = vk

    @staticmethod
    def createKeyboard(keyboard, list):
        for element in list[0:-1]:
            keyboard.add_button(element)
            keyboard.add_line()
        keyboard.add_button(list[-1])
        return keyboard

    def getResponseData(self, args=None):
        keyboard = VkKeyboard()
        message = ''

        if self.state.getType() == States.Menu:
            keyboard = Bot.createKeyboard(keyboard, list(State.STATE_TYPES_NAMES.keys()))
            message = 'Выберите действие'

        elif self.state.getType() == States.RemindDuty:
            if self.state.getState() == 1:
                keyboard = Bot.createKeyboard(keyboard, self.locations)
                message = 'Выберите локацию'
            elif self.state.getState() == State.STATE[States.RemindDuty]['End']:
                # TODO: Add action
                keyboard = Bot.createKeyboard(keyboard, list(State.STATE_TYPES_NAMES.keys()))
                # TODO: Add message
                message = 'TODO'
                pass


        return {
            'keyboard': keyboard.get_keyboard(),
            'message': message
        }

    def send(self, args=None):
        self.state.next(args)
        self.logState(args)
        responseData = self.getResponseData(args)

        self.vk.messages.send(
            user_id=self.peer,
            random_id=get_random_id(),
            message=responseData['message'],
            keyboard=responseData['keyboard']
        )

    def logState(self, args=None):
        print('Type: {}, State: {}, args:{}'.format(self.state.getType(), self.state.getState(), args))


class Task:

    def __init__(self, task_text, task_author, task_perfomer):
        self.task_text = task_text
        self.task_author = task_author
        self.task_perfomer = task_perfomer
        self.task_create_date = datetime.now().__str__()
        self.task_close_date = 0

        self.task_comment = ''

    def Log(self):
        f = open('log.txt', 'a')
        f.write(
            '!' + '=' * 10 + '!' + '\n' +
            'Task: {}'.format(self.task_text) + '\n' +
            'To: {}'.format(self.task_perfomer) + '\n' +
            'From: {}'.format(self.task_author) + '\n' +
            'Create Date ' + self.task_create_date + '\n' +
            'Close Date' + datetime.now().__str__()
        )
