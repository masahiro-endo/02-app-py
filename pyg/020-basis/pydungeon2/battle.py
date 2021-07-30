
import pygame
import sys
import random
from pygame.locals import *

import chara

import mojimoji # 半角⇄全角変換
import time
import collections

# 色の定義
WHITE = (255, 255, 255)
WARNING = (255, 191, 0)
DANGER = (255, 101, 101)
BLACK = (0, 0, 0)
RED   = (255, 0, 0) # プレイヤーの体力・食料が僅かの時、ゲームオーバーの時
CYAN  = (0, 255, 255)
BLINK = [(224,255,255), (192,240,255), (128,224,255), (64,192,255), (128,224,255), (192,240,255)] # 選択中の戦闘コマンドなどを点滅させる

# 画像の読み込み
imgBtlBG = pygame.image.load("image/btlbg.png")
imgEffect = [
    pygame.image.load("image/effect_a.png"), # 攻撃
]

# 変数の宣言
# 0: タイトル画面 1: プレイヤーの移動 2: 画面切り替え（階段） 3: アイテム入手もしくはトラップ（宝箱・繭） 9: ゲームオーバー 10: 戦闘開始 11: プレイヤーのターン（入力待ち）
# 12: プレイヤーの攻撃 13: 敵のターン、敵の攻撃 14: 逃げられる？ 15: 敗北 16: 勝利 17: レベルアップ 20: Potion 21: Blaze gem 22: 戦闘終了
idx = 0
tmr = 0
floor = 0 # 階層 出現する敵や敵のレベルに影響（階層が上がるほど出現する敵の種類が増え、レベルの上限が上がる）出現する敵とレベルはランダム
fl_max = 1 # 最高到達階層 タイトル画面に表示

monster = [] # 敵のオブジェクト
dead_monster = [] # 倒した敵のオブジェクト
emy_step = 0 # 敵が攻撃する時の動きの大きさ（前に出るステップの大きさ）
emy_blink = 0 # 攻撃した時に敵を点滅させる（奇数:表示させない、偶数:表示させる）

dmg_eff = 0
btl_cmd_x = 0 # コマンド選択の時の"▶︎"のx位置
btl_cmd_y = 0 # コマンド選択の時の"▶︎"のy位置
btl_enemy = 0 # 敵選択の時の"▶︎"の位置
battle_order = {} # 戦闘の順番

COMMAND = [["こうげき", "どうぐ"], ["じゅもん", "そうび"], ["ぼうぎょ", "にげる"]]
TRE_NAME = ["Potion", "Blaze gem", "Food spoiled.", "Food +20", "Food +100"]

（省略）

def main(screen, clock, font, fontS, player):
    global idx, tmr, floor
    global emy_step, emy_blink, dmg_eff
    global btl_cmd_x, btl_cmd_y, btl_enemy

    idx = 10
    tmr = 0
    dmg = 0 # プレイヤーが与えるダメージ、受けるダメージ

    turn_obj = "" # 戦闘で行動するオブジェクト
    btl_exp = 0 # 戦闘で獲得した経験値（逃げたら0）
    btl_start = 0 # 0:通常、1:先制攻撃、2:不意打ち
    mon_typ = "" # モンスターの種類が複数："まもののむれ"、１種類：モンスターの名前

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        tmr = tmr + 1
        key = pygame.key.get_pressed()

        if idx == 9: # ゲームオーバー
            if tmr == 10:
                monster.clear() # モンスターオブジェクトを削除
                dead_monster.clear()
                return 0

        elif idx == 10: # 戦闘開始
            if tmr == 1:
                mon_typ = init_battle(screen)
                init_message()
            elif tmr <= 4:
                bx = (4-tmr)*220
                by = 0
                screen.blit(imgBtlBG, [bx, by]) # バトル画面を右から左へ挿入していく
                draw_text(screen, "Encounter!", 350, 200, font, WHITE)
            elif tmr == 5:
                set_message(monster[0].name + " が現れた！")
                draw_battle(screen, fontS, turn_obj, player)
            elif tmr == 6:
                if len(monster) >= 2:
                    set_message(monster[1].name + " が現れた！")
                    draw_battle(screen, fontS, turn_obj, player)
                    time.sleep(0.3)
            elif tmr == 7:
                if len(monster) >= 3:
                    set_message(monster[2].name + " が現れた！")
                    draw_battle(screen, fontS, turn_obj, player)
                    time.sleep(0.3)
            elif tmr == 8:
                if len(monster) == 4:
                    set_message(monster[3].name + " が現れた！")
                    draw_battle(screen, fontS, turn_obj, player)
                    time.sleep(0.3)
            elif tmr == 9:
                btl_start = random.randint(1, 32)
                if btl_start == 1: # 先制攻撃
                    init_message()
                    if random.randint(0, 1) == 0:
                        set_message("しかし " + mon_typ + "は")
                        set_message("まだ こちらに きづいていない！")
                    else:
                        set_message("しかし " + mon_typ + "は")
                        set_message("おどろき とまどっている！")
                    draw_battle(screen, fontS, turn_obj, player)
                    time.sleep(0.5)
                elif btl_start == 2: # 不意打ち
                    init_message()
                    if random.randint(0, 1) == 0:
                        set_message(mon_typ + "は")
                        set_message("いきなり おそいかかってきた！")
                    else:
                        set_message(mon_typ + "は")
                        set_message(player.name + "が みがまえるまえに")
                        set_message("おそいかかってきた！")
                    draw_battle(screen, fontS, turn_obj, player)
                    time.sleep(0.5)
                else: # 通常攻撃
                    btl_start = 0
                    
            elif tmr <= 16:
                draw_battle(screen, fontS, turn_obj, player)
                time.sleep(1)
                # draw_text(screen, monster.name+" appear!", 300, 150, font, WHITE)
                init_message()
                if btl_start == 2: # 表示時間の問題でここで改めて判定
                    idx = 23
                else:
                    idx = 11
                tmr = 0

        elif idx == 11: # プレイヤーのターン（入力待ち）
            btl_enemy = 0
            player.re_defense() # ぼうぎょを元に戻す（ぼうぎょ効果を消す）（呪文効果が残っているか確認）
            draw_battle(screen, fontS, turn_obj, player)
            if battle_command(screen, key) == True:
                if COMMAND[btl_cmd_y][btl_cmd_x] == "こうげき":
                    idx = 19
                    tmr = 0
                if COMMAND[btl_cmd_y][btl_cmd_x] == "じゅもん":
                    idx = 18
                    tmr = 0
                if COMMAND[btl_cmd_y][btl_cmd_x] == "ぼうぎょ":
                    player.act = 18 # get_battle_turnの戻り値idxを18
                    player.defense() # 選択した時点で防御力2倍（ターンが回ってきてからではない）
                    idx = 23
                    tmr = 0
                if COMMAND[btl_cmd_y][btl_cmd_x] == "にげる":
                    idx = 14
                    tmr = 0

                # コマンドの位置のリセット
                btl_cmd_x = 0
                btl_cmd_y = 0

        elif idx == 12: # プレイヤーの攻撃
            draw_battle(screen, fontS, turn_obj, player)
            if tmr == 1:
                set_message(turn_obj.name + " の攻撃！")
                dmg = player.attack(monster[btl_enemy])
            if 2 <= tmr and tmr <= 4:
                screen.blit(imgEffect[0], [monster[btl_enemy].x+monster[btl_enemy].img.get_width()-tmr*80, tmr*80])
            if tmr == 5:
                emy_blink = 5
                if dmg > 0:
                    set_message(monster[btl_enemy].name + "に " + str(dmg)+"ポイントのダメージを与えた！")
                else:
                    set_message("ミス！" + monster[btl_enemy].name + "にダメージを与えられない！")

            if tmr == 11:
                monster[btl_enemy].hp = monster[btl_enemy].hp - dmg
                if monster[btl_enemy].hp <= 0:
                    monster[btl_enemy].hp = 0
                    set_message(turn_obj.name + " は " + monster[btl_enemy].name + " をやっつけた！")
                    btl_exp += monster[btl_enemy].exp
                    del_battle_turn(monster[btl_enemy]) # ターンオブジェクトから消す（倒したモンスターは攻撃しない）
                    dead_monster.append(monster[btl_enemy]) # 先に加える
                    monster.pop(btl_enemy)

                if not monster: # 空だとFalseを返すので not monsterがTrueだと空
                    idx = 16 # 勝利
                    tmr = 0
            if tmr == 16:
                init_message()
                idx = 24 # ターンの確認
                tmr = 0

        elif idx == 13: # 敵のターン、敵の攻撃
            draw_battle(screen, fontS, turn_obj, player)
            if tmr == 5:
                set_message(turn_obj.name + " の攻撃！")
                emy_step = 30
            if tmr == 9:
                dmg = turn_obj.attack(player)
                if dmg > 0:
                    set_message(player.name + "は " + str(dmg) + "ポイントのダメージを受けた！")
                    dmg_eff = 5
                else:
                    set_message("ミス！" + player.name + " はダメージを受けない！")
                    dmg_eff = 0
                emy_step = 0
            if tmr == 15:
                player.hp = player.hp - dmg
                if player.hp <= 0:
                    player.hp = 0
                    idx = 15 # 敗北
                    tmr = 0
            if tmr == 20:
                init_message()
                idx = 24 # ターンの確認
                tmr = 0

        elif idx == 14: # 逃げられる？
            draw_battle(screen, fontS, turn_obj, player)
            if tmr == 1: set_message(player.name + " は逃げ出した！")
            if tmr == 5:
                if random.randint(0, 99) < 60:
                    btl_exp = 0 # 逃げたら0
                    idx = 22 # 戦闘終了
                else:
                    set_message("しかし、まわりこまれてしまった！")
            if tmr == 10:
                init_message()
                btl_start = 2 # 不意打ちと同じ状態にする
                idx = 23 # ターンセット
                tmr = 0
             
        elif idx == 15: # 敗北
            draw_battle(screen, fontS, turn_obj, player)
            if tmr == 1:
                set_message(player.name + " は気絶した...")
            if tmr == 11:
                idx = 9 # ゲームオーバー
                tmr = 0

        elif idx == 16: # 勝利
            draw_battle(screen, fontS, turn_obj, player)
            if tmr == 1:
                if len(dead_monster) != 1: # １匹の時はいらない
                    set_message(player.name + " は " + mon_typ + " をやっつけた！")
                player.exp += btl_exp
                if player.exp >= player.lv_exp:
                    idx = 17
                    tmr = 0
            if tmr == 28:
                idx = 22 # 戦闘終了

        elif idx == 17: # レベルアップ
            draw_battle(screen, fontS, turn_obj, player)
            if tmr == 1:
                set_message(player.name + " はレベルが上がった！")
                # se[4].play()
                # lif_p = random.randint(10, 20)
                # str_p = random.randint(5, 10)
                player.lv_up()
            if tmr == 21:
                # set_message("Max life + "+str(lif_p))
                # player.maxhp = player.maxhp + lif_p
                init_message()
                set_message("最大HP："+str(player.maxhp))
            if tmr == 26:
                set_message("素早さ："+str(player.quick))
            if tmr == 30:
                set_message("攻撃力："+str(player.atk))
            if tmr == 34:
                set_message("防御力："+str(player.dfs))
            if tmr == 40:
                if player.exp >= player.lv_exp:
                    idx = 17
                    tmr = 0
            if tmr == 50:
                idx = 22 # 戦闘終了
        
        elif idx == 18: # ぼうぎょ
            draw_battle(screen, fontS, turn_obj, player)
            if tmr == 1:
                player.defense()
                set_message(player.name + "は みをまもっている！")
            if tmr == 5:
                init_message()
                idx = 24 # ターンの確認
                tmr = 0

        elif idx == 19: # 敵の選択
            draw_battle(screen, fontS, turn_obj, player)
            if battle_select(screen, key) == True:
                player.act = 12 # get_battle_turnの戻り値idxを12
                idx = 23
                tmr = 0

        elif idx == 22: # 戦闘終了
            idx = 1
            monster.clear() # モンスターオブジェクトを削除
            dead_monster.clear()
            btl_exp = 0
            return 1

        elif idx == 23: # ターンセット
            set_battle_turn(btl_start, player)
            btl_start = 0 # 戦闘は通常に戻す
            idx = 24
            tmr = 0

        elif idx == 24: # ターン確認
            tmr = 0 # 0にしないと idx=12では battle_calに行かない()
            turn_obj, idx = get_battle_turn(player)

        pygame.display.update()
        clock.tick(10)




