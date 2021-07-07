#!/usr/bin/env python
import pygame
from pygame.locals import *
import sys
import os

SCR_RECT = Rect(0, 0, 640, 480)
ROW,COL = 15,20
GS = 32
DOWN,LEFT,RIGHT,UP = 0,1,2,3
map = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

def load_image(filename, colorkey=None):
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def split_image(image):
    """128x128のキャラクターイメージを32x32の16枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    imageList = []
    for i in range(0, 128, GS):
        for j in range(0, 128, GS):
            surface = pygame.Surface((GS,GS))
            surface.blit(image, (0,0), (j,i,GS,GS))
            surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
            surface.convert()
            imageList.append(surface)
    return imageList

def draw_map(screen):
    """マップを描画する"""
    for r in range(ROW):
        for c in range(COL):
            if map[r][c] == 0:
                screen.blit(grassImg, (c*GS,r*GS))
            elif map[r][c] == 1:
                screen.blit(waterImg, (c*GS,r*GS))

def is_movable(x, y):
    """(x,y)は移動可能か？"""
    # マップ範囲内か？
    if x < 0 or x > COL-1 or y < 0 or y > ROW-1:
        return False
    # マップチップは移動可能か？
    if map[y][x] == 1:  # 水は移動できない
        return False
    return True

pygame.init()
screen = pygame.display.set_mode(SCR_RECT.size)
pygame.display.set_caption("PyRPG 06 カニ足移動を直す")

# イメージロード
playerImgList = split_image(load_image("player.png"))  # プレイヤー
grassImg = load_image("grass.png")         # 草地
waterImg = load_image("water.png")         # 水

x,y = 1,1  # プレイヤーの位置（単位：マス）
direction = DOWN
animcycle = 24  # アニメーション速度
frame = 0

clock = pygame.time.Clock()

while True:
    clock.tick(60)

    # 経過フレーム数に応じて表示する画像を変える
    frame += 1
    playerImg = playerImgList[int(direction*4+frame/animcycle%4)]

    draw_map(screen)  # マップ描画
    screen.blit(playerImg, (x*GS,y*GS))  # プレイヤー描画
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()

        # プレイヤーの移動処理
        if event.type == KEYDOWN and event.key == K_DOWN:
            direction = DOWN
            if is_movable(x, y+1):
                y += 1
        if event.type == KEYDOWN and event.key == K_LEFT:
            direction = LEFT
            if is_movable(x-1, y):
                x -= 1
        if event.type == KEYDOWN and event.key == K_RIGHT:
            direction = RIGHT
            if is_movable(x+1, y):
                x += 1
        if event.type == KEYDOWN and event.key == K_UP:
            direction = UP
            if is_movable(x, y-1):
                y -= 1
