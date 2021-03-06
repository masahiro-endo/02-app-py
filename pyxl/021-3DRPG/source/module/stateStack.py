# -*- coding: utf-8 -*-
from typing import List

from module.baseState import BaseState
from module.battleStates.stateBattle import StateBattle
from module.constant.state import State
from module.facilityStates.stateArmorShop import StateArmorShop
from module.facilityStates.stateBarbar import StateBarbar
from module.facilityStates.stateDrugs import StateDrugs
from module.facilityStates.stateExaminations import StateExaminations
from module.facilityStates.stateHelmetShop import StateHelmetShop
from module.facilityStates.stateShieldShop import StateShieldShop
from module.facilityStates.stateSurgery import StateSurgery
from module.facilityStates.stateWeaponShop import StateWeaponShop
from module.fieldStates.baseFieldState import BaseFieldState
from module.fieldStates.stateBlacktower import StateBlackTower
from module.fieldStates.stateCemetery import StateCemetery
from module.fieldStates.stateCity import StateCity
from module.fieldStates.stateColordBlack import StateColordBlack
from module.fieldStates.stateColordBlue import StateColordBlue
from module.fieldStates.stateColordGreen import StateColordGreen
from module.fieldStates.stateColordPurple import StateColordPurple
from module.fieldStates.stateColordRed import StateColordRed
from module.fieldStates.stateColordWhite import StateColordWhite
from module.fieldStates.stateColordYellow import StateColordYellow
from module.fieldStates.stateDungeonB1 import StateDungeonB1
from module.fieldStates.stateDungeonB2 import StateDungeonB2
from module.fieldStates.stateDungeonB3 import StateDungeonB3
from module.fieldStates.stateDungeonB4 import StateDungeonB4
from module.fieldStates.stateDungeonB5 import StateDungeonB5
from module.fieldStates.stateWellB1 import StateWellB1
from module.fieldStates.stateWellB2 import StateWellB2
from module.fieldStates.stateWellB3 import StateWellB3
from module.fieldStates.stateWellB4 import StateWellB4
from module.systemStates.stateCamp import StateCamp
from module.systemStates.stateEnding import StateEnding
from module.systemStates.stateMakeChracter import StateMakeCharacter
from module.systemStates.stateTitle import StateTitle


class StateStack(object):
    '''
    State???????????????????????????????????????
    '''
    def __init__(self) -> None:
        '''
        ??????????????????
        '''
        # State???Enum???????????????State??????????????????
        self.__stateDict = {
            State.TITLE: StateTitle,
            State.MAKECHARACTER: StateMakeCharacter,
            State.CAMP: StateCamp,
            State.ENDING: StateEnding,
            State.CEMETERY: StateCemetery,
            State.CITY: StateCity,
            State.WELLB1: StateWellB1,
            State.WELLB2: StateWellB2,
            State.WELLB3: StateWellB3,
            State.WELLB4: StateWellB4,
            State.DUNGEONB1: StateDungeonB1,
            State.DUNGEONB2: StateDungeonB2,
            State.DUNGEONB3: StateDungeonB3,
            State.DUNGEONB4: StateDungeonB4,
            State.DUNGEONB5: StateDungeonB5,
            State.COLORD_YELLOW: StateColordYellow,
            State.COLORD_RED: StateColordRed,
            State.COLORD_PURPLE: StateColordPurple,
            State.COLORD_GREEN: StateColordGreen,
            State.COLORD_BLUE: StateColordBlue,
            State.COLORD_WHITE: StateColordWhite,
            State.COLORD_BLACK: StateColordBlack,
            State.BLACKTOWER: StateBlackTower,
            State.ARMORSHOP: StateArmorShop,
            State.BARBAR: StateBarbar,
            State.DRUGS: StateDrugs,
            State.EXAMINATIONS: StateExaminations,
            State.HELMETSHOP: StateHelmetShop,
            State.SHIELDSHOP: StateShieldShop,
            State.SURGERY: StateSurgery,
            State.WEAPONSHOP: StateWeaponShop,
            State.BATTLE: StateBattle,
        }

        # ??????????????????????????????
        self.clear()

        if __debug__:
            print("StateStack : Initialized.")

    def update(self) -> None:
        '''
        ?????????????????????State???update???????????????????????????
        '''
        if len(self.states) > 0 and self.states[0] != None:
            self.states[0].update()

    def draw(self) -> None:
        '''
        ?????????????????????State???render???????????????????????????
        '''
        if len(self.states) > 0 and self.states[0] != None:
            self.states[0].draw()

    def push(self, stateEnum: int, **kwargs) -> None:
        '''
        stateEnum??????????????????State????????????????????????????????????????????????????????????????????????????????????\n
        ???????????????State????????????buildState???????????????????????????????????????????????????????????????????????????onEnter?????????????????????????????????
        '''
        if __debug__:
            print(f"StateStack : push({stateEnum}).")

        # stateEnum??????????????????State?????????????????????????????????????????????
        state = self.getInstance(stateEnum, **kwargs)

        # ????????????????????????????????????
        self.states.insert(0, state)

        # ????????????????????????????????????????????????
        if state != None:
            # State?????????????????????????????????
            self.states[0].onEnter()

        if __debug__:
            print("StateStack : pushed -> " + str(state))

    def pop(self) -> None:
        '''
        ???????????????????????????State??????????????????\n
        ????????????Stack???onExit?????????????????????????????????
        '''
        if __debug__:
            print("StateStack : pop " + str(self.states[0]))

        # State?????????????????????????????????
        if self.states[0] != None:
            self.states[0].onExit()

        # ???????????????????????????State??????????????????
        self.states.pop(0)

        # ?????????????????????????????????State???onEnter???????????????????????????
        if self.states[0] != None:
            self.states[0].onEnter()

    def isField(self) -> bool:
        '''
        ?????????State???BaseField????????????????????????????????????
        '''
        if len(self.states) > 0 and isinstance(self.states[0], BaseFieldState):
            return True
        else:
            return False

    def clear(self) -> None:
        '''
        ??????????????????????????????stateName??????????????????state??????????????????????????????
        '''
        if __debug__:
            print("StateStack : clear")

        # ?????????????????????
        self.states = []

    def setStates(self, states) -> None:
        '''
        List????????????????????????????????????????????????????????????\n
        ????????????????????????????????????????????????
        '''
        self.states = states

    def getStates(self) -> List:
        '''
        state???????????????????????????
        '''
        return self.states

    def getInstance(self, stateEnum: int, **kwargs) -> BaseState:
        '''
        State???Enum??????????????????state????????????????????????
        '''
        # ?????????????????????
        state = None

        # ?????????None?????????None?????????
        if stateEnum == None:
            return None

        # state???????????????stateEnum???????????????state????????????????????????
        c = self.__stateDict.get(stateEnum, None)

        # state????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        if c != None:
            kwargs["stateStack"] = self
            state = c(**kwargs)

        return state


stateStack = StateStack()
