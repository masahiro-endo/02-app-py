import pyxel
import math # math.floorを使うので必要

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
    def __init__(self):        
        pyxel.init(160, 120, fps=60)
        # マップデータ読み込み
        self.map = self.load_map("map.txt")
        # プレイヤーの位置を取得
        self.x, self.y = self.search_map(8)
        # マップデータからプレイヤーを削除
        self.set_map(self.x, self.y, 0)
        pyxel.image(0).load(0, 0, "tileset.png")
        pyxel.run(self.update, self.draw)

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

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

        # マップの描画
        self.draw_map()
        # プレイヤーの描画
        self.draw_player()

    # プレイヤーの描画
    def draw_player(self):
        Map.draw_chip(self.x, self.y, 8)        

    def draw_map(self):
        # 外枠の描画
        pyxel.rectb(0, 0, Map.SIZE*6, Map.SIZE*6, 5)
        
        # 各チップの描画
        for j, arr in enumerate(self.map):
            for i, d in enumerate(arr):
                Map.draw_chip(i, j, d)

App()
