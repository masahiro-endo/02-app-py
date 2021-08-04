

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
import floor
import const
import global_value as g





class Character(object):
    '''
    キャラクタの基底クラス
    '''

    def __init__(self):
        '''
        クラス初期化
        '''
        self.name = ""
        self.level = 0
        self.maxlife = 0
        self.life = 0
        self.strength = 0
        self.defend = 0
        self.dexterity = 0
        self.exp = 0
        self.gold = 0
        self.isEscape = False
        self.isPlayer = False
        self.blt_w = 0
        self.bly_h = 0
        self.x = 0
        self.y = 0
        self.hasItem = False

    def setDisplayPosition(self, _count: int, _idx: int) -> None:
        '''
        敵キャラクターの表示位置を算出して設定する。\n
        引数として、敵パーティーのメンバー総数と、対象キャラクターのインデックスを指定する。
        '''
        if _count < 12:
            _x_step = (104 - self.blt_w) / (_count + 1)
            self.x = 132 + ((_idx + 1) * _x_step)
        else:
            if _idx < 12:
                _x_step = (104 - self.blt_w) / 11
                self.x = 132 + ((_idx + 1) * _x_step)
            else:
                _x_step = (104 - self.blt_w) / ((_count - 12) + 1)
                self.x = 132 + (((_idx - 12) + 1) * _x_step)
        if isinstance(self, Monster) and self.blt_h == 32:
            self.y = 98
        else:
            self.y = random.randint(100, (128 - self.blt_h)) if _count < 12 else (
                random.randint(100, (128 - self.blt_h)) if _idx < 12 else random.randint(110, (132 - self.blt_h)))




class Party(object):
    '''
    パーティーを管理するクラス

    Characterクラスの派生クラスを格納したListを管理する
    リストに登録するCharacterの上限はない
    このクラスを直接使用せず、派生クラスのplayerParty、enemyPartyを使用すること
    '''

    # パーティーメンバーのリスト
    memberList = []

    def __init__(self):
        '''
        クラス初期化
        '''
        # パーティーメンバーのリスト
        self.memberList = []

    def addMember(self, chr: Character) -> None:
        '''
        パーティーメンバー追加
        '''
        self.memberList.append(chr)

    def removeMember(self, idx: int) -> None:
        '''
        パーティーメンバー削除

        削除したいパーティーメンバーのリストのインデックスを指定する
        リストに存在しないインデックスを指定した場合は、Exceptionが発生する
        '''
        try:
            del self.memberList[idx]
        except:
            raise Exception(
                "specified a member who doesn't exist.：" + str(idx))


class PlayerParty(Party):
    '''
    プレイヤーパーティーのクラス

    Partyクラスを継承
    Humanクラスを格納したListを管理する
    リストに登録するHumanの上限は5とする
    直接このクラスを使用せず、インスタンスを格納したplayerPartyをimportして使用すること
    '''
    eventFlg = [0] * 256

    def __init__(self):
        '''
        クラス初期化
        '''
        super().__init__()

        # 方向に対する増分
        self.VX = (0, 1, 0, -1)
        self.VY = (-1, 0, 1, 0)

        # プレイヤーパーティーの位置と方向
        self.x = 0
        self.y = 0
        self.direction = 0

        # プレイヤーパーティーの直前の位置と方向
        self.x_save = 0
        self.y_save = 0
        self.direction_save = 0

        # 状況のフラグ
        self.isEscaped = False

        # イベントフラグ
        self.eventFlg = [0] * 100

        if __debug__:
            print("PlayerParty : Initialized.")

    def saveCondition(self) -> None:
        '''
        状態を保存する
        '''
        self.x_save = self.x
        self.y_save = self.y
        self.direction_save = self.direction
        if __debug__:
            print("PlayerParty : Condition saved. x={:02d}".format(
                self.x_save) + ",y={:02d}".format(self.y_save) + ",direction={:01d}".format(self.direction_save))

    def restoreCondition(self) -> None:
        '''
        状態を復元する
        '''
        self.x = self.x_save
        self.y = self.y_save
        self.direction = self.direction_save
        if __debug__:
            print("PlayerParty : Condition restored. x={:02d}".format(
                self.x) + ",y={:02d}".format(self.y) + ",direction={:01d}".format(self.direction))

    def turnLeft(self) -> None:
        '''
        左を向く
        '''
        # 状態を保存
        self.saveCondition()
        # 方向を変える
        self.direction -= 1
        if self.direction < const.Direction.NORTH:
            self.direction = const.Direction.WEST

    def turnRight(self) -> None:
        '''
        右を向く
        '''
        # 状態を保存
        self.saveCondition()
        # 方向を変える
        self.direction += 1
        if self.direction > const.Direction.WEST:
            self.direction = const.Direction.NORTH

    def turnBack(self) -> None:
        '''
        後ろを向く
        '''
        # 状態を保存
        self.saveCondition()
        # 方向を変える
        self.direction = (self.direction + 2) % 4

    def moveForward(self) -> None:
        '''
        前に進む
        '''
        # 状態を保存
        self.saveCondition()
        # 座標を変更
        self.x = self.x + self.VX[self.direction]
        self.y = self.y + self.VY[self.direction]


g.playerParty: PlayerParty







class CCharacter:
    """一般キャラクタークラス"""
    speed = 4  # 1フレームの移動ピクセル数
    animcycle = 24  # アニメーション速度
    frame = 0
    # キャラクターイメージ（mainで初期化）
    # キャラクター名 -> 分割画像リストの辞書
    images = {}
    def __init__(self, name, pos, dir, movetype, message):
        self.name = name  # キャラクター名（ファイル名と同じ）
        self.image = self.images[name][0]  # 描画中のイメージ
        self.x, self.y = pos[0], pos[1]  # 座標（単位：マス）
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.vx, self.vy = 0, 0  # 移動速度
        self.moving = False  # 移動中か？
        self.direction = dir  # 向き
        self.movetype = movetype  # 移動タイプ
        self.message = message  # メッセージ
    def update(self, map):
        """キャラクター状態を更新する。
        mapは移動可能かの判定に必要。"""
        # プレイヤーの移動処理
        if self.moving == True:
            # ピクセル移動中ならマスにきっちり収まるまで移動を続ける
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  # マスにおさまったら移動完了
                self.moving = False
                self.x = int(self.rect.left / GS)
                self.y = int(self.rect.top / GS)
        elif self.movetype == MOVE and random.random() < PROB_MOVE:
            # 移動中でないならPROB_MOVEの確率でランダム移動開始
            self.direction = random.randint(0, 3)  # 0-3のいずれか
            if self.direction == DOWN:
                if map.is_movable(self.x, self.y+1):
                    self.vx, self.vy = 0, self.speed
                    self.moving = True
            elif self.direction == LEFT:
                if map.is_movable(self.x-1, self.y):
                    self.vx, self.vy = -self.speed, 0
                    self.moving = True
            elif self.direction == RIGHT:
                if map.is_movable(self.x+1, self.y):
                    self.vx, self.vy = self.speed, 0
                    self.moving = True
            elif self.direction == UP:
                if map.is_movable(self.x, self.y-1):
                    self.vx, self.vy = 0, -self.speed
                    self.moving = True
        # キャラクターアニメーション（frameに応じて描画イメージを切り替える）
        self.frame += 1
        self.image = self.images[self.name][int(self.direction*4+self.frame/self.animcycle%4)]
    def draw(self, screen, offset):
        """オフセットを考慮してプレイヤーを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
    def set_pos(self, x, y, dir):
        """キャラクターの位置と向きをセット"""
        self.x, self.y = x, y
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
        self.direction = dir
    def __str__(self):
        return "CHARA,%s,%d,%d,%d,%d,%s" % (self.name,self.x,self.y,self.direction,self.movetype,self.message)

class Player(Character):
    """プレイヤークラス"""
    def __init__(self, name, pos, dir, leader, party):
        Character.__init__(self, name, pos, dir, False, None)
        self.leader = leader
        self.party = party
    def update(self, map, battle):
        """プレイヤー状態を更新する。
        mapは移動可能かの判定に必要。
        battleはエンカウントに必要。"""
        global game_state
        # プレイヤーの移動処理
        if self.moving == True:
            # ピクセル移動中ならマスにきっちり収まるまで移動を続ける
            self.rect.move_ip(self.vx, self.vy)
            if self.rect.left % GS == 0 and self.rect.top % GS == 0:  # マスにおさまったら移動完了
                self.moving = False
                self.x = int(self.rect.left / GS)
                self.y = int(self.rect.top / GS)
                if not self.leader: return  # リーダーでなければイベントは無視
                event = map.get_event(self.x, self.y)
                if isinstance(event, MoveEvent):  # MoveEventなら
                    sounds["step"].play()
                    dest_map = event.dest_map
                    dest_x = event.dest_x
                    dest_y = event.dest_y
                    map.create(dest_map)
                    # パーティの全員を移動先マップへ
                    for player in self.party.member:
                        player.set_pos(dest_x, dest_y, DOWN)  # プレイヤーを移動先座標へ
                        player.moving = False
                # エンカウント発生
                if map.name == "field" and random.random() < PROB_ENCOUNT:
                    game_state = BATTLE_INIT
                    battle.start()
        # キャラクターアニメーション（frameに応じて描画イメージを切り替える）
        self.frame += 1
        self.image = self.images[self.name][int(self.direction*4+self.frame/self.animcycle%4)]
    def move_to(self, destx, desty):
        """現在位置から(destx,desty)への移動を開始"""
        dx = destx - self.x
        dy = desty - self.y
        # 向きを変える
        if dx == 1: self.direction = RIGHT
        elif dx == -1: self.direction = LEFT
        elif dy == -1: self.direction = UP
        elif dy == 1: self.direction = DOWN
        # 速度をセット
        self.vx, self.vy = dx*self.speed, dy*self.speed
        # 移動開始
        self.moving = True
    def talk(self, map):
        """キャラクターが向いている方向のとなりにキャラクターがいるか調べる"""
        # 向いている方向のとなりの座標を求める
        nextx, nexty = self.x, self.y
        if self.direction == DOWN:
            nexty = self.y + 1
            event = map.get_event(nextx, nexty)
            if isinstance(event, Object) and event.mapchip == 41:
                nexty += 1  # テーブルがあったらさらに隣
        elif self.direction == LEFT:
            nextx = self.x - 1
            event = map.get_event(nextx, nexty)
            if isinstance(event, Object) and event.mapchip == 41:
                nextx -= 1
        elif self.direction == RIGHT:
            nextx = self.x + 1
            event = map.get_event(nextx, nexty)
            if isinstance(event, Object) and event.mapchip == 41:
                nextx += 1
        elif self.direction == UP:
            nexty = self.y - 1
            event = map.get_event(nextx, nexty)
            if isinstance(event, Object) and event.mapchip == 41:
                nexty -= 1
        # その方向にキャラクターがいるか？
        chara = map.get_chara(nextx, nexty)
        # キャラクターがいればプレイヤーの方向へ向ける
        if chara != None:
            if self.direction == DOWN:
                chara.direction = UP
            elif self.direction == LEFT:
                chara.direction = RIGHT
            elif self.direction == RIGHT:
                chara.direction = LEFT
            elif self.direction == UP:
                chara.direction = DOWN
            chara.update(map)  # 向きを変えたので更新
        return chara
    def search(self, map):
        """足もとに宝箱があるか調べる"""
        event = map.get_event(self.x, self.y)
        if isinstance(event, Treasure):
            return event
        return None
    def open(self, map):
        """目の前にとびらがあるか調べる"""
        # 向いている方向のとなりの座標を求める
        nextx, nexty = self.x, self.y
        if self.direction == DOWN:
            nexty = self.y + 1
        elif self.direction == LEFT:
            nextx = self.x - 1
        elif self.direction == RIGHT:
            nextx = self.x + 1
        elif self.direction == UP:
            nexty = self.y - 1
        # その場所にとびらがあるか？
        event = map.get_event(nextx, nexty)
        if isinstance(event, Door):
            return event
        return None

class Party:
    def __init__(self):
        # Partyのメンバーリスト
        self.member = []
    def add(self, player):
        """Partyにplayerを追加"""
        self.member.append(player)
    def update(self, map, battle):
        # Party全員を更新
        for player in self.member:
            player.update(map, battle)
        # 移動中でないときにキー入力があったらParty全員を移動開始
        if not self.member[0].moving:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_DOWN]:
                # 先頭キャラは移動できなくても向きは変える
                self.member[0].direction = DOWN
                # 先頭キャラが移動できれば
                if map.is_movable(self.member[0].x, self.member[0].y+1):
                    # 後ろにいる仲間から1つ前の仲間の位置へ移動開始
                    for i in range(len(self.member)-1,0,-1):
                        self.member[i].move_to(self.member[i-1].x,self.member[i-1].y)
                    # 先頭キャラを最後に移動開始
                    self.member[0].move_to(self.member[0].x,self.member[0].y+1)
            elif pressed_keys[K_LEFT]:
                self.member[0].direction = LEFT
                if map.is_movable(self.member[0].x-1, self.member[0].y):
                    for i in range(len(self.member)-1,0,-1):
                        self.member[i].move_to(self.member[i-1].x,self.member[i-1].y)
                    self.member[0].move_to(self.member[0].x-1,self.member[0].y)
            elif pressed_keys[K_RIGHT]:
                self.member[0].direction = RIGHT
                if map.is_movable(self.member[0].x+1, self.member[0].y):
                    for i in range(len(self.member)-1,0,-1):
                        self.member[i].move_to(self.member[i-1].x,self.member[i-1].y)
                    self.member[0].move_to(self.member[0].x+1,self.member[0].y)
            elif pressed_keys[K_UP]:
                self.member[0].direction = UP
                if map.is_movable(self.member[0].x, self.member[0].y-1):
                    for i in range(len(self.member)-1,0,-1):
                        self.member[i].move_to(self.member[i-1].x,self.member[i-1].y)
                    self.member[0].move_to(self.member[0].x,self.member[0].y-1)
    def draw(self, screen, offset):
        # Partyの全員を描画
        # 重なったとき先頭キャラが表示されるように後ろの人から描画
        for player in self.member[::-1]:
            player.draw(screen, offset)




