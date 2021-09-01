#!/usr/bin/env python
import pygame
from pygame.locals import *
import codecs
import os
import random
import struct
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



SCR_RECT = Rect(0, 0, 800, 600)

g.USREVENT_OOPS = pygame.USEREVENT + 1


class App:

    def __init__(self):
        pygame.mixer.quit()
        pygame.mixer.pre_init(buffer=128)
        pygame.mixer.init()
        pygame.init()
        
        # フルスクリーン化 + Hardware Surface使用
        self.surfaceScreen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF|HWSURFACE)
        pygame.display.set_caption("PyRPG 27 戦闘画面")
        g.enfont = pygame.font.Font('./assets/fonts/ipaexg.ttf', 12)

        g.playerParty = actor.PlayerParty()
        g.playerParty.x = 5
        g.playerParty.y = 5
        g.playerParty.direction = const.Direction.NORTH
        g.playerParty.saveCondition()

        g.msg_engine= UI.MessageEngine()

        g.currentScene = deque()
        g.currentScene.appendleft(scene.BaseField())

        g.gamewindow = UI.GameWindow()

        # メインループを起動
        g.game_state = TITLE
        
        g.running = True
        self.mainloop()        

    def mainloop(self):
        """メインループ"""
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

            pygame.display.update()  # 画面に描画


        pygame.mixer.music.stop()
        pygame.mixer.quit()


g.USREVENT_OOPS: pygame.USEREVENT

g.enfont: pygame.font

g.currentScene: deque[scene]





if __name__ == "__main__":
    App()





