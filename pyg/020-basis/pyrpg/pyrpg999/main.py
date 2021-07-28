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
import screen




SCR_RECT = Rect(0, 0, 640, 480)
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
        pygame.init()
        # フルスクリーン化 + Hardware Surface使用
        self.surfaceScreen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF|HWSURFACE)
        pygame.display.set_caption("PyRPG 27 戦闘画面")

        global msg_engine 
        msg_engine= MessageEngine()

        global currentScene
        currentScene = deque()
        currentScene.append(screen.Title(msg_engine))

        # メインループを起動
        global game_state
        game_state = TITLE
        
        self.mainloop()        

    def mainloop(self):
        """メインループ"""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            for scene in currentScene:
                scene.update()
                scene.draw(self.screen)
                
                for event in pygame.event.get():
                    scene.handler(event)

            pygame.display.update()  # 画面に描画



class MessageEngine:
    FONT_WIDTH = 16
    FONT_HEIGHT = 22
    WHITE, RED, GREEN, BLUE = 0, 160, 320, 480
    def __init__(self):
        self.image = control.Method.load_image("data", "font.png", -1)
        self.color = self.WHITE
        self.kana2rect = {}
        self.create_hash()
    def set_color(self, color):
        """文字色をセット"""
        self.color = color
        # 変な値だったらWHITEにする
        if not self.color in [self.WHITE,self.RED,self.GREEN,self.BLUE]:
            self.color = self.WHITE
    def draw_character(self, screen, pos, ch):
        """1文字だけ描画する"""
        x, y = pos
        try:
            rect = self.kana2rect[ch]
            screen.blit(self.image, (x,y), (rect.x+self.color,rect.y,rect.width,rect.height))
        except KeyError:
            print("描画できない文字があります:%s" % ch)
            return
    def draw_string(self, screen, pos, str):
        """文字列を描画"""
        x, y = pos
        for i, ch in enumerate(str):
            dx = x + self.FONT_WIDTH * i
            self.draw_character(screen, (dx,y), ch)
    def create_hash(self):
        """文字から座標への辞書を作成"""
        filepath = os.path.join("data", "kana2rect.dat")
        fp = codecs.open(filepath, "r", "utf-8")
        for line in fp.readlines():
            line = line.rstrip()
            d = line.split("\t")
            kana, x, y, w, h = d[0], int(d[1]), int(d[2]), int(d[3]), int(d[4])
            self.kana2rect[kana] = Rect(x, y, w, h)
        fp.close()


currentScene: deque
msg_engine: MessageEngine





if __name__ == "__main__":
    App()





