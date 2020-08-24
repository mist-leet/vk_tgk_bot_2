from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id

from StateMachine import State, States
from Data import Data


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
        print('Type: {}, State: {}, args:{}'.format(self.state.getType(),self.state.getState(), args))