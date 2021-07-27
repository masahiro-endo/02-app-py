#!/usr/bin/env python
import pygame
from pygame.locals import *
import codecs
import os
import random
import struct
import sys
os.chdir(os.path.dirname(__file__))


SCR_RECT = Rect(0, 0, 640, 480)
GS = 32
DOWN,LEFT,RIGHT,UP = 0,1,2,3
STOP, MOVE = 0, 1  # 移動タイプ
PROB_MOVE = 0.005  # 移動確率
PROB_ENCOUNT = 0.05  # エンカウント確率
TRANS_COLOR = (190,179,145)  # マップチップの透明色

sounds = {}  # サウンド

TITLE, FIELD, TALK, COMMAND, BATTLE_INIT, BATTLE_COMMAND, BATTLE_PROCESS = range(7)


class PyRPG:
    def __init__(self):
        pygame.init()
        # フルスクリーン化 + Hardware Surface使用
        self.screen = pygame.display.set_mode(SCR_RECT.size, DOUBLEBUF|HWSURFACE|FULLSCREEN)
        pygame.display.set_caption("PyRPG 27 戦闘画面")
        # サウンドをロード
        self.load_sounds("data", "sound.dat")
        # キャラクターチップをロード
        self.load_charachips("data", "charachip.dat")
        # マップチップをロード
        self.load_mapchips("data", "mapchip.dat")
        # パーティの作成
        self.party = Party()
        player1 = Player("swordman_female", (3,5), DOWN, True, self.party)
        player2 = Player("elf_female2", (3,4), DOWN, False, self.party)
        player3 = Player("priestess", (3,3), DOWN, False, self.party)
        player4 = Player("magician_female", (3,2), DOWN, False, self.party)
        self.party.add(player1)
        self.party.add(player2)
        self.party.add(player3)
        self.party.add(player4)
        # マップの作成
        self.map = Map("field", self.party)
        # メッセージエンジン
        self.msg_engine = MessageEngine()
        # メッセージウィンドウ
        self.msgwnd = MessageWindow(Rect(140,334,360,140), self.msg_engine)
        # コマンドウィンドウ
        self.cmdwnd = CommandWindow(Rect(16,16,216,160), self.msg_engine)
        # タイトル画面
        self.title = Title(self.msg_engine)
        # 戦闘画面
        self.battle = Battle(self.msgwnd, self.msg_engine)
        # メインループを起動
        global game_state
        game_state = TITLE
        self.mainloop()
    def mainloop(self):
        """メインループ"""
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()             # ゲーム状態の更新
            self.render()             # ゲームオブジェクトのレンダリング
            pygame.display.update()  # 画面に描画
            self.check_event()        # イベントハンドラ
    def update(self):
        """ゲーム状態の更新"""
        global game_state
        if game_state == TITLE:
            self.title.update()
        elif game_state == FIELD:
            self.map.update()
            self.party.update(self.map, self.battle)
        elif game_state == TALK:
            self.msgwnd.update()
        elif game_state == BATTLE_INIT or game_state == BATTLE_COMMAND or game_state == BATTLE_PROCESS:
            self.battle.update()
            self.msgwnd.update()
    def render(self):
        """ゲームオブジェクトのレンダリング"""
        global game_state
        if game_state == TITLE:
            self.title.draw(self.screen)
        elif game_state == FIELD or game_state == TALK or game_state == COMMAND:
            offset = self.calc_offset(self.party.member[0])
            self.map.draw(self.screen, offset)
            self.party.draw(self.screen, offset)
            self.msgwnd.draw(self.screen)
            self.cmdwnd.draw(self.screen)
            self.show_info()
        elif game_state in (BATTLE_INIT, BATTLE_COMMAND, BATTLE_PROCESS):
            self.battle.draw(self.screen)
            self.msgwnd.draw(self.screen)
    def check_event(self):
        """イベントハンドラ"""
        global game_state
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            # 表示されているウィンドウに応じてイベントハンドラを変更
            if game_state == TITLE:
                self.title_handler(event)
            elif game_state == FIELD:
                self.field_handler(event)
            elif game_state == COMMAND:
                self.cmd_handler(event)
            elif game_state == TALK:
                self.talk_handler(event)
            elif game_state == BATTLE_INIT:
                self.battle_init_handler(event)
            elif game_state == BATTLE_COMMAND:
                self.battle_cmd_handler(event)
            elif game_state == BATTLE_PROCESS:
                self.battle_proc_handler(event)
    def title_handler(self, event):
        """タイトル画面のイベントハンドラ"""
        global game_state
        if event.type == KEYUP and event.key == K_UP:
            self.title.menu -= 1
            if self.title.menu < 0:
                self.title.menu = 0
        elif event.type == KEYDOWN and event.key == K_DOWN:
            self.title.menu += 1
            if self.title.menu > 2:
                self.title.menu = 2
        if event.type == KEYDOWN and event.key == K_SPACE:
            sounds["pi"].play()
            if self.title.menu == Title.START:
                game_state = FIELD
                self.map.create("field")  # フィールドマップへ
            elif self.title.menu == Title.CONTINUE:
                pass
            elif self.title.menu == Title.EXIT:
                pygame.quit()
                sys.exit()
    def field_handler(self, event):
        """フィールド画面のイベントハンドラ"""
        global game_state
        # スペースキーでコマンドウィンドウ表示
        if event.type == KEYDOWN and event.key == K_SPACE:
            sounds["pi"].play()
            self.cmdwnd.show()
            game_state = COMMAND
    def cmd_handler(self, event):
        """コマンドウィンドウが開いているときのイベントハンドラ"""
        global game_state
        player = self.party.member[0]  # 先頭プレイヤー
        # 矢印キーでコマンド選択
        if event.type == KEYDOWN and event.key == K_LEFT:
            if self.cmdwnd.command <= 3: return
            self.cmdwnd.command -= 4
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if self.cmdwnd.command >= 4: return
            self.cmdwnd.command += 4
        elif event.type == KEYUP and event.key == K_UP:
            if self.cmdwnd.command == 0 or self.cmdwnd.command == 4: return
            self.cmdwnd.command -= 1
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if self.cmdwnd.command == 3 or self.cmdwnd.command == 7: return
            self.cmdwnd.command += 1
        # スペースキーでコマンド実行
        if event.type == KEYDOWN and event.key == K_SPACE:
            if self.cmdwnd.command == CommandWindow.TALK:  # はなす
                sounds["pi"].play()
                self.cmdwnd.hide()
                chara = player.talk(self.map)
                if chara != None:
                    self.msgwnd.set(chara.message)
                    game_state = TALK
                else:
                    self.msgwnd.set("そのほうこうには　だれもいない。")
                    game_state = TALK
            elif self.cmdwnd.command == CommandWindow.STATUS:  # つよさ
                # TODO: ステータスウィンドウ表示
                sounds["pi"].play()
                self.cmdwnd.hide()
                self.msgwnd.set("つよさウィンドウが　ひらくよてい。")
                game_state = TALK
            elif self.cmdwnd.command == CommandWindow.EQUIPMENT:  # そうび
                # TODO: そうびウィンドウ表示
                sounds["pi"].play()
                self.cmdwnd.hide()
                self.msgwnd.set("そうびウィンドウが　ひらくよてい。")
                game_state = TALK
            elif self.cmdwnd.command == CommandWindow.DOOR:  # とびら
                sounds["pi"].play()
                self.cmdwnd.hide()
                door = player.open(self.map)
                if door != None:
                    door.open()
                    self.map.remove_event(door)
                    game_state = FIELD
                else:
                    self.msgwnd.set("そのほうこうに　とびらはない。")
                    game_state = TALK
            elif self.cmdwnd.command == CommandWindow.SPELL:  # じゅもん
                # TODO: じゅもんウィンドウ表示
                sounds["pi"].play()
                self.cmdwnd.hide()
                self.msgwnd.set("じゅもんウィンドウが　ひらくよてい。")
                game_state = TALK
            elif self.cmdwnd.command == CommandWindow.ITEM:  # どうぐ
                # TODO: どうぐウィンドウ表示
                sounds["pi"].play()
                self.cmdwnd.hide()
                self.msgwnd.set("どうぐウィンドウが　ひらくよてい。")
                game_state = TALK
            elif self.cmdwnd.command == CommandWindow.TACTICS:  # さくせん
                # TODO: さくせんウィンドウ表示
                sounds["pi"].play()
                self.cmdwnd.hide()
                self.msgwnd.set("さくせんウィンドウが　ひらくよてい。")
                game_state = TALK
            elif self.cmdwnd.command == CommandWindow.SEARCH:  # しらべる
                sounds["pi"].play()
                self.cmdwnd.hide()
                treasure = player.search(self.map)
                if treasure != None:
                    treasure.open()
                    self.msgwnd.set("%s　をてにいれた。" % treasure.item)
                    game_state = TALK
                    self.map.remove_event(treasure)
                else:
                    self.msgwnd.set("しかし　なにもみつからなかった。")
                    game_state = TALK
    def calc_offset(self, player):
        """オフセットを計算する"""
        offsetx = int(player.rect.topleft[0] - SCR_RECT.width/2)
        offsety = int(player.rect.topleft[1] - SCR_RECT.height/2)
        return offsetx, offsety
    def show_info(self):
        """デバッグ情報を表示"""
        player = self.party.member[0]  # 先頭プレイヤー
        self.msg_engine.draw_string(self.screen, (300,10), self.map.name.upper())  # マップ名
        self.msg_engine.draw_string(self.screen, (300,40), player.name.upper())  # プレイヤー名
        self.msg_engine.draw_string(self.screen, (300,70), "%d_%d" % (player.x, player.y))  # プレイヤー座標



class Item:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def retrieve_from_api(cls, id):
        res = requests.get(f"https://api.example.com/items/{id}")
        data = res.json()
        return cls(id, data["name"])


def FunctionObject(fnc):
    fnc()


class Handler:
    def __init__(self)->None:
        pass
    @classmethod
    def handler(cls, event: pygame.event):
        return cls(*args)


class TalkHandler(Handler):
    def handler(self, event: pygame.event)->None:
        """会話中のイベントハンドラ"""
        global game_state
        # スペースキーでメッセージウィンドウを次のページへ
        # なかった場合、フィールド状態へ戻る
        if event.type == KEYDOWN and event.key == K_SPACE:
            if not self.msgwnd.next():
                game_state = FIELD

class BattleInitHandler(Handler):
    def handler(self, event):
        """戦闘開始のイベントハンドラ"""
        global game_state
        if event.type == KEYDOWN and event.key == K_SPACE:
            self.msgwnd.hide()
            sounds["pi"].play()
            self.battle.cmdwnd.show()
            for bsw in self.battle.status_wnd:
                bsw.show()
            game_state = BATTLE_COMMAND
    def battle_cmd_handler(self, event):
        """戦闘コマンドウィンドウが出ているときのイベントハンドラ"""
        global game_state
        # バトルコマンドのカーソル移動
        if event.type == KEYUP and event.key == K_UP:
            if self.battle.cmdwnd.command == 0: return
            self.battle.cmdwnd.command -= 1
        elif event.type == KEYDOWN and event.key == K_DOWN:
            if self.battle.cmdwnd.command == 3: return
            self.battle.cmdwnd.command += 1
        # バトルコマンドの決定
        if event.type == KEYDOWN and event.key == K_SPACE:
            sounds["pi"].play()
            if self.battle.cmdwnd.command == BattleCommandWindow.ATTACK:  # たたかう
                self.msgwnd.set("ちょっっ　まじで？/ＬＶ１でたおせるわけないよう。/じっそうしてないから　かんべんして。")
            elif self.battle.cmdwnd.command == BattleCommandWindow.SPELL:  # じゅもん
                self.msgwnd.set("じゅもんを　おぼえていない。")
            elif self.battle.cmdwnd.command == BattleCommandWindow.ITEM:  # どうぐ
                self.msgwnd.set("どうぐを　もっていない。")
            elif self.battle.cmdwnd.command == BattleCommandWindow.ESCAPE:  # にげる
                self.msgwnd.set("けんしたちは　にげだした。")
            self.battle.cmdwnd.hide()
            game_state = BATTLE_PROCESS
    def battle_proc_handler(self, event):
        global game_state
        if event.type == KEYDOWN and event.key == K_SPACE:
            self.msgwnd.hide()
            if self.battle.cmdwnd.command == BattleCommandWindow.ESCAPE:
                # フィールドへ戻る
                self.map.play_bgm()
                game_state = FIELD
            else:
                # コマンド選択画面へ戻る
                self.battle.cmdwnd.show()
                game_state = BATTLE_COMMAND




class MessageEngine:
    FONT_WIDTH = 16
    FONT_HEIGHT = 22
    WHITE, RED, GREEN, BLUE = 0, 160, 320, 480
    def __init__(self):
        self.image = load_image("data", "font.png", -1)
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


class MoveEvent():
    """移動イベント"""
    def __init__(self, pos, mapchip, dest_map, dest_pos):
        self.x, self.y = pos[0], pos[1]  # イベント座標
        self.mapchip = mapchip  # マップチップ
        self.dest_map = dest_map  # 移動先マップ名
        self.dest_x, self.dest_y = dest_pos[0], dest_pos[1]  # 移動先座標
        self.image = Map.images[self.mapchip]
        self.rect = self.image.get_rect(topleft=(self.x*GS, self.y*GS))
    def draw(self, screen, offset):
        """オフセットを考慮してイベントを描画"""
        offsetx, offsety = offset
        px = self.rect.topleft[0]
        py = self.rect.topleft[1]
        screen.blit(self.image, (px-offsetx, py-offsety))
    def __str__(self):
        return "MOVE,%d,%d,%d,%s,%d,%d" % (self.x, self.y, self.mapchip, self.dest_map, self.dest_x, self.dest_y)




if __name__ == "__main__":
    PyRPG()





