import pyxel
from scene_abc import AbstractScene


class CastleScene(AbstractScene):
    def __init__(self):
        super().__init__()

    def update(self) -> bool:
        # TODO: 暫定でスペースで変更にしている
        if pyxel.btnp(pyxel.KEY_SPACE):
            return self.GAMEMODE.Dungeon
        return self.GAMEMODE.Castle

    def draw(self):
        # TODO: 暫定で文字のみ
        pyxel.text(75, 0, "Castle Scene", 11)
