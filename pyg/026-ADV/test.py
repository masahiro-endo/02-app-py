
from collections import OrderedDict, deque
import typing
import pygame
from pygame.locals import *
import global_value as g
from enum import IntEnum, auto
import json
from typing import Any, Dict
from enum import IntEnum



class AutoMessageWindow():

    class LIMIT(IntEnum):
        CHAR_COUNT = 10
        LINE_COUNT = 4
        PAGE_COUNT = 999

    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.pause = 0

        self.surfs: deque[pygame.Surface] = deque()

        self.buf = ""
        self.ptr = 0
        self.init_scenario("prologue")

    def init_scenario(self, filename: str):
        self.json_dict = self.read_json(filename)

        for self.currPage in self.json_dict: break
        self.init_page(self.currPage)

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

        self.surfs.clear()
        self.surfs.append(g.UIfont.render(self.buf))

        self.buf = ""
        self.ptr = 0

    def update(self):
        self.pause += 1        
        self.pause %= self.speed
        if not self.pause == 0:
            return

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
        for i in range(len(self.surfs)):
            dx: int = self.rect.left
            dy: int = self.rect.top + (i * g.UIfont.HEIGHT + (i * 5))
            screen.blit(self.surfs[i], (dx, dy))
        
    def handler(self, event: pygame.event):
        if event.type == KEYUP:
            if event.key == K_RETURN:
                pass
