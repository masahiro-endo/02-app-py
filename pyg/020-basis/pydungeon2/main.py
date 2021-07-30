
import pygame
import sys
from pygame.locals import *
import os
os.chdir(os.path.dirname(__file__))
import chara
import maps, move, battle




# 色の定義
WHITE = (255, 255, 255)
WARNING = (255, 191, 0)
DANGER = (255, 101, 101)
BLACK = (0, 0, 0)
RED   = (255, 0, 0) # プレイヤーの体力・食料が僅かの時、ゲームオーバーの時
CYAN  = (0, 255, 255)
BLINK = [(224,255,255), (192,240,255), (128,224,255), (64,192,255), (128,224,255), (192,240,255)] # 選択中の戦闘コマンドなどを点滅させる

# 画像の読み込み
imgTitle = pygame.image.load("image/title.png")
# 変数の宣言
speed = 1 # 速度(1-3) 大きいほど速い sキーで変化
# 0: タイトル画面 1: プレイヤーの移動 2: 画面切り替え（階段） 3: アイテム入手もしくはトラップ（宝箱・繭） 9: ゲームオーバー 10: 戦闘開始 11: プレイヤーのターン（入力待ち）
# 12: プレイヤーの攻撃 13: 敵のターン、敵の攻撃 14: 逃げられる？ 15: 敗北 16: 勝利 17: レベルアップ 20: Potion 21: Blaze gem 22: 戦闘終了
idx = 0
tmr = 0
floor = 0 # 階層 出現する敵や敵のレベルに影響（階層が上がるほど出現する敵の種類が増え、レベルの上限が上がる）出現する敵とレベルはランダム
fl_max = 1 # 最高到達階層 タイトル画面に表示

player = chara.Brave()

n_map = [[]]

def draw_text(bg, txt, x, y, fnt, col): # 影付き文字の表示
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

def main(): # メイン処理
    global speed, idx, tmr, floor, fl_max
    global n_map
    global food

    pygame.init()
    pygame.display.set_caption("One hour Dungeon") # タイトル
    screen = pygame.display.set_mode((880, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40) # fontS以外の画面表示フォント
    fontS = pygame.font.Font("font/JKG-L_3.ttf", 20, bold=True) # プレイヤーのパラメータ・位置情報・スピードなどの表示フォント
    fontS.set_bold(True) # ↑でなぜかTrueになっていない → print(fontS.get_bold())

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_s:
                    speed = speed + 1
                    if speed == 4:
                        speed = 1

        tmr = tmr + 1
        key = pygame.key.get_pressed()

        if idx == 0: # タイトル画面
            screen.fill(BLACK)
            screen.blit(imgTitle, [40, 60])
            if fl_max >= 2:
                draw_text(screen, "You reached floor {}.".format(fl_max), 300, 460, font, CYAN)
            draw_text(screen, "Press space key", 320, 560, font, BLINK[tmr%6])
            if key[K_SPACE] == 1:
                player.reset()
                floor = 1
                food = 300
                idx = 2 # マップの設定
        elif idx == 1:
            idx = move.main(screen, clock, font, fontS, n_map, player)
            tmr = 0
        elif idx == 2: # マップの設定
            n_map = maps.get_map(0, player)
            idx = 1
        elif idx == 10: # 戦闘開始
            idx = battle.main(screen, clock, font, fontS, player)
            tmr = 0
        draw_text(screen, "[S]peed "+str(speed), 740, 40, fontS, WHITE)

        pygame.display.update()
        clock.tick(4+2*speed)

if __name__ == '__main__':
    main()





