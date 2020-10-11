# coding=utf-8
import re

from vk_api.keyboard import VkKeyboard
from vk_api.utils import get_random_id
from vk_api.exceptions import ApiError

from Duty import Duty
from StateMachine import State, States
from Data import Data, Room
from datetime import datetime, date, time


class Bot:
    def __init__(self, vk, peer):
        self.state = State()

        self.rooms = Data.getRooms()
        self.locations = Data.getLocations()

        self.peer = str(peer)
        self.vk = vk

        self.duty: Duty = None
        self.new_duty: Duty = None
        self.old_duty: Duty = None

        # Remind Duty
        self.CURRENT_LOCATION = ''
        self.CURRENT_COMMENT = ''

        # Update Duty
        self.CURRENT_DUTY = []
        self.CURRENT_ROOMS = []
        self.CURRENT_LOCS = []

    def updateDuty(self, duty: Duty):
        self.duty = duty

    @staticmethod
    def createKeyboard(keyboard, list, elements_per_line=1):
        if elements_per_line == 1:
            for element in list[0:-1]:
                keyboard.add_button(element)
                keyboard.add_line()
            keyboard.add_button(list[-1])
            return keyboard
        elif elements_per_line == 2:
            i = 1

            is_odd = len(list) % 2 == 0

            end_point = - 2
            if not is_odd:
                end_point = -1

            for element in list[0:end_point]:
                keyboard.add_button(element)
                if i == 2:
                    keyboard.add_line()
                    i = 0
                i += 1

            if is_odd:
                keyboard.add_button(list[-2])
                keyboard.add_button(list[-1])
            else:
                keyboard.add_button(list[-1])

            return keyboard

    def getResponseData(self, args=None):
        keyboard = VkKeyboard()
        message = ''

        # Main Menu State
        if self.state.getType() == States.Menu:
            keyboard = self.__startMenuKeyboard()
            message = 'Выберите действие'

        # Main Remind Duty State
        elif self.state.getType() == States.RemindDuty:
            if self.state.getState() == State.STATE[States.RemindDuty]['ChoiceLocation']:
                keyboard = Bot.createKeyboard(keyboard, self.locations)
                message = 'Выберите локацию'

            if self.state.getState() == State.STATE[States.RemindDuty]['Comment']:
                keyboard = Bot.createKeyboard(keyboard, ['Отправить без комментария'])
                message = 'Введите комментарий и нажмите отправить'
                self.CURRENT_LOCATION = args

            elif self.state.getState() == State.STATE[States.RemindDuty]['End']:
                self.CURRENT_COMMENT = args
                keyboard = self.__startMenuKeyboard()
                message = self.__RemindDutyEndAction(self.CURRENT_LOCATION, self.CURRENT_COMMENT)

                self.CURRENT_LOCATION = ''
                self.CURRENT_COMMENT = ''

        # Main Show duty State
        elif self.state.getType() == States.ShowDuty:
            if self.state.getState() == State.STATE[States.ShowDuty]['End']:
                keyboard = self.__startMenuKeyboard()
                message = self.__ShowDutyEndAction()

        # Main Update Duty State
        elif self.state.getType() == States.UpdateDuty:
            if self.state.getState() == State.STATE[States.UpdateDuty]['SelectLocation']:
                if not Data.isModerator(self.peer):
                    self.state.setStartState()

                    keyboard = Bot.createKeyboard(keyboard, list(State.STATE_TYPES_NAMES.keys()))
                    message = 'У вас недостаточно прав доступа'
                    return {
                        'keyboard': keyboard.get_keyboard(),
                        'message': message
                    }

                if args in State.STATE_TYPES_NAMES.keys():
                    self.CURRENT_ROOMS = [room.rooms_name for room in self.rooms]
                    self.CURRENT_LOCS = self.locations
                else:
                    self.CURRENT_LOCS.remove(args)
                    self.CURRENT_DUTY.append(args)

                message = 'Выберите место: '
                keyboard = Bot.createKeyboard(keyboard, self.CURRENT_ROOMS, elements_per_line=2)

            if self.state.getState() == State.STATE[States.UpdateDuty]['SelectRoom']:
                self.CURRENT_ROOMS.remove(args)
                self.CURRENT_DUTY.append(args)
                print(self.CURRENT_ROOMS)
                message = 'Выберите дежурных: '
                keyboard = Bot.createKeyboard(keyboard, self.CURRENT_LOCS, elements_per_line=2)

                if len(self.CURRENT_LOCS) > 0:
                    self.state.currentState -= 2

        else:
            self.state.setStartState()
            return self.getResponseData(args)

        if self.state.isOnLastState():
            self.state.next()

        return {
            'keyboard': keyboard.get_keyboard(),
            'message': message
        }

    def send(self, args=None):
        self.state.next(args)
        self.logState(args)
        responseData = self.getResponseData(args)

        self.send_message(self.peer,
                          responseData['message'],
                          responseData['keyboard'])

    def logState(self, args=None):
        print('Type: {}\n State: {}\n args: {}\n peer: {}\n\n'.format(self.state.getType(), self.state.getState(), args,
                                                                      self.peer))

    def send_message(self, peer, message, keyboard=None, name=None):
        try:
            if keyboard is not None:
                if re.match(r'[\d]+', str(peer)) is not None:
                    self.vk.messages.send(
                        user_id=peer,
                        random_id=get_random_id(),
                        message=message,
                        keyboard=keyboard
                    )
                else:
                    self.vk.messages.send(
                        domain=peer,
                        random_id=get_random_id(),
                        message=message,
                        keyboard=keyboard
                    )
            else:
                if re.match('[\d]+', str(peer)) is not None:
                    self.vk.messages.send(
                        user_id=peer,
                        random_id=get_random_id(),
                        message=message,
                    )
                else:
                    self.vk.messages.send(
                        domain=peer,
                        random_id=get_random_id(),
                        message=message,
                    )
        except ApiError as e:
            print(e.args)
            print(e.values)
            self.send_message(self.peer, 'Кажется, резидент {} с id: {} еще не зарегистрировался.'
                                   ' \n Пожалуйста, перешлите это сообщение @mistleet'.format(str(name), str(peer)))
            return False
        return True

    def __startMenuKeyboard(self):
        keyboard = VkKeyboard()
        if not Data.isModerator(self.peer):
            keyboard = Bot.createKeyboard(keyboard, list(State.STATE_TYPES_NAMES.keys())[:-1])
        else:
            keyboard = Bot.createKeyboard(keyboard, list(State.STATE_TYPES_NAMES.keys()))
        return keyboard


    def __RemindDutyEndAction(self, location, comment):
        room: Room = self.duty.duty[location]

        message = ''

        for name, id in room.room.items():
            result = self.send_message(
                id,
                'Привет, {}, кажется, {} стоит уделить внимание!'.format(Helper.BuildPersonLink(id, name), location) +
                '\n' + Helper.BuildComment(comment),
                name=name
            )
            if result:
                message += '{} уведомлен(a) \n'.format(name)
            if message == '':
                message = '...'
        return message

    def __ShowDutyEndAction(self):
        message = ''

        for location, room in self.duty.duty.items():
            message += '{} ------ {}\n'.format(
                room.rooms_name, location
            )
        return message



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


class Helper:
    _url = 'https://cataas.com/cat/'

    @staticmethod
    def BuildComment(comment):
        if comment != '' and comment != 'Отправить без комментария':
            return 'Комментарий: ' + comment
        else:
            return ''

    @staticmethod
    def BuildPersonLink(id, name):
        if re.match('[\d]+', str(id)) is not None:
            return '[id{}|{}]'.format(id, name)
        else:
            return '@{}'.format(id)

    @staticmethod
    def getCat(tag='cute'):
        pass

