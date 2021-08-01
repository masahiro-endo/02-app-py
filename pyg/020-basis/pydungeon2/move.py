
import pygame
import sys
import random
from pygame.locals import *
import os
os.chdir(os.path.dirname(__file__))



# 色の定義
WHITE = (255, 255, 255)
WARNING = (255, 191, 0)
DANGER = (255, 101, 101)
BLACK = (0, 0, 0)
RED   = (255, 0, 0) # プレイヤーの体力・食料が僅かの時、ゲームオーバーの時
CYAN  = (0, 255, 255)
BLINK = [(224,255,255), (192,240,255), (128,224,255), (64,192,255), (128,224,255), (192,240,255)] # 選択中の戦闘コマンドなどを点滅させる

treasure = 0 # TRE_NAMEの添字 1,2,3：宝箱、4,5:繭

n_map = [[]]
map_w = 0
map_h = 0
food = 10 # プレイヤーの食料（1歩ごとに1減少） 0になったら体力が1歩ごとに5減少
floor = 1
tmr = 0

potion = 0 # ポーションを使える回数（使うと全快する）
blazegem = 0 # blazeを使える回数
treasure = 0 # TRE_NAMEの添字 1,2,3：宝箱、4,5:繭






imgWall = pygame.image.load("image/wall.png")
imgWall2 = pygame.image.load("image/wall2.png")
imgDark = pygame.image.load("image/dark.png")
imgPara = pygame.image.load("image/parameter.png")
imgItem = [
    pygame.image.load("image/potion.png"),
    pygame.image.load("image/blaze_gem.png"),
    pygame.image.load("image/spoiled.png"),
    pygame.image.load("image/apple.png"),
    pygame.image.load("image/meat.png")
]
imgFloor = [
    pygame.image.load("image/floor.png"),
    pygame.image.load("image/tbox.png"),
    pygame.image.load("image/cocoon.png"),
    pygame.image.load("image/stairs.png")
]

TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food +20", "Food +100"]


def draw_map(bg, fnt, player): # マップを描画する
    bg.fill(BLACK)
    for y in range(-4, 6):
        for x in range(-5, 6):
            X = (x+5)*80
            Y = (y+4)*80
            dx = player.x + x
            dy = player.y + y
            if 0 <= dx and dx < map_w and 0 <= dy and dy < map_h:
                if n_map[dy][dx] <= 3:
                    bg.blit(imgFloor[n_map[dy][dx]], [X, Y])
                if n_map[dy][dx] == 9:
                    bg.blit(imgWall, [X, Y-40])
                    if dy >= 1 and n_map[dy-1][dx] == 9:
                        bg.blit(imgWall2, [X, Y-80])
            if x == 0 and y == 0: # 主人公キャラの表示
                bg.blit(player.img[player.a], [X, Y-40])
    bg.blit(imgDark, [0, 0]) # 四隅が暗闇の画像を重ねる
    draw_para(bg, fnt, player) # 主人公の能力を表示

def move_player(key, player): # 主人公の移動
    global tmr, food, potion, blazegem, treasure

    if n_map[player.y][player.x] == 0: # 何もない床
        # プレイヤーがいる場所(リストimgFloor 0:床 1:宝箱 2:繭 3:階段 -にしたらリストの逆からになるので-4にしたら床になる)
        # これがないと連続して敵が出る。下の方で、移動後にいた場所を0にする
        n_map[player.y][player.x] = -4
        r = random.randint(0, 99)
        if r < 10: # 敵出現
            tmr = 0
            return 10
    elif n_map[player.y][player.x] == 1: # 宝箱に載った
        n_map[player.y][player.x] = 0
        treasure = random.choice([0,0,0,1,1,1,1,1,1,2])
        if treasure == 0:
            potion = potion + 1
        if treasure == 1:
            blazegem = blazegem + 1
        if treasure == 2: # ハズレ
            food = int(food/2)
        tmr = 0
        return 3
    elif n_map[player.y][player.x] == 2: # 繭に載った
        n_map[player.y][player.x] = 0
        r = random.randint(0, 99)
        if r < 40: # 食料
            treasure = random.choice([3,3,3,4])
            if treasure == 3:
                food = food + 20
            if treasure == 4:
                food = food + 100
            tmr = 0
            return 3
        return 1
    elif n_map[player.y][player.x] == 3: # 階段に載った
        tmr = 0
        return 2
    # 方向キーで上下左右に移動
    x = player.x # 移動したかを確認する為に今の位置を保存
    y = player.y
    if key[K_UP] == 1:
        player.d = 0
        if n_map[player.y-1][player.x] != 9:
            player.y = player.y - 1
    if key[K_DOWN] == 1:
        player.d = 1
        if n_map[player.y+1][player.x] != 9:
            player.y = player.y + 1
    if key[K_LEFT] == 1:
        player.d = 2
        if n_map[player.y][player.x-1] != 9:
            player.x = player.x - 1
    if key[K_RIGHT] == 1:
        player.d = 3
        if n_map[player.y][player.x+1] != 9:
            player.x = player.x + 1
    player.a = player.d*2 # 0:上 1:下 2:左 3:右
    if player.x != x or player.y != y: # 移動したら食料の量と体力を計算
        player.a = player.a + tmr%2 # 移動したら足踏みのアニメーション
        n_map[y][x] = 0 # いた場所を0にする
        if food > 0:
            food = food - 1
            if player.hp < player.maxhp:
                player.hp = player.hp + 1
        else:
            player.hp = player.hp - 5
            if player.hp <= 0:
                player.hp = 0
                pygame.mixer.music.stop()
                tmr = 0
                return 9
    return 1

def draw_para(bg, fnt, player): # 主人公の能力を表示
    X = 30
    Y = 600
    bg.blit(imgPara, [X, Y])
    col = WHITE
    if player.hp < 10 and tmr%2 == 0:
        col = RED
    draw_text(bg, "{}/{}".format(player.hp, player.maxhp), X+128, Y+6, fnt, col)
    draw_text(bg, str(player.atk), X+128, Y+33, fnt, WHITE)
    col = WHITE
    if food == 0 and tmr%2 == 0:
        col = RED
    draw_text(bg, str(food), X+128, Y+60, fnt, col)
    draw_text(bg, str(potion), X+266, Y+6, fnt, WHITE)
    draw_text(bg, str(blazegem), X+266, Y+33, fnt, WHITE)

def draw_text(bg, txt, x, y, fnt, col): # 影付き文字の表示
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

def main(screen, clock, font, fontS, use_map, player):
    global n_map, map_w, map_h
    global floor, tmr
    n_map = use_map
    map_w = len(n_map[0])
    map_h = len(n_map)
    idx = 1 # 歩く

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        tmr += 1
        key = pygame.key.get_pressed()

        if idx == 1:
            idx = move_player(key, player)
            draw_map(screen, fontS, player)
            draw_text(screen, "{}階 ({},{})".format(floor, player.x, player.y), 60, 40, fontS, WHITE)
        elif idx == 2: # 画面切り替え（階段）
            draw_map(screen, fontS, player)
            if 1 <= tmr and tmr <= 5:
                h = 80*tmr
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h]) # 上側を閉じていく
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h]) # 下側を閉じていく
            if tmr == 5:
                floor = floor + 1
                player.x = 3
                player.y = 3
            if 6 <= tmr and tmr <= 9:
                h = 80*(10-tmr)
                pygame.draw.rect(screen, BLACK, [0, 0, 880, h]) # 上側を開いていく
                pygame.draw.rect(screen, BLACK, [0, 720-h, 880, h]) # 下側を開いていく
            if tmr == 10:
                idx = 1

        elif idx == 3: # アイテム入手もしくはトラップ（宝箱・繭）
            draw_map(screen, fontS, player)
            screen.blit(imgItem[treasure], [320, 220]) # アイテム画像
            draw_text(screen, TRE_NAME[treasure], 380, 240, font, WHITE) # アイテムテキスト
            if tmr == 10:
                idx = 1
        elif idx == 9:
            if tmr <= 30:
                PL_TURN = [2, 4, 0, 6]
                player.a = PL_TURN[tmr%4] # プレイヤーを回転
                if tmr == 30:
                    player.a = 8 # 倒れた絵
                draw_map(screen, fontS, player)
            elif tmr == 31:
                draw_text(screen, "You died.", 360, 240, font, RED)
                draw_text(screen, "Game over.", 360, 380, font, RED)
            elif tmr == 80:
                return 0
        elif idx == 10: # 戦闘
            return 10
        pygame.display.update()
        clock.tick(10)




