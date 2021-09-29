
from typing import Any, Dict
import pygame
from pygame.locals import *
import sys

from pygame.mixer import pause
import global_value as g
import threading
import UI
import extend


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

    _arg: Dict[str, Any] = {
            'interval': 5,
            'func': None,
    }
    _subwnd: Dict[str, Any] = {
            'image': UI.ImageWindow,
            'script': extend.ScriptWindow,
    }
    _perser: extend.ScriptPerser

    def __init__(self):
        super().__init__()
        self.stopevent = None
        self._subwnd['image'] = UI.ImageWindow(UI.WindowAssign.IMAGE, 
                                    image='1701325i.jpg', speed=2)
        self._subwnd['image'].effect = None
        self._subwnd['script'] = extend.ScriptWindow(UI.WindowAssign.IMAGE)
        self._perser = extend.ScriptPerser(scenario='prologue')
 
    def validate_args(self, args: Dict[str, Any]):
        for key in self._arg.keys():
            arg: Any = args.get(key)
            if arg != None:
                self._arg[key] = arg

    def stop(self):
        if not self.stopevent is None:
            self.stopevent.set()

    def is_stop(self) -> bool:
        return self.stopevent.is_set()

    def do_interval(self, **kwargs: Dict[str, Any]):
        self.validate_args(kwargs)
        intvl: Any = self._arg['interval']
        func: Any = self._arg['func'] 

        self.stop()
        self.timer = threading.Timer(intvl, func)
        self.stopevent = threading.Event()
        self.timer.setDaemon(True)
        self.timer.start()
    
    def seq_begin(self, **kwargs: Dict[str, Any]):
        self._subwnd['image'].effect = UI.ImageWindow.SHOW.FADEIN
        self.do_interval(interval=5, func=self.seq_1)

    def seq_1(self):
        self._subwnd['script'].init_buf(self._perser.text)
        self._subwnd['image'].effect = None
        self.do_interval(interval=5, func=self.seq_2)

    def seq_2(self):
        self._perser.init_page(self._perser.next)
        self._subwnd['script'].init_buf(self._perser.text)
        self._subwnd['image'].set_image("1701327i.jpg")
        self.do_interval(interval=5, func=self.seq_3)

    def seq_3(self):
        self._subwnd['script'].effect = UI.ImageWindow.SHOW.FADEOUT
        self._subwnd['image'].effect = UI.ImageWindow.SHOW.FADEOUT
        self.do_interval(interval=5, func=self.seq_end)

    def seq_end(self):
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





