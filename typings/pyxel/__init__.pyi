"""
This type stub file was generated by pyright.
"""

import inspect
import os
import signal
import sys
import traceback
from collections import MutableSequence
from ctypes import CFUNCTYPE, c_char_p, c_int32, cast, create_string_buffer
from typing import Any, Callable, Dict, List, Optional
from . import core

if sys.version_info < (3, 6, 8):
    ...
VERSION: str = ...
COLOR_COUNT: int = ...
COLOR_BLACK: int = ...
COLOR_NAVY: int = ...
COLOR_PURPLE: int = ...
COLOR_GREEN: int = ...
COLOR_BROWN: int = ...
COLOR_DARKBLUE: int = ...
COLOR_LIGHTBLUE: int = ...
COLOR_WHITE: int = ...
COLOR_RED: int = ...
COLOR_ORANGE: int = ...
COLOR_YELLOW: int = ...
COLOR_LIME: int = ...
COLOR_CYAN: int = ...
COLOR_GRAY: int = ...
COLOR_PINK: int = ...
COLOR_PEACH: int = ...
FONT_WIDTH: int = ...
FONT_HEIGHT: int = ...
USER_IMAGE_BANK_COUNT: int = ...
IMAGE_BANK_FOR_SYSTEM: int = ...
TILEMAP_BANK_COUNT: int = ...
USER_SOUND_BANK_COUNT: int = ...
SOUND_BANK_FOR_SYSTEM: int = ...
MUSIC_BANK_COUNT: int = ...
MUSIC_CHANNEL_COUNT: int = ...
RESOURCE_FILE_EXTENSION: str = ...
DEFAULT_CAPTION: str = ...
DEFAULT_SCALE: int = ...
DEFAULT_PALETTE: List[int] = ...
DEFAULT_FPS: int = ...
DEFAULT_QUIT_KEY: int = ...
KEY_SPACE: int = ...
KEY_QUOTE: int = ...
KEY_COMMA: int = ...
KEY_MINUS: int = ...
KEY_PERIOD: int = ...
KEY_SLASH: int = ...
KEY_0: int = ...
KEY_1: int = ...
KEY_2: int = ...
KEY_3: int = ...
KEY_4: int = ...
KEY_5: int = ...
KEY_6: int = ...
KEY_7: int = ...
KEY_8: int = ...
KEY_9: int = ...
KEY_SEMICOLON: int = ...
KEY_EQUAL: int = ...
KEY_A: int = ...
KEY_B: int = ...
KEY_C: int = ...
KEY_D: int = ...
KEY_E: int = ...
KEY_F: int = ...
KEY_G: int = ...
KEY_H: int = ...
KEY_I: int = ...
KEY_J: int = ...
KEY_K: int = ...
KEY_L: int = ...
KEY_M: int = ...
KEY_N: int = ...
KEY_O: int = ...
KEY_P: int = ...
KEY_Q: int = ...
KEY_R: int = ...
KEY_S: int = ...
KEY_T: int = ...
KEY_U: int = ...
KEY_V: int = ...
KEY_W: int = ...
KEY_X: int = ...
KEY_Y: int = ...
KEY_Z: int = ...
KEY_LEFT_BRACKET: int = ...
KEY_BACKSLASH: int = ...
KEY_RIGHT_BRACKET: int = ...
KEY_BACKQUOTE: int = ...
KEY_ESCAPE: int = ...
KEY_ENTER: int = ...
KEY_TAB: int = ...
KEY_BACKSPACE: int = ...
KEY_INSERT: int = ...
KEY_DELETE: int = ...
KEY_RIGHT: int = ...
KEY_LEFT: int = ...
KEY_DOWN: int = ...
KEY_UP: int = ...
KEY_PAGE_UP: int = ...
KEY_PAGE_DOWN: int = ...
KEY_HOME: int = ...
KEY_END: int = ...
KEY_CAPS_LOCK: int = ...
KEY_SCROLL_LOCK: int = ...
KEY_NUM_LOCK: int = ...
KEY_PRINT_SCREEN: int = ...
KEY_PAUSE: int = ...
KEY_F1: int = ...
KEY_F2: int = ...
KEY_F3: int = ...
KEY_F4: int = ...
KEY_F5: int = ...
KEY_F6: int = ...
KEY_F7: int = ...
KEY_F8: int = ...
KEY_F9: int = ...
KEY_F10: int = ...
KEY_F11: int = ...
KEY_F12: int = ...
KEY_KP_0: int = ...
KEY_KP_1: int = ...
KEY_KP_2: int = ...
KEY_KP_3: int = ...
KEY_KP_4: int = ...
KEY_KP_5: int = ...
KEY_KP_6: int = ...
KEY_KP_7: int = ...
KEY_KP_8: int = ...
KEY_KP_9: int = ...
KEY_KP_DECIMAL: int = ...
KEY_KP_DIVIDE: int = ...
KEY_KP_MULTIPLY: int = ...
KEY_KP_SUBTRACT: int = ...
KEY_KP_ADD: int = ...
KEY_KP_ENTER: int = ...
KEY_KP_EQUAL: int = ...
KEY_LEFT_SHIFT: int = ...
KEY_LEFT_CONTROL: int = ...
KEY_LEFT_ALT: int = ...
KEY_LEFT_SUPER: int = ...
KEY_RIGHT_SHIFT: int = ...
KEY_RIGHT_CONTROL: int = ...
KEY_RIGHT_ALT: int = ...
KEY_RIGHT_SUPER: int = ...
KEY_MENU: int = ...
KEY_SHIFT: int = ...
KEY_CONTROL: int = ...
KEY_ALT: int = ...
KEY_SUPER: int = ...
KEY_NONE: int = ...
MOUSE_LEFT_BUTTON: int = ...
MOUSE_MIDDLE_BUTTON: int = ...
MOUSE_RIGHT_BUTTON: int = ...
GAMEPAD_1_A: int = ...
GAMEPAD_1_B: int = ...
GAMEPAD_1_X: int = ...
GAMEPAD_1_Y: int = ...
GAMEPAD_1_LEFT_SHOULDER: int = ...
GAMEPAD_1_RIGHT_SHOULDER: int = ...
GAMEPAD_1_SELECT: int = ...
GAMEPAD_1_START: int = ...
GAMEPAD_1_UP: int = ...
GAMEPAD_1_RIGHT: int = ...
GAMEPAD_1_DOWN: int = ...
GAMEPAD_1_LEFT: int = ...
GAMEPAD_2_A: int = ...
GAMEPAD_2_B: int = ...
GAMEPAD_2_X: int = ...
GAMEPAD_2_Y: int = ...
GAMEPAD_2_LEFT_SHOULDER: int = ...
GAMEPAD_2_RIGHT_SHOULDER: int = ...
GAMEPAD_2_SELECT: int = ...
GAMEPAD_2_START: int = ...
GAMEPAD_2_UP: int = ...
GAMEPAD_2_RIGHT: int = ...
GAMEPAD_2_DOWN: int = ...
GAMEPAD_2_LEFT: int = ...
class Image:
    def __init__(self, obj: Any) -> None:
        ...
    
    @property
    def width(self) -> int:
        ...
    
    @property
    def height(self) -> int:
        ...
    
    @property
    def data(self) -> Any:
        ...
    
    def get(self, x: int, y: int) -> int:
        ...
    
    def set(self, x: int, y: int, data: Any) -> None:
        ...
    
    def load(self, x: int, y: int, filename: str) -> None:
        ...
    
    def copy(self, x: int, y: int, img: int, u: int, v: int, w: int, h: int) -> None:
        ...
    


class Tilemap:
    def __init__(self, obj: Any) -> None:
        ...
    
    @property
    def width(self) -> int:
        ...
    
    @property
    def height(self) -> int:
        ...
    
    @property
    def data(self) -> Any:
        ...
    
    @property
    def refimg(self) -> int:
        ...
    
    @refimg.setter
    def refimg(self, img: int) -> int:
        ...
    
    def get(self, x: int, y: int) -> int:
        ...
    
    def set(self, x: int, y: int, data: Any) -> None:
        ...
    
    def copy(self, x: int, y: int, tm: int, u: int, v: int, w: int, h: int) -> None:
        ...
    


class Sound:
    def __init__(self, c_obj: Any) -> None:
        ...
    
    @property
    def note(self) -> List[int]:
        ...
    
    @property
    def tone(self) -> List[int]:
        ...
    
    @property
    def volume(self) -> List[int]:
        ...
    
    @property
    def effect(self) -> List[int]:
        ...
    
    @property
    def speed(self) -> int:
        ...
    
    @speed.setter
    def speed(self, speed: int) -> None:
        ...
    
    def set(self, note: str, tone: str, volume: str, effect: str, speed: int) -> None:
        ...
    
    def set_note(self, note: str) -> None:
        ...
    
    def set_tone(self, tone: str) -> None:
        ...
    
    def set_volume(self, volume: str) -> None:
        ...
    
    def set_effect(self, effect: str) -> None:
        ...
    


class Music:
    def __init__(self, c_obj: Any) -> None:
        ...
    
    @property
    def ch0(self) -> List[int]:
        ...
    
    @property
    def ch1(self) -> List[int]:
        ...
    
    @property
    def ch2(self) -> List[int]:
        ...
    
    @property
    def ch3(self) -> List[int]:
        ...
    
    def set(self, ch0: List[int], ch1: List[int], ch2: List[int], ch3: List[int]) -> None:
        ...
    
    def set_ch0(self, ch0: List[int]) -> None:
        ...
    
    def set_ch1(self, ch1: List[int]) -> None:
        ...
    
    def set_ch2(self, ch2: List[int]) -> None:
        ...
    
    def set_ch3(self, ch3: List[int]) -> None:
        ...
    


width: int = ...
height: int = ...
frame_count: int = ...
_drop_file: str = ...
@property
def width(mod):
    ...

@property
def height(mod):
    ...

@property
def frame_count(mod):
    ...

def init(width: int, height: int, *, caption: str = ..., scale: int = ..., palette: List[int] = ..., fps: int = ..., quit_key: int = ..., fullscreen: bool = ...) -> None:
    ...

def run(update: Callable[[], None], draw: Callable[[], None]) -> None:
    ...

def quit() -> None:
    ...

def flip() -> None:
    ...

def show() -> None:
    ...

def save(filename: str) -> None:
    ...

def load(filename: str, image: bool = ..., tilemap: bool = ..., sound: bool = ..., music: bool = ...) -> None:
    ...

mouse_x: int = ...
mouse_y: int = ...
mouse_wheel: int = ...
@property
def mouse_x(mod):
    ...

@property
def mouse_y(mod):
    ...

@property
def mouse_wheel(mod):
    ...

def btn(key: int) -> bool:
    ...

def btnp(key: int, hold: int = ..., period: int = ...) -> bool:
    ...

def btnr(key: int) -> bool:
    ...

def mouse(visible: bool) -> None:
    ...

_image_bank: Dict[int, Image] = ...
_tilemap_bank: Dict[int, Tilemap] = ...
def image(img: int, *, system: bool = ...) -> Image:
    ...

def tilemap(tm: int) -> Tilemap:
    ...

def clip(x: Optional[int] = ..., y: Optional[int] = ..., w: Optional[int] = ..., h: Optional[int] = ...) -> None:
    ...

def pal(col1: Optional[int] = ..., col2: Optional[int] = ...) -> None:
    ...

def cls(col: int) -> None:
    ...

def pget(x: int, y: int) -> int:
    ...

def pset(x: int, y: int, col: int) -> None:
    ...

def line(x1: int, y1: int, x2: int, y2: int, col: int) -> None:
    ...

def rect(x: int, y: int, w: int, h: int, col: int) -> None:
    ...

def rectb(x: int, y: int, w: int, h: int, col: int) -> None:
    ...

def circ(x: int, y: int, r: int, col: int) -> None:
    ...

def circb(x: int, y: int, r: int, col: int) -> None:
    ...

def tri(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, col: int) -> None:
    ...

def trib(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, col: int) -> None:
    ...

def blt(x: int, y: int, img: int, u: int, v: int, w: int, h: int, colkey: int = ...) -> None:
    ...

def bltm(x: int, y: int, tm: int, u: int, v: int, w: int, h: int, colkey: int = ...) -> None:
    ...

def text(x: int, y: int, s: str, col: int) -> None:
    ...

_sound_bank: Dict[int, Sound] = ...
_music_bank: Dict[int, Music] = ...
def sound(snd: int, *, system: bool = ...) -> Sound:
    ...

def music(msc: int) -> Music:
    ...

def play_pos(ch: int) -> int:
    ...

def play(ch: int, snd: Any, *, loop: bool = ...) -> None:
    ...

def playm(msc: int, *, loop: bool = ...) -> None:
    ...

def stop(ch: int = ...) -> None:
    ...

class _CListInterface(MutableSequence):
    def __init__(self, c_obj, data_getter, length_getter, length_setter) -> None:
        ...
    
    def __getitem__(self, ii):
        ...
    
    def __setitem__(self, ii, val): # -> None:
        ...
    
    def __delitem__(self, ii): # -> None:
        ...
    
    def __len__(self):
        ...
    
    def insert(self, ii, val): # -> None:
        ...
    


class Module:
    ...


module = ...
