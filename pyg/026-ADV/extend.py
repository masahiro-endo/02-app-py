
from collections import OrderedDict, deque
import typing
import pygame
from pygame.locals import *
import global_value as g
from enum import IntEnum, auto
import json
from typing import Any, Dict
from enum import IntEnum
from UI import UIfonts




class ScriptPerser():

    def __init__(self, **kwargs: Dict[str, Any]):
        scenario: Any = kwargs.get('scenario') if kwargs.get('scenario') != None else 'scenario1'
        self.speed: Any = kwargs.get('speed') if kwargs.get('speed') != None else 1

        self.init_scenario(scenario)
        for self.currPage in self.json_dict: break
        self.init_page(self.currPage)

    def init_scenario(self, filename: str):
        self.json_dict = self.read_json(filename)

    def read_json(self, filename: str) -> typing.Any:
        f = open(f'./assets/events/{filename}.json', 'r', encoding="utf-8")
        json_dict = json.load(f, object_pairs_hook=OrderedDict)

        if __debug__:
            for x in json_dict:
                print(f'{x}:{json_dict[x]}')

        return json_dict

    def init_page(self, currPage: str):
        self.text = self.json_dict[currPage]["text"]
        self.next = self.json_dict[currPage]["next"]
        self.speed = int(self.json_dict[currPage]["speed"])




class ScriptWindow():

    class LIMIT(IntEnum):
        CHAR_COUNT = 10
        LINE_COUNT = 4
        PAGE_COUNT = 999

    class SHOW(IntEnum):
        FADEIN = auto()
        FADEOUT = auto()

    _arg: Dict[str, Any] = {
            'func': 'clear',
            'text': '',
            'speed': 1,
            'effect': None,
    }

    def __init__(self, rect: pygame.Rect, **kwargs: Dict[str, Any]):
        func: Any = kwargs.get('func') if kwargs.get('func') != None else 'clear'
        txt: Any = kwargs.get('text') if kwargs.get('text') != None else ''
        self.speed: Any = kwargs.get('speed') if kwargs.get('speed') != None else 1
        self.effect: Any = kwargs.get('effect')
        self.rect = rect
        self.pause = 0

        self.init_trans()

        self.surfs: deque[pygame.Surface] = deque()
        if func == 'clear':
            self.init_buf(txt)
        else:
            self.append_buf(txt)

    def init_buf(self, txt: str):
        self.text = txt
        self.buf = ""
        self.ptr = 0

        self.surfs.clear()
        self.surfs.append(g.UIfont.render(self.buf))

    def append_buf(self, txt: str):
        self.text += txt

    def init_trans(self):
        self.trans = 250
        if self.effect is None:
            pass
        elif self.effect == self.SHOW.FADEIN:
            self.trans = 0
        elif self.effect == self.SHOW.FADEOUT:
            pass

    def update_trans(self):
        if self.effect is None:
            pass
        elif self.effect == self.SHOW.FADEIN:
            self.trans += 1
            self.trans = self.trans if self.trans < 250 else 250
        elif self.effect == self.SHOW.FADEOUT:
            self.trans -= 1
            self.trans = self.trans if self.trans > 0 else 0

    def update(self):
        self.pause += 1        
        self.pause %= self.speed
        if not self.pause == 0:
            return

        self.update_trans()

        if len(self.buf) >= self.LIMIT.CHAR_COUNT:
            self.buf = ""
            self.surfs.append(g.UIfont.render(self.buf))

        if len(self.surfs) >= self.LIMIT.LINE_COUNT:
            self.surfs.popleft()

        if len(self.buf) >= len(self.text) or self.ptr >= len(self.text):
            return

        self.buf += self.text[self.ptr]
        self.surfs[-1] = g.UIfont.render(self.buf) 
        self.ptr += 1

    def draw(self, screen: pygame.Surface):
        max: int = len(self.surfs)
        min: int = max - self.LIMIT.LINE_COUNT if max - self.LIMIT.LINE_COUNT > 0 else 0
        for i in range(min, max):
            dx: int = self.rect.left
            dy: int = self.rect.top + (i * g.UIfont.HEIGHT + (i * 5))
            self.surfs[i].set_alpha(self.trans)
            screen.blit(self.surfs[i], (dx, dy))
        
    def handler(self, event: pygame.event):
        if event.type == KEYUP:
            if event.key == K_RETURN:
                pass



