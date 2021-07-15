

import pyxel
from source.module.appstatus import AppStatus


class AppSytem:

    _sts: AppStatus

    def __init__(self):
        self._sts = AppStatus()


    #システムデータのロード
    def load_system_data(self):
        pyxel.load("assets/system/system-data.pyxres") #システムデータを読み込む
        self._sts.game_difficulty = pyxel.tilemap(0).get(0,120) - 16 #数字の[0]はアスキーコード16番なので16引いて数値としての0にしてやります
        self.stage_number    = pyxel.tilemap(0).get(0,121) - 16
        self.stage_loop      = pyxel.tilemap(0).get(0,122) - 16
        self.stage_age       = 0
        #総ゲームプレイ時間(秒)を計算する
        sec_1  = pyxel.tilemap(0).get(9,5) - 16 #秒の  1の位取得
        sec_10 = pyxel.tilemap(0).get(8,5) - 16 #秒の  10の位取得
        min_1  = pyxel.tilemap(0).get(6,5) - 16 #分の  1の位取得
        min_10 = pyxel.tilemap(0).get(5,5) - 16 #分の  10の位取得
        hour_1 = pyxel.tilemap(0).get(3,5) - 16 #時の   1の位取得
        hour_10 = pyxel.tilemap(0).get(2,5) - 16 #時の   10の位取得
        hour_100 = pyxel.tilemap(0).get(1,5) - 16 #時の   100の位取得
        hour_1000 = pyxel.tilemap(0).get(0,5) - 16 #時の   1000の位取得
        
        s = sec_10 * 10 + sec_1
        m = min_10 * 10 + min_1
        h = hour_1000 * 1000 + hour_100 * 100 + hour_10 * 10 + hour_1
        t_sec = h * 3600 + m * 60 + s
        self.total_game_playtime_seconds = t_sec
        
        #総開発テスト時間(分)を計算する
        min_1  = pyxel.tilemap(0).get(7,3) - 16 #分の  1の位取得
        min_10 = pyxel.tilemap(0).get(6,3) - 16 #分の  10の位取得
        hour_1 = pyxel.tilemap(0).get(4,3) - 16 #時の   1の位取得
        hour_10 = pyxel.tilemap(0).get(3,3) - 16 #時の   10の位取得
        hour_100 = pyxel.tilemap(0).get(2,3) - 16 #時の   100の位取得
        hour_1000 = pyxel.tilemap(0).get(1,3) - 16 #時の   1000の位取得
        hour_10000 = pyxel.tilemap(0).get(0,3) - 16 #時の   10000の位取得
        m = min_10 * 10 + min_1
        h = hour_10000 * 10000 + hour_1000 * 1000 + hour_100 * 100 + hour_10 * 10 + hour_1
        t_min = h * 60 + m
        self.total_development_testtime_min = t_min
        
        #デバッグモード＆ゴッドモード用のフラグやパラメーターの初期化とか宣言はこちらで行うようにします
        #debug_menu_status                  #デバッグパラメータの表示ステータス
                                            #0=表示しない 1=フル表示タイプ 2=簡易表示タイプ
        self.debug_menu_status             = (pyxel.tilemap(0).get(0,126)) - 16 #数字の[0]はアスキーコード16番なので16引いて数値としての0にしてやります
        
        #boss_collision_rect_display_flag        ボス用の当たり判定確認の為の矩形表示フラグ(デバッグ時に1にします)
        self.boss_collision_rect_display_flag = (pyxel.tilemap(0).get(0,127)) - 16
        #bg_collision_Judgment_flag            背景の障害物との衝突判定を行うかどうかのフラグ
                                            #0=背景の障害物との当たり判定をしない 1=行う
        self.bg_collision_Judgment_flag      = (pyxel.tilemap(0).get(0,128)) - 16
        #boss_test_mode                      ボス戦闘のみのテストモード 
                                            #0=オフ 1=オン scroll_countを増やさない→マップスクロールしないので敵が発生しません
                                            #イベントリストもボス専用の物が読み込まれます
        self.boss_test_mode                = (pyxel.tilemap(0).get(0,129)) - 16
        #no_enemy_mode                       マップチップによる敵の発生を行わないモードのフラグですです(地上の敵が出ない！)2021 03/07現在機能してない模様
                                            #0=マップスクロールによって敵が発生します
                                            #1=                    発生しません        
        self.no_enemy_mode                 = (pyxel.tilemap(0).get(0,130)) - 16
        #god_mode_status                    #ゴッドモードのステータス
                                            #0=ゴッドモードオフ 1=ゴッドモードオン
        self.god_mode_status               = (pyxel.tilemap(0).get(0,131)) - 16
        #fullscreen_mode                    #フルスクリーンでの起動モード
                                            #0=ウィンドウモードでの起動 1=フルスクリーンモードでの起動
        self.fullscreen_mode               = (pyxel.tilemap(0).get(0,132)) - 16
        #ctrl_type                          #コントロールパッドのタイプ
                                            #0~5
        self.ctrl_type                     = (pyxel.tilemap(0).get(0,133)) - 16
        #master_bgm_vol                     #BGMのマスターボリューム
                                            #0~100
        self.master_bgm_vol                = self.read_system_data_num(2,134,3)
        #master_se_vol                      #SEのマスターボリューム
                                            #0~7
        self.master_se_vol                 = self.read_system_data_num(2,135,3)
        #language                           #選択言語
                                            #0=英語 1=日本語
        self.language                      = (pyxel.tilemap(0).get(0,136)) - 16
        
        # self.test_read_num = self.read_system_data_num(15,156,16) #数値の読み取りテストです



    #漢字フォントデータの読み込み
    def load_kanji_font_data(self):
        
        pyxel.load("assets/fonts/misaki_font_k8x12s_001.pyxres") #漢字フォントデータ(その1)を読み込みます
        # self.kanji_fonts = [] #漢字フォントリストデータをまずは初期化して使えるようにします この方法だとダメだわ
        self.kanji_fonts = [[None for col in range(752)] for row in range(1128)] #横752,縦1128の空っぽの漢字フォントデータリストを作成します(Pythonクックブックで奨められている書き方ですのんって、判りにくいよなぁ・・これ)
        
        for y in range(256):  #左端A列のk8x12s_jisx0208___001a.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(0,0)
            for x in range(256):
                col = pyxel.image(0).get(x,y)
                self.kanji_fonts[y+0][x+0] = col #ぐへぇ最初, self.kanji_fonts[x][y] = colってやってた・・リストの最初の[]はy軸になるんだよね・考えてみればそうだったｗ 嵌りどころだわ～～～～
        for y in range(256):  #左端A列のk8x12s_jisx0208___002a.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(0,256)
            for x in range(256):
                col = pyxel.image(1).get(x,y)
                self.kanji_fonts[y+256][x+0] = col
        for y in range(256):  #左端A列のk8x12s_jisx0208___003a.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(0,512)
            for x in range(256):
                col = pyxel.image(2).get(x,y)
                self.kanji_fonts[y+512][x+0] = col
        
        pyxel.load("assets/fonts/misaki_font_k8x12s_002.pyxres") #漢字フォントデータ(その2)を読み込みます
        for y in range(256):  #左端A列の  k8x12s_jisx0208___004a.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(0,768)
            for x in range(256):
                col = pyxel.image(0).get(x,y)
                self.kanji_fonts[y+768][x+0] = col
        for y in range(256):  #真ん中B列のk8x12s_jisx0208___001b.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(256,0)
            for x in range(256):
                col = pyxel.image(1).get(x,y)
                self.kanji_fonts[y+0][x+256] = col
        for y in range(256):  #真ん中B列のk8x12s_jisx0208___002b.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(256,256)
            for x in range(256):
                col = pyxel.image(2).get(x,y)
                self.kanji_fonts[y+256][x+256] = col
        
        pyxel.load("assets/fonts/misaki_font_k8x12s_003.pyxres") #漢字フォントデータ(その3)を読み込みます
        for y in range(256):  #真ん中B列のk8x12s_jisx0208___003b.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(256,512)
            for x in range(256):
                col = pyxel.image(0).get(x,y)
                self.kanji_fonts[y+512][x+256] = col
        for y in range(256):  #真ん中B列のk8x12s_jisx0208___004b.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(256,768)
            for x in range(256):
                col = pyxel.image(1).get(x,y)
                self.kanji_fonts[y+768][x+256] = col
        for y in range(256):  #右端C列の  k8x12s_jisx0208___001c.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(512,0)
            for x in range(752-512):
                col = pyxel.image(2).get(x,y)
                self.kanji_fonts[y+0][x+512] = col
        
        pyxel.load("assets/fonts/misaki_font_k8x12s_004.pyxres") #漢字フォントデータ(その4)を読み込みます
        for y in range(256):  #真ん中B列のk8x12s_jisx0208___002c.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(512,256)
            for x in range(752-512):
                col = pyxel.image(0).get(x,y)
                self.kanji_fonts[y+256][x+512] = col
        for y in range(256):  #真ん中B列のk8x12s_jisx0208___003c.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(512,512)
            for x in range(752-512):
                col = pyxel.image(1).get(x,y)
                self.kanji_fonts[y+512][x+512] = col
        for y in range(256):  #右端C列の  k8x12s_jisx0208___004c.pngを読みだしてフォントデータリストに書き込んでいきます 書き込みオフセット値は(512,768)
            for x in range(752-512):
                col = pyxel.image(2).get(x,y)
                self.kanji_fonts[y+768][x+512] = col

    #漢字テキストの表示
    def kanji_text(self,x,y,text,col):
        base_x,base_y = x,y
        for char in text:
            found = self.font_code_table.find(char) #foundにテキスト(char)を使ってフォント対応表にある位置を調べる→位置がfoundに入ります(見つからなかったらfoundに-1が入ります)
            if found >= 0 and char != '\n': #文字を見つけて尚且つ改行コードでないのなら漢字を描画し始めます
                sy = self.font_code_table[:found].count('\n') #対応表のリストの先頭から改行コードの数を数えるとその数値がY座標となります
                sx = self.font_code_table.split('\n')[sy].find(char)
                
                for i in range(8): #漢字フォントの横ドット数8
                    for j in range(12): #漢字フォントの縦ドット数12
                        if self.kanji_fonts[(sy-1)*12+j][sx*8+i] == 7: #フォントのデータは 0=黒が透明で 7=白が描画する点なので色コードが7だったらpsetで点を打ちます
                            pyxel.pset(x+i,y+j,col)
                
                x += 8
                if char == '\n':
                    x = base_x
                    y += 12

