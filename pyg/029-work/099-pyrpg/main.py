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
GS = 32
DOWN,LEFT,RIGHT,UP = 0,1,2,3
STOP, MOVE = 0, 1  # 移動タイプ
PROB_MOVE = 0.005  # 移動確率
PROB_ENCOUNT = 0.05  # エンカウント確率
TRANS_COLOR = (190,179,145)  # マップチップの透明色

sounds = {}  # サウンド

TITLE, FIELD, TALK, COMMAND, BATTLE_INIT, BATTLE_COMMAND, BATTLE_PROCESS = range(7)




class App:

    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        # フルスクリーン化 + Hardware Surface使用
        self.surfaceScreen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF|HWSURFACE)
        pygame.display.set_caption("PyRPG 27 戦闘画面")
        g.jpfont12 = pygame.font.Font('./assets/fonts/姫明朝ともえごぜんmini.otf', 12)
        g.enfont = pygame.font.Font('./assets/fonts/ipaexg.ttf', 12)

        g.playerParty = actor.PlayerParty()
        g.playerParty.x = 5
        g.playerParty.y = 5
        g.playerParty.direction = const.Direction.NORTH
        g.playerParty.saveCondition()

        g.msg_engine= UI.MessageEngine()

        g.currentScene = deque()
        g.currentScene.appendleft(scene.DemoField())

        g.gamewindow = UI.PlayerStatus()

        # メインループを起動
        global game_state
        game_state = TITLE
        
        self.mainloop()        

    def mainloop(self):
        """メインループ"""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)

            for scene in reversed(g.currentScene):
                if scene is None:
                    continue
                scene.update()
                scene.draw(self.surfaceScreen)
                
            for event in pygame.event.get():
                scene.handler(event)

            g.gamewindow.draw(self.surfaceScreen)
            
            pygame.display.update()  # 画面に描画


        pygame.mixer.music.stop()
        pygame.mixer.quit()


g.jpfont12: pygame.font
g.enfont: pygame.font

g.currentScene: deque[scene]





if __name__ == "__main__":
    App()





