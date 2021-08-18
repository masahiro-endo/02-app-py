

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




class CombatAction:

    _msg: str
    _snd: pygame.mixer.Sound
    
    def __init__(self):
        self._msg = "１１１のダメージ%"
    
class PlayerDicide(CombatAction):
    def __init__(self):
        super().__init__()
        self._snd = pygame.mixer.Sound("./assets/sounds/" + "ステータス治療1.mp3")

class AIDicide(CombatAction):
    def __init__(self):
        super().__init__()
        self._snd = pygame.mixer.Sound("./assets/sounds/" + "剣の素振り2.mp3")




class CombatBattle(BaseScene):

    _actlist: deque = deque()
    _wnd: UI.Window
    _actorimg: pygame.image

    def __init__(self):
        self._wnd = UI.MessageWindow(Rect(0,334,600,140) )
        self._wnd.settext(u"ＥＮＣＯＵＮＴＥＲ！")
        self._wnd.show()

        self._actorimg = control.Method.load_image("./assets/images/npc/", "pngegg(32).png", -1)
        self._actorimg = pygame.transform.scale(self._actorimg, (200, 200))
        self._actorimg = None
        
        self._actlist.appendleft(PlayerDicide())
        self._actlist.appendleft(AIDicide())

    def update(self):
        super().update()
        if len(self._actlist) > 0:
            if not self._actlist[0]._snd is None:
                self._actlist[0]._snd.play()
                self._actlist[0]._snd = None
        self._wnd.update()
                    
    def draw(self, screen):
        super().draw(screen)
        self._wnd.draw(screen)
        if not self._actorimg is None:
            screen.blit(self._actorimg, (200, 100))

    def handler(self, event):
        super().handler(event)
        self._wnd.handler(event)

        if event.type == KEYDOWN:
            
            if self._wnd.is_visible:
                self._wnd.hide()
                
            if event.key == K_SPACE:
                g.currentScene.popleft()

            if event.key == K_RETURN:
                if len(self._actlist) > 0:
                    self._wnd.settext(self._actlist[0]._msg)
                    self._actlist.popleft()




class BaseField(BaseScene):

    # 自分の位置と方向からマップのどこを参照するかを、参照順に定義
    # 参照順のイメージは以下（上向きである前提、自分の位置はDとする）
    # |0|1|4|3|2|
    #   |5|7|6|
    #   |8|A|9|
    #   |B|D|C|
    POS_X = (
        (-2, -1, 2, 1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0),
        (3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
        (2, 1, -2, -1, 0, 1, -1, 0, 1, -1, 0, 1, -1, 0),
        (-3, -3, -3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, 0)
    )
    POS_Y = (
        (-3, -3, -3, -3, -3, -2, -2, -2, -1, -1, -1, 0, 0, 0),
        (-2, -1, 2, 1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0),
        (3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
        (2, 1, -2, -1, 0, 1, -1, 0, 1, -1, 0, 1, -1, 0)
    )

    # 迷路描画の壁の色（正面）
    WALLCOLOR_FRONT = [
        None,
        pygame.Color('lightblue'),
        pygame.Color('blue'),
        pygame.Color('black'),
        pygame.Color('lightblue'),
    ]

    # 迷路描画の壁の色（側面）
    WALLCOLOR_SIDE = [
        None,
        pygame.Color('darkblue'),
        pygame.Color('blue'),
        pygame.Color('black'),
        pygame.Color('darkblue'),
    ]


    _map = field.demotown.floormap

    def __init__(self):
        pass

    def update(self):
        super().update()
                  
    def draw(self, screen):
        super().draw(screen)
        screen.fill((0,0,0))
        lnw = 1

        # 迷路の枠線
        pygame.draw.rect(screen, Color('darkblue'), (self.DRAW_OFFSET_X - 10, self.DRAW_OFFSET_Y - 10, 610, 610), lnw )

        # 地面部のグリッド
        if self.isSky():
            pygame.draw.rect(screen, Color('darkblue'), (self.DRAW_OFFSET_X, self.DRAW_OFFSET_Y, 590, 590 ), lnw )
        else:
            pygame.draw.line(screen, Color('darkblue'), 
                      (   0 + self.DRAW_OFFSET_X, 350 + self.DRAW_OFFSET_Y), 
                      ( 600 + self.DRAW_OFFSET_X, 350 + self.DRAW_OFFSET_Y), lnw )
            pygame.draw.line(screen, Color('darkblue'), 
                      (   0 + self.DRAW_OFFSET_X, 425 + self.DRAW_OFFSET_Y), 
                      ( 600 + self.DRAW_OFFSET_X, 425 + self.DRAW_OFFSET_Y), lnw )
            pygame.draw.line(screen, Color('darkblue'), 
                      (   0 + self.DRAW_OFFSET_X, 550 + self.DRAW_OFFSET_Y), 
                      ( 600 + self.DRAW_OFFSET_X, 550 + self.DRAW_OFFSET_Y), lnw )
            
            pygame.draw.line(screen, Color('darkblue'), 
                      ( 250 + self.DRAW_OFFSET_X, 350 + self.DRAW_OFFSET_Y), 
                      (   0 + self.DRAW_OFFSET_X, 600 + self.DRAW_OFFSET_Y), lnw )
            pygame.draw.line(screen, Color('darkblue'), 
                      ( 350 + self.DRAW_OFFSET_X, 350 + self.DRAW_OFFSET_Y), 
                      ( 600 + self.DRAW_OFFSET_X, 600 + self.DRAW_OFFSET_Y), lnw )


        if self.tick > 0:
            if self.isOuter():
                pass
            else:
                # 天井部のグリッド
                pygame.draw.line(screen, Color('darkblue'), 
                          (   0 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y), 
                          ( 600 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y), lnw )
                pygame.draw.line(screen, Color('darkblue'), 
                          (   0 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y), 
                          ( 600 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y), lnw )
                pygame.draw.line(screen, Color('darkblue'), 
                          (   0 + self.DRAW_OFFSET_X,  50 + self.DRAW_OFFSET_Y), 
                          ( 600 + self.DRAW_OFFSET_X,  50 + self.DRAW_OFFSET_Y), lnw )
                
                pygame.draw.line(screen, Color('darkblue'), 
                          ( 250 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y), 
                          (   0 + self.DRAW_OFFSET_X,   0 + self.DRAW_OFFSET_Y), lnw )
                pygame.draw.line(screen, Color('darkblue'), 
                          ( 350 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y), 
                          ( 600 + self.DRAW_OFFSET_X,   0 + self.DRAW_OFFSET_Y), lnw )


            # 迷路
            self.draw_maze(screen, g.playerParty.x, g.playerParty.y,
                          g.playerParty.direction, self._map)

            # self.draw_minimap(screen, g.playerParty.x, g.playerParty.y,
            #               g.playerParty.direction, self._map)



    def handler(self, event):
        super().handler(event)

        if event.type == KEYDOWN:

            if event.key == K_RIGHT:
                self.tick = 0
                g.playerParty.turnRight()
                return

            if event.key == K_LEFT:
                self.tick = 0
                g.playerParty.turnLeft()
                return

            if event.key == K_DOWN:
                self.tick = 0
                g.playerParty.turnBack()
                return

            if event.key == K_UP:
                if self.can_move_forward(self._map, g.playerParty.x, g.playerParty.y, g.playerParty.direction):
                    self.tick = 0
                    g.playerParty.moveForward()
                    if __debug__:
                        print("g.playerParty.moveForward")

                    if self.doEncounted():
                        self.tick = 0
                        g.currentScene.appendleft(CombatBattle())
                        return

                else:
                    # pyxel.play(3, 6)
                    self.cntOops = 20
                    pygame.time.set_timer(g.USREVENT_OOPS, 10)


    def can_move_forward(self, _map, _x: int, _y: int, _direction: int) -> bool:
        '''
        前進できるかを判定する。\n
        マップデータを方向によりシフトした結果の下位1ビットが立っている（＝目の前の壁情報が通行不可）場合は、前進不可と判定する。
        '''
        # _value = self.get_mapinfo(_map, _x, _y, _direction)
        _value = _map[ _y + self.POS_Y[_direction][10] ][ _x + self.POS_X[_direction][10] ]

        if _value & 0b000000000001 == 0b000000000001:
            return False
        else:
            return True

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

    def doEncounted(self) -> bool:
        '''
        エンカウントしたかを返却する\n
        出現確率を変更する場合は、継承先クラスでオーバーライドする。
        '''
        if random.randint(0, 1) == 0:
            return True
        else:
            return False

    def draw_isotri(self, screen, x, y, edge, angle):
        ok = edge/2/math.sqrt(3)
        r = math.radians(angle)         #---ラジアンに変換

        x1, y1 = -edge/2, ok
        x2, y2 = edge/2, ok
        x3, y3 = 0, -ok*2

        #---angle度回転時の座標
        point1 = [(x1*math.cos(r)-y1*math.sin(r))+x,
                (x1*math.sin(r)+y1*math.cos(r))+y]
        point2 = [(x2*math.cos(r)-y2*math.sin(r))+x,
                (x2*math.sin(r)+y2*math.cos(r))+y]
        point3 = [(x3*math.cos(r)-y3*math.sin(r))+x,
                (x3*math.sin(r)+y3*math.cos(r))+y]

        #---描画
        pygame.draw.polygon(screen, Color('white'), 
                   [ ( point1[0] + self.DRAW_OFFSET_X, point1[1] +  self.DRAW_OFFSET_Y ),
                     ( point2[0] + self.DRAW_OFFSET_X, point2[1] +  self.DRAW_OFFSET_Y ), 
                     ( point3[0] + self.DRAW_OFFSET_X, point3[1] +  self.DRAW_OFFSET_Y ) ] )
        pygame.draw.circle(screen, Color('blue'),(point3[0], point3[1]), 2 )

    '''
    def draw_minimap(self, screen, _x, _y, _direction, _map):

        lnw = 0
        _cpos = (_x ,_y)
        
        pygame.draw.rect(screen, pygame.Color('black'), 
               ( 600 + self.DRAW_OFFSET_X,  0 + self.DRAW_OFFSET_Y,
                 200 , 200 ), lnw)

        for i in range(10):
            _get_x = _x - 5 + i
            if _get_x < 0 or _get_x > len(_map) - 1:
                pass
            else:
                for j in range(10):
                    _get_y = _y - 5 + j
                    if _get_y < 0 or _get_y > len(_map) - 1:
                        pass
                    else:
                        _getpos = (_get_x , _get_y)
                        _data = _map[_y - 5 + j][_x - 5 + i]

                        if _data & 0b000000000001 == 0b000000000001:
                            _Color = pygame.Color('black')
                        else:
                            _Color = pygame.Color('gray')

                        pygame.draw.rect(screen, _Color, 
                             ( 600 + (i * 20) + self.DRAW_OFFSET_X,   0 + (j * 20) + self.DRAW_OFFSET_Y,
                                20 , 20 ), lnw)

                        if _cpos == _getpos:
                            self.draw_isotri(screen, 
                                    610 + (i * 20) + self.DRAW_OFFSET_X , 
                                     10 + (j * 20) + self.DRAW_OFFSET_Y ,
                                    15, 90 * _direction )
    '''


    def draw_maze(self, screen, _x, _y, _direction, _map):
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

            self.draw_wall(screen, i, _data)

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
        # if _direction > const.Direction.NORTH:
        #     for _ in range(_direction):
        #         _data = self.__right_3bit_rotate(_data)
        return _data

    def line_symmetry(self, pos, cpos):
        return ( pos[0] + ( (cpos[0] - pos[0]) * 2 ) )

    def draw_wall(self, screen, _idx, _data):
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
        lnw = 0

        if _idx == 1:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      ( 150 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y,
                        100 , 100 ), lnw)
                # pygame.draw.polygon(screen, self.WALLCOLOR_SIDE[_Color], 
                #          [ ( 250 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y ),
                #            ( 300 + self.DRAW_OFFSET_X, 300 + self.DRAW_OFFSET_Y ), 
                #            ( 250 + self.DRAW_OFFSET_X, 350 + self.DRAW_OFFSET_Y ) ], lnw)

        if _idx == 3:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      ( 350 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y,
                        100 , 100 ), lnw)
                # pygame.draw.polygon(screen, self.WALLCOLOR_SIDE[_Color], 
                #          [ ( 350 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y ),
                #            ( 350 + self.DRAW_OFFSET_X, 350 + self.DRAW_OFFSET_Y ), 
                #            ( 300 + self.DRAW_OFFSET_X, 300 + self.DRAW_OFFSET_Y ) ], lnw)

        if _idx == 4:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      ( 250 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y,
                        100 , 100 ), lnw)



        if _idx == 5:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      (   0 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y, 
                        175 , 250 ), lnw)
                pygame.draw.polygon(screen, self.WALLCOLOR_SIDE[_Color], 
                         [ ( 175 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y ),
                           ( 250 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y ), 
                           ( 250 + self.DRAW_OFFSET_X, 350 + self.DRAW_OFFSET_Y ), 
                           ( 175 + self.DRAW_OFFSET_X, 425 + self.DRAW_OFFSET_Y ) ], lnw)

        if _idx == 6:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      ( 425 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y, 
                        175 , 250 ), lnw)
                pygame.draw.polygon(screen, self.WALLCOLOR_SIDE[_Color], 
                         [ ( 350 + self.DRAW_OFFSET_X, 250 + self.DRAW_OFFSET_Y ),
                           ( 425 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y ), 
                           ( 425 + self.DRAW_OFFSET_X, 425 + self.DRAW_OFFSET_Y ), 
                           ( 350 + self.DRAW_OFFSET_X, 350 + self.DRAW_OFFSET_Y ) ], lnw)

        if _idx == 7:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      ( 175 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y, 
                        250 , 250 ), lnw)



        if _idx == 8:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      (  0 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y, 
                        50, 500 ), lnw)
                pygame.draw.polygon(screen, self.WALLCOLOR_SIDE[_Color], 
                         [ (  50 + self.DRAW_OFFSET_X,  50 + self.DRAW_OFFSET_Y ),
                           ( 175 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y ), 
                           ( 175 + self.DRAW_OFFSET_X, 425 + self.DRAW_OFFSET_Y ), 
                           (  50 + self.DRAW_OFFSET_X, 550 + self.DRAW_OFFSET_Y ) ], lnw)

        if _idx == 9:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      ( 550 + self.DRAW_OFFSET_X, 50 + self.DRAW_OFFSET_Y, 
                        50, 500 ), lnw)
                pygame.draw.polygon(screen, self.WALLCOLOR_SIDE[_Color], 
                         [ ( 425 + self.DRAW_OFFSET_X, 175 + self.DRAW_OFFSET_Y ),
                           ( 550 + self.DRAW_OFFSET_X,  50 + self.DRAW_OFFSET_Y ), 
                           ( 550 + self.DRAW_OFFSET_X, 550 + self.DRAW_OFFSET_Y ), 
                           ( 425 + self.DRAW_OFFSET_X, 425 + self.DRAW_OFFSET_Y ) ], lnw)

        if _idx == 10:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                      (  50 + self.DRAW_OFFSET_X,  50 + self.DRAW_OFFSET_Y, 
                        500, 500 ), lnw)



        if _idx == 11:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.polygon(screen, self.WALLCOLOR_SIDE[_Color], 
                         [ (  0 + self.DRAW_OFFSET_X,   0 + self.DRAW_OFFSET_Y ),
                           ( 50 + self.DRAW_OFFSET_X,  50 + self.DRAW_OFFSET_Y ), 
                           ( 50 + self.DRAW_OFFSET_X, 550 + self.DRAW_OFFSET_Y ), 
                           (  0 + self.DRAW_OFFSET_X, 600 + self.DRAW_OFFSET_Y ) ], lnw)

        if _idx == 12:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                pygame.draw.polygon(screen, self.WALLCOLOR_SIDE[_Color], 
                         [ ( 550 + self.DRAW_OFFSET_X,  50 + self.DRAW_OFFSET_Y ),
                           ( 600 + self.DRAW_OFFSET_X,   0 + self.DRAW_OFFSET_Y ), 
                           ( 600 + self.DRAW_OFFSET_X, 600 + self.DRAW_OFFSET_Y ), 
                           ( 550 + self.DRAW_OFFSET_X, 550 + self.DRAW_OFFSET_Y ) ], lnw)

        if _idx == 13:
            if _data & 0b000000000111 != 0:
                _Color = _data & 0b000000000111
                # pygame.draw.rect(screen, self.WALLCOLOR_FRONT[_Color], 
                #       ( 10 + self.DRAW_OFFSET_X, 10 + self.DRAW_OFFSET_Y, 
                #         59, 59 ), lnw)

                # if _data & 0b00000011 == 0b00000010:
                #     pygame.draw.circle(screen, self.WALLCOLOR_FRONT[_Color], 
                #        ( 17 + self.DRAW_OFFSET_X, 40 + self.DRAW_OFFSET_Y ) , 2, lnw)







