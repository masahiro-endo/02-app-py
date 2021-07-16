import pyxel
from scene_abc import AbstractScene


class DungeonScene(AbstractScene):
    def __init__(self):
        super().__init__()

    def update(self) -> bool:
        # TODO: 暫定でスペースで変更にしている
        if pyxel.btnp(pyxel.KEY_SPACE):
            return self.GAMEMODE.Title
        return self.GAMEMODE.Dungeon

    def draw(self):
        # TODO: 暫定で文字のみ
        pyxel.text(75, 0, "Dungeon Scene", 11)
