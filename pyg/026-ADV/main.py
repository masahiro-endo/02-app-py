#!/usr/bin/env python
from typing import Any
import pygame as pg
from pygame.locals import *
import os
import sys
from collections import deque
import scene
import UI
import global_value as g
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))



class DisplayResolution():
    VGA = Rect(0, 0, 640, 480)
    SVGA = Rect(0, 0, 800, 600)
    XGA = Rect(0, 0, 1024, 768)


g.USREVENT_OOPS = pg.USEREVENT + 1


class App:

    def __init__(self):
        pg.mixer.quit()
        pg.mixer.pre_init(buffer=128)
        pg.mixer.init()

        pg.init()
        pg.key.set_repeat()
        
        self.mainScreen = pg.display.set_mode(DisplayResolution.VGA.size, DOUBLEBUF | HWSURFACE)
        pg.display.set_caption("caption")

        g.sceneStack = deque()
        g.sceneStack.appendleft(scene.Demo())

        g.UIfont = UI.UIfont(20)
        g.term = UI.TerminalWindow()
        
        g.running = True
        self.mainloop()

    def mainloop(self):

        clock = pg.time.Clock()
        while g.running:
            clock.tick(20)
            
            events: pg.Eventlist = pg.event.get()
            scene: Any
            for scene in reversed(g.sceneStack):
                if scene is None:
                    continue
                scene.update()
                scene.draw(self.mainScreen)
                for event in events:
                    scene.handler(event)

            g.term.update()
            g.term.draw(self.mainScreen)
            for event in events:
                g.term.handler(event)

            pg.display.update()

        pg.mixer.music.stop()
        pg.mixer.quit()


g.running: bool
g.USREVENT_OOPS: pg.USEREVENT
g.currentScene: deque[scene]



if __name__ == "__main__":
    App()





