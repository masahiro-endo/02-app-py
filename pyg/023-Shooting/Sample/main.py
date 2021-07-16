from random import random
from typing import Any, List

import pyxel


enemy_list = []
bullet_list = []
blast_list = []


def update_list(list: List[Any]) -> None:
    for elem in list:
        elem.update()

def draw_list(list: List[Any]) -> None:
    for elem in list:
        elem.draw()

def clear_list(list: List[Any]) -> None:
    i = 0
    while i < len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1




class App:
    def __init__(self):
        pyxel.init(120, 160, caption="Pyxel Shooter")

        pyxel.image(0).set(
            0,
            0,
            [
                "00c00c00",
                "0c7007c0",
                "0c7007c0",
                "c703b07c",
                "77033077",
                "785cc587",
                "85c77c58",
                "0c0880c0",
            ],
        )

        pyxel.image(0).set(
            8,
            0,
            [
                "00088000",
                "00ee1200",
                "08e2b180",
                "02882820",
                "00222200",
                "00012280",
                "08208008",
                "80008000",
            ],
        )

        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)

        self.scene = SCENE_TITLE
        self.score = 0
        self.background = Background()
        self.player = Player(pyxel.width / 2, pyxel.height - 20)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        if pyxel.frame_count % 6 == 0:
            Enemy(random() * (pyxel.width - PLAYER_WIDTH), 0)

        for a in enemy_list:
            for b in bullet_list:
                if (
                    a.x + a.w > b.x
                    and b.x + b.w > a.x
                    and a.y + a.h > b.y
                    and b.y + b.h > a.y
                ):
                    a.alive = False
                    b.alive = False

                    blast_list.append(
                        Blast(a.x + ENEMY_WIDTH / 2, a.y + ENEMY_HEIGHT / 2)
                    )

                    pyxel.play(1, 1)

                    self.score += 10

        for enemy in enemy_list:
            if (
                self.player.x + self.player.w > enemy.x
                and enemy.x + enemy.w > self.player.x
                and self.player.y + self.player.h > enemy.y
                and enemy.y + enemy.h > self.player.y
            ):
                enemy.alive = False

                # 自機の爆発を生成する
                blast_list.append(
                    Blast(
                        self.player.x + PLAYER_WIDTH / 2,
                        self.player.y + PLAYER_HEIGHT / 2,
                    )
                )

                pyxel.play(1, 1)

                self.scene = SCENE_GAMEOVER

        self.player.update()
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)

    def update_gameover_scene(self):
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)

        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)

        if pyxel.btnp(pyxel.KEY_ENTER):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width / 2
            self.player.y = pyxel.height - 20
            self.score = 0

            enemy_list.clear()
            bullet_list.clear()
            blast_list.clear()

    def draw(self):
        pyxel.cls(0)

        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        pyxel.text(39, 4, "SCORE {:5}".format(self.score), 7)

    def draw_title_scene(self):
        pyxel.text(35, 66, "Pyxel Shooter", pyxel.frame_count % 16)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        self.player.draw()
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)

    def draw_gameover_scene(self):
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)

        pyxel.text(43, 66, "GAME OVER", 8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)




if __name__ == '__main__':
    App()




