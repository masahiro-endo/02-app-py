
import pygame
from pygame import rect
from pygame import draw
from pygame.locals import *
import codecs
import os
import random
import struct
import sys
import control
import global_value as g
from enum import IntEnum
import math







class BaseWindow:

    EDGE_WIDTH = 2

    def __init__(self, rect: pygame.Rect):
        linewidth: int = 0

        self.surf = pygame.Surface( (rect.width, rect.height) )
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH * 2, -self.EDGE_WIDTH * 2)
        pygame.draw.rect(self.surf, Color('white'), self.rect, linewidth)
        pygame.draw.rect(self.surf, Color('black'), self.inner_rect, linewidth)
        self.rect = rect

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surf, (self.rect.left, self.rect.top) )

    def handler(self, event):
        pass


class PageCursor():

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.theta = 0

    def update(self):
        self.theta += 10

    def draw(self, screen):

        self.theta %= 360 
        r = abs( 5 * math.sin(math.radians(self.theta)) )
        pygame.draw.polygon(screen, self.color, 
                ([self.x - r, self.y], [self.x + r, self.y], [self.x, self.y + 12]) )


class MessageWindow(BaseWindow):

    MAX_CHARS_PER_LINE = 20    # 1行の最大文字数
    MAX_LINES_PER_PAGE = 3     # 1行の最大行数（4行目は▼用）
    MAX_CHARS_PER_PAGE = 20*3  # 1ページの最大文字数
    MAX_LINES = 30             # メッセージを格納できる最大行数
    LINE_HEIGHT = 8            # 行間の大きさ
    animcycle = 24

    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)

        self.text = [
            "あああああああああ",
            "いいいいいいい",
            "ううううう",
            "えええ",
            "おお",
        ]
        self.cur_page = 0  # 現在表示しているページ
        self.cur_pos = 0  # 現在ページで表示した最大文字数
        self.next_flag = False  # 次ページがあるか？
        self.hide_flag = False  # 次のキー入力でウィンドウを消すか？
        self.cursor = PageCursor(rect.left + (rect.width // 2), rect.top + (rect.height - 20), Color("white"))
        self.tick = 0

    def set(self, message):
        """メッセージをセットしてウィンドウを画面に表示する"""
        self.cur_pos = 0
        self.cur_page = 0
        self.next_flag = False
        self.hide_flag = False
        # 全角スペースで初期化
        self.text = [u'　'] * (self.MAX_LINES*self.MAX_CHARS_PER_LINE)
        # メッセージをセット
        p = 0
        for i in range(len(message)):
            ch = message[i]
            if ch == "/":  # /は改行文字
                self.text[p] = "/"
                p += self.MAX_CHARS_PER_LINE
                p = int((p/self.MAX_CHARS_PER_LINE)*self.MAX_CHARS_PER_LINE)
            elif ch == "%":  # \fは改ページ文字
                self.text[p] = "%"
                p += self.MAX_CHARS_PER_PAGE
                p = int((p/self.MAX_CHARS_PER_PAGE)*self.MAX_CHARS_PER_PAGE)
            else:
                self.text[p] = ch
                p += 1
        self.text[p] = "$"  # 終端文字
        self.show()

    def update(self):
        super().update()
        self.cursor.update()

        '''
        if self.next_flag == False:
            self.cur_pos += 1  # 1文字流す
            # テキスト全体から見た現在位置
            p = self.cur_page * self.MAX_CHARS_PER_PAGE + self.cur_pos
            if self.text[p] == "/":  # 改行文字
                self.cur_pos += self.MAX_CHARS_PER_LINE
                self.cur_pos = int((self.cur_pos/self.MAX_CHARS_PER_LINE) * self.MAX_CHARS_PER_LINE)
            elif self.text[p] == "%":  # 改ページ文字
                self.cur_pos += self.MAX_CHARS_PER_PAGE
                self.cur_pos = int((self.cur_pos/self.MAX_CHARS_PER_PAGE) * self.MAX_CHARS_PER_PAGE)
            elif self.text[p] == "$":  # 終端文字
                self.hide_flag = True
            # 1ページの文字数に達したら▼を表示
            if self.cur_pos % self.MAX_CHARS_PER_PAGE == 0:
                self.next_flag = True

        self.tick += 1
        '''

    def draw(self, screen):
        super().draw(screen)
        self.cursor.draw(screen)

        '''
        # 現在表示しているページのcur_posまでの文字を描画
        for i in range(self.cur_pos):
            ch = self.text[self.cur_page*self.MAX_CHARS_PER_PAGE+i]
            if ch == "/" or ch == "%" or ch == "$": continue  # 制御文字は表示しない
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH * (i % self.MAX_CHARS_PER_LINE)
            dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * (i // self.MAX_CHARS_PER_LINE)
            self.msg_engine.draw_character(screen, (dx,dy), ch)
        # 最後のページでない場合は▼を表示
        if (not self.hide_flag) and self.next_flag:
            if self.frame / self.animcycle % 2 == 0:
                dx = self.text_rect[0] + (self.MAX_CHARS_PER_LINE/2) * MessageEngine.FONT_WIDTH - MessageEngine.FONT_WIDTH/2
                dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * 3
                screen.blit(self.cursor, (dx,dy))
        '''

    def next(self):
        """メッセージを先に進める"""
        # 現在のページが最後のページだったらウィンドウを閉じる
        if self.hide_flag:
            self.hide()
            return False
        # ▼が表示されてれば次のページへ
        if self.next_flag:
            self.cur_page += 1
            self.cur_pos = 0
            self.next_flag = False
            return True


class CaptionWindow(BaseWindow):

    EDGE_WIDTH = 2

    def __init__(self, rect: pygame.Rect, caption: str):
        linewidth: int = 0

        self.surf = pygame.Surface( (rect.width, rect.height) )
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH * 2, -self.EDGE_WIDTH * 2)
        pygame.draw.rect(self.surf, Color('white'), self.rect, linewidth)
        pygame.draw.rect(self.surf, Color('black'), self.inner_rect, linewidth)
        self.rect = rect

        self._caption = g.enfont.render(f"{caption}", False, Color('white') )

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surf, (self.rect.left, self.rect.top) )
        screen.blit(self._caption, (self.rect.left + 10, self.rect.top + 10) )

    def handler(self, event):
        pass


class PlayerStatus(BaseWindow):

    _rows: list[pygame.Surface] = []

    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)

        txt = g.enfont.render(f"＃   {'ＣＨＡＲＡＣＴＥＲ　ＮＡＭＥ':<30} {'ＣＬＡＳＳ':>20} {'ＡＣ':>10} {'ＨＩＴＳ':>10} {'ＳＴＡＴＵＳ':>10}",
                                   False, Color('white') )
        self._rows.append( txt )
        txt = g.enfont.render(f"{'１':<1}   {'ａａａａａａａ':<50} {'Ｎ－ＦＩＧ':>20} {'－１０':>10} {'５５５':>10} {'５５５':>15}",
                                   False, Color('white') )
        self._rows.append( txt )

    def update(self):
        pass

    def draw(self, screen):
        super().draw(screen)
        for i in range( len(self._rows) ):
            screen.blit(self._rows[i], (20, 465 + (i * 20)) )


class MenuStatus(BaseWindow):

    _rows: list[pygame.Surface] = []

    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)

        txt = g.enfont.render(f"{'Ｃ）ＡＭＰ':>15} {'Ｓ）ＴＡＴＵＳ':>15} {'Ｉ）ＮＳＰＥＣＴ':>15} {'Ｐ）ＩＣＫ':>15} {'Ｕ）ＳＥ':>15} {'Ｏ）ＦＦ':>15}",
                                   False, Color('white') )
        self._rows.append( txt )

    def update(self):
        pass

    def draw(self, screen):
        super().draw(screen)
        for i in range( len(self._rows) ):
            screen.blit(self._rows[i], (0, 10)) 


class Camp():

    _caption: CaptionWindow
    _selectmenu: BaseWindow
    _rows: list[pygame.Surface] = []

    def __init__(self):
        # super().__init__()

        self._caption = CaptionWindow( pygame.Rect( (260, 0), (70, 30) ), "ＣＡＭＰ" )
        self._selectmenu = BaseWindow( pygame.Rect( (225, 200), (150, 150) ) )

        txt = g.enfont.render(f"{'＃）ＩＮＳＰＥＣＴ'}", False, Color('white') )
        self._rows.append( txt )
        txt = g.enfont.render(f"{'Ｒ）ＥＯＲＤＥＲ'}", False, Color('white') )
        self._rows.append( txt )
        txt = g.enfont.render(f"{'Ｅ）ＱＵＩＰ'}", False, Color('white') )
        self._rows.append( txt )
        txt = g.enfont.render(f"{'Ｌ⏎ＥＡＶＥ'}", False, Color('white') )
        self._rows.append( txt )

    def update(self):
        pass

    def draw(self, screen):
        # super().draw(screen)
        self._caption.draw(screen)
        self._selectmenu.draw(screen)

        for i in range( len(self._rows) ):
            screen.blit(self._rows[i], (250, 220 + (i * 20)) ) 




class GameWindow():
    
    _keydict = {
            pygame.K_c: {"func" : Camp, "visible": False},
            pygame.K_s: {"func" : PlayerStatus, "visible": False},
            pygame.K_i: {"func" : None, "visible": False},
            pygame.K_p: {"func" : None, "visible": False},
            pygame.K_u: {"func" : MessageWindow, "visible": True},
            pygame.K_o: {"func" : MenuStatus, "visible": False},
    }

    def __init__(self):
        self._keydict[K_c]["func"] = Camp()
        self._keydict[K_o]["func"] = MenuStatus( pygame.Rect( (0, 0), (600, 30) ) )
        self._keydict[K_s]["func"] = PlayerStatus( pygame.Rect( (0, 450), (600, 150) ) )

        self._keydict[K_u]["func"] = MessageWindow( pygame.Rect( (0, 450), (600, 150) ) )

    def draw(self, screen):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].draw(screen)

    def update(self):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].update()

    def handler(self, pressed_keys):

        if pressed_keys[pygame.K_RETURN]:
            if self._keydict[K_c]["visible"]:
                self._keydict[K_c]["visible"] = not self._keydict[K_c]["visible"]
                self._keydict[K_o]["visible"] = not self._keydict[K_o]["visible"]
                
        if pressed_keys[K_c]:
            self._keydict[K_c]["visible"] = not self._keydict[K_c]["visible"]
            self._keydict[K_o]["visible"] = not self._keydict[K_o]["visible"]

        if pressed_keys[K_s]:
            self._keydict[K_s]["visible"] = not self._keydict[K_s]["visible"]

        if pressed_keys[K_o]:
            '''
            if __debug__:
                print(f"event.key={pressed_keys}")
            '''
            self._keydict[pygame.K_o]["visible"] = not self._keydict[K_o]["visible"]



g.gamewindow: GameWindow




