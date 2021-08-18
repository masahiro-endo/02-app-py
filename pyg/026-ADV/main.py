#!/usr/bin/env python
import pygame
from pygame.locals import *
import os
import random
import sys
from collections import deque
os.chdir(os.path.dirname(__file__))

sys.path.append(os.path.dirname(__file__))
import control
import scene
import UI
import actor
import const
import global_value as g



MAIN_SCREEN = Rect(0, 0, 800, 600)


g.USREVENT_OOPS = pygame.USEREVENT + 1


class App:

    def __init__(self):
        pygame.mixer.quit()
        pygame.mixer.pre_init(buffer=128)
        pygame.mixer.init()
        pygame.init()
        
        self.surfaceScreen = pygame.display.set_mode(MAIN_SCREEN.size, DOUBLEBUF | HWSURFACE)
        pygame.display.set_caption("caption")
        g.jpfont12 = pygame.font.Font('./assets/fonts/姫明朝ともえごぜんmini.otf', 12)
        g.enfont = pygame.font.Font('./assets/fonts/ipaexg.ttf', 12)

        g.currentScene = deque()
        g.currentScene.appendleft(scene.Demo())

        g.gamewindow = UI.GameWindow()
        
        g.running = True
        self.mainloop()

    def mainloop(self):

        clock = pygame.time.Clock()
        while g.running:
            clock.tick(20)

            for scene in reversed(g.currentScene):
                if scene is None:
                    continue
                scene.update()
                scene.draw(self.surfaceScreen)
                
            for event in pygame.event.get():
                scene.handler(event)

            pressed_keys = pygame.key.get_pressed()
            g.gamewindow.handler(pressed_keys)
            g.gamewindow.update()
            g.gamewindow.draw(self.surfaceScreen)

            pygame.display.update()


        pygame.mixer.music.stop()
        pygame.mixer.quit()


g.running: bool

g.USREVENT_OOPS: pygame.USEREVENT

g.jpfont12: pygame.font
g.enfont: pygame.font

g.currentScene: deque[scene]





if __name__ == "__main__":
    App()





