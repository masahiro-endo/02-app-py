
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




class Window:

    EDGE_WIDTH = 2  # 白枠の幅

    _visible: bool

    def __init__(self, rect):
        self.rect = rect  # 一番外側の白い矩形
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH * 2, -self.EDGE_WIDTH * 2)  # 内側の黒い矩形
        self._visible = False

    def update(self):
        pass

    def draw(self, screen):
        """ウィンドウを描画"""
        if not self.is_visible:
            return

        pygame.draw.rect(screen, (255,255,255), self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.inner_rect, 0)

    def handler(self, event):
        pass


    def show(self):
        """ウィンドウを表示"""
        self._visible = True

    def hide(self):
        """ウィンドウを隠す"""
        self._visible = False

    @property
    def is_visible(self):
        return self._visible

    @is_visible.setter
    def is_visible(self, value):
        self._visible = value



class MessageWindow(Window):

    """メッセージウィンドウ"""
    MAX_CHARS_PER_LINE = 20    # 1行の最大文字数
    MAX_LINES_PER_PAGE = 3     # 1行の最大行数（4行目は▼用）
    MAX_CHARS_PER_PAGE = 20*3  # 1ページの最大文字数
    MAX_LINES = 30             # メッセージを格納できる最大行数
    LINE_HEIGHT = 8            # 行間の大きさ
    animcycle = 24

    def __init__(self, rect ):
        super().__init__(rect)
        self.text_rect = self.inner_rect.inflate(-32, -32)  # テキストを表示する矩形
        self.text = []  # メッセージ
        self.cur_page = 0  # 現在表示しているページ
        self.cur_pos = 0  # 現在ページで表示した最大文字数
        self.next_flag = False  # 次ページがあるか？
        self.hide_flag = False  # 次のキー入力でウィンドウを消すか？
        self.cursor = control.Method.load_image("data", "cursor.png", -1)  # カーソル画像
        self.frame = 0

    def settext(self, message):
        """メッセージをセットしてウィンドウを画面に表示する"""
        self.cur_pos = 0
        self.cur_page = 0
        self.next_flag = False
        self.hide_flag = False
        # 全角スペースで初期化
        self.text = [u'　'] * (self.MAX_LINES * self.MAX_CHARS_PER_LINE)
        # メッセージをセット
        p = 0
        for i in range(len(message)):
            ch = message[i]
            if ch == "/":  # /は改行文字
                self.text[p] = "/"
                p += self.MAX_CHARS_PER_LINE
                p = int( (p/self.MAX_CHARS_PER_LINE) * self.MAX_CHARS_PER_LINE)
            elif ch == "%":  # \fは改ページ文字
                self.text[p] = "%"
                p += self.MAX_CHARS_PER_PAGE
                p = int( (p/self.MAX_CHARS_PER_PAGE) * self.MAX_CHARS_PER_PAGE)
            else:
                self.text[p] = ch
                p += 1
        self.text[p] = "$"  # 終端文字
        self.show()

    def update(self):
        """メッセージウィンドウを更新する
        メッセージが流れるように表示する"""
        if self.is_visible:
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
        self.frame += 1

    def draw(self, screen):
        """メッセージを描画する
        メッセージウィンドウが表示されていないときは何もしない"""
        super().draw(screen)
        if not self.is_visible: 
            return
        
        # 現在表示しているページのcur_posまでの文字を描画
        for i in range(self.cur_pos):
            ch = self.text[self.cur_page*self.MAX_CHARS_PER_PAGE+i]
            if ch == "/" or ch == "%" or ch == "$": continue  # 制御文字は表示しない
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH * (i % self.MAX_CHARS_PER_LINE)
            dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * (i // self.MAX_CHARS_PER_LINE)
            g.msg_engine.draw_character(screen, (dx,dy), ch)
            
            if __debug__:
                print(f"ch={ch}")

        # 最後のページでない場合は▼を表示
        if (not self.hide_flag) and self.next_flag:
            if self.frame / self.animcycle % 2 == 0:
                dx = self.text_rect[0] + (self.MAX_CHARS_PER_LINE/2) * MessageEngine.FONT_WIDTH - MessageEngine.FONT_WIDTH/2
                dy = self.text_rect[1] + (self.LINE_HEIGHT + MessageEngine.FONT_HEIGHT) * 3
                screen.blit(self.cursor, (dx,dy))

    def handler(self, event):
        super().handler(event)

        if event.type == KEYDOWN:
            
            if event.key == K_SPACE:
                if __debug__:
                    print(f"K_SPACE")
            
            if event.key == K_RETURN:
                if __debug__:
                    print(f"K_RETURn")
                self.next()

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

    def update(self, pressed_keys):
        pass

    def draw(self, screen):
        screen.blit(self.surf, (self.rect.left, self.rect.top) )

    def handler(self, event):
        pass


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

    def update(self, pressed_keys):
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

    def update(self, pressed_keys):
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

    def update(self, pressed_keys):
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

    def update(self, pressed_keys):
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
            pygame.K_u: {"func" : None, "visible": False},
            pygame.K_o: {"func" : MenuStatus, "visible": False},
    }

    def __init__(self):
        self._keydict[K_c]["func"] = Camp()
        self._keydict[K_o]["func"] = MenuStatus( pygame.Rect( (0, 0), (600, 30) ) )
        self._keydict[K_s]["func"] = PlayerStatus( pygame.Rect( (0, 450), (600, 150) ) )

    def draw(self, screen):
        for _key, _cont in self._keydict.items():
            if _cont["func"] != None:
                if _cont["visible"]:
                    _cont["func"].draw(screen)

    def update(self, event):
        pass

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


class CommandWindow(Window):

    LINE_HEIGHT = 8  # 行間の大きさ

    TALK, STATUS, EQUIPMENT, DOOR, SPELL, ITEM, TACTICS, SEARCH = range(0, 8)

    COMMAND = ["はなす", "つよさ", "そうび", "とびら",
               "じゅもん", "どうぐ", "さくせん", "しらべる"]

    def __init__(self, rect, msg_engine):
        super().__init__(rect)
        self.text_rect = self.inner_rect.inflate(-32, -32)
        self.command = self.TALK  # 選択中のコマンド
        self.msg_engine = msg_engine
        self.cursor = control.Method.load_image("data", "cursor2.png", -1)
        self.frame = 0

    def update(self):
        pass

    def draw(self, screen):
        super().draw(screen)
        if not self.is_visible:
            return
        # はなす、つよさ、そうび、とびらを描画
        for i in range(0, 4):
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH
            dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * int((i % 4))
            self.msg_engine.draw_string(screen, (dx,dy), self.COMMAND[i])

        # じゅもん、どうぐ、さくせん、しらべるを描画
        for i in range(4, 8):
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH * 6
            dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * int((i % 4))
            self.msg_engine.draw_string(screen, (dx,dy), self.COMMAND[i])

        # 選択中のコマンドの左側に▶を描画
        dx = self.text_rect[0] + MessageEngine.FONT_WIDTH * 5 * (self.command // 4)
        dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * int((self.command % 4))
        screen.blit(self.cursor, (dx,dy))

    def show(self):
        """オーバーライド"""
        self.command = self.TALK  # 追加
        self.is_visible = True

    def handler(self, event):
        """コマンドウィンドウが開いているときのイベント処理"""
        # 矢印キーでコマンド選択
        if event.type == KEYDOWN:

            if event.key == K_LEFT:
                if cmdwnd.command <= 3:
                    return
                cmdwnd.command -= 4
        
            elif event.key == K_RIGHT:
                if cmdwnd.command >= 4:
                    return
                cmdwnd.command += 4

            elif event.key == K_UP:
                if cmdwnd.command == 0 or cmdwnd.command == 4:
                    return
                cmdwnd.command -= 1
    
            elif event.key == K_DOWN:
                if cmdwnd.command == 3 or cmdwnd.command == 7:
                    return
                cmdwnd.command += 1

            # スペースキーでコマンド実行
            elif event.key == K_SPACE:
                if cmdwnd.command == CommandWindow.TALK:  # はなす
                    sounds["pi"].play()
                    cmdwnd.hide()
                    chara = player.talk(map)
                    if chara != None:
                        msgwnd.set(chara.message)
                    else:
                        msgwnd.set("そのほうこうには　だれもいない。")
        
                elif cmdwnd.command == CommandWindow.STATUS:  # つよさ
                    # TODO: ステータスウィンドウ表示
                    sounds["pi"].play()
                    cmdwnd.hide()
                    msgwnd.set("つよさウィンドウが　ひらくよてい。")
        
                elif cmdwnd.command == CommandWindow.EQUIPMENT:  # そうび
                    # TODO: そうびウィンドウ表示
                    sounds["pi"].play()
                    cmdwnd.hide()
                    msgwnd.set("そうびウィンドウが　ひらくよてい。")
                elif cmdwnd.command == CommandWindow.DOOR:  # とびら
                    sounds["pi"].play()
                    cmdwnd.hide()
                    door = player.open(map)
                    if door != None:
                        door.open()
                        map.remove_event(door)
                    else:
                        msgwnd.set("そのほうこうに　とびらはない。")
        
                elif cmdwnd.command == CommandWindow.SPELL:  # じゅもん
                    # TODO: じゅもんウィンドウ表示
                    sounds["pi"].play()
                    cmdwnd.hide()
                    msgwnd.set("じゅもんウィンドウが　ひらくよてい。")
        
                elif cmdwnd.command == CommandWindow.ITEM:  # どうぐ
                    # TODO: どうぐウィンドウ表示
                    sounds["pi"].play()
                    cmdwnd.hide()
                    msgwnd.set("どうぐウィンドウが　ひらくよてい。")
                elif cmdwnd.command == CommandWindow.TACTICS:  # さくせん
                    # TODO: さくせんウィンドウ表示
                    sounds["pi"].play()
                    cmdwnd.hide()
                    msgwnd.set("さくせんウィンドウが　ひらくよてい。")
                elif cmdwnd.command == CommandWindow.SEARCH:  # しらべる
                    sounds["pi"].play()
                    cmdwnd.hide()
                    treasure = player.search(map)
                    if treasure != None:
                        treasure.open()
                        msgwnd.set("%s　をてにいれた。" % treasure.item)
                        map.remove_event(treasure)
                    else:
                        msgwnd.set("しかし　なにもみつからなかった。")



class BattleCommandWindow(Window):
    """戦闘のコマンドウィンドウ"""
    LINE_HEIGHT = 8  # 行間の大きさ
    ATTACK, SPELL, ITEM, ESCAPE = range(4)
    COMMAND = ["たたかう", "じゅもん", "どうぐ", "にげる"]
    
    def __init__(self, rect, msg_engine):
        super().__init__(rect)
        self.text_rect = self.inner_rect.inflate(-32, -16)
        self.command = self.ATTACK  # 選択中のコマンド
        self.msg_engine = msg_engine
        self.cursor = load_image("data", "cursor2.png", -1)
        self.frame = 0
    
    def draw(self, screen):
        super().draw(screen)
        if not self.is_visible:
            return
        # コマンドを描画
        for i in range(0, 4):
            dx = self.text_rect[0] + MessageEngine.FONT_WIDTH
            dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * (i % 4)
            self.msg_engine.draw_string(screen, (dx,dy), self.COMMAND[i])
        # 選択中のコマンドの左側に▶を描画
        dx = self.text_rect[0]
        dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * (self.command % 4)
        screen.blit(self.cursor, (dx,dy))

    def show(self):
        """オーバーライド"""
        self.command = self.ATTACK  # 追加
        self.is_visible = True

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



class BattleStatusWindow(Window):
    """戦闘画面のステータスウィンドウ"""
    LINE_HEIGHT = 8  # 行間の大きさ
    def __init__(self, rect, status, msg_engine):
        super().__init__(rect)
        self.text_rect = self.inner_rect.inflate(-32, -16)
        self.status = status  # status = ["なまえ", HP, MP, LV]
        self.msg_engine = msg_engine
        self.frame = 0
    def draw(self, screen):
        super().draw(screen)
        if not self.is_visible:
            return
        # ステータスを描画
        status_str = [self.status[0], u"H%3d" % self.status[1], u"M%3d" % self.status[2], u"%s%3d" % (self.status[0][0], self.status[3])]
        for i in range(0, 4):
            dx = self.text_rect[0]
            dy = self.text_rect[1] + (self.LINE_HEIGHT+MessageEngine.FONT_HEIGHT) * (i % 4)
            self.msg_engine.draw_string(screen, (dx,dy), status_str[i])





class MessageEngine:

    FONT_WIDTH = 16
    FONT_HEIGHT = 22

    class COLOR_POS(IntEnum):
        WHITE = 0
        RED = 160
        GREEN = 320
        BLUE = 480

    def __init__(self):
        self.image = control.Method.load_image("./assets/fonts/", "font.png", -1)
        self.kana2rect = {}
        self.read_hash()

    def draw_character(self, screen, pos, ch, cpos = COLOR_POS.WHITE ):
        """1文字だけ描画する"""
        x, y = pos
        try:
            rect = self.kana2rect[ch]
            screen.blit(self.image, (x, y), (rect.x + cpos, rect.y, rect.width, rect.height ) )
        except KeyError:
            print("描画できない文字があります:%s" % ch)
            return

    def draw_string(self, screen, pos, str, cpos = COLOR_POS.WHITE ):
        """文字列を描画"""
        x, y = pos
        for i, ch in enumerate(str):
            dx = x + MessageEngine.FONT_WIDTH * i
            self.draw_character(screen, (dx,y), ch, cpos)

    def read_hash(self):
        """文字から座標への辞書を作成"""
        filepath = os.path.join("data", "kana2rect.dat")
        fp = codecs.open(filepath, "r", "utf-8")

        for line in fp.readlines():
            line = line.rstrip()
            buf = line.split("\t")
            kana, x, y, w, h = buf[0], int(buf[1]), int(buf[2]), int(buf[3]), int(buf[4])
            self.kana2rect[kana] = Rect(x, y, w, h)
        fp.close()




g.msg_engine: MessageEngine





