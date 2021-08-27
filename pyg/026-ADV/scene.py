

from typing import Any
import pygame
from pygame.locals import *
import sys
import global_value as g
import threading


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

    def __init__(self):
        pass

    def pause(self):
        self.stopevent.set()

    def is_stop(self) -> bool:
        return self.stopevent.is_set()

    def beginSequence(self, **kwargs):
        interval: int = kwargs.get('interval') 
        func: Any = kwargs.get('func') 


    def sequenceBegin(self):
        self.pause()
        self.interval = threading.Timer(5, self.sequence1)
        self.stopevent = threading.Event()
        self.interval.setDaemon(True)
        self.interval.start()

    def sequence1(self):
        self.pause()
        self.interval = threading.Timer(5, self.sequence1)
        self.stopevent = threading.Event()
        self.interval.setDaemon(True)
        self.interval.start()

    def sequence2(self):

    def sequenceEnd(self):

    def update(self):
        super().update()

    def draw(self, screen: pygame.Surface):
        super().draw(screen)

    def handler(self, event: pygame.event):
        super().handler(event)

        self.onEntert = threading.Timer(5, hello)




