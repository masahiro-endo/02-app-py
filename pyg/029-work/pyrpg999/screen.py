

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
import global_value as g


class Scene:
    def __init__(self):
        pass


class Demo(Scene):

    wnd: UI.Window

    def __init__(self):
        global msg_engine
        self.wnd = UI.MessageWindow(Rect(140,334,360,140), g.msg_engine)

    def update(self):
        self.wnd.update()
    
    def draw(self, screen):
        screen.fill((128,128,128))
        self.wnd.draw(screen)  # ウィンドウの描画

    def handler(self, event):

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_SPACE:

                if self.wnd.is_visible:  # ウィンドウ表示中
                    self.wnd.next()
                else:
                    self.wnd.show()  # ウィンドウを表示
                    self.wnd.set(u"そのほうこうには　だれもいない。")
                if __debug__:
                    print("wnd.visible=" + str(self.wnd.is_visible))

            if event.key == K_RETURN:
                global msg_engine
                global currentScene
                currentScene.pop()
                currentScene.append(screen.Title(msg_engine))




class Camp(Scene):

    wnd: UI.Window

    def __init__(self):
        global msg_engine
        self.wnd = UI.CommandWindow(Rect(16,16,216,160), g.msg_engine)

    def update(self):
        self.wnd.update()
    
    def draw(self, screen):
        screen.fill((128,128,128))
        self.wnd.draw(screen)  # ウィンドウの描画

    def handler(self, event):

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_SPACE:

                if self.wnd.is_visible:  # ウィンドウ表示中
                    self.wnd.handler(event)
                else:
                    self.wnd.show()  # ウィンドウを表示

            if event.key == K_RETURN:
                global msg_engine
                global currentScene
                currentScene.pop()
                currentScene.append(screen.Title(msg_engine))




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



class Prologue(Scene):

    def __init__(self):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        pass
    
    def handler(self, event):
        pass





class Battle(Scene):

    """戦闘画面"""
    def __init__(self, msgwnd, msg_engine):
        self.msgwnd = msgwnd
        self.msg_engine = msg_engine
        # 戦闘コマンドウィンドウ
        self.cmdwnd = BattleCommandWindow(Rect(96, 338, 136, 136), self.msg_engine)
        # プレイヤーステータス（Playerクラスに実装した方がよい）
        status = [["けんし　", 16, 0, 1],
                  ["エルフ　", 15, 24, 1],
                  ["そうりょ", 10, 8, 1],
                  ["まどうし", 8, 12, 1]]
        # 戦闘ステータスウィンドウ
        self.status_wnd = []
        self.status_wnd.append(BattleStatusWindow(Rect(90, 8, 104, 136), status[0], self.msg_engine))
        self.status_wnd.append(BattleStatusWindow(Rect(210, 8, 104, 136), status[1], self.msg_engine))
        self.status_wnd.append(BattleStatusWindow(Rect(330, 8, 104, 136), status[2], self.msg_engine))
        self.status_wnd.append(BattleStatusWindow(Rect(450, 8, 104, 136), status[3], self.msg_engine))
        self.monster_img = control.Method.load_image("data", "dragon.png", -1)

    def start(self):
        """戦闘の開始処理、モンスターの選択、配置など"""
        self.cmdwnd.hide()
        for bsw in self.status_wnd:
            bsw.hide()
        self.msgwnd.set("やまたのおろちが　あらわれた。")
        self.play_bgm()

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.monster_img, (200, 170))
        self.cmdwnd.draw(screen)
        for bsw in self.status_wnd:
            bsw.draw(screen)

    def play_bgm(self):
        bgm_file = "battle.mp3"
        bgm_file = os.path.join("bgm", bgm_file)
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.play(-1)

    def handler(self, event):

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == K_SPACE:

                if self.wnd.is_visible:  # ウィンドウ表示中
                    self.wnd.handler(event)
                else:
                    self.wnd.show()  # ウィンドウを表示

            if event.key == K_RETURN:
                global msg_engine
                global currentScene
                currentScene.pop()
                currentScene.append(screen.Title(msg_engine))



