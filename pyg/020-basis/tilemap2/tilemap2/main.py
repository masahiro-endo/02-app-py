import pyxel
import math # math.floorを使うので必要
from enum import Enum

# 状態
class State(Enum):
    Standby = 1 # 待機中
    Moving  = 2 # 移動中 
    GameClear = 3 # ゲームクリア

class Map:
    SIZE = 8 # チップサイズ
    CHIP_WIDTH = 5 # 1列に5つ並んでいる
    CHIP_HEIGHT = 5 # 5行並んでいる
    
    # マップチップ座標をスクリーン座標に変換
    @classmethod
    def to_screen(cls, i, j):
        return (i * cls.SIZE, j * cls.SIZE)
    
    # マップチップの描画
    @classmethod
    def draw_chip(cls, i, j, val):
        # スクリーン座標に変換
        x, y = cls.to_screen(i, j)
        # チップ画像の座標を計算
        u = (val % cls.CHIP_WIDTH) * cls.SIZE
        v = (math.floor(val / cls.CHIP_WIDTH)) * cls.SIZE
        pyxel.blt(x, y, 0, u, v, cls.SIZE, cls.SIZE, 2)

class App:
    MOVE_SPEED = 10 # 移動速度
    def __init__(self):        
        pyxel.init(160, 120, fps=60)
        self.init() # 初期化
        pyxel.image(0).load(0, 0, "tileset.png")
        pyxel.run(self.update, self.draw)

    def init(self):
        # 初期化
        # マップデータ読み込み
        self.map = self.load_map("map.txt")
        # プレイヤーの位置を取得
        self.x, self.y = self.search_map(8)
        # マップデータからプレイヤーを削除
        self.set_map(self.x, self.y, 0)
        self.xnext = self.x # 移動先X座標
        self.ynext = self.y # 移動先Y座標
        self.move_timer = 0 # 移動中タイマー
        self.state = State.Standby # 状態

    def load_map(self, txt):
        # マップ読み込み
        map = []
        map_file = open(txt)
        for line in map_file:
            # １行ずつ読み込み
            array = []
            data = line.split(",")
            for d in data:
                # 余分な文字を削除
                s = d.strip()
                if s == "":
                    break
                v = int(d.strip())
                array.append(v)
            map.append(array)

        return map

    def search_map(self, val):
        # 指定の値が存在する座標を返す
        for j, arr in enumerate(self.map):
            for i, v in enumerate(arr):
                if v == val:
                    # 見つかった
                    return i, j
        # 見つからなかったら (-1, -1) を返す
        return -1, -1

    def set_map(self, i, j, val):
        # 指定の位置に値を設定する
        self.map[j][i] = val

    def check_wall(self, i, j):
        # 指定の座標が壁かどうかチェックする
        if i < 0 or 6 <= i:
            return True # マップ外
        if j < 0 or 6 <= j:
            return True # マップ外

        v = self.map[j][i]
        if v in [5, 6, 7, 10, 11, 12, 15, 16, 17]:
            # 壁なので移動できない
            return True

        # 移動可能
        return False

    def update(self):
        # 更新
        if self.state == State.Standby:
            # キー入力待ち
            if self.input_key():
                # 移動開始する
                self.move_timer = 0
                self.state = State.Moving
        elif self.state == State.Moving:
            # 移動中
            self.move_timer += 1
            if self.move_timer == self.MOVE_SPEED:
                # 移動完了
                self.x = self.xnext
                self.y = self.ynext
                # アイテム回収
                self.set_map(self.x, self.y, 0)
                # りんごを検索
                px, py = self.search_map(1)
                if px == -1:
                    # 見つからなかったのでゲームクリア
                    self.state = State.GameClear
                else:
                    self.state = State.Standby

    def input_key(self):
        # キー入力判定
        xnext = self.x
        ynext = self.y
        if pyxel.btn(pyxel.KEY_LEFT):
            xnext -= 1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            xnext += 1
        if pyxel.btn(pyxel.KEY_UP):
            ynext -= 1
        elif pyxel.btn(pyxel.KEY_DOWN):
            ynext += 1
        
        if self.x == xnext and self.y == ynext:
            # 異動先が同じなので移動しない
            return False
        
        if self.check_wall(xnext, ynext):
            # 壁なので移動できない
            return False

        # 移動する
        self.xnext = xnext
        self.ynext = ynext

        return True

    def draw(self):
        pyxel.cls(0)

        # マップの描画
        self.draw_map()
        # プレイヤーの描画
        self.draw_player()

        if self.state == State.GameClear:
            pyxel.text(4, 52, "GAME CLEAR", 9)

    # プレイヤーの描画
    def draw_player(self):
        px = self.x
        py = self.y
        if self.state == State.Moving:
            # 移動中だけ特殊処理
            dx = self.xnext - self.x
            dy = self.ynext - self.y
            # 移動先との差を線形補間する
            px += dx * self.move_timer / self.MOVE_SPEED
            py += dy * self.move_timer / self.MOVE_SPEED
        Map.draw_chip(px, py, 8)        

    def draw_map(self):
        # 外枠の描画
        pyxel.rectb(0, 0, Map.SIZE*6, Map.SIZE*6, 5)
        
        # 各チップの描画
        for j, arr in enumerate(self.map):
            for i, d in enumerate(arr):
                Map.draw_chip(i, j, d)

App()
