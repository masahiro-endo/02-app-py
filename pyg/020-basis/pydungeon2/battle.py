
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

party = 1 # パーティーの数




def draw_text(bg, txt, x, y, fnt, col): # 影付き文字の表示
    sur = fnt.render(txt, True, BLACK)
    bg.blit(sur, [x+1, y+2])
    sur = fnt.render(txt, True, col)
    bg.blit(sur, [x, y])

def init_battle(bg): # 戦闘に入る準備をする
    global monster
    num_enemy = random.randint(1, 4)
    sum_x = 0
    list_typ = []
    for _ in range(num_enemy):
        if floor >= 10:
            typ = random.randint(1, 10)
        else:
            typ = random.randint(1, floor+1)
        list_typ.append(typ)

    dic_typ = collections.Counter(list_typ) # 重複を抽出
    i = 0
    for k, v in dic_typ.items(): # k:typ、v:数（typの種類がvの数だけ存在）
        for j in range(v):
            monster.append(chara.Monster(k))
            if v != 1: # 同じ種類が複数いる時
                monster[i].set_name(j)
            sum_x += monster[i].img.get_width() + 35 # 35はモンスターの間隔
            monster[i].set_y(bg.get_height()*0.6 - monster[i].img.get_height()) # どのモンスターも画面の7割が一番下に揃えられる
            i += 1
    sum_x -= 35 # 最後のモンスターは間隔を開ける必要がない
    x_i_i = bg.get_width()/2 - sum_x/2 # 一番左のモンスターのx座標
    monster[0].set_x(x_i_i) # 1匹目
    for i in range(num_enemy-1): # 2匹目
        x_i_i += monster[i].img.get_width() + 35 # 2匹目以降のモンスターの横幅+間隔 (2匹目は1匹目の横幅+間隔分をずらす)
        monster[i+1].set_x(x_i_i) # 各モンスターのx座標 2匹目以降なので i+1

    if len(dic_typ) == 1: # １種類はモンスター名
        if num_enemy == 1: # １匹はそのまま表示
            return monster[0].name
        else: # 複数は" A"や" B"などを消す
            return monster[0].name[:-2] # モンスターが１種類
    else: # 複数種類
        return "まもののむれ" # モンスターが複数種類

def draw_battle(bg, fnt, obj, player): # 戦闘画面の描画 obj:戦闘で行動中のオブジェクト
    global emy_blink, dmg_eff
    bx = 0
    by = 0
    if dmg_eff > 0:
        dmg_eff = dmg_eff - 1
        bx = random.randint(-20, 20)
        by = random.randint(-10, 10)
    bg.blit(imgBtlBG, [bx, by])
    for i, mon in enumerate(monster):
        display_flg = False # 生存しているモンスターを表示
        if mon.hp> 0 and btl_enemy != i:
            display_flg = True
        elif mon.hp> 0 and btl_enemy == i: # 攻撃対象のモンスターにエフェクト効果
            if emy_blink%2 == 0:
                display_flg = True
        if display_flg:
            if monster[i] is obj: # 行動中のモンスターなら
                bg.blit(mon.img, [monster[i].x, monster[i].y+emy_step])
            else:
                bg.blit(mon.img, [monster[i].x, monster[i].y])
            # 敵の体力を表示するバー
            # draw_bar(bg, 340, 580, 200, 10, monster.hp, monster.maxhp)
            x_i = monster[i].x + mon.img.get_width()/2 - 100 # 体力バーのx座標
            x_w = 200 # 体力バーの幅
            y_i = bg.get_height()*0.6 + 10 # モンスター表示の一番下（画面の７割）
            y_h = 10
            pygame.draw.rect(bg, WHITE, [x_i-2, y_i-2, x_w+4, y_h+4])
            pygame.draw.rect(bg, BLACK, [x_i, y_i, x_w, y_h])
            if mon.hp > 0:
                pygame.draw.rect(bg, (0,128,255), [x_i, y_i, x_w*mon.hp/mon.maxhp, y_h]) # 残り体力

    if emy_blink > 0:
        emy_blink = emy_blink - 1

    # パラメータ表示
    x_i = int(bg.get_width()/4) # x座標の開始位置
    x_w = int(bg.get_width()/8) # 幅
    y_i = 20 # y座標の開始位置
    y_h = 120 # 高さ
    x_i_t = x_i+x_w/2-50 # テキストのx座標の開始位置
    if party == 1: # 一人の時の全体の表示幅
        x_w *= 1
    col = WHITE
    if player.hp < player.maxhp/4:
        col = DANGER
    elif player.hp < player.maxhp/2:
        col = WARNING
    pygame.draw.rect(bg, col, [x_i, y_i, x_w, y_h], 2, 5)
    pygame.draw.line(bg, col, [x_i, y_i+33], [x_i+x_w-1, y_i+33], 2) # -1がないと少し出る
    draw_text(bg, "{}".format(player.name), x_i_t, y_i+6, fnt, col)
    if len(str(player.hp)) == 3:
        draw_text(bg, mojimoji.han_to_zen("H{}".format(player.hp)), x_i_t, y_i+36, fnt, col)
    elif len(str(player.hp)) == 2:
        draw_text(bg, mojimoji.han_to_zen("H {}".format(player.hp)), x_i_t, y_i+36, fnt, col)
    elif len(str(player.hp)) == 1:
        draw_text(bg, mojimoji.han_to_zen("H  {}".format(player.hp)), x_i_t, y_i+36, fnt, col)

    if len(str(player.mp)) == 3:
        draw_text(bg, mojimoji.han_to_zen("M{}".format(player.mp)), x_i_t, y_i+66, fnt, col)
    elif len(str(player.mp)) == 2:
        draw_text(bg, mojimoji.han_to_zen("M {}".format(player.mp)), x_i_t, y_i+66, fnt, col)
    elif len(str(player.mp)) == 1:
        draw_text(bg, mojimoji.han_to_zen("M  {}".format(player.mp)), x_i_t, y_i+66, fnt, col)
    
    if len(str(player.lv)) == 2:
        draw_text(bg, mojimoji.han_to_zen("L:{}".format(player.lv)), x_i_t, y_i+96, fnt, col)
    elif len(str(player.lv)) == 1:
        draw_text(bg, mojimoji.han_to_zen("L: {}".format(player.lv)), x_i_t, y_i+96, fnt, col)

    if idx == 11 or idx == 19: # コマンド選択 or モンスター選択
        # コマンド表示
        x_i = 50 # x座標の開始位置
        x_w = bg.get_width()*0.4
        y_i = bg.get_height()*0.6 + 40
        y_h = bg.get_height()*0.4 - 40 # 高さ
        if len(player.name) <= 2:
            x_i_t = x_i+x_w/2-25 # テキストのx座標の開始位置
        else:
            x_i_t = x_i+x_w/2-50 # テキストのx座標の開始位置
        y_i_t = y_i + 6
        pygame.draw.rect(bg, col, [x_i, y_i, x_w, y_h], 2, 5)
        pygame.draw.line(bg, col, [x_i, y_i+33], [x_i+x_w-1, y_i+33], 2) # -1がないと少し出る
        draw_text(bg, "{}".format(player.name), x_i_t, y_i_t, fnt, col)

        # COMMAND = [["こうげき", "どうぐ"], 
        # ["じゅもん", "そうび"], 
        # ["ぼうぎょ", "にげる"]]
        for i in range(3):
            for j in range(2):
                draw_text(bg, COMMAND[i][j], x_i+50+j*x_w/2, y_i+70+i*60, fnt, col)
        if idx == 11:
            if tmr%5 != 0:
                draw_text(bg, "▶︎", x_i+btl_cmd_x*x_w/2, y_i+70+btl_cmd_y*60, fnt, col)
        
        # 敵の名前表示
        x_i = bg.get_width()*0.4 + 60 # x座標の開始位置
        x_w = bg.get_width()*0.6 - 100 # 100は両端の50の合計
        y_i = bg.get_height()*0.6 + 40
        y_h = bg.get_height()*0.1 - 10 # 高さ(敵の名前1個分の高さ：62)
        x_i_t = x_i + 50 # テキストのx座標の開始位置
        y_i_t = y_i + 21 # テキストのy座標の開始位置 20+21+21=62の21
        pygame.draw.rect(bg, col, [x_i, y_i, x_w, y_h*len(monster)], 2, 5) # 枠
        for i, mon in enumerate(monster):
            draw_text(bg, "{}".format(mon.name), x_i_t, y_i_t+y_h*i, fnt, col) # font:20(20+21+21=62)
        if idx == 19:
            if tmr%5 != 0:
                draw_text(bg, "▶︎", x_i_t-50, y_i_t+y_h*btl_enemy, fnt, col) # btl_nenmy(モンスターの名前の位置)

    elif idx == 21: # 「じゅもん」選択
        # 呪文の表示
        x_i = 50 # x座標の開始位置
        x_w = bg.get_width() - 100 # 幅（両端の50を引いたのが幅）
        y_i = bg.get_height()*0.6 + 40 # 6割+40のところからメッセージ枠を出す
        y_h = bg.get_height()*0.1 - 10 # 高さ（一個分の高さ）
        x_i_t = x_i + 50 # テキストのx座標の開始位置
        y_i_t = y_i + 21 # テキストのy座標の開始位置 20+21+21=62の21
        pygame.draw.rect(bg, col, [x_i, y_i, x_w, y_h*4], 2, 5)
        for i, spell in enumerate(player.chara1_mas_spell):
            draw_text(bg, "{}".format(spell), x_i_t, y_i_t+y_h*i, fnt, col) # font:20(20+21+21=62)
        if tmr%5 != 0:
            draw_text(bg, "▶︎", x_i_t-50, y_i_t+y_h*0, fnt, col)
    else:
        # 戦闘メッセージ表示
        x_i = 50 # x座標の開始位置
        x_w = bg.get_width() - 100 # 幅（両端の50を引いたのが幅）
        y_i = bg.get_height()*0.6 + 40 # 6割+40のところからメッセージ枠を出す
        y_h = bg.get_height()*0.4 - 40 # 高さ
        pygame.draw.rect(bg, col, [x_i, y_i, x_w, y_h], 2, 5)

        for i in range(5): # 戦闘メッセージの表示
            draw_text(bg, message[i], x_i+10, y_i+10+i*40, fnt, col)

def spell_select(key):
    global idx
    ent = False
    if key[K_UP]: # ↑キー
        pass
    elif key[K_DOWN]: # ↓キー
        pass
    elif key[K_LEFT]: # ←キー
        pass
    elif key[K_RIGHT]: # →キー
        pass
    elif key[K_SPACE] or key[K_RETURN]: # 決定
        ent = True
    elif key[K_b]: # キャンセル
        idx = 11
    return ent

def battle_command(bg, key): # コマンドの入力と表示
    global btl_cmd_x, btl_cmd_y
    ent = False # Trueで返すと選択したコマンド(btl_cmd)を実行する
    if key[K_UP] and btl_cmd_y > 0: # ↑キー
        btl_cmd_y -= 1
    elif key[K_DOWN] and btl_cmd_y < 2: # ↓キー
        btl_cmd_y += 1
    elif key[K_LEFT] and btl_cmd_x > 0: # ←キー
        btl_cmd_x -= 1
    elif key[K_RIGHT] and btl_cmd_x < 1: # →キー
        btl_cmd_x += 1
    elif key[K_SPACE] or key[K_RETURN]: # 決定s
        ent = True
    return ent

def battle_select(bg, key):
    global idx, btl_enemy
    ent = False
    if key[K_UP] and btl_enemy > 0: # ↑キー
        btl_enemy -= 1
    elif key[K_DOWN] and btl_enemy < len(monster)-1: # ↓キー
        btl_enemy += 1
    elif key[K_SPACE] or key[K_RETURN]: # 決定
        ent = True
    elif key[K_b]: # キャンセル
        idx = 11
    return ent

def set_battle_turn(num, player): # 0:通常、1:先制攻撃、2:不意打ち
    global battle_order
    tmp_order = {}
    if num == 0 or num == 1:
        r = random.randint(66, 100)
        tmp_order[player] = int(player.quick * r/100)
    if num == 0 or num == 2:
        for mon in monster:
            r = random.randint(66, 100)
            tmp_order[mon] = int(mon.quick * r/100)
    # [(obj, quick), (ojb, quick), ...]のリストになる
    battle_order = sorted(tmp_order.items(), key=lambda x:x[1], reverse=True)

def get_battle_turn(player):
    global battle_order
    if not battle_order: # 全て消えたらプレイヤーのコマンド選択
        return None, 11
    # [(obj, quick), (ojb, quick), ...]のリスト、[0][0]で先頭（ターン）のobjを取得
    turn_key = battle_order[0][0]
    battle_order.pop(0) # 先頭を削除
    if turn_key is player:
        return turn_key, player.act
    else:
        return turn_key, 13

def del_battle_turn(obj1): # ターン内に気絶したオブエクトを削除（気絶したオブジェクトが攻撃しないように）
    for i, obj2 in enumerate(battle_order): # 行がobj2に入る, iはi行目
        if obj1 is obj2[0]: # obj2[0]は各行の1列目（オブジェクト）２列目は素早さ
            battle_order.pop(i) # i行目を削除

# 戦闘メッセージの表示処理
message = [""]*5
def init_message():
    for i in range(5):
        message[i] = ""
    
def set_message(msg):
    for i in range(5):
        if message[i] == "":
            message[i] = msg
            return
    for i in range(4): # 下が最新のメッセージ
        message[i] = message[i+1]
    message[4] = msg



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
                    idx = 21
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
            if tmr == 38:
                tmp_spell = player.master_spell()
                if tmp_spell != "":
                    set_message(tmp_spell + " を覚えた")
            if tmr == 40:
                if player.exp >= player.lv_exp:
                    idx = 17
                    tmr = 0
            if tmr == 45:
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

        elif idx == 21: # コマンドで「じゅもん」を選択
            draw_battle(screen, fontS, turn_obj, player)
            if spell_select(key) == True:
                player.act = 25 # get_battle_turnの戻り値idxを25
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




