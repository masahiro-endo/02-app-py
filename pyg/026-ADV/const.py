# -*- coding: utf-8 -*-
from enum import IntEnum, auto
 
class Direction():
    '''
    方向のクラス
    '''
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Alignment(IntEnum):
    '''
    性格のEnumクラス
    '''

    GOOD = auto()
    NEUTRAL = auto()
    EVIL = auto()
