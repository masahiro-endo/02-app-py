
from collections import OrderedDict, deque
import typing
import pygame
from pygame import rect
from pygame import draw
from pygame.locals import *
import codecs
import os
import random
import struct
import sys
import control
import global_value as g
from enum import IntEnum, auto
import math
import json
from typing import Any, List, Text, Tuple





class BaseWindow:

    EDGE_WIDTH = 2

    def __init__(self, rect: pygame.Rect):
        linewidth: int = 0

        self.surf = pygame.Surface( (rect.width, rect.height) )
        self.surf.fill(Color('black'))
        self.rect = self.surf.get_rect()

        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH * 2, -self.EDGE_WIDTH * 2)
        pygame.draw.rect(self.surf, Color('white'), self.rect, linewidth)
        pygame.draw.rect(self.surf, Color('black'), self.inner_rect, linewidth)
        self.rect = rect

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, (self.rect.left, self.rect.top) )



class LineCursor():

    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color
        self.theta = 0

    def update(self):
        self.theta += 10

    def draw(self, screen: pygame.Surface):
        self.theta %= 360 
        r = abs( 5 * math.sin(math.radians(self.theta)) )
        pygame.draw.polygon(screen, self.color, 
                ([self.x - r, self.y], [self.x + r, self.y], [self.x, self.y + 12]) )

class SelectCursor():

    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color
        self.theta = 0

    def update(self):
        self.theta += 10

    def draw(self, screen: pygame.Surface):
        self.theta %= 360 
        r = abs( 5 * math.sin(math.radians(self.theta)) )
        pygame.draw.polygon(screen, self.color, 
                ([self.x, self.y - r], [self.x + 12, self.y], [self.x, self.y + r]) )

class PageCursor():

    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color
        self.trans = 0

        self.surf = pygame.Surface( (10, 15), flags=pygame.SRCALPHA)
        self.surf.set_colorkey(Color('black'))
        self.surf.fill(Color('black'))
        self.rect = self.surf.get_rect()

        pygame.draw.polygon(self.surf, self.color, 
                ( [self.rect.x, self.rect.y], 
                  [self.rect.x + 10, self.rect.y], 
                  [self.rect.x + 10, self.rect.y + 10], 
                  [self.rect.x + 5, self.rect.y + 10], 
                  [self.rect.x + 5, self.rect.y + 15], 
                  [self.rect.x, self.rect.y + 15]) )
        pygame.draw.polygon(self.surf, self.color, 
                ( [self.rect.x + 7, self.rect.y + 12], 
                  [self.rect.x + 10, self.rect.y + 12], 
                  [self.rect.x + 7, self.rect.y + 15]) )

    def update(self):
        self.trans += 10

    def draw(self, screen: pygame.Surface):
        self.trans %= 250
        self.surf.set_alpha(self.trans)
        screen.blit(self.surf, (self.x, self.y) )


class FontCursor():

    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color
        self.trans = 0

        self.font: pygame.Surface = g.enfont.render(f"{'ＰＲＥＳＳ　ＥＮＴＥＲ　ＫＥＹ':<30}", False, Color('white') )
        self.rect: pygame.Rect = self.font.get_rect()
        self.surf = pygame.Surface( (self.rect.width, self.rect.height), flags=pygame.SRCALPHA)
        self.surf.set_colorkey(Color('black'))
        self.surf.fill(Color('black'))
        self.surf.blit(self.font, (self.rect.left, self.rect.top) )


    def update(self):
        self.trans += 10

    def draw(self, screen: pygame.Surface):
        self.trans %= 250
        self.surf.set_alpha(self.trans)
        screen.blit(self.surf, (self.x, self.y) )



class MessageWindow(BaseWindow):

    class CHARPTR(IntEnum):
        IS_ACTIVE = 0
        WAIT_LINE = auto()
        WAIT_PAGE = auto()
        ENDOFLINE = auto()
        WAIT_SELECT = auto()

    class LIMIT(IntEnum):
        CHAR_COUNT = 10
        LINE_COUNT = 4
        PAGE_COUNT = 999

    font_width: int
    font_height: int

    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)

        dx = rect.left + (rect.width // 2)
        dy = rect.top + (rect.height - 20)
        self.lineCursor = LineCursor(dx, dy, Color("white"))
        self.pageCursor = PageCursor(dx, dy, Color("white"))
        self.endCursor = FontCursor(dx, dy, Color("white"))
        self.selectCursor = SelectCursor(dx, dy, Color("white"))
        self.interval = 0

        self.json_dict = self.read_json()
        for self.currPage in self.json_dict: break
        self.text = self.json_dict[self.currPage]["text"]
        self.next = self.json_dict[self.currPage]["next"]
        self.speed = int(self.json_dict[self.currPage]["speed"])

        self.buf: str = ""
        self.ptr = 0

        self.surfs: deque[pygame.Surface] = deque()
        self.surfs.append(self.font_surface(self.buf))
        self.font_width, self.font_height = self.font_size()
        
        self.choices: deque[List[int, bool, pygame.Surface]] = deque()

        '''
        s = '123456789'
        v = [s[i: i+3] for i in range(0, len(s), 3)]
        # ['123', '456', '789']
        '''
        self.status = self.CHARPTR.IS_ACTIVE


    def read_json(self)->typing.Any:
        f = open('./assets/events/scenario1.json', 'r', encoding="utf-8")
        json_dict = json.load(f, object_pairs_hook=OrderedDict)

        if __debug__:
            for x in json_dict:
                print(f'{x}:{json_dict[x]}')

        return json_dict

    def font_surface(self, buf: str) -> pygame.Surface:
        return g.enfont.render(f"{buf}", False, Color("white"))

    def font_size(self) -> Tuple[int, int]:
        return g.enfont.size("あ")

    def prepare_nextpage(self):
        self.currPage = self.next
        self.text = self.json_dict[self.currPage]["text"]
        self.next = self.json_dict[self.currPage]["next"]
        self.speed = int(self.json_dict[self.currPage]["speed"])
        self.buf = ""

        self.ptr = 0
        self.status = self.CHARPTR.WAIT_PAGE

    def update(self):
        super().update()
        self.interval += 1

        if self.status == self.CHARPTR.WAIT_LINE:
            self.lineCursor.update()
            return
        if self.status == self.CHARPTR.WAIT_PAGE:
            self.pageCursor.update()
            return
        if self.status == self.CHARPTR.ENDOFLINE:
            self.endCursor.update()
            return
        if self.status == self.CHARPTR.WAIT_SELECT:
            self.selectCursor.update()
            return

        self.interval %= self.speed
        if not self.interval == 0:
            return

        if len(self.buf) >= self.LIMIT.CHAR_COUNT:
            self.buf = ""
            self.surfs.append(self.font_surface(self.buf))

        if len(self.surfs) >= self.LIMIT.LINE_COUNT:
            self.surfs.popleft()

        if len(self.buf) >= len(self.text) or self.ptr >= len(self.text):
            self.prepare_nextpage()
            return

        ch = self.text[self.ptr]

        if ch == "/":
            self.buf = ""
            self.surfs.append(self.font_surface(self.buf))
            self.ptr += 1
            self.status = self.CHARPTR.WAIT_LINE
            return

        if ch == "%":
            self.prepare_nextpage()
            return

        if ch == "#":
            for _id, _cont in self.json_dict[self.currPage]["select"].items():
                self.choices.append([int(_id), bool(_cont["selected"]), self.font_surface(_cont["text"])] )
            self.ptr += 1
            self.status = self.CHARPTR.WAIT_SELECT
            return

        if ch == "$":
            pass

        self.buf += self.text[self.ptr]
        self.surfs[len(self.surfs) - 1] = self.font_surface(self.buf) 
        self.ptr += 1


    def draw(self, screen: pygame.Surface):
        super().draw(screen)

        if self.status == self.CHARPTR.WAIT_LINE:
            self.lineCursor.draw(screen)
        if self.status == self.CHARPTR.WAIT_PAGE:
            self.pageCursor.draw(screen)
        if self.status == self.CHARPTR.ENDOFLINE:
            self.endCursor.draw(screen)
        if self.status == self.CHARPTR.WAIT_SELECT:
            self.selectCursor.draw(screen)

        for i in range(len(self.surfs)):
            screen.blit(self.surfs[i], (self.rect.left + 10, self.rect.top + 10 + (i * self.font_height) ) )
        

    def handler(self, event: pygame.event):
        if event.type == KEYUP:
            if event.key == K_RETURN:
                if self.status == self.CHARPTR.WAIT_LINE:
                    self.status = self.CHARPTR.IS_ACTIVE
                if self.status == self.CHARPTR.WAIT_PAGE:
                    self.surfs.clear()
                    self.surfs.append(self.font_surface(self.buf))     
                    self.status = self.CHARPTR.IS_ACTIVE

            if self.status == self.CHARPTR.WAIT_SELECT:
                if event.key == K_UP:
                    for _id, _sel, _surf in self.choices:
                        if _sel == True:
                            self.choices[_id][1] = False
                            self.choices[0 if _id - 1 < 0 else _id - 1][1] = True
                            break

                if event.key == K_DOWN:
                    for _id, _sel, _surf in reversed(self.choices):
                        if _sel == True:
                            self.choices[_id][1] = False
                            self.choices[ len(self.choices) - 1 if _id + 1 >= len(self.choices) else _id + 1][1] = True
                            break


    def key_handler(self, pressed_keys: List[bool]):

        if pressed_keys[pygame.K_RETURN]:
            if self.status == self.CHARPTR.WAIT_LINE:
                self.status = self.CHARPTR.IS_ACTIVE
            if self.status == self.CHARPTR.WAIT_PAGE:
                self.surfs.clear()
                self.surfs.append(self.font_surface(self.buf))     
                self.status = self.CHARPTR.IS_ACTIVE




class GameWindow():
    
    _keydict = {
            pygame.K_c: {"func" : None, "visible": False},
            pygame.K_s: {"func" : None, "visible": False},
            pygame.K_i: {"func" : None, "visible": False},
            pygame.K_p: {"func" : None, "visible": False},
            pygame.K_u: {"func" : MessageWindow, "visible": True},
            pygame.K_o: {"func" : None, "visible": False},
    }

    def __init__(self):
        self._keydict[K_u]["func"] = MessageWindow( pygame.Rect( (0, 450), (600, 150) ) )

    def draw(self, screen):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].draw(screen)

    def update(self):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].update()

    def handler(self, event: pygame.event) -> None:
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].handler(event)

    def key_handler(self, pressed_keys: List[bool]):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].handler(pressed_keys)

        if pressed_keys[K_c]:
            self._keydict[K_c]["visible"] = not self._keydict[K_c]["visible"]
            self._keydict[K_o]["visible"] = not self._keydict[K_o]["visible"]

        if pressed_keys[K_s]:
            self._keydict[K_s]["visible"] = not self._keydict[K_s]["visible"]

        if pressed_keys[K_o]:
            '''
            if __debug__:
                print(f"event.key={pressed_keys}")
            '''
            self._keydict[pygame.K_o]["visible"] = not self._keydict[K_o]["visible"]



g.gamewindow: GameWindow




