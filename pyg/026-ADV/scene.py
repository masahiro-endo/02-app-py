
from typing import Any, Dict
import pygame
from pygame.locals import *
import sys

from pygame.mixer import pause
import global_value as g
import threading
import UI
import test


class BaseScene:

    class DRAW_OFFSET():
        X = 0
        Y = 0

    def __init__(self):
        self.tick = 0

    def update(self):
        self.tick += 1

    def draw(self, screen: pygame.Surface):
        pass

    def handler(self, event: pygame.event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    def onEnter(self):
        self.tick = 0

    def onExit(self):
        pass




class Demo(BaseScene):

    _subwnd: Dict[str, Any] = {
            'image': UI.ImageWindow,
            'message': test.AutoMessageWindow,
    }

    def __init__(self):
        super().__init__()
        self.stopevent = None
        self._subwnd['image'] = UI.ImageWindow(UI.WindowAssign.IMAGE, image='1701325i.jpg', speed=2)
        self._subwnd['image'].effect = None

    def stop(self):
        if not self.stopevent is None:
            self.stopevent.set()

    def is_stop(self) -> bool:
        return self.stopevent.is_set()

    def do_interval(self, **kwargs: Dict[str, Any]):
        intvl: Any = kwargs.get('interval') 
        func: Any = kwargs.get('func') 

        self.stop()
        # self.interval = threading.Timer(intvl, eval(func))
        self.interval = threading.Timer(intvl, func)
        self.stopevent = threading.Event()
        self.interval.setDaemon(True)
        self.interval.start()
    
    def sequence_begin(self, **kwargs: Dict[str, Any]):
        if __debug__:
            print(f'{"sequence"}:{"begin"}')

        self._subwnd['image'].effect = UI.ImageWindow.SHOW.FADEIN
        self.do_interval(interval=5, func=self.sequence1)

    def sequence1(self):
        if __debug__:
            print(f'{"sequence"}:{"1"}')

        self._subwnd['image'].effect = None
        self.do_interval(interval=5, func=self.sequence2)

    def sequence2(self):
        if __debug__:
            print(f'{"sequence"}:{"2"}')

        self._subwnd['image'].effect = UI.ImageWindow.SHOW.FADEOUT
        self.do_interval(interval=5, func=self.sequence_end)

    def sequence_end(self):
        if __debug__:
            print(f'{"sequence"}:{"end"}')

        self._subwnd['image'].effect = None
        self.stop()

    def update(self):
        super().update()
        for _name, _instance in self._subwnd.items():
            if not _instance is None:
                _instance.update()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
        for _name, _instance in self._subwnd.items():
            if not _instance is None:
                _instance.draw(screen)

    def handler(self, event: pygame.event):
        super().handler(event)





