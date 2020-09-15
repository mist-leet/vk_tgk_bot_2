# coding=utf-8
import enum


class States(enum.Enum):
    Menu = 0
    RemindDuty = 1
    ShowDuty = 2
    UpdateDuty = 3
    #ShowTasks = 3
    #CloseTask = 4
    #MakeTask = 5


class State:
    STATE_TYPES = {
        'Menu': 0,
        'RemindDuty': 1,
        'ShowDuty': 2,
        'UpdateDuty': 3,
    }

    STATE_TYPES_NAMES = {
        # 'Начать': 0,
        'Напомнить дежурным': 1,
        'Показать расписание': 2,
        'Обновить расписание' : 3
    }

    STATE = {
        States.Menu: {'Start': 0},

        States.RemindDuty: {
            'Start': 0,
            'ChoiceLocation': 1,
            'Comment' : 2,
            'End': 3
        },

        States.ShowDuty: {
            'Start': 0,
            'End': 1
        },

        States.UpdateDuty: {
            'Start': 0,
            'SelectLocation' : 1,
            'SelectRoom' : 2,
            'Verify' : 3,
            'End' : 4
        },

    }

    def getType(self):
        return self.currentType

    def getState(self):
        return self.currentState

    def setStartState(self):
        self.currentType = States.Menu
        self.currentState = 0

    def __init__(self):
        self.currentState = 0
        self.currentType = States.Menu

    def isOnLastState(self):
        if not self.currentState + 1 in list(State.STATE[self.currentType].values()):
            return True
        else:
            return False

    def next(self, arg=None):
        if arg in list(self.STATE_TYPES_NAMES.keys()):
            self.currentType = States(self.STATE_TYPES_NAMES[arg])

            if self.currentState + 1 in list(State.STATE[self.currentType].values()):
                self.currentState += 1
            else:
                self.currentType = States.Menu
                self.currentState = 0
        elif self.currentState + 1 in list(State.STATE[self.currentType].values()):
            self.currentState += 1
        else:
            self.currentState = 0
            self.currentType = States.Menu