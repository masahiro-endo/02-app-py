

import pygame
from pygame.locals import *
import codecs
import os
import random
import struct
import sys
import control
from enum import IntEnum



class Scene:
    def __init__(self):
        pass



class Title(Scene):

    class SELECT(IntEnum):
        START = 0
        CONTINUE = 1
        EXIT = 2

    def __init__(self, msg_engine):
        self.msg_engine = msg_engine
        self.title_img = control.Method.load_image("data", "title.png", -1)
        self.cursor_img = control.Method.load_image("data", "cursor2.png", -1)
        self.menu = self.SELECT.START
        self.play_bgm()
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.fill((0,0,128))
        # タイトルの描画
        screen.blit(self.title_img, (20,60))
        # メニューの描画
        self.msg_engine.draw_string(screen, (260,240), "ＳＴＡＲＴ")
        self.msg_engine.draw_string(screen, (260,280), "ＣＯＮＴＩＮＵＥ")
        self.msg_engine.draw_string(screen, (260,320), "ＥＸＩＴ")
        # クレジットの描画
        self.msg_engine.draw_string(screen, (130,400), "ＣＲＥＤＩＴ")
        # メニューカーソルの描画
        if self.menu == self.SELECT.START:
            screen.blit(self.cursor_img, (240, 240))

        elif self.menu == self.SELECT.CONTINUE:
            screen.blit(self.cursor_img, (240, 280))

        elif self.menu == self.SELECT.EXIT:
            screen.blit(self.cursor_img, (240, 320))
    
    def play_bgm(self):
        bgm_file = "title.mp3"
        bgm_file = os.path.join("bgm", bgm_file)
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.play(-1)

    def handler(self, event):

#        if __debug__:
#            print("TitleHandler : Begin.")

        global game_state
        if event.type == KEYUP and event.key == K_UP:
            self.menu -= 1 if self.menu > min(self.SELECT) else min(self.SELECT)

        elif event.type == KEYDOWN and event.key == K_DOWN:
            self.menu += 1 if self.menu < max(self.SELECT) else max(self.SELECT)

        if event.type == KEYDOWN and event.key == K_SPACE:
            sounds["pi"].play()
            
            if self.menu == self.SELECT.START:
                game_state = PROLOGUE
                self.map.create("field")  # フィールドマップへ
            
            elif self.menu == self.SELECT.CONTINUE:
                pass
            
            elif self.menu == self.SELECT.EXIT:
                pygame.quit()
                sys.exit()



class Prologue:





