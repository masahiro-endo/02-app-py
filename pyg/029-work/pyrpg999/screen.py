

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

    # 経過時間
    tick = 0

    # stateStackへの参照
    stateStack = None

    # 描画の座標オフセット
    DRAW_OFFSET_X = 150
    DRAW_OFFSET_Y = 14


    def __init__(self):
        pass

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
                global msg_engine
                global currentScene
                currentScene.pop()
                currentScene.append(screen.Title(msg_engine))



class DemoField(Scene):

    wnd: UI.Window

    def __init__(self):
        global msg_engine
        self.wnd = UI.MessageWindow(Rect(140,334,360,140), g.msg_engine)

    def update(self):
        self.wnd.update()
    
    def draw(self, screen):
        screen.fill((128,128,128))
        self.wnd.draw(screen)  # ウィンドウの描画
        super().draw(screen)

        # 迷路の枠線
        pygame.draw.rect(screen, Color('darkblue'), (self.DRAW_OFFSET_X - 1, self.DRAW_OFFSET_Y - 1, 81, 81))

        # 地面部のグリッド
        if self.isSky():
            pygame.draw.rect(screen, Color('darkblue'), (self.DRAW_OFFSET_X, self.DRAW_OFFSET_Y, 79, 79))
        else:
            pygame.draw.line(screen, Color('darkblue'), 
                      (0 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y), 5)
            pygame.draw.line(screen, Color('darkblue'), 
                      (0 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y), 5)
            pygame.draw.line(screen, Color('darkblue'), 
                      (0 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y), 5)
            pygame.draw.line(screen, Color('darkblue'), 
                      (0 + self.DRAW_OFFSET_X, 69 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 69 + self.DRAW_OFFSET_Y), 5)
            
            pygame.draw.line(screen, Color('darkblue'), 
                      (39 + self.DRAW_OFFSET_X, 39 + self.DRAW_OFFSET_Y), 
                      (0 + self.DRAW_OFFSET_X, 78 + self.DRAW_OFFSET_Y), 5)
            pygame.draw.line(screen, Color('darkblue'), 
                      (39 + self.DRAW_OFFSET_X, 39 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 78 + self.DRAW_OFFSET_Y), 5)


        if self.tick > 0:
            if self.isOuter():
                pass
            else:
                # 天井部のグリッド
                pygame.draw.line(screen, Color('darkblue'), 
                      (0 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y), 5)
                pygame.draw.line(screen, Color('darkblue'), 
                      (0 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y), 5)
                pygame.draw.line(screen, Color('darkblue'), 
                      (0 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y), 5)
                pygame.draw.line(screen, Color('darkblue'), 
                      (0 + self.DRAW_OFFSET_X, 9 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 9 + self.DRAW_OFFSET_Y), 5)
            
                pygame.draw.line(screen, Color('darkblue'), 
                      (39 + self.DRAW_OFFSET_X, 39 + self.DRAW_OFFSET_Y), 
                      (0 + self.DRAW_OFFSET_X, 0 + self.DRAW_OFFSET_Y), 5)
                pygame.draw.line(screen, Color('darkblue'), 
                      (39 + self.DRAW_OFFSET_X, 39 + self.DRAW_OFFSET_Y), 
                      (78 + self.DRAW_OFFSET_X, 0 + self.DRAW_OFFSET_Y), 5)



            # 迷路
            # self.draw_maze(playerParty.x, playerParty.y,
            #               playerParty.direction, self._map)


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
                global msg_engine
                global currentScene
                currentScene.pop()
                currentScene.append(screen.Title(msg_engine))



    def isOuter(self) -> bool:
        '''
        屋外かどうかをboolで返却する。\n
        Falseが初期値。Trueとしたければ子クラスでこのメソッドをオーバーライドする。\n
        '''
        return False

    def isSky(self) -> bool:
        '''
        屋外かどうかをboolで返却する。\n
        Falseが初期値。Trueとしたければ子クラスでこのメソッドをオーバーライドする。\n
        '''
        return False

    def draw_maze(self, _x, _y, _direction, _map):
        '''
        迷路を表示する。\n
        利用元からは、X座標、Y座標、方向、マップデータを引数に与えること。\n
        '''
        _data = 0
        for i in range(14):
            _get_x = _x + self.POS_X[_direction][i]
            _get_y = _y + self.POS_Y[_direction][i]

            if _get_x < 0 or _get_x > len(_map[_y]) - 1 or _get_y < 0 or _get_y > len(_map) - 1:
                _data = 0
            else:
                _data = self.get_mapinfo(_map, _get_x, _get_y, _direction)
            self.draw_wall(i, _data)

    def __right_3bit_rotate(self, n) -> int:
        '''
        3ビット右にローテートした値を返却する。
        '''
        return ((n & 0b000000000111) << 9) | ((n >> 3) & 0b111111111111)

    def __left_3bit_rotate(self, n) -> int:
        '''
        3ビット左にローテートした値を返却する。
        '''
        return ((n << 3) & 0b111111111111) | (n >> 9)

    def get_mapinfo(self, _map, _x, _y, _direction) -> int:
        '''
        指定した座標のマップ情報を取得する。\n
        取得対象のマップデータと方向は引数で指定する。\n
        返却される値は、方向によりデータをシフトした結果となる。
        '''
        _data = _map[_y][_x]
        if _direction > Direction.NORTH:
            for _ in range(_direction):
                _data = self.__right_3bit_rotate(_data)
        return _data

    def draw_wall(self, _idx, _data):
        '''
        迷路を表示する。\n
        drawMazeクラスからの利用を想定し、他のモジュールからの使用は想定していない。\n
        描画番号とマップの地形情報に従って壁を描画する
        '''
        # dataが0の場合は壁を描画しないので抜ける
        if _data == 0:
            return

        # idxとの値により壁を描画する
        # |0|1|4|3|2|
        #   |5|7|6|
        #   |8|A|9|
        #   |B|D|C|
        if _idx == 1:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 39
                _h = 38 if (self.isOuter() and _Color == 3) else 1
                pyxel.rect(35 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLColor_FRONT[_Color])
        if _idx == 3:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 39
                _h = 38 if (self.isOuter() and _Color == 3) else 1
                pyxel.rect(41 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLColor_FRONT[_Color])
        if _idx == 4:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 39
                _h = 38 if (self.isOuter() and _Color == 3) else 1
                pyxel.rect(38 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLColor_FRONT[_Color])
            if _data & 0b000000111000 != 0:
                _Color = (_data >> 3) & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 39
                _h = 38 if (self.isOuter() and _Color == 3) else 1
                pyxel.tri(43 + self.DRAW_OFFSET_X, 36 + self.DRAW_OFFSET_Y,
                          41 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y,
                          43 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.tri(41 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y,
                          43 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y,
                          43 + self.DRAW_OFFSET_X, 42 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.rect(41 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLColor_SIDE[_Color])
            if _data & 0b111000000000 != 0:
                _Color = (_data >> 9) & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 39
                _h = 38 if (self.isOuter() and _Color == 3) else 1
                pyxel.tri(35 + self.DRAW_OFFSET_X, 36 + self.DRAW_OFFSET_Y,
                          37 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y,
                          35 + self.DRAW_OFFSET_X, 38 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.tri(35 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y,
                          37 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y,
                          35 + self.DRAW_OFFSET_X, 42 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.rect(35 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           3, _h,
                           self.WALLColor_SIDE[_Color])

        if _idx == 5:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 36
                _h = 43 if (self.isOuter() and _Color == 3) else 7
                pyxel.rect(26 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           9, _h,
                           self.WALLColor_FRONT[_Color])
        if _idx == 6:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 36
                _h = 43 if (self.isOuter() and _Color == 3) else 7
                pyxel.rect(44 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           9, _h,
                           self.WALLColor_FRONT[_Color])
        if _idx == 7:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 36
                _h = 43 if (self.isOuter() and _Color == 3) else 7
                pyxel.rect(35 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           9, _h,
                           self.WALLColor_FRONT[_Color])
            if _data & 0b000000111000 != 0:
                _Color = (_data >> 3) & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 36
                _h = 43 if (self.isOuter() and _Color == 3) else 7
                pyxel.tri(50 + self.DRAW_OFFSET_X, 29 + self.DRAW_OFFSET_Y,
                          44 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y,
                          50 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.tri(44 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y,
                          50 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y,
                          50 + self.DRAW_OFFSET_X, 49 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.rect(44 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           7, _h,
                           self.WALLColor_SIDE[_Color])
            if _data & 0b111000000000 != 0:
                _Color = (_data >> 9) & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 36
                _h = 43 if (self.isOuter() and _Color == 3) else 7
                pyxel.tri(28 + self.DRAW_OFFSET_X, 29 + self.DRAW_OFFSET_Y,
                          34 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y,
                          28 + self.DRAW_OFFSET_X, 35 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.tri(28 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y,
                          34 + self.DRAW_OFFSET_X, 43 + self.DRAW_OFFSET_Y,
                          28 + self.DRAW_OFFSET_X, 49 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.rect(28 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           7, _h,
                           self.WALLColor_SIDE[_Color])

        if _idx == 8:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 29
                _h = 50 if (self.isOuter() and _Color == 3) else 21
                pyxel.rect(5 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           23, _h,
                           self.WALLColor_FRONT[_Color])
        if _idx == 9:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 29
                _h = 50 if (self.isOuter() and _Color == 3) else 21
                pyxel.rect(51 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           23, _h,
                           self.WALLColor_FRONT[_Color])
        if _idx == 10:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 29
                _h = 50 if (self.isOuter() and _Color == 3) else 21
                pyxel.rect(28 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           23, _h,
                           self.WALLColor_FRONT[_Color])
            if _data & 0b000000111000 != 0:
                _Color = (_data >> 3) & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 29
                _h = 50 if (self.isOuter() and _Color == 3) else 21
                pyxel.tri(69 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          51 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y,
                          69 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.tri(51 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y,
                          69 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y,
                          69 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.rect(51 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           19, _h,
                           self.WALLColor_SIDE[_Color])
            if _data & 0b111000000000 != 0:
                _Color = (_data >> 9) & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 29
                _h = 50 if (self.isOuter() and _Color == 3) else 21
                pyxel.tri(9 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          27 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y,
                          9 + self.DRAW_OFFSET_X, 28 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.tri(9 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y,
                          27 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y,
                          9 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.rect(9 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           19, _h,
                           self.WALLColor_SIDE[_Color])

        if _idx == 11:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 10
                _h = 69 if (self.isOuter() and _Color == 3) else 59
                pyxel.rect(0 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           10, _h,
                           self.WALLColor_FRONT[_Color])
        if _idx == 12:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 10
                _h = 69 if (self.isOuter() and _Color == 3) else 59
                pyxel.rect(69 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           10, _h,
                           self.WALLColor_FRONT[_Color])
        if _idx == 13:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 10
                _h = 69 if (self.isOuter() and _Color == 3) else 59
                pyxel.rect(10 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           59, _h,
                           self.WALLColor_FRONT[_Color])
                if _data & 0b00000011 == 0b00000010:
                    pyxel.circ(17 + self.DRAW_OFFSET_X, 40 +
                               self.DRAW_OFFSET_Y, 2, pyxel.Color_BLACK)
            if _data & 0b000000111000 != 0:
                _Color = (_data >> 3) & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 10
                _h = 69 if (self.isOuter() and _Color == 3) else 59
                pyxel.tri(78 + self.DRAW_OFFSET_X, 1 + self.DRAW_OFFSET_Y,
                          69 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          78 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.tri(69 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          78 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          78 + self.DRAW_OFFSET_X, 77 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.rect(69 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           10, _h,
                           self.WALLColor_SIDE[_Color])
            if _data & 0b111000000000 != 0:
                _Color = (_data >> 9) & 0b000000000111
                _y = 0 if (self.isOuter() and _Color == 3) else 10
                _h = 69 if (self.isOuter() and _Color == 3) else 59
                pyxel.tri(0 + self.DRAW_OFFSET_X, 1 + self.DRAW_OFFSET_Y,
                          9 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          0 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.tri(0 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          9 + self.DRAW_OFFSET_X, 68 + self.DRAW_OFFSET_Y,
                          0 + self.DRAW_OFFSET_X, 77 + self.DRAW_OFFSET_Y,
                          self.WALLColor_SIDE[_Color])
                pyxel.rect(0 + self.DRAW_OFFSET_X, _y + self.DRAW_OFFSET_Y,
                           10, _h,
                           self.WALLColor_SIDE[_Color])








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
        super().handler(event)

        if event.type == KEYDOWN:

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
        super().handler(event)

        if event.type == KEYDOWN:

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







