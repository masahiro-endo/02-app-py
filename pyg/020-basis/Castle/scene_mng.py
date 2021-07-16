import pyxel

from gamemode import GAMEMODE
from title_scene import TitleScene
from castle_scene import CastleScene
from dangeon_scene import DungeonScene


class App:
    def __init__(self):
        pyxel.init(128, 128)
        pyxel.load("sample.pyxres")
        self.scene = {
            GAMEMODE.Title: TitleScene(),
            GAMEMODE.Castle: CastleScene(),
            GAMEMODE.Dungeon: DungeonScene(),
        }

        self.my_gamemode = GAMEMODE.Title  # 最初に表示したいシーンを初期値に設定します。

        pyxel.run(self.update, self.draw)

    def update(self):
        # 現在選択されているシーンのupdateを読み込みます。
        self.my_gamemode = self.scene[self.my_gamemode].update()

    def draw(self):
        # こちらでは，画面の描画処理を行っています。

        pyxel.cls(0)  # 一旦画面を真っ新にしています。前書いていた映像が残ってしまうので
        self.scene[self.my_gamemode].draw()


if __name__ == "__main__":
    App()
