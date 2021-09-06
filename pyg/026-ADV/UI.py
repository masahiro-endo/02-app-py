
from collections import OrderedDict, deque
import typing
import pygame
from pygame.locals import *
import global_value as g
from enum import IntEnum, auto
import json
from typing import Any, Dict
from enum import IntEnum
import UIcontrol
import os




class BaseWindow:

    class Style():
        BORDER = 2

    def __init__(self, rect: pygame.Rect):
        linewidth: int = 0

        self.surf: pygame.Surface = pygame.Surface( (rect.width, rect.height) )
        self.surf.fill(Color('black'))
        self.rect = self.surf.get_rect(topleft=(rect.top,rect.left))

        self.inner_rect = self.rect.inflate(-self.Style.BORDER * 2, -self.Style.BORDER * 2)
        pygame.draw.rect(self.surf, Color('white'), self.rect, linewidth)
        pygame.draw.rect(self.surf, Color('black'), self.inner_rect, linewidth)
        # self.rect = rect

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, (self.rect.left, self.rect.top) )


class ImageWindow():

    class SHOW(IntEnum):
        FADEIN = auto()
        FADEOUT = auto()

    def __init__(self, rect: pygame.Rect, **kwargs: Dict[str, Any]):
        self.x = rect.left
        self.y = rect.top
        img: Any = kwargs.get('image')
        self.effect: Any = kwargs.get('effect')
        self.speed: Any = kwargs.get('speed') if kwargs.get('speed') != None else 1
        self.set_image(img)
        self.pause: int = 0

        self.effect == self.SHOW.FADEIN
        self.trans = 0
        if self.effect is None:
            pass
        elif self.effect == self.SHOW.FADEIN:
            pass
        elif self.effect == self.SHOW.FADEOUT:
            self.trans = 250

    def set_image(self, img: str):
        path: str = f'./assets/images/bg/{img}'
        if __debug__:
            print(path)
        if path == os.path.basename(self.image):
            return

        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width // 3, self.rect.height // 3))
        self.image = self.image.convert()
        self.image.set_colorkey(-1, RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (320,240)

    def update(self):
        self.pause %= self.speed
        if not self.pause == 0:
            return

        if self.effect is None:
            pass
        elif self.effect == self.SHOW.FADEIN:
            self.trans += 1
            self.trans = self.trans if self.trans < 250 else 250
        elif self.effect == self.SHOW.FADEOUT:
            self.trans -= 1
            self.trans = self.trans if self.trans > 0 else 0

    def draw(self, screen: pygame.Surface):
        self.image.set_alpha(self.trans)
        screen.blit(self.image, (self.x, self.y) )


class CHARPTR(IntEnum):
    IS_ACTIVE = 0
    WAIT_LINE = auto()
    WAIT_PAGE = auto()
    ENDOFLINE = auto()
    WAIT_SELECT = auto()


class SelectWindow():

    class Style():
        LINE_SPACE = 5

    _cur: Dict[CHARPTR, Dict[str, Any]] = {
        CHARPTR.WAIT_SELECT: {"cursor" : UIcontrol.SelectCursor},
    }

    def __init__(self, rect: pygame.Rect, dict: Dict[str,Dict[str,Any]]):
        self.rect = rect
        dx = self.rect.left
        dy = self.rect.top
        self.selectCursor = UIcontrol.SelectCursor(dx, dy, Color("white"))

        self.init_selectitems(dict)
        self.sid: int = 0
        
        self.status = CHARPTR.WAIT_SELECT

    def init_selectitems(self, dict: Dict[str, Dict[str,Any]]):
        self.dict = dict
        for x, sl in dict.items():
            if __debug__:
                print(f'{x}:{sl}')
            sl["surf"] = None
            sl["surf"] = g.UIfont.render(sl["text"])
            if sl["selected"] == 'True':
                self.sid = int(x)

    def update(self):
        for x, sl in self.dict.items():
            if sl["selected"] == 'True':
                self._cur[self.status]["cursor"].update(self.rect.top + (self.sid * g.UIfont.HEIGHT) + (g.UIfont.HEIGHT // 2))
        return

    def draw(self, screen: pygame.Surface):
        self._cur[self.status]["cursor"].draw(screen)

        for x, sl in self.dict.items():
            dx: int = self.rect.left
            dy: int = self.rect.top + (int(x) * g.UIfont.HEIGHT + self.Style.LINE_SPACE)
            screen.blit(sl["surf"], (dx, dy))
        
    def handler(self, event: pygame.event):
        if event.type == KEYUP:
            if event.key == K_RETURN:
                if self.status == CHARPTR.WAIT_SELECT:
                    pass
 
            if self.status == CHARPTR.WAIT_SELECT:
                if event.key == K_UP:
                    self.sid -= 1
                    self.sid = 0 if self.sid < 0 else self.sid

                if event.key == K_DOWN:
                    self.sid += 1
                    self.sid = len(self.dict) - 1 if self.sid >= len(self.dict) else self.sid


class MessageScriptWindow():

    class LIMIT(IntEnum):
        CHAR_COUNT = 10
        LINE_COUNT = 4
        PAGE_COUNT = 999

    _subwnd: Dict[str, Any] = {
            'select': SelectWindow,
            'image': ImageWindow,
    }
    _cur: Dict[CHARPTR, Dict[str, Any]] = {
            CHARPTR.IS_ACTIVE: {"cursor" : None},
            CHARPTR.WAIT_LINE: {"cursor" : UIcontrol.LineCursor},
            CHARPTR.WAIT_PAGE: {"cursor" : UIcontrol.PageCursor},
            CHARPTR.ENDOFLINE: {"cursor" : UIcontrol.FontCursor},
            CHARPTR.WAIT_SELECT: {"cursor" : _subwnd['select']},
    }

    def __init__(self, rect: pygame.Rect, **kwargs: Dict[str, Any]):
        scenario: Any = kwargs.get('scenario') if kwargs.get('scenario') != None else 'scenario1'
        self.rect = rect
        dx = rect.left + (rect.width // 2)
        dy = rect.top + (rect.height - 20)
        self._cur[CHARPTR.WAIT_LINE]["cursor"] = UIcontrol.LineCursor(dx, dy, Color("white"))
        self._cur[CHARPTR.WAIT_PAGE]["cursor"] = UIcontrol.PageCursor(dx, dy, Color("white"))
        self._cur[CHARPTR.ENDOFLINE]["cursor"] = UIcontrol.FontCursor(dx, dy, Color("white"))
        self.pause = 0

        self.surfs: deque[pygame.Surface] = deque()

        self.buf = ""
        self.ptr = 0
        self.init_scenario(scenario)
        # self._subwnd['image'] = ImageWindow(WindowAssign.IMAGE, image=self.json_dict[self.currPage])
        self._subwnd['image'] = None
        
        self.status = CHARPTR.IS_ACTIVE

    def init_scenario(self, filename: str):
        self.json_dict = self.read_json(filename)

        for self.currPage in self.json_dict: break
        self.init_page(self.currPage)
        self.status = CHARPTR.IS_ACTIVE

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

    def update_selectvalue(self):
        _sid = str(self._subwnd['select'].sid)
        for x, sl in self.json_dict[self.currPage]["select"].items():
            if _sid == x:
                sl["selected"] = 'True'
                if "page" in sl["value"]:
                    self.init_page(sl["value"])
                elif "scenario" in sl["value"]:
                    self.init_scenario(sl["value"])
                else:
                    pass
            else:
                sl["selected"] = 'False'

    def update(self):
        if not self._subwnd['image'] is None:
            self._subwnd['image'].update()
        self.pause += 1
        
        if not self._cur[self.status]["cursor"] == None:
            self._cur[self.status]["cursor"].update()
            return

        self.pause %= self.speed
        if not self.pause == 0:
            return

        if len(self.buf) >= self.LIMIT.CHAR_COUNT:
            self.buf = ""
            self.surfs.append(g.UIfont.render(self.buf))

        if len(self.surfs) >= self.LIMIT.LINE_COUNT:
            self.surfs.popleft()

        if len(self.buf) >= len(self.text) or self.ptr >= len(self.text):
            self.status = CHARPTR.WAIT_PAGE
            return

        ch = self.text[self.ptr]

        if ch == "/":
            self.buf = ""
            self.surfs.append(g.UIfont.render(self.buf))
            self.ptr += 1
            self.status = CHARPTR.WAIT_LINE
            return

        if ch == "%":
            self.status = CHARPTR.WAIT_PAGE
            return

        if ch == "#":
            self._subwnd['select'] = None
            self._subwnd['select'] = SelectWindow(WindowAssign.SELECT, self.json_dict[self.currPage]["select"] )
            self.ptr += 1
            self.status = CHARPTR.WAIT_SELECT
            return

        if ch == "$":
            pass

        self.buf += self.text[self.ptr]
        self.surfs[-1] = g.UIfont.render(self.buf) 
        self.ptr += 1

    def draw(self, screen: pygame.Surface):
        if not self._subwnd['image'] is None:
            self._subwnd['image'].draw(screen)

        if not self._cur[self.status]["cursor"] == None:
            self._cur[self.status]["cursor"].draw(screen)

        for i in range(len(self.surfs)):
            dx: int = self.rect.left
            dy: int = self.rect.top + (i * g.UIfont.HEIGHT + (i * 5))
            screen.blit(self.surfs[i], (dx, dy))
        
    def handler(self, event: pygame.event):
        if event.type == KEYUP:
            if self.status == CHARPTR.WAIT_SELECT:
                self._subwnd['select'].handler(event)
            
            if event.key == K_RETURN:
                if self.status == CHARPTR.WAIT_LINE:
                    self.status = CHARPTR.IS_ACTIVE
                
                if self.status == CHARPTR.WAIT_PAGE:
                    self.currPage = self.next
                    self.init_page(self.currPage)
                    self.status = CHARPTR.IS_ACTIVE
                
                if self.status == CHARPTR.WAIT_SELECT:
                    self.update_selectvalue()
                    self.status = CHARPTR.IS_ACTIVE


class WindowAssign():
    MESSAGE = pygame.Rect((100, 100), (200, 200))
    SELECT = pygame.Rect((100, 200), (200, 200))
    IMAGE = pygame.Rect((100, 100), (100, 150))


class UIfonts():
    
    def __init__(self, size: int):
        self.FONT: pygame.font = pygame.font.Font('./assets/fonts/ipaexg.ttf', size)
        self.WIDTH, self.HEIGHT = self.FONT.size("あ")

    def render(self, buf: str) -> pygame.Surface:
        return self.create_surface(buf)

    def create_surface(self, buf: str) -> pygame.Surface:
        return self.FONT.render(f"{buf}", False, Color("white"))

    def size(self, ) -> Any:
        return self.HEIGHT, self.WIDTH

g.UIfont: UIfonts


class TerminalWindow():
    
    _keydict: Dict[int, Dict[str,Any]] = {
            pygame.K_c: {"func" : None, "visible": False},
            pygame.K_s: {"func" : None, "visible": False},
            pygame.K_i: {"func" : None, "visible": False},
            pygame.K_p: {"func" : None, "visible": False},
            pygame.K_u: {"func" : None, "visible": True},
            pygame.K_o: {"func" : None, "visible": False},
    }

    def __init__(self):
        # self._keydict[K_u]["func"] = MessageScriptWindow( WindowAssign.MESSAGE, scenario='scenario1')
        pass

    def draw(self, screen: pygame.Surface):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].draw(screen)

    def update(self):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].update()

    def handler(self, event: pygame.event):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].handler(event)

        if event.type == KEYUP:
            if event.key in self._keydict.keys():
                self._keydict[event.key]["visible"] = not self._keydict[event.key]["visible"]



g.term: TerminalWindow




