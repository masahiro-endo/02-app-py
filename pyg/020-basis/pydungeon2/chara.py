
import gspread
import pygame
import random
from pygame.locals import *

import os.path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Google Cloud Platform
# https://console.cloud.google.com/apis/api/sheets.googleapis.com/quotas?hl=ja

from oauth2client.service_account import ServiceAccountCredentials 
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread-serialize-185488b.json', scope)
gc = gspread.authorize(credentials)
# https://docs.google.com/spreadsheets/d/11f13rV05c2LzQ6nUIdJK6bbCxuONfkX7O4Gj8QdVXQk/edit#gid=0
SPREADSHEET_KEY = '11f13rV05c2LzQ6nUIdJK6bbCxuONfkX7O4Gj8QdVXQk'

wb = gc.open_by_key(SPREADSHEET_KEY)
ws_chara = wb.worksheet("勇者")
ws_mon = wb.worksheet("モンスター")

chara1_name = ws_chara.acell('C2').value
chara1_maxhp = ws_chara.col_values(5) # E列
chara1_hp = ws_chara.acell('F2').value
chara1_maxmp = ws_chara.col_values(7) # G列
chara1_mp = ws_chara.acell('H2').value
chara1_quick = ws_chara.col_values(9) # I列
chara1_atk = ws_chara.col_values(10) # J列
chara1_dfs = ws_chara.col_values(11) # K列
chara1_exp = ws_chara.col_values(12) # L列
chara1_spell = ws_chara.col_values(13) # M列 ←覚える呪文

mon_name = ws_mon.col_values(2) # B列
mon_maxhp = ws_mon.col_values(4) # D列
mon_quick = ws_mon.col_values(8) # H列
mon_atk = ws_mon.col_values(9) # I列
mon_dfs = ws_mon.col_values(10) # J列
mon_exp = ws_mon.col_values(11) # K列

class Chara():
    def attack(self, obj):
        base_dmg = self.atk/2 - obj.dfs/4
        if base_dmg <= 0:
            return 0
        width_dmg = base_dmg/16 + 1
        min_dmg = int(base_dmg - width_dmg)
        max_dmg = int(base_dmg + width_dmg)
        return random.randint(min_dmg, max_dmg)
    def defense(self):
        self.dfs *= 2

class Brave(Chara):
    def __init__(self):
        self.name = chara1_name
        self.lv = 1
        self.maxhp = int(chara1_maxhp[self.lv])
        self.hp = self.maxhp
        self.maxmp = int(chara1_maxmp[self.lv])
        self.mp = self.maxmp
        self.quick = int(chara1_quick[self.lv])
        self.atk = int(chara1_atk[self.lv])
        self.dfs = int(chara1_dfs[self.lv])
        self.lv_exp = int(chara1_exp[self.lv])
        self.exp = 0
        self.chara1_mas_spell = [] # 覚えた呪文
        if chara1_spell[self.lv] != "": # レベル1で覚える呪文があるなら
            self.chara1_mas_spell.append(chara1_spell[self.lv])

        self.act = 0 # 戦闘のコマンド（行動）12:攻撃、18:防御
        self.img = [
                pygame.image.load("image/mychr0.png"), # 上
                pygame.image.load("image/mychr1.png"), # 上
                pygame.image.load("image/mychr2.png"), # 下
                pygame.image.load("image/mychr3.png"), # 下
                pygame.image.load("image/mychr4.png"), # 左
                pygame.image.load("image/mychr5.png"), # 左
                pygame.image.load("image/mychr6.png"), # 右
                pygame.image.load("image/mychr7.png"), # 右
                pygame.image.load("image/mychr8.png") # 倒れた
            ]
        self.x = 0 # プレイヤーのx座標
        self.y = 0 # プレイヤーのy座標
        self.d = 0 # プレイヤーの向き 0:上 1:下 2:左 3:右
        self.a = 0 # imgPlayerの添字
    def reset(self):
        self.hp = self.maxhp
        self.mp = self.maxmp
    def lv_up(self):
        self.lv += 1
        self.maxhp = int(chara1_maxhp[self.lv])
        self.maxmp = int(chara1_maxmp[self.lv])
        self.quick = int(chara1_quick[self.lv])
        self.atk = int(chara1_atk[self.lv])
        self.dfs = int(chara1_dfs[self.lv])
        self.lv_exp = int(chara1_exp[self.lv])

    def re_defense(self):
        # 呪文効果とかが残っているか確認
        self.dfs = int(chara1_dfs[self.lv])

    def master_spell(self):
        if chara1_spell[self.lv] != "": # レベルアップして覚える呪文があるなら
            self.chara1_mas_spell.append(chara1_spell[self.lv])
            return chara1_spell[self.lv]
        return ""
        
class Monster(Chara):
    def __init__(self, num):
        self.num = num
        self.img = pygame.image.load("image/enemy"+str(num)+".png")
        self.name = mon_name[num]
        self.maxhp = int(mon_maxhp[num])
        self.hp = self.maxhp
        self.quick = int(mon_quick[num])
        self.atk = int(mon_atk[num])
        self.dfs = int(mon_dfs[num])
        self.exp = int(mon_exp[num])
        self.x = 0 # 画像の表示位置
        self.y = 0 # 画像の表示位置
    def set_name(self, num):
        if num == 0:
            self.name += " A"
        elif num == 1:
            self.name += " B"
        elif num == 2:
            self.name += " C"
        elif num == 3:
            self.name += " D"
    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y
    def re_defense(self):
        # 呪文効果とかが残っているか確認
        self.dfs = int(mon_dfs[self.num])




