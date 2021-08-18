

from collections import deque
from typing import List
import pygame
from pygame.locals import *
import codecs
import os
import random
import struct
import sys
import control
from enum import IntEnum
import UI
import actor
import field
import const
import math
import global_value as g


class BaseScene:

    # 経過時間
    tick = 0

    # stateStackへの参照
    stateStack = None

    # 描画の座標オフセット
    DRAW_OFFSET_X = 0
    DRAW_OFFSET_Y = 0


    def __init__(self):
        pass

    def update(self):
        self.tick += 1

    def draw(self, screen):
        pass

    def handler(self, event):

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    def onEnter(self):
        # タイマーカウンタ初期化
        self.tick = 0

    def onExit(self):
        pass




class Demo(Scene):

    wnd: UI.Window

    def __init__(self):
        self.wnd = UI.MessageWindow(Rect(140,334,360,140), g.msg_engine)

    def update(self):
        self.wnd.update()
    
    def draw(self, screen):
        screen.fill((128,128,128))
        self.wnd.draw(screen)  # ウィンドウの描画

    def handler(self, event):
        super().handler(event)

        if event.type == KEYDOWN:

            if event.key == K_SPACE:

                if self.wnd.is_visible:  # ウィンドウ表示中
                    self.wnd.next()
                else:
                    self.wnd.show()  # ウィンドウを表示
                    self.wnd.set(u"そのほうこうには　だれもいない。")
                if __debug__:
                    print("wnd.visible=" + str(self.wnd.is_visible))

            if event.key == K_RETURN:
                g.currentScene.pop()
                g.currentScene.append(screen.Title(g.msg_engine))





