import pyxel
from scene_abc import AbstractScene


class TitleScene(AbstractScene):
    def __init__(self):
        super().__init__()

    def update(self) -> bool:
        # スペースキーを押したらスタートするようにする
        if pyxel.btnp(pyxel.KEY_SPACE):
            return self.GAMEMODE.Castle
        return self.GAMEMODE.Title

    def draw(self):
        pyxel.bltm(x=0, y=0, tm=3, u=0, v=0, w=100, h=100)
        pyxel.text(40, 45, "Title Scene!", 11)
