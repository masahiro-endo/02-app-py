from random import random
from typing import Any, List, Sized, Tuple

import pyxel




SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5


ELM_WIDTH = 0
ELM_HEIGHT = 1
ELM_SPEED = 2

PLAYER_INFO: Tuple[Any,Any,Any] = (8,8,2)
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2

BULLET_WIDTH = 2
BULLET_HEIGHT = 8
BULLET_COLOR = 11
BULLET_SPEED = -4

ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
ENEMY_SPEED = 1

BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8
BLAST_COLOR_IN = 7
BLAST_COLOR_OUT = 10



class Background:
    star_list: List[Tuple[Any,Any,Any]] = []
    
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                tuple(random() * pyxel.width, random() * pyxel.height, random() * 1.5 + 1)
            )

    def update(self):
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        for (x, y, speed) in self.star_list:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)



class Pos:
    x: int
    y: int
    
class Size:
    w: int
    h: int


class Actor:
    x: int
    y: int
    spd: int

    def __init__(self, tpl: Tuple[Any,Any,Any]) -> None:
        for (x, y, spd) in tpl:
            self.x = x
            self.y = y
            self.spd = spd

    def update(self) -> None:
        self.x += self.spd
        self.y += self.spd


class Player(Actor):
    def __init__(self, x: int, y: int, spd: int = PLAYER_SPEED):
        super().__init__(x,y,spd)
        
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.alive = True

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= self.spd

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += self.spd

        if pyxel.btn(pyxel.KEY_UP):
            self.y -= self.spd

        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += self.spd

        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(
                self.x + (PLAYER_WIDTH - BULLET_WIDTH) / 2, self.y - BULLET_HEIGHT / 2
            )

            pyxel.play(0, 0)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)


class Bullet(Actor):
    def __init__(self, x: int, y: int, spd: int = BULLET_SPEED):
        super().__init__(x,y,spd)

        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.alive = True

        bullet_list.append(self)

    def update(self):
        super().update()

        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)


class Enemy(Actor):
    def __init__(self, x: int, y: int, spd: int = ENEMY_SPEED):
        super().__init__(x,y,spd)
 
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        enemy_list.append(self)

    def update(self):
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += self.spd
            self.dir = 1
        else:
            self.x += self.spd
            self.dir = -1

        self.y += self.spd

        if self.y > pyxel.height - 1:
            self.alive = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w * self.dir, self.h, 0)


class Blast(Actor):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True

        blast_list.append(self)

    def update(self):
        self.radius += 1

        if self.radius > BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, BLAST_COLOR_OUT)





