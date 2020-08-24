import enum


class States(enum.Enum):
    Menu = 0
    RemindDuty = 1
    ShowDuty = 2
    ShowTasks = 3
    CloseTask = 4
    MakeTask = 5


class State:
    STATE_TYPES = {
        'Menu': 0,
        'RemindDuty': 1,
        'ShowDuty': 2,
        'ShowTasks': 3,
        'CloseTask': 4,
        'MakeTask': 5,
    }
    STATE = {
        States.Menu: {'Start': 0},
        'ShowD': {
            'Start': 0
        },
        States.RemindDuty: {
            'Start': 0,
            'ChoiceLocation': 1,
        },
        States.ShowTasks: {
            'Start': 0,
        },
        States.CloseTask: {
            'Start': 0
        },
        States.MakeTask: {
            'Start': 0,
            'WriteTask': 1
        }
    }

    def getType(self):
        return self.currentType

    def getState(self):
        return self.currentState

    def __init__(self):
        self.currentState = 0
        self.currentType = States.Menu

    def next(self, arg=None):
        if arg is None:
            if self.currentState + 1 in State.STATE[self.currentType].values():
                self.currentState += 1
            else:
                self.currentType = States.Menu
                self.currentState = 0
        else:
            self.currentState = 0
            self.currentType = arg
