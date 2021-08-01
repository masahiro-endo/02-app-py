import pygame
from pygame.locals import *
import sys




def main():
    wsize:int = 0

    pygame.init()                                   # Pygameの初期化
    screen = pygame.display.set_mode((300, 200),FULLSCREEN)    # 大きさ600*500の画面を生成
    pygame.display.set_caption("GAME")              # タイトルバーに表示する文字
    font = pygame.font.Font(None, 55)               # フォントの設定(55px)
    
    while (1):
        screen.fill((0,0,0))                                    # 画面を黒色に塗りつぶし
        text = font.render("TEST", True, (255,255,255))   # 描画する文字列の設定
        screen.blit(text, [20, 100])# 文字列の表示位置
        pygame.display.update()     # 画面を更新
        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                wsize = 0 if wsize != 0 else FULLSCREEN
                screen = pygame.display.set_mode((300, 200),wsize)



if __name__ == "__main__":
    main()


