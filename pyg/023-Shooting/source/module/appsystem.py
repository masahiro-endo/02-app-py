

import pyxel
from module.appstatus import AppStatus


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

    #シャドウドロップテキスト(影落ちテキスト)の表示
    def shadow_drop_text(self,x,y,text,col):
        pyxel.text(x+1,y,  text,0)
        pyxel.text(x+1,y+1,text,0)
        pyxel.text(x,  y,  text,col)

    #システムデータからの数値読み込み
    def read_system_data_num(self,x,y,digit):      #x,yは1の位の座標です digitは桁数です
        global num   #なんやようわからんが・・・global命令で 「numはグローバル変数やで～」って宣言したら上手くいくようになった、なんでや・・・？？謎
        num = 0
        a = 1
        for i in range(digit):
            n = pyxel.tilemap(0).get(x-i,y) - 16
            num += n * a
            a = a * 10
        return(num)

    #システムデータへの数値書き込み
    def write_system_data_num(self,x,y,digit,num): #x,yは1の位の座標です digitは桁数 numは書き込む数値です(整数を推奨)
        a = 10
        for i in range(digit):
            n = num % a*10 // a
            pyxel.tilemap(0).set(x-i,y,n + 16)
            a = a * 10                      #めっちゃ判りにくいなぁ・・・試行錯誤で上手くいった？かも？です！？
                                            #書き込みテストで段々ステップアップしていくと上手くいくね☆彡
        
        #書き込みテストその１ 0からdigit桁数まで数値と桁数が増えてく digit=1なら0 digit=3なら210 digit=7なら6543210 digit=10なら9876543210
        # n = 0 
        # for i in range(digit):
            # pyxel.tilemap(0).set(x-i,y,n + 16)
            # n += 1
        
        #書き込みテストその２
        # for i in range(digit):
            # pyxel.tilemap(0).set(x-i,y,(digit - i) + 16)


    #システムデータのセーブ
    def save_system_data(self):
        pyxel.load("assets/system/system-data.pyxres") #システムデータにアクセスするためにローディングだけしてやります(グラフイック関連のアセットをローディングしている時がほとんどなので)
        #各種設定値書き込み 数字の[0]はアスキーコード16番なので16足してアスキーコードとしての0にしてやります
        pyxel.tilemap(0).set(0,120,self.game_difficulty + 16)                 #難易度書き込み
        pyxel.tilemap(0).set(0,121,self.stage_number + 16)                    #スタートステージ数書き込み
        pyxel.tilemap(0).set(0,122,self.stage_loop + 16)                      #スタート周回数書き込み
        pyxel.tilemap(0).set(0,126,self.debug_menu_status + 16)               #デバッグメニュー表示フラグ書き込み
        pyxel.tilemap(0).set(0,127,self.boss_collision_rect_display_flag + 16)#ボス当たり判定矩形表示フラグ書き込み
        pyxel.tilemap(0).set(0,128,self.bg_collision_Judgment_flag + 16)      #BGとの当たり判定フラグ書き込み
        pyxel.tilemap(0).set(0,129,self.boss_test_mode + 16)                  #ボステストモードフラグ書き込み
        pyxel.tilemap(0).set(0,130,self.no_enemy_mode + 16)                   #敵が出ないモードフラグ書き込み
        pyxel.tilemap(0).set(0,131,self.god_mode_status + 16)                 #ゴッドモードフラグ書き込み
        pyxel.tilemap(0).set(0,132,self.fullscreen_mode + 16)                 #フルスクリーン起動フラグ書き込み
        pyxel.tilemap(0).set(0,133,self.ctrl_type + 16)                       #パッドコントロールタイプ書き込み
        self.write_system_data_num(2,134,3,self.master_bgm_vol)               #マスターBGMボリューム値書き込み
        self.write_system_data_num(2,135,3,self.master_se_vol)                #マスターSEボリューム値書き込み
        pyxel.tilemap(0).set(0,136,self.language + 16)                        #選択言語書き込み
        
        #総ゲームプレイ時間(秒)のそれぞれの桁の数値を計算する (自分でも訳が分からないよ・・・)------------------------------
        t_sec = self.total_game_playtime_seconds
        se = t_sec % 60       #se 秒は 総秒数を60で割った余り
        mi = t_sec // 60 % 60  #mi 分は 総秒数を60で割った数(切り捨て)を更に60で割った余り
        ho = t_sec // 3600    #ho 時は 総秒数を3600で割った数(切り捨て)
        #それぞれの桁の数値(0~9)を計算して求めていく
        sec_1  = se  % 10
        sec_10 = se // 10
        min_1  = mi  % 10
        min_10 = mi // 10
        hour_1 = ho % 10
        hour_10 = ho % 100 // 10
        hour_100 = ho % 1000 // 100
        hour_1000 = ho % 10000 // 1000
        #総ゲームプレイ時間(秒)を書き込んでいく
        pyxel.tilemap(0).set(9,5,sec_1 + 16) #秒の  1の位を書き込む
        pyxel.tilemap(0).set(8,5,sec_10 + 16) #秒の  10の位を書き込む
        pyxel.tilemap(0).set(6,5,min_1 + 16) #分の  1の位を書き込む
        pyxel.tilemap(0).set(5,5,min_10 + 16) #分の  10の位を書き込む
        pyxel.tilemap(0).set(3,5,hour_1  + 16) #時の   1の位を書き込む
        pyxel.tilemap(0).set(2,5,hour_10 + 16) #時の   10の位を書き込む
        pyxel.tilemap(0).set(1,5,hour_100 + 16) #時の   100の位を書き込む
        pyxel.tilemap(0).set(0,5,hour_1000 + 16) #時の   1000の位を書き込む
        
        #総開発テストプレイ時間(分)を計算します------------------------------------------------------
        self.total_development_testtime_min += self.one_game_playtime_seconds // 60 #今プレイしているゲームの時間(分)を総ゲームテスト時間に加算
        t_dev_min = self.total_development_testtime_min
        mi = t_dev_min % 60    #mi 分は 総分数を60で割った余り
        ho = t_dev_min // 60      #ho 時は 総秒数を60で割った数(切り捨て)
        #それぞれの桁の数値(0~9)を計算して求めていく
        min_1  = mi  % 10
        min_10 = mi // 10
        hour_1 = ho % 10
        hour_10 = ho % 100 // 10
        hour_100 = ho % 1000 // 100
        hour_1000 = ho % 10000 // 1000
        hour_10000 = ho % 100000 // 10000
        #総開発テストプレイ時間を書き込んでいく
        pyxel.tilemap(0).set(7,3,min_1 + 16) #分の  1の位を書き込む
        pyxel.tilemap(0).set(6,3,min_10 + 16) #分の  10の位を書き込む
        pyxel.tilemap(0).set(4,3,hour_1  + 16) #時の   1の位を書き込む
        pyxel.tilemap(0).set(3,3,hour_10 + 16) #時の   10の位を書き込む
        pyxel.tilemap(0).set(2,3,hour_100 + 16) #時の   100の位を書き込む
        pyxel.tilemap(0).set(1,3,hour_1000 + 16) #時の   1000の位を書き込む
        pyxel.tilemap(0).set(0,3,hour_10000 + 16) #時の   10000の位を書き込む
        
        self.write_system_data_num(16,152,16,8777992360588341) #!############################ test write
        
        test_num = -0.123
        test_num = test_num * 1000
        test_num = test_num + 1000                             #この式と逆の方法で計算してやれば符号の付いた実数値を取り出せる
        self.write_system_data_num(10,162,10,int(test_num))    #!############################ test write マイナス符号付き実数値の数値が書き込めるかのテスト
        
        pyxel.save("assets/system/system-data.pyxres") #システムデータを書き込み


    def update_ipl(self):
        self.display_ipl_time -= 1    #IPLメッセージを表示する時間カウンターを1減らす
        if self.display_ipl_time <= 0: #カウンターが0以下になったら・・・
            self.game_status = SCENE_TITLE_INIT #ゲームステータスを「SCENE_TITLE_INIT(タイトル表示に必要な変数を初期化)」にする
        
        if (pyxel.frame_count % 10) == 0:
            if len(self.ipl_mes1) > self.ipl_mes_write_line_num: #まだ書き込むべき文字列があるのなら・・・
                text_mes = str(self.ipl_mes1[self.ipl_mes_write_line_num][0])
                text_col = str(self.ipl_mes1[self.ipl_mes_write_line_num][1])
                self.text_screen.append([text_mes,text_col]) #文字列群をテキストスクリーンのリストに追加する
                self.ipl_mes_write_line_num +=1  #スクリーンに表示したIPLメッセージデータの行数カウンタを1インクリメント

    #タイトル表示に必要な変数を設定＆初期化する##############
    def update_title_init(self):
        pyxel.load("assets/graphic/min-sht2.pyxres") #タイトル＆ステージ1＆2のリソースファイルを読み込む
        #タイトル関連の変数を初期化
        
        self.display_title_time = 204               #タイトルを表示する時間
        self.title_oscillation_count = 200          #タイトルグラフイックの振れ幅カウンター
        self.title_slash_in_count =    100          #タイトルグラフイックが下から切り込んで競りあがってくる時に使うカウンター
        
        # self.display_title_time      = 10         #タイトルを表示する時間
        # self.title_oscillation_count = 10         #タイトルグラフイックの振れ幅カウンター
        # self.title_slash_in_count =    10         #タイトルグラフイックが下から切り込んで競りあがってくる時に使うカウンター
        
        self.stars = []                        #タイトル表示時も背景の星を流したいのでリストをここで初期化してやります
        self.star_scroll_speed = 1             #背景の流れる星のスクロールスピード 1=通常スピード 0.5なら半分のスピードとなります
        self.window = []                       #タイトル表示時もメッセージウィンドウを使いたいのでリストをここで初期化してあげます
        self.cursor = []                       #タイトル表示時もウィンドウカーソルを使いたいのでリストをここで初期化してあげます
        
        #リプレイ記録用に使用する横無限大,縦50ステージ分の空っぽのリプレイデータリストを作成します
        self.replay_recording_data =[[] for i in range(50)]
        
        self.bg_cls_color = 0         #BGをCLS(クリアスクリーン)するときの色の指定(通常は0=黒色です)ゲーム時に初期値から変更されることがあるのでここで初期化する
        
        # セレクトカーソル関連の変数宣言   タイトル画面でセレクトカーソルを使いたいのでここで変数などを宣言＆初期化します
        self.cursor_type = CURSOR_TYPE_NO_DISP #セレクトカーソルを表示するかしないかのフラグ用
        self.cursor_x = 0                      #セレクトカーソルのx座標
        self.cursor_y = 0                      #セレクトカーソルのy座標
        self.cursor_step_x = 4                 #横方向の移動ドット数(初期値は4ドット)
        self.cursor_step_y = 7                 #縦方向の移動ドット数(初期値は7ドット)
        self.cursor_page = 0                   #いま指し示しているページナンバー
        self.cursor_pre_page = 0               #前フレームで表示していたページ数 pre_pageとpageが同じなら新規ウィンドウは育成しない
        self.cursor_page_max = 0               #セレクトカーソルで捲ることが出来る最多ページ数
        self.cursor_item_x = 0                 #いま指し示しているアイテムナンバーx軸方向
        self.cursor_item_y = 0                 #いま指し示しているアイテムナンバーy軸方向
        self.cursor_decision_item_x = -1       #ボタンが押されて「決定」されたアイテムのナンバーx軸方向 -1は未決定 ここをチェックしてどのアイテムが選択されたのか判断する
        self.cursor_decision_item_y = -1       #ボタンが押されて「決定」されたアイテムのナンバーy軸方向 -1は未決定 ここをチェックしてどのアイテムが選択されたのか判断する
        self.cursor_max_item_x = 0             #x軸の最大項目数 5の場合(0~4)の5項目分カーソルが移動することになります 3だったら(0~2)って感じで
        self.cursor_max_item_y = 0             #y軸の最大項目数 5の場合(0~4)の5項目分カーソルが移動することになります 3だったら(0~2)って感じで
        self.cursor_color = 0                  #セレクトカーソルの色
        self.cursor_menu_layer = 0             #現在選択中のメニューの階層の数値が入ります
        self.cursor_pre_decision_item_y = 0    #前の階層で選択したアイテムのナンバーを入れます
                                            #選択してcursor_decision_item_yに入ったアイテムナンバーをcursor_pre_decision_item_yに入れて次の階層に潜るって手法かな？
        self.cursor_move_direction = 0         #セレクトカーソルがどう動かせることが出来るのか？の状態変数です
        self.cursor_move_data = 0              #カーソルが実際に動いた方向のデータが入ります
        
        self.active_window_id = 0              #アクティブになっているウィンドウのIDが入ります
        self.active_window_index = 0           #アクティブになっているウィンドウのインデックスナンバー(i)が入ります(ウィンドウIDを元にして全ウィンドウデータから検索しインデックス値を求めるのです！)
        #system-data.pyxresリソースファイルからこれらの設定値を読み込むようにしたのでコメントアウトしています
        # self.game_difficulty = GAME_NORMAL         #難易度                  タイトルメニューで難易度を選択して変化させるのでここで初期化します
        
        self.stage_number = STAGE_MOUNTAIN_REGION  #最初に出撃するステージ   タイトルメニューでステージを選択して変化させるのでここで初期化します
        self.stage_loop   = 1                      #ループ数(ステージ周回数) タイトルメニューで周回数を選択して変化させるのでここで初期化します
        
        pygame.mixer.init(frequency = 44100)     #pygameミキサー関連の初期化
        pygame.mixer.music.set_volume(0.7)       #音量設定(0~1の範囲内)
        pygame.mixer.music.load('assets/music/BGM200-171031-konotenitsukame-intro.wav') #タイトルイントロ部分のwavファイルを読み込み
        pygame.mixer.music.set_volume(self.master_bgm_vol / 100)
        pygame.mixer.music.play(1)               #イントロを1回だけ再生
        
        self.game_status = SCENE_TITLE           #ゲームステータスを「SCENE_TITLE」にしてタイトル表示を開始する

    #タイトルの更新#######################################
    def update_title(self):
        self.display_title_time -= 1          #タイトルを表示する時間カウンターを1減らす
        if self.display_title_time <= 0:      #カウンターが0以下になったら・・・
            self.display_title_time = 0       #強制的に0の状態にする
        
        self.title_oscillation_count -= 1     #タイトルグラフイックの振れ幅カウンターを1減らす
        if self.title_oscillation_count < 0:  #カウンターが0以下になったら・・・
            self.title_oscillation_count = 0  #強制的に0の状態にする
        
        self.title_slash_in_count -= 1        #タイトルグラフイックが下から切り込んで競りあがってくる時に使うカウンターを1減らす
        if self.title_slash_in_count < 0:     #カウンターが0以下になったら・・・
            self.title_slash_in_count = 0     #強制的に0の状態にする
        
        #BGMイントロ再生が終了したらBGMループ部分を再生し始める
        if pygame.mixer.music.get_pos() == -1:      #pygame.mixer.music.get_posはBGM再生が終了すると-1を返してきます
            pygame.mixer.init(frequency = 44100)    #pygameミキサー関連の初期化
            pygame.mixer.music.set_volume(0.7)      #音量設定(0~1の範囲内)
            pygame.mixer.music.load('assets/music/BGM200-171031-konotenitsukame-loop.wav') #タイトルBGMループ部分のwavファイルを読み込み
            pygame.mixer.music.set_volume(self.master_bgm_vol / 100)
            pygame.mixer.music.play(-1)             #タイトルBGMをループ再生
        
        #全てのカウンター類が0になったらゲームメニューウィンドウを育成する
        if self.title_oscillation_count == 0 and self.title_slash_in_count == 0 and self.display_title_time == 0:
            self.create_window(WINDOW_ID_MAIN_MENU)             #メニューウィンドウを作製
            #選択カーソル表示をon,カーソルは上下移動のみ,いま指示しているアイテムナンバーは0,まだボタンも押されておらず未決定状態なのでdecision_item_yは-1
            #選択できる項目数は11項目なので 11-1=10を代入,メニューの階層は最初は0にします,カーソル移動ステップはx4,y7
            self.set_cursor_data(CURSOR_TYPE_NORMAL,CURSOR_MOVE_UD,49,44,STEP4,STEP7,0,0,0,0,UNSELECTED,UNSELECTED,0,11-1,0,MENU_LAYER0)
            self.active_window_id = WINDOW_ID_MAIN_MENU         #このウィンドウIDを最前列アクティブなものとする
            self.game_status = SCENE_TITLE_MENU_SELECT          #ゲームステータスを「TITLE_MENU_SELECT」(タイトルでメニューを選択中)」にする

    #タイトルメニューの選択中の更新#####################################
    def update_title_menu_select(self):
        if   self.cursor_menu_layer == 0: #メニューが0階層目の選択分岐
            if   self.cursor_decision_item_y == 0:            #GAME STARTが押されたら
                self.cursor_type = CURSOR_TYPE_NO_DISP      #セレクトカーソルの表示をoffにする
                self.move_mode = MOVE_MANUAL                #移動モードを「手動移動」にする
                self.replay_status = REPLAY_RECORD          #リプレイデータを「記録中」にする
                self.start_stage_number = self.stage_number #リプレイファイル保存用にゲーム開始時のステージナンバーとループ数を保管しておきます（リプレイデータはゲーム終了後にセーブされるのでstage_numberなどの値が変化するのでstart_stage_numberって変数を作ってリプレイ記録時にはこれを使うのです)
                self.start_stage_loop   = self.stage_loop
                self.game_status = SCENE_GAME_START_INIT    #ゲームステータスを「GAME_START_INIT」にしてゲーム全体を初期化＆リスタートする
                self.active_window_id = WINDOW_ID_MAIN_MENU #メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_decision_item_y == 1:            #SELECT STAGEが押されて
                if self.search_window_id(WINDOW_ID_SELECT_STAGE_MENU) == -1: #SELECT_STAGE_MENUウィンドウが存在しないのなら・・
                    self.move_left_main_menu_window() #メインメニューウィンドウを左にずらす関数の呼び出し
                    
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「SELECT STAGE」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)       #メインメニューのカーソルデータをPUSH
                    self.create_window(WINDOW_ID_SELECT_STAGE_MENU)  #ステージセレクトウィンドウの作製
                    #選択カーソル表示をon,カーソルは上下移動のみ,,カーソル移動ステップはx4,y7,いま指示しているアイテムナンバーは0の「1」
                    #まだボタンも押されておらず未決定状態なのでdecision_item_yはUNSELECTED,y最大項目数は3項目なので 3-1=2を代入,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_NORMAL,CURSOR_MOVE_UD,92,71,STEP4,STEP7,0,0,0,0,UNSELECTED,UNSELECTED,0,3-1,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_SELECT_STAGE_MENU #このウィンドウIDを最前列アクティブなものとする
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 2:            #SELECT LOOPが押されて
                if self.search_window_id(WINDOW_ID_SELECT_LOOP_MENU) == -1: #SELECT_LOOP_MENUウィンドウが存在しないのなら・・
                    self.move_left_main_menu_window() #メインメニューウィンドウを左にずらす関数の呼び出し
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「SELECT LOOP」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPUSH
                    self.create_window(WINDOW_ID_SELECT_LOOP_MENU)      #ループセレクトウィンドウの作成
                    #選択カーソル表示をon,カーソルは上下移動のみ,,カーソル移動ステップはx4,y7,いま指示しているアイテムナンバーは0の「1」
                    #まだボタンも押されておらず未決定状態なのでdecision_item_yはUNSELECTED,y最大項目数は3項目なので 3-1=2を代入,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_NORMAL,CURSOR_MOVE_UD,90+24,72+5,STEP4,STEP7,0,0,0,0,UNSELECTED,UNSELECTED,0,3-1,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_SELECT_LOOP_MENU  #このウィンドウIDを最前列でアクティブなものとする
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 3:            #BOSS MODEが押されて
                if self.search_window_id(WINDOW_ID_BOSS_MODE_MENU) == -1: #BOSS MODEウィンドウが存在しないのなら・・
                    self.move_left_main_menu_window() #メインメニューウィンドウを左にずらす関数の呼び出し
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「BOSS MODE」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPUSH
                    self.create_window(WINDOW_ID_BOSS_MODE_MENU)        #ボスモードon/offウィンドウの作製
                    #選択カーソル表示をon,カーソルは上下移動のみ,,カーソル移動ステップはx4,y7,いま指示しているアイテムナンバーは0の「ON」
                    #まだボタンも押されておらず未決定状態なのでdecision_item_yはUNSELECTED,y最大項目数は2項目なので 2-1=1を代入,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_NORMAL,CURSOR_MOVE_UD,96+5,69+self.boss_test_mode * STEP7,STEP4,STEP7,0,0,0,self.boss_test_mode,UNSELECTED,UNSELECTED,0,2-1,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_BOSS_MODE_MENU    #このウィンドウIDを最前列でアクティブなものとする
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 4:            #HITBOXが押されて....
                if self.search_window_id(WINDOW_ID_HITBOX_MENU) == -1: #HITBOXウィンドウが存在しないのなら・・
                    self.move_left_main_menu_window() #メインメニューウィンドウを左にずらす関数の呼び出し
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「HITBOX」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPUSH
                    self.create_window(WINDOW_ID_HITBOX_MENU)           #ヒットボックスon/offウィンドウの作製
                    #選択カーソル表示をon,カーソルは上下移動のみ,,カーソル移動ステップはx4,y7,いま指示しているアイテムナンバーは0の「OFF」
                    #まだボタンも押されておらず未決定状態なのでdecision_item_yはUNSELECTED,y最大項目数は2項目なので 2-1=1を代入,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_NORMAL,CURSOR_MOVE_UD,96+5,69+self.boss_collision_rect_display_flag * STEP7,STEP4,STEP7,0,0,0,self.boss_collision_rect_display_flag,UNSELECTED,UNSELECTED,0,2-1,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_HITBOX_MENU       #このウィンドウIDを最前列でアクティブなものとする
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 5:            #DIFFICULTYが押されて
                if self.search_window_id(WINDOW_ID_SELECT_DIFFICULTY) == -1: #SELECT_DIFFICULTYウィンドウが存在しないのなら・・
                    self.move_left_main_menu_window() #メインメニューウィンドウを左にずらす関数の呼び出し
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「DIFFICULTY」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPUSH
                    self.create_window(WINDOW_ID_SELECT_DIFFICULTY)     #「SELECT DIFFICULTY」ウィンドウの作製
                    #選択カーソル表示をon,カーソルは上下移動のみ,,カーソル移動ステップはx4,y7,いま指示しているアイテムナンバーは2の「NORMAL」
                    #まだボタンも押されておらず未決定状態なのでdecision_item_yはUNSELECTED,y最大項目数は6項目なので 6-1=5を代入,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_NORMAL,CURSOR_MOVE_UD,96,63 + self.game_difficulty * STEP7,STEP4,STEP7,0,0,0,self.game_difficulty,UNSELECTED,UNSELECTED,0,6-1,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_SELECT_DIFFICULTY #このウィンドウIDを最前列でアクティブなものとする
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 6:            #SCORE BOARDが押されて...
                if self.search_window_id(WINDOW_ID_SCORE_BOARD) == -1: #SCORE_BOARDウィンドウが存在しないのなら・・
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「SCORE BOARD」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPUSH
                    self.window_score_board(GAME_NORMAL)                #スコアボードウィンドウを育成=============
                    #選択カーソル表示をoff,カーソルは表示せずLRキーもしくはLショルダーRショルダーで左右に頁をめくる動作,カーソル移動ステップはx4,y7,いま指示しているアイテムナンバーは0の「1」
                    #まだボタンも押されておらず未決定状態なのでdecision_item_yはUNSELECTED,y最大項目数は1項目なので 1-1=0を代入,いま指し示しているページナンバー 0=very easy,#最大ページ数 難易度は0~5の範囲 なのでMAX5,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_NO_DISP,CURSOR_MOVE_SHOW_PAGE,92,71,STEP4,STEP7,0,5,0,0,UNSELECTED,UNSELECTED,0,0,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_SCORE_BOARD       #このウィンドウIDを最前列でアクティブなものとする
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 7:            #NAME ENTRYが押されて...
                if self.search_window_id(WINDOW_ID_INPUT_YOUR_NAME) == -1: #INPUT_YOUR_NAMEウィンドウが存在しないのなら・・
                    self.move_left_main_menu_window() #メインメニューウィンドウを左にずらす関数の呼び出し
                    self.cursor_pre_decision_item_x = self.cursor_decision_item_x #現時点で選択されたアイテム「NAME ENTRY」を前のレイヤー選択アイテムとしてコピーする
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「NAME ENTRY」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPUSH
                    self.create_window(WINDOW_ID_INPUT_YOUR_NAME)       #「ENTER YOUR NAME」ウィンドウの作製
                    #選択カーソルのタイプはアンダーバーの点滅にします,カーソルは左右でスライダー入力,カーソル移動ステップはx4,y7,いま指示しているアイテムナンバーx軸は0,y軸は0(縦には動かないので常に0となります)
                    #まだボタンも押されておらず未決定状態なのでdecision_item_x,decision_item_yはUNSELECTED,最大項目数x軸方向は(8文字+OKボタンなので)合計9項目 9-1=8を代入,最大項目数y軸方向は0,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_UNDER_BAR,CURSOR_MOVE_LR_SLIDER,100,66,STEP4,STEP7,0,0,0,0,UNSELECTED,UNSELECTED,9-1,0,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_INPUT_YOUR_NAME   #このウィンドウIDを最前列でアクティブなものとする
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 8:            #CONFIGが押されて
                if self.search_window_id(WINDOW_ID_CONFIG) == -1: #SELECT_CONFIGウィンドウが存在しないのなら・・
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「CONFIG」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPUSH
                    self.create_window(WINDOW_ID_CONFIG)                #「CONFIG」ウィンドウの作製
                    #選択カーソル表示をon,カーソルは上下移動+左右によるパラメーターの変更,カーソル移動ステップはx4,y9,いま指示しているアイテムナンバーは0の
                    #まだボタンも押されておらず未決定状態なのでdecision_item_yはUNSELECTED,y最大項目数は11項目なので11-1=10を代入,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_NORMAL,CURSOR_MOVE_UD_SLIDER,9,17,STEP4,STEP9,0,0,0,0,UNSELECTED,UNSELECTED,0,11-1,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_CONFIG #このウィンドウIDを最前列でアクティブなものとする
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 9:            #REPLAYが押されたら
                self.game_status = SCENE_SELECT_LOAD_SLOT           #ゲームステータスを「SCENE_SELECT_LOAD_SLOT」にしてロードデータスロットの選択に移る
                self.window_replay_data_slot_select()               #リプレイデータファイルスロット選択ウィンドウの表示
                #選択カーソル表示をonにする,カーソルは上下移動のみ,カーソル移動ステップはx4,y7,いま指示しているアイテムナンバーは0の「1」
                #まだボタンも押されておらず未決定状態なのでdecision_item_yは-1最大項目数は「1」「2」「3」「4」「5」「6」「7」の7項目なので 7-1=6を代入,メニューの階層が増えたので,MENU_LAYER0からMENU_LAYER1にします
                self.set_cursor_data(CURSOR_TYPE_NORMAL,CURSOR_MOVE_UD,67,55,STEP4,STEP7,0,0,0,0,UNSELECTED,UNSELECTED,0,6,0,MENU_LAYER1)
                self.active_window_id = WINDOW_ID_SELECT_FILE_SLOT  #このウィンドウIDを最前列でアクティブなものとする
                pyxel.play(0,self.window[self.active_window_index].cursor_push_se) #カーソルボタンプッシュ音を鳴らす
                
            elif self.cursor_decision_item_y == 10:            #MEDALが押されて
                if self.search_window_id(WINDOW_ID_MEDAL_LIST) == -1: #MEDAL_LISTウィンドウが存在しないのなら・・
                    self.move_left_main_menu_window() #メインメニューウィンドウを左にずらす関数の呼び出し
                    self.cursor_pre_decision_item_y = self.cursor_decision_item_y #現時点で選択されたアイテム「MEDAL_LIST」を前のレイヤー選択アイテムとしてコピーする
                    self.push_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPUSH
                    self.create_window(WINDOW_ID_MEDAL_LIST)                #「MEDAL_LIST」ウィンドウの作製
                    #カーソルは点滅囲み矩形タイプ,カーソルは4方向,カーソル移動ステップはx9,y9,いま指示しているアイテムナンバーは0
                    #まだボタンも押されておらず未決定状態なのでdecision_item_yはUNSELECTED,x最大項目数は9項目なので9-1=8を代入,メニューの階層が増えたのでMENU_LAYER0からMENU_LAYER1にします
                    self.set_cursor_data(CURSOR_TYPE_BOX_FLASH,CURSOR_MOVE_4WAY,46,60,STEP10,STEP10,0,0,0,0,UNSELECTED,UNSELECTED,9-1,3-1,0,MENU_LAYER1)
                    self.active_window_id = WINDOW_ID_MEDAL_LIST #このウィンドウIDを最前列でアクティブなものとする
                    self.make_medal_list_window_comment_disp_flag_table() #メダルリストウィンドウで「存在するアイテム」を調べ上げコメント表示フラグテーブルを作製する関数の呼び出す
                    pyxel.play(0,self.window[self.active_window_index].cursor_push_se)#カーソルボタンプッシュ音を鳴らす
            
        elif self.cursor_menu_layer == 1: #メニューが1階層目の選択分岐
            if   self.cursor_pre_decision_item_y == 1 and self.cursor_decision_item_y == 0:
                #「SELECT STAGE」→「1」
                self.stage_number   = 1                          #ステージナンバー1
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                
                i = self.search_window_id(WINDOW_ID_SELECT_STAGE_MENU)
                self.window[i].vx = 0.6            #WINDOW_ID_SELECT_STAGE_MENUウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.1
                self.window[i].vy = 0.1 * self.stage_number
                self.window[i].vy_accel = 1.1
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 1 and self.cursor_decision_item_y == 1:
                #「SELECT STAGE」→「2」
                self.stage_number   = 2                         #ステージナンバー2
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                
                i = self.search_window_id(WINDOW_ID_SELECT_STAGE_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_STAGE_MENUウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.1
                self.window[i].vy = 0.1 * self.stage_number
                self.window[i].vy_accel = 1.1
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 1 and self.cursor_decision_item_y == 2:
                #「SELECT STAGE」→「3」
                self.stage_number   = 3                        #ステージナンバー3
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                
                i = self.search_window_id(WINDOW_ID_SELECT_STAGE_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_STAGE_MENUウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.1
                self.window[i].vy = 0.1 * self.stage_number
                self.window[i].vy_accel = 1.1
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_pre_decision_item_y == 2 and self.cursor_decision_item_y == 0:
                #「SELECT LOOP NUMBER」→「1」
                self.stage_loop = 1                           #ループ数に1週目を代入
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                i = self.search_window_id(WINDOW_ID_SELECT_LOOP_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_LOOP_MENUウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 2 and self.cursor_decision_item_y == 1:
                #「SELECT LOOP NUMBER」→「2」
                self.stage_loop = 2                           #ループ数に2週目を代入
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                i = self.search_window_id(WINDOW_ID_SELECT_LOOP_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_LOOP_MENUウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 2 and self.cursor_decision_item_y == 2:
                #「SELECT LOOP NUMBER」→「3」
                self.stage_loop = 3                          #ループ数に3週目を代入
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                i = self.search_window_id(WINDOW_ID_SELECT_LOOP_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_LOOP_MENUウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_pre_decision_item_y == 3 and self.cursor_decision_item_y == 0:
                #「BOSS MODE」→「OFF」
                self.boss_test_mode = 0        #ボステストモードをoff
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_BOSS_MODE_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_BOSS_MODE_MENUウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_cancel_se)#カーソルキャンセル音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 3 and self.cursor_decision_item_y == 1:
                #「BOSS MODE」→「ON」
                self.boss_test_mode = 1                              #ボステストモードをon
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_BOSS_MODE_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_BOSS_MODE_MENUウィンドウを右下にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].vy = 0.2
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_pre_decision_item_y == 4 and self.cursor_decision_item_y == 0:
                #「HITBOX」→「OFF」
                self.boss_collision_rect_display_flag = 0            #ボス当たり判定表示をoff
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_HITBOX_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_HITBOX_MENUウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_cancel_se)#カーソルキャンセル音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 4 and self.cursor_decision_item_y == 1:
                #「HITBOX」→「ON」
                self.boss_collision_rect_display_flag = 1            #ボス当たり判定表示をon
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_HITBOX_MENU)
                self.window[i].vx = 0.3            #WINDOW_ID_HITBOX_MENUウィンドウを右下にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].vy = 0.2
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_pre_decision_item_y == 5 and self.cursor_decision_item_y == 0:
                #「DIFFICULTY」→「VERY_EASY」
                self.game_difficulty = GAME_VERY_EASY
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_SELECT_DIFFICULTY)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_DIFFICULTYウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].vy = -0.1
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 5 and self.cursor_decision_item_y == 1:
                #「DIFFICULTY」→「EASY」
                self.game_difficulty = GAME_EASY
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_SELECT_DIFFICULTY)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_DIFFICULTYウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].vy = -0.05
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 5 and self.cursor_decision_item_y == 2:
                #「DIFFICULTY」→「NORMAL」
                self.game_difficulty = GAME_NORMAL
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_SELECT_DIFFICULTY)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_DIFFICULTYウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 5 and self.cursor_decision_item_y == 3:
                #「DIFFICULTY」→「HARD」
                self.game_difficulty = GAME_HARD
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_SELECT_DIFFICULTY)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_DIFFICULTYウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].vy = 0.1
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 5 and self.cursor_decision_item_y == 4:
                #「DIFFICULTY」→「VERY_HARD」
                self.game_difficulty = GAME_VERY_HARD
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_SELECT_DIFFICULTY)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_DIFFICULTYウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].vy = 0.2
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
            elif self.cursor_pre_decision_item_y == 5 and self.cursor_decision_item_y == 5:
                #「DIFFICULTY」→「INSAME」
                self.game_difficulty = GAME_INSAME
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_SELECT_DIFFICULTY)
                self.window[i].vx = 0.3            #WINDOW_ID_SELECT_DIFFICULTYウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].vy = 0.3
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.window[i].flag_list = self.master_flag_list #ボステストフラグを更新→マスターフラグデータリスト更新→ウィンドウのフラグリストに書き込んで更新します
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_pre_decision_item_y == 6 and self.cursor_page == 0 and self.cursor_pre_page != self.cursor_page: #前に表示していたページ数と現在のページ数に変化があった時だけ
                if self.cursor_move_data == PAD_RIGHT:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD, 0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを右方向にフッ飛ばしていく
                else:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD,-0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを左方向にフッ飛ばしていく
                
                self.window_score_board(0)                           #スコアボードウィンドウ育成
                self.cursor_pre_page = self.cursor_page              #前回のページ数を保存
            elif self.cursor_pre_decision_item_y == 6 and self.cursor_page == 1 and self.cursor_pre_page != self.cursor_page: #前に表示していたページ数と現在のページ数に変化があった時だけ
                if self.cursor_move_data == PAD_RIGHT:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD, 0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを右方向にフッ飛ばしていく
                else:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD,-0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを左方向にフッ飛ばしていく
                
                self.window_score_board(1)                           #スコアボードウィンドウ育成
                self.cursor_pre_page = self.cursor_page              #前回のページ数を保存
            elif self.cursor_pre_decision_item_y == 6 and self.cursor_page == 2 and self.cursor_pre_page != self.cursor_page: #前に表示していたページ数と現在のページ数に変化があった時だけ
                if self.cursor_move_data == PAD_RIGHT:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD, 0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを右方向にフッ飛ばしていく
                else:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD,-0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを左方向にフッ飛ばしていく
                
                self.window_score_board(2)                           #スコアボードウィンドウ育成
                self.cursor_pre_page = self.cursor_page              #前回のページ数を保存
            elif self.cursor_pre_decision_item_y == 6 and self.cursor_page == 3 and self.cursor_pre_page != self.cursor_page: #前に表示していたページ数と現在のページ数に変化があった時だけ
                if self.cursor_move_data == PAD_RIGHT:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD, 0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを右方向にフッ飛ばしていく
                else:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD,-0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを左方向にフッ飛ばしていく
                
                self.window_score_board(3)                           #スコアボードウィンドウ育成
                self.cursor_pre_page = self.cursor_page              #前回のページ数を保存
            elif self.cursor_pre_decision_item_y == 6 and self.cursor_page == 4 and self.cursor_pre_page != self.cursor_page: #前に表示していたページ数と現在のページ数に変化があった時だけ
                if self.cursor_move_data == PAD_RIGHT:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD, 0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを右方向にフッ飛ばしていく
                else:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD,-0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを左方向にフッ飛ばしていく
                
                self.window_score_board(4)                           #スコアボードウィンドウ育成
                self.cursor_pre_page = self.cursor_page              #前回のページ数を保存
            elif self.cursor_pre_decision_item_y == 6 and self.cursor_page == 5 and self.cursor_pre_page != self.cursor_page: #前に表示していたページ数と現在のページ数に変化があった時だけ
                if self.cursor_move_data == PAD_RIGHT:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD, 0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを右方向にフッ飛ばしていく
                else:
                    self.all_move_window(WINDOW_ID_SCORE_BOARD,-0.3,0, 1.2,0) #すべてのSCORE_BOARDウィンドウを左方向にフッ飛ばしていく
                
                self.window_score_board(5)                           #スコアボードウィンドウ育成
                self.cursor_pre_page = self.cursor_page              #前回のページ数を保存
            elif self.cursor_pre_decision_item_y == 6 and self.cursor_decision_item_y != -1: #何かしらのアイテムの所でボタンが押されたのなら
                #SCORE BOARDはキー入力のタイミングで同じウィンドウIDを持つウィンドウが複数存在してしまう可能性があるので
                #ウィンドウIDナンバーを元にすべての同一IDウィンドウを調べ上げ画面外にフッ飛ばすようにする
                self.all_move_window(WINDOW_ID_SCORE_BOARD,0,0.3,0,1.2) #すべてのSCORE_BOARDウィンドウを下方向にフッ飛ばしていく
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)               #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1                    #前回選択したアイテムも未決定に
                pyxel.play(0,self.window[self.active_window_index].cursor_cancel_se)#カーソルキャンセル音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_pre_decision_item_y == 7 and self.cursor_decision_item_x == 8:
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                #「ENTER YOUR NAME」→「OK」ボタンを押した
                text = self.window[self.active_window_index].edit_text[LIST_WINDOW_TEXT]
                self.my_name = text[:8] #文字列textの先頭から8文字までをmy_nameとします
                self.all_move_window(WINDOW_ID_INPUT_YOUR_NAME,0.2,0.3,1.2,1.2) #すべてのINPUT_YOUR_NAMEウィンドウを右下方向にフッ飛ばしていく
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_ok_se)#カーソルOK音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_pre_decision_item_y == 8 and self.cursor_decision_item_y == 10:
                self.restore_master_flag_list() #フラグ＆データ関連のマスターリストを参照して個別のフラグ変数へリストアする
                i = self.search_window_id(WINDOW_ID_CONFIG)
                self.window[i].vx = -0.1            #WINDOW_ID_CONFIGウィンドウを左下にフッ飛ばしていく
                self.window[i].vx_accel = 1.1
                self.window[i].vy = 0.2
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.save_system_data()                            #システムデータをセーブします
                pyxel.load("assets/graphic/min-sht2.pyxres") #タイトル＆ステージ1＆2のリソースファイルを読み込む
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_cancel_se)#カーソルキャンセル音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする
                
            elif self.cursor_pre_decision_item_y == 10 and self.cursor_decision_item_y == 0:
                self.move_right_main_menu_window() #メインメニューウィンドウを右にずらす関数の呼び出し
                self.create_master_flag_list() #フラグ＆データ関連のマスターリスト作成関数を呼び出す
                i = self.search_window_id(WINDOW_ID_MEDAL_LIST)
                self.window[i].vx = 0.3            #WINDOW_ID_MEDAL_LISTウィンドウを右にフッ飛ばしていく
                self.window[i].vx_accel = 1.2
                self.window[i].vy = 0.1
                self.window[i].vy_accel = 1.2
                self.window[i].window_status = WINDOW_CLOSE
                self.window[i].comment_flag = COMMENT_FLAG_OFF
                self.pop_cursor_data(WINDOW_ID_MAIN_MENU)          #メインメニューのカーソルデータをPOP
                self.cursor_pre_decision_item_y = -1
                pyxel.play(0,self.window[self.active_window_index].cursor_cancel_se)#カーソルキャンセル音を鳴らす
                self.active_window_id = WINDOW_ID_MAIN_MENU #1階層前メインメニューウィンドウIDを最前列でアクティブなものとする

    #!ゲームスタート時の初期化#########################################
    def update_game_start_init(self):
        self.score = 0               #スコア
        self.my_shield = 5           #自機のシールド耐久値
        self.my_speed = 1            #自機の初期スピード
        
        self.my_x = 24    #自機のx座標の初期値
        self.my_y = 50    #自機のy座標の初期値
        self.my_vx = 1    #自機のx方向の移動量
        self.my_vy = 0    #自機のy方向の移動量
        
        self.run_away_bullet_probability = 10 #敵が過ぎ去っていくときに弾を出す確率
        
        self.game_playing_flag = 1     #ゲームプレイフラグを「ゲームプレイ中」にする
        self.select_cursor_flag = 0   #セレクトカーソルの移動更新は行わないのでフラグを降ろす
        
        self.select_shot_id = 0        #現在使用しているショットのIDナンバー(ナンバーの詳細はshot_levelを参照するのです！)
        
        self.shot_exp = 0                   #自機ショットの経験値 パワーアップアイテムを取ることにより経験値がたまりショットのレベルが上がっていく
        self.shot_level = 0                 #自機ショットのレベル  0~3バルカンショット  4=レーザー 5=ツインレーザー 6=3WAYレーザー
                                            #7=ウェーブカッターLv1  8=ウェーブカッターLv2  9=ウェーブカッターLv3   10=ウェーブカッターLv4
        self.shot_speed_magnification=1     #自機ショットのスピードに掛ける倍率(vxに掛け合わせる)  
        self.shot_rapid_of_fire = 1         #自機ショットの連射数  初期値は1連射
        
        self.missile_exp = 0               #自機ミサイルの経験値 パワーアップアイテムを取ることにより経験値が溜まりミサイルのレベルが上がっていく
        self.missile_level = 0             #自機ミサイルのレベル  0~2 0=右下のみ  1=右下左上前方2方向  2=右下右上  左下左上4方向
        self.missile_speed_magnification=1 #自機ミサイルのスピードに掛ける倍率(vxに掛け合わせる)
        self.missile_rapid_of_fire = 1     #自機ミサイルの連射数  初期値は1連射
        
        self.select_sub_weapon_id = 0      #現在使用しているサブウェポンのIDナンバー -1だと何も所有していない状態
        self.sub_weapon_list = [5,10,10,3,10] #どのサブウェポンを所持しているかのリスト(インデックスオフセット値)
                                        #0=テイルショット 1=ペネトレートロケット 2=サーチレーザー 3=ホーミングミサイル 4=ショックバンバー
        self.star_scroll_speed = 1          #背景の流れる星のスクロールスピード 1=通常スピード 0.5なら半分のスピードとなります
        #self.pow_item_bounce_num = 6       #パワーアップアイテムが画面の左端で跳ね返って戻ってくる回数
                                            #初期値は6でアップグレードすると増えていくです
        
        self.playtime_frame_counter    = 0 #プレイ時間(フレームのカウンター) 60フレームで＝1秒        
        self.one_game_playtime_seconds = 0 #1プレイでのゲームプレイ時間(秒単位)
        
        self.game_play_count = 0        #ゲーム開始から経過したフレームカウント数(1フレームは60分の1秒)1面～今プレイしている面までのトータルフレームカウント数です
        self.rnd09_num = 0              #乱数0~9ルーレットの初期化
        
        self.replay_stage_num = 0       #リプレイ再生、録画時のステージ数を0で初期化します(1ステージ目=0→2ステージ目=1→3ステージ目=2って感じ)
        
        if self.replay_status != REPLAY_PLAY:       #リプレイデータでの再生時は乱数の種の更新は行いません、それ以外の時は更新します
            self.rnd_seed = pyxel.frame_count % 256 #線形合同法を使った乱数関数で使用する乱数種を現在のフレーム数とします(0~255の範囲)
            self.master_rnd_seed = self.rnd_seed    #リプレイデータ記録用として元となる乱数種を保存しておきます
        
        self.claw_type = 0              # クローのタイプ 
                                        # 0=ローリングクロー 1=トレースクロー 2=フィックスクロー 3=リバースクロー
        self.claw_number = 0            # クローの装備数 0=装備無し 1=1機 2=2機 3=3機 4=4機
        self.claw_difference = 360      # クロ―同士の角度間隔 1機=360 2機=180度 3機=120度 4機=90度
        self.trace_claw_index = 0       #トレースクロー（オプション）時のトレース用配列のインデックス値
        self.trace_claw_distance = 12   #トレースクロー同士の間隔
        self.fix_claw_magnification = 1 #フイックスクロー同士の間隔の倍率 0.5~2まで0.1刻み
        self.reverse_claw_svx = 1       #リバースクロー用の攻撃方向ベクトル(x軸)
        self.reverse_claw_svy = 0       #リバースクロー用の攻撃方向ベクトル(y軸)
        self.claw_shot_speed = 2        #クローショットのスピード（初期値は移動量２ドット）
        
        self.ls_shield_hp = 0           #L'sシールドの耐久力 0=シールド装備していない 1以上はシールド耐久値を示す
        
        self.claw = []                  #クローのリスト初期化 クローのリストはステージスタート時に初期化してしまうと次のステージに進んだときクローが消滅してしまうのでgame_start_initで初期化します
        
        #難易度に応じた数値をリストから取得する
        self.get_difficulty_data() #難易度データリストから数値を取り出す関数の呼び出し
        #ランクに応じた数値をリストから取得する
        self.get_rank_data() #ランクデータリストから数値を取り出す関数の呼び出し
        
        self.shot_table_list = self.j_python_shot_table_list      #とりあえずショットテーブルリストは初期機体のj_pythonのものをコピーして使用します
                                                        #将来的には選択した機体で色々な機体のリストがコピーされるはず
        self.missile_table_list = self.j_python_missile_table_list #とりあえずミサイルテーブルリストは初期機体のj_pythonのものをコピーして使用します
                                                        #将来的には選択した機体で色々な機体のリストがコピーされるはず・・・ほんとかなぁ？
        
        #ゲームスタート時のいろいろなボーナスの処理
        self.shot_exp  += self.start_bonus_shot
        self.missile_exp += self.start_bonus_missile
        self.my_shield += self.start_bonus_shield
        self.level_up_my_shot()            #自機ショットの経験値を調べ可能な場合レベルアップをさせる関数を呼び出す
        self.level_up_my_missile()         #自機ミサイルの経験値を調べ可能な場合レベルアップをさせる関数を呼び出す
        if self.start_claw == ONE_CLAW:    #ゲーム開始時クローの数が1の時は
            self.update_append_claw()      #クロー追加ボーナスの数値の回数分、追加関数を呼び出す
        elif self.start_claw == TWO_CLAW:  #ゲーム開始時クローの数が2の時は
            self.update_append_claw()      #2回呼び出し
            self.update_append_claw()
        elif self.start_claw == THREE_CLAW:#ゲーム開始時クローの数が3の時は
            self.update_append_claw()       #3回呼び出し
            self.update_append_claw()
            self.update_append_claw()

    #!ステージスタート時の初期化#######################################
    def update_stage_start_init(self):
        #画像リソースファイルを読み込みます
        pyxel.load("assets/graphic/min-sht2.pyxres")
        pygame.mixer.init(frequency = 44100)    #pygameミキサー関連の初期化
        pygame.mixer.music.set_volume(0.7)      #音量設定(0~1の範囲内)
        self.load_stage_bgm()                   #BGMファイルの読み込み
        pygame.mixer.music.play(-1)             #BGMループ再生
        self.my_x = 24    #自機のx座標の初期値
        self.my_y = 50    #自機のy座標の初期値
        self.my_vx = 1    #自機のx方向の移動量
        self.my_vy = 0    #自機のy方向の移動量
        
        if self.replay_status == REPLAY_RECORD:
            self.update_save_replay_stage_data()    #リプレイ保存時は,ステージスタート時のパラメーターをセーブする関数を呼び出します(リプレイ再生で使用)
            
        elif self.replay_status == REPLAY_PLAY:
            
            self.update_load_replay_stage_data()    #リプレイ再生時は,ステージスタート時のパラメーターをロードする関数を呼び出します
        
        self.pad_data_h = 0b00000000#パッド入力用ビットパターンデータを初期化します
        self.pad_data_l = 0b00000000#各ビットの詳細
                                    #上位バイトから 0,0,0,0, RS,LS,START,SELECT
                                    #下位バイトは   BY,BX,BB,BA, R,L,D,U
                                    # U=上 D=下 L=左 R=右 BA~BY=各ボタン START,SELECT=スタート,セレクト LS,RS=左ショルダー,右ショルダーボタン
        self.replay_frame_index = 0 #リプレイ時のフレームインデックス値を初期化
        
        #各ステージに応じた数値をリストから取得する
        self.get_stage_data()             #ステージデータリストからステージごとに設定された数値を取り出す関数の呼び出し
        
        self.present_repair_item_flag = 0 #ボス破壊後の爆発シーンでリペアアイテムを出すときに使用するフラグ 0=まだアイテム出してない 1=アイテム放出したよ～
        self.rank_down_count = 0          #ダメージを受けて難易度別に設定された規定値まで行ったかどうかをカウントする変数
        self.bg_cls_color = 0             #BGをCLS(クリアスクリーン)するときの色の指定(通常は0=黒色です) ゲーム中のイベントで変化することもあるのでステージスタート時でも初期化する
        self.bg_transparent_color = 0     #BGタイルマップを敷き詰めるときに指定する透明色です          ゲーム中のイベントで変化することもあるのでステージスタート時でも初期化する
        
        self.my_boost_injection_count = 0 #ステージクリア後のブースト噴射用のカウンター
        
        self.timer_flare_flag = 0         #タイマーフレア（触れると物質の時間経過が遅くなるフレア）を放出するかどうかのフラグ
        
        self.move_mode_auto_x,self.move_mode_auto_y = 0,0 #自動移動モードがonの時はこの座標に向かって毎フレームごと自動で移動して行きます
        self.move_mode_auto_complete                = 0   #自動移動モードで目標座標まで移動したらこのフラグを立てます
        
        self.add_appear_flag = 0     #敵を追加発生させる時に立てるフラグです
        
        self.record_games_status = 0 #ポーズを掛けたときに直前のゲームステータスを記録しておく変数
        
        self.scroll_count = 0           #ステージ開始からスクロールした背景のドット数カウンタ
                                        #(スクロールスピードが小数になったときはこのカウントも少数になるので注意！)
        self.vertical_scroll_count = 0  #ステージ開始から縦スクロールした背景のドット数カウンタ 主に縦スクロールするステージで使用します
                                        #(スクロールスピードが小数になったときはこのカウントも小数になるので注意！)
        
        self.stage_count = 0          #ステージ開始から経過したフレームカウント数(1フレームは60分の1秒)常に整数だよ
        
        self.side_scroll_speed              =1  #横スクロールするスピードの現在値が入ります 1フレームで1ドットスクロール(実数ですのん)
        self.side_scroll_speed_set_value    =1  #横スクロールスピードの設定値(変化量の分だけ1フレームごと増加減させ、この設定値までもって行く)
        self.side_scroll_speed_variation    =0  #横スクロールスピードを変化させる時の差分(変化量)
        
        self.vertical_scroll_speed           =0  #縦スクロールするスピードの現在値が入ります 1フレームで1ドットスクロール(実数ですのん)
        self.vertical_scroll_speed_set_value =0  #縦スクロールスピードの設定値(変化量の分だけ1フレームごと増加減させ、この設定値までもって行く)
        self.vertical_scroll_speed_variation =0  #縦スクロールスピードを変化させる時の差分(変化量)
        
        self.display_cloud_flag    = 0    #背景の流れる雲を表示するかどうかのフラグ(0=表示しない 1=表示する)
        
        self.cloud_append_interval = 6    #雲を追加させる間隔
        self.cloud_quantity        = 0    #雲の量
        self.cloud_how_flow        = 0    #雲の流れ方
        self.cloud_flow_speed      = 0    #雲の流れるスピード
        
        self.warning_dialog_flag         = 0 #WARINIGダイアログを表示するかどうかのフラグ
        self.warning_dialog_display_time = 0 #WARINIGダイアログの表示時間(フレーム単位)
        self.warning_dialog_logo_time    = 0 #WARNINGグラフイックロゴの表示に掛ける時間(フレーム単位)
        self.warning_dialog_text_time    = 0 #WARNINGテキスト表示に掛ける時間(フレーム単位)
        
        self.stage_clear_dialog_flag         = 0 #STAGE CLEARダイアログを表示するかどうかのフラグ
        self.stage_clear_dialog_display_time = 0 #STAGE CLEARダイアログの表示時間(フレーム単位)
        self.stage_clear_dialog_logo_time1   = 0 #STAGE CLEARグラフイックロゴの表示に掛ける時間その１(フレーム単位)
        self.stage_clear_dialog_logo_time2   = 0 #STAGE CLEARグラフイックロゴの表示に掛ける時間その２(フレーム単位)
        self.stage_clear_dialog_text_time    = 0 #STAGE CLEARテキスト表示に掛ける時間(フレーム単位)
        
        self.event_index = 0                #イベントリストのインデックス値（イベントリストが現在どの位置にあるのかを示す値です）
        self.type_check_quantity = 0        #特定のショットタイプがリストにどれだけあるのかチェックして数えた数がここに入る
        self.my_ship_explosion_timer = 0    #自機が爆発した後、まだどれだけゲームが進行するかのタイマーカウント
        self.game_over_timer = 0            #ゲームオーバーダイアログを表示した後まだどれだけゲームが進行するかのタイマーカウント
        self.fade_in_out_counter = 0        #フェードイン＆フェードアウト用エフェクトスクリーン用のカウンタ（基本的にx軸(キャラクター単位）の値です)
                                            #0~19 で 19になった状態が一番右端を描画したという事になります
                                            #19になった時点で完了となります
        self.fade_complete_flag = 0             #フェードイン＆フェードアウトが完了したかのフラグが入る所(0=まだ終わっていない 1=完了！)
        self.shadow_in_out_counter = 0          #シャドウイン＆シャドウアウト用エフェクトスクリーン用のカウンタ
        self.shadow_in_out_complete_flag = 0    #シャドウイン＆シャドウアウトが完了したかのフラグが入る所(0=まだ終わっていない 1=完了！)
        
        self.current_formation_id = 1   #現在の敵編隊のＩＤナンバー（0は単独機で編隊群は1からの数字が割り当てられます）
                                        #編隊が1編隊出現するごとにこの数字が1増えていく
                                        #例 1→2→3→4→5→6→7→8→9→10みたいな感じで増えていく
        self.fast_forward_destruction_num = 0       #早回しの条件を満たすのに必要な「破壊するべき編隊の総数」が入ります
        self.fast_forward_destruction_count = 0     #破壊するべき編隊の総数」が1以上ならば編隊を破壊すると次の編隊の出現カウントがこの数値だけ少なくなり出現が早まります
        self.add_appear_flag = 0                    #早回しの条件をすべて満たしたときに建つフラグです、このフラグが立った時、イベントリストに「EVENT_ADD_APPEAR_ENEMY」があったらそこで敵編隊を追加発生させます
        
        self.my_rolling_flag = 0    #0=通常の向き  1=下方向に移動中のキャラチップ使用  2=上方向に移動中のキャラチップ使用
        self.my_moved_flag = 0      #自機が移動したかどうかのフラグ（トレースクローの時、自機のＸＹ座標を履歴リストに記録するのか？しないのか？で使う）
                                    #0=自機は止まっているので座標履歴リストに記録はしない 
                                    #1=自機は移動したので座標履歴リストに記録する
        
        self.invincible_counter = 0 #無敵時間(単位はフレーム)のカウンタ 0の時以外は無敵状態です
        
        self.enemy_bound_collision_flag = 0 #ホッパー君が地面に接触してバウンドしたかどうかのフラグ(デバッグ用に使います)
        self.mountain_x = 0                 #8wayフリースクロール＋ラスタースクロール時の背景に表示される山のBGX座標用の変数です（デバッグ様に使用します）
        self.cp = 0                         #外積計算用の変数(何故か判らないけど関数内で宣言せずに使うとintじゃなくてtupleになってしまうので・・・何故？)
        self.point_inside_triangle_flag = 0 #三角形の中に点が存在するかを判別する関数用のフラグを初期化
        
        #リスト群の初期化#############################################################################
        #新しいクラスを作った時はここで必ず初期化するコードを記述する事！！！！！！
        #リストは初期化しないと使えないっポイ！？ぞ・・・っと・・・・・・
        #############################################################################################
        self.shots = []                #自機弾のリスト
        self.missile = []              #ミサイルのリスト
        self.claw_shot = []            #クローの弾のリスト
        self.enemy = []                #敵のリスト
        self.enemy_shot = []           #敵の弾のリスト
        self.obtain_item = []          #取得アイテム類のリスト(パワーアップカプセルなど)
        self.stars = []                #背景の流れる星々のリスト         当たり判定はありません
        self.explosions = []           #爆発パターン群のリスト           当たり判定はありません
        self.particle = []             #パーティクル（火花の粒子）のリスト  当たり判定はありません
        self.background_object = []    #背景オブジェクトのリスト         当たり判定はありません
        self.window = []               #メッセージウィンドウのリスト       当たり判定はありません
        self.claw_coordinates = []     #自機クロー（トレースモード）のxy座標リスト まぁオプションのxy座標が入るリストです
        self.enemy_formation = []      #敵の編隊数のＩＤと出現時の総数と現在の生存数が入るリストです
        self.event_append_request = [] #イベント追加リクエストが入るリストです(敵などの臨時追加発注発生）
        self.boss = []                 #ボスのリスト
        self.raster_scroll = []        #ラスタースクロール用のリスト
        
        #各ステージのイベントリストだよ
        #イベントリストは早回しで「イベントが実行されるステージカウント数タイマー」が書き換えられるので関数「update_stage_start_init」内でリスタートごとに再読み込みする
        #
        #データリスト形式
        #[イベントが実行されるステージカウント数タイマー,イベントの内容,敵キャラのIDナンバー,x座標,y座標,編隊の場合は編隊数,通常or早回し発生の判別,編隊殲滅後カウントを減少させる数,実際に減らすカウント数]
        #スクロールカウント数が99999999の場合は実質エンドコードみたいな～☆彡
        #
        #各イベントのフォーマット
        #EVENT_FAST_FORWARD_NUM   早回しする編隊群数と時間の設定[この時点から早回しする編隊群の数(例 3だとこのイベントからあと3イベント早回しが発生します),早回しするタイマー数(例 30だとこれ以降カウントタイマーが編隊を全滅させる事で30早まります)]
        #EVENT_ENEMY            敵の出現                [敵キャラのＩＤナンバー,出現x座標,出現y座標,編隊群の場合は編隊数の指定]
        #EVENT_WARNING          ワーニングダイアログ表示     [警告表示時間,グラフイックロゴ表示に掛ける時間,テキスト表示に掛ける時間](単位は全てフレームです)
        #EVENT_BOSS            各ステージに対応したボスを出現させる
        #EVENT_ADD_APPEAR_ENEMY   早回しの条件が成立したとき敵を出現させる [敵キャラのＩＤナンバー,出現x座標,出現y座標,編隊数]
        #EVENT_SCROLL           スクロール制御
        #   SCROLL_NUM_SET        スクロール関連のパラメーター設定 [横スクロールスピード設定値,横スクロールスピードの変化量,縦スクロールスピード設定値,縦スクロールスピードの変化量]
        #   SCROLL_START          スクロールの開始（横スクロールでスピードは通常の1)
        #   SCROLL_STOP           スクロールの停止
        #   SCROLL_SPEED_CHANGE    スクロールスピードを変化させる[スクロールスピードの設定値(-ならバックスクロール),スクロールスピードの変化量(-なら減速,+なら加速)]
        #   VERTICAL_SCROLL_START   縦スクロールの開始
        #   VERTICAL_SCROLL_STOP    縦スクロールのスタート
        #EVENT_DISPLAY_STAR      背景星スクロールのon/off [0=off/1=on]
        #EVENT_CHANGE_BG_CLS_COLOR 背景でまず最初に塗りつぶす色の指定 0~15 pyxelのカラーコード
        #EVENT_CHANGE_BG_TRANSPARENT_COLOR 背景マップチップを敷き詰める時に使用する透明色の指定 0~15 pyxelのカラーコード
        #EVENT_CLOUD            背景の雲の制御
        #   CLOUD_NUM_SET          雲のパラメータ設定[発生させる間隔(単位はフレーム),
        #                                    雲の量(0=比較的小さい雲だけ,1=小中サイズの雲を流す,2=小中大すべての種類の雲を流す),
        #                                    流れ方(0=そのまま左に素直に流れていく-0.25=上方向に流されていく0.25=下方向に流されていく),
        #                                    流れるスピード(倍率となります,通常は1,少数も使用可です)
        #                                    ]            
        #   CLOUD_START            雲を流すのを開始する
        #   CLOUS_STOP            雲を流すのを停止する
        #EVENT_RASTER_SCROLL        ラスタースクロールの制御
        #   RASTER_SCROLL_OFF         ラスタースクロールの表示をoffにする[表示オフにするラスタスクロールのid]
        #   RASTER_SCROLL_ON          ラスタースクロールの表示をonにする [表示オンにするラスタスクロールのid]
        #EVENT_BG_SCREEN_ON_OFF    背景ＢＧの表示のon/off
        #   BG_BACK or BG_MIDDLE or BG_FRONT  BGの種類を選択
        #   DISP_OFF or DISP_ON            表示オフ/表示オン
        #EVENT_ENTRY_SPARK_ON_OFF  大気圏突入の火花表示のon/off
        #   SPARK_OFF or SPARK_ON           火花表示on/off
        
        #ボステストモード専用のボスだけを出現させるイベントリスト
        self.event_list_boss_test_mode = [
            [   50,EVENT_WARNING,500,120,240],
            [  100,EVENT_BOSS],
            [99999999],]
            
        self.event_list_no_enemy_mode = [
            [200000,EVENT_WARNING,500,120,240],
            [200200,EVENT_BOSS],
            [99999999],]
            
        self.event_list_stage_mountain_region_l1= [
            [ 100,EVENT_BG_SCREEN_ON_OFF,BG_BACK,DISP_OFF],
            [ 110,EVENT_ENTRY_SPARK_ON_OFF,SPARK_OFF],
            
            [ 200,EVENT_ENEMY,CIR_COIN    ,160, 40   ,6],
            [ 300,EVENT_SCROLL,SCROLL_NUM_SET,    2,0.5,        0.5,0.01],
            [ 303,EVENT_ENTRY_SPARK_ON_OFF,SPARK_ON],
            [ 350,EVENT_SCROLL,SCROLL_NUM_SET,  2.5,0.5,        0.5,0.01],
            [ 400,EVENT_SCROLL,SCROLL_NUM_SET,    3,0.5,        0.5,0.01],
            [ 403,EVENT_ENEMY,CIR_COIN    ,160, 70   ,6],
            [ 450,EVENT_SCROLL,SCROLL_NUM_SET,  3.5,0.5,        0.5,0.01],
            [ 500,EVENT_SCROLL,SCROLL_NUM_SET,    4,0.5,        0.5,0.01],
            [ 550,EVENT_ENEMY,CIR_COIN    ,160, 40   ,6],
            [ 600,EVENT_SCROLL,SCROLL_NUM_SET,    5,0.5,        0.5,0.01],
            [ 690,EVENT_ENEMY,CIR_COIN    ,160, 70   ,6],
            [ 700,EVENT_SCROLL,SCROLL_NUM_SET,    6,0.5,        0.5,0.01],
            [ 800,EVENT_SCROLL,SCROLL_NUM_SET,    7,0.5,        0.5,0.01],
            [ 891,EVENT_ENEMY,SAISEE_RO,170, 50-10],
            [ 892,EVENT_ENEMY,SAISEE_RO,169, 50   ],
            [ 893,EVENT_ENEMY,SAISEE_RO,168, 50+10],
            [ 900,EVENT_SCROLL,SCROLL_NUM_SET,    8,0.5,        0.5,0.01],
            
            [ 910,EVENT_BG_SCREEN_ON_OFF,BG_BACK,DISP_ON],
            
            [ 951,EVENT_ENEMY,SAISEE_RO,170, 50-20],
            [ 952,EVENT_ENEMY,SAISEE_RO,169, 50   ],
            [ 953,EVENT_ENEMY,SAISEE_RO,168, 50+20],
            
            [1000,EVENT_CLOUD,CLOUD_NUM_SET,6,1,-0.25,1],
            [1010,EVENT_CLOUD,CLOUD_START],
            
            [1051,EVENT_ENEMY,SAISEE_RO,170, 50-30],
            [1052,EVENT_ENEMY,SAISEE_RO,169, 50-20],
            [1053,EVENT_ENEMY,SAISEE_RO,168, 50   ],
            [1054,EVENT_ENEMY,SAISEE_RO,167, 50+20],
            [1055,EVENT_ENEMY,SAISEE_RO,166, 50+30],
            
            [1100,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            [1110,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            [1120,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            [1130,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            [1140,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            [1150,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            [1160,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            [1170,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            [1180,EVENT_ENEMY,SAISEE_RO,170, 30   ],
            
            [1300,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            [1310,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            [1320,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            [1330,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            [1340,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            [1350,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            [1360,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            [1370,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            [1380,EVENT_ENEMY,SAISEE_RO,170, 70   ],
            
            [1451,EVENT_ENEMY,SAISEE_RO,170, 10   ],
            [1452,EVENT_ENEMY,SAISEE_RO,169, 20   ],
            [1453,EVENT_ENEMY,SAISEE_RO,168, 30   ],
            [1454,EVENT_ENEMY,SAISEE_RO,167, 40   ],
            [1455,EVENT_ENEMY,SAISEE_RO,166, 50   ],
            [1456,EVENT_ENEMY,SAISEE_RO,165, 60   ],
            [1457,EVENT_ENEMY,SAISEE_RO,164, 70   ],
            [1458,EVENT_ENEMY,SAISEE_RO,163, 80   ],
            [1459,EVENT_ENEMY,SAISEE_RO,162, 90   ],
            
            [1500,EVENT_DISPLAY_STAR,           DISP_OFF],
            [1510,EVENT_CHANGE_BG_CLS_COLOR,        12],
            [1560,EVENT_CHANGE_BG_TRANSPARENT_COLOR,  12],
            
            [1561,EVENT_ENEMY,SAISEE_RO,170, 10   ],
            [1562,EVENT_ENEMY,SAISEE_RO,169, 20   ],
            [1563,EVENT_ENEMY,SAISEE_RO,168, 30   ],
            [1564,EVENT_ENEMY,SAISEE_RO,167, 40   ],
            [1565,EVENT_ENEMY,SAISEE_RO,166, 50   ],
            [1566,EVENT_ENEMY,SAISEE_RO,165, 60   ],
            [1567,EVENT_ENEMY,SAISEE_RO,164, 70   ],
            [1568,EVENT_ENEMY,SAISEE_RO,163, 80   ],
            [1569,EVENT_ENEMY,SAISEE_RO,162, 90   ],
            
            [1600,EVENT_CLOUD,CLOUD_NUM_SET,6,2,-0.4,1],
            
            [1610,EVENT_ENEMY,VOLDAR,168, 0],
            
            
            [1710,EVENT_ENEMY,RAY_BLASTER,168, 40-20],
            [1720,EVENT_ENEMY,RAY_BLASTER,168, 40   ],
            [1730,EVENT_ENEMY,RAY_BLASTER,168, 40+20],
            
            [1810,EVENT_ENEMY,RAY_BLASTER,168, 60-20],
            [1850,EVENT_ENEMY,RAY_BLASTER,168, 60   ],
            [1890,EVENT_ENEMY,RAY_BLASTER,168, 60+20],
            
            
            
            [2300,EVENT_SCROLL,SCROLL_SPEED_CHANGE,0.5,-0.01],
            
            [2310,EVENT_RASTER_SCROLL,RASTER_SCROLL_OFF,1],
            
            [2340,EVENT_ENEMY,TWIN_ARROW,160,  20],
            [2341,EVENT_ENEMY,TWIN_ARROW,160,  60],
            [2342,EVENT_ENEMY,TWIN_ARROW,160, 100],
            
            [2600,EVENT_ENEMY,TWIN_ARROW,160, 60   ],
            [2601,EVENT_ENEMY,TWIN_ARROW,160, 60+10],
            [2602,EVENT_ENEMY,TWIN_ARROW,160, 60-10],
            [2603,EVENT_ENEMY,TWIN_ARROW,160, 60+20],
            [2604,EVENT_ENEMY,TWIN_ARROW,160, 60-20],
            
            [2740,EVENT_ENEMY,TWIN_ARROW,120,  -8],
            [2741,EVENT_ENEMY,TWIN_ARROW,160, 60],
            [2742,EVENT_ENEMY,TWIN_ARROW,120,  130],
            
            [2840,EVENT_ENEMY,TWIN_ARROW,120,  -8],
            [2841,EVENT_ENEMY,TWIN_ARROW,80,  -8],
            [2842,EVENT_ENEMY,TWIN_ARROW,160, 60],
            [2843,EVENT_ENEMY,TWIN_ARROW,80,  130],
            [2844,EVENT_ENEMY,TWIN_ARROW,120,  130],
            
            [3000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,0,-0.004],
            [3100,EVENT_CLOUD,CLOUD_STOP],
            [3110,EVENT_ENTRY_SPARK_ON_OFF,SPARK_OFF],
            
            [3200,EVENT_WARNING,500,120,240],
            
            
            [3320,EVENT_SCROLL,SCROLL_SPEED_CHANGE,3.0,0.0001],
            [3340,EVENT_BOSS],
            
            [3420,EVENT_SCROLL,SCROLL_SPEED_CHANGE,4.0,0.001],
            
            
            
            [99999999],]
            
        self.event_list_stage_mountain_region_l2= [
            
            [ 300,EVENT_SCROLL,SCROLL_NUM_SET,    2,0.5,        0.5,0.01],
            [ 350,EVENT_SCROLL,SCROLL_NUM_SET,  2.5,0.5,        0.5,0.01],
            [ 400,EVENT_SCROLL,SCROLL_NUM_SET,    3,0.5,        0.5,0.01],
            [ 450,EVENT_SCROLL,SCROLL_NUM_SET,  3.5,0.5,        0.5,0.01],
            [ 500,EVENT_SCROLL,SCROLL_NUM_SET,    4,0.5,        0.5,0.01],
            [ 600,EVENT_SCROLL,SCROLL_NUM_SET,    5,0.5,        0.5,0.01],
            [ 700,EVENT_SCROLL,SCROLL_NUM_SET,    6,0.5,        0.5,0.01],
            [ 800,EVENT_SCROLL,SCROLL_NUM_SET,    7,0.5,        0.5,0.01],
            [ 900,EVENT_SCROLL,SCROLL_NUM_SET,    8,0.5,        0.5,0.01],
            
            [1000,EVENT_CLOUD,CLOUD_NUM_SET,6,1,-0.25,1],
            
            [1010,EVENT_CLOUD,CLOUD_START],
            
            [1500,EVENT_DISPLAY_STAR,           0],
            [1510,EVENT_CHANGE_BG_CLS_COLOR,        12],
            [1560,EVENT_CHANGE_BG_TRANSPARENT_COLOR,  12],
            
            
            [1600,EVENT_CLOUD,CLOUD_NUM_SET,6,2,-0.4,1],
            
            [2300,EVENT_SCROLL,SCROLL_SPEED_CHANGE,0.5,-0.01],
            
            [2310,EVENT_RASTER_SCROLL,RASTER_SCROLL_OFF,1],
            
            [3000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,0,-0.004],
            [3100,EVENT_CLOUD,CLOUD_STOP],
            [3200,EVENT_SCROLL,SCROLL_SPEED_CHANGE,3.0,0.0001],
            [4000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,0.05,0.01],
            [5000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,-0.05,-0.01],
            [6000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,0.05,0.01],
            [7000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,-0.05,-0.01],
            [8000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,0.05,0.01],
            [9000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,-0.05,-0.01],
            [11000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,0.05,0.01],
            [14000,EVENT_SCROLL,SCROLL_SPEED_CHANGE_VERTICAL,-0.05,-0.01],
            
            
            
            [99999999],]
            
        self.event_list_stage_mountain_region_dummy= [
            [99999999],]
            
        self.event_list_stage_advance_base_l1= [
            
            [  10,EVENT_FAST_FORWARD_NUM,4,30],
            [ 200,EVENT_ENEMY,CIR_COIN    ,160, 10   ,6],
            [ 500,EVENT_ENEMY,CIR_COIN    ,160, 90   ,6],
            [ 700,EVENT_ENEMY,CIR_COIN    ,160, 20   ,6],
            [ 900,EVENT_ENEMY,CIR_COIN    ,160, 80   ,6],
            
            [950,EVENT_ADD_APPEAR_ENEMY,CIR_COIN,160, 60,10],
            
            [1050,EVENT_ENEMY,SAISEE_RO,160, 60-24],
            [1051,EVENT_ENEMY,SAISEE_RO,160, 60   ],
            [1052,EVENT_ENEMY,SAISEE_RO,160, 60+24],
            
            [1080,EVENT_ENEMY,SAISEE_RO,160, 40-24],
            [1081,EVENT_ENEMY,SAISEE_RO,160, 40,  ],
            [1082,EVENT_ENEMY,SAISEE_RO,160, 40+24],
            
            [1095,EVENT_ENEMY,GREEN_LANCER,180,10],
            
            [1100,EVENT_ENEMY,CIR_COIN,    160,20    ,7],
            [1300,EVENT_ENEMY,CIR_COIN,    160,80    ,7],
            
            [1400,EVENT_ENEMY,TWIN_ARROW,160, 40],
            [1401,EVENT_ENEMY,TWIN_ARROW,160, 60],
            [1402,EVENT_ENEMY,TWIN_ARROW,160, 80],
            
            [1500,EVENT_ENEMY,TWIN_ARROW,160,  20],
            [1501,EVENT_ENEMY,TWIN_ARROW,160,  60],
            [1502,EVENT_ENEMY,TWIN_ARROW,160, 100],
            
            [1600,EVENT_ENEMY,TWIN_ARROW,160, 60   ],
            [1601,EVENT_ENEMY,TWIN_ARROW,160, 60+10],
            [1602,EVENT_ENEMY,TWIN_ARROW,160, 60-10],
            [1603,EVENT_ENEMY,TWIN_ARROW,160, 60+20],
            [1604,EVENT_ENEMY,TWIN_ARROW,160, 60-20],
            
            [3000,EVENT_SCROLL,SCROLL_SPEED_CHANGE,-4,-0.001],
            [4800,EVENT_SCROLL,SCROLL_STOP],
            [5010,EVENT_SCROLL,SCROLL_SPEED_CHANGE,1, 0.002],
            [6000,EVENT_SCROLL,SCROLL_SPEED_CHANGE,5, 0.002],
            
            [7000,EVENT_WARNING,500,120,240],
            [7300,EVENT_BOSS],
            [99999999],]
            
        self.event_list_stage_advance_base_l2= [
            [  10,EVENT_FAST_FORWARD_NUM,4,30],
            [ 200,EVENT_ENEMY,CIR_COIN    ,160, 10   ,6],
            [ 500,EVENT_ENEMY,CIR_COIN    ,160, 90   ,6],
            [ 700,EVENT_ENEMY,CIR_COIN    ,160, 20   ,6],
            [ 900,EVENT_ENEMY,CIR_COIN    ,160, 80   ,6],
            
            [950,EVENT_ADD_APPEAR_ENEMY,CIR_COIN,160, 60,10],
            
            [1050,EVENT_ENEMY,SAISEE_RO,160, 60-24],
            [1051,EVENT_ENEMY,SAISEE_RO,160, 60   ],
            [1052,EVENT_ENEMY,SAISEE_RO,160, 60+24],
            
            [1080,EVENT_ENEMY,SAISEE_RO,160, 40-24],
            [1081,EVENT_ENEMY,SAISEE_RO,160, 40,  ],
            [1082,EVENT_ENEMY,SAISEE_RO,160, 40+24],
            
            [1095,EVENT_ENEMY,GREEN_LANCER,180,10],
            
            [6000,EVENT_WARNING,500,120,240],
            [6300,EVENT_BOSS],
            [99999999],]
            
        self.event_list_stage_advance_base_l3= [    
            [  10,EVENT_FAST_FORWARD_NUM,4,30],
            [ 200,EVENT_ENEMY,CIR_COIN    ,160, 10   ,6],
            [ 500,EVENT_ENEMY,CIR_COIN    ,160, 90   ,6],
            [ 700,EVENT_ENEMY,CIR_COIN    ,160, 20   ,6],
            [ 900,EVENT_ENEMY,CIR_COIN    ,160, 80   ,6],
            
            [950,EVENT_ADD_APPEAR_ENEMY,CIR_COIN,160, 60,10],
            
            [1050,EVENT_ENEMY,SAISEE_RO,160, 60-24],
            [1051,EVENT_ENEMY,SAISEE_RO,160, 60   ],
            [1052,EVENT_ENEMY,SAISEE_RO,160, 60+24],
            
            [1080,EVENT_ENEMY,SAISEE_RO,160, 40-24],
            [1081,EVENT_ENEMY,SAISEE_RO,160, 40,  ],
            [1082,EVENT_ENEMY,SAISEE_RO,160, 40+24],
            
            [1095,EVENT_ENEMY,GREEN_LANCER,180,10],
            
            [1100,EVENT_ENEMY,CIR_COIN,    160,20    ,7],
            [1300,EVENT_ENEMY,CIR_COIN,    160,80    ,7],
            
            [1400,EVENT_ENEMY,TWIN_ARROW,160, 40],
            [1401,EVENT_ENEMY,TWIN_ARROW,160, 60],
            [1402,EVENT_ENEMY,TWIN_ARROW,160, 80],
            
            [1500,EVENT_ENEMY,TWIN_ARROW,160,  20],
            [1501,EVENT_ENEMY,TWIN_ARROW,160,  60],
            [1502,EVENT_ENEMY,TWIN_ARROW,160, 100],
            
            [1600,EVENT_ENEMY,TWIN_ARROW,160, 60   ],
            [1601,EVENT_ENEMY,TWIN_ARROW,160, 60+10],
            [1602,EVENT_ENEMY,TWIN_ARROW,160, 60-10],
            [1603,EVENT_ENEMY,TWIN_ARROW,160, 60+20],
            [1604,EVENT_ENEMY,TWIN_ARROW,160, 60-20],
            
            [6000,EVENT_WARNING,500,120,240],
            [6300,EVENT_BOSS],
            [99999999],] 
            
        #ゲーム全体のイベントリスト(ステージ、ループ数も考慮されてます)
        #フォーマット(このリストの書き方）は
        # game_event_list[
        #[ステージ1周回1、ステージ1周回2、ステージ1周回3],
        #[ステージ2周回1、ステージ2周回2、ステージ2周回3],
        #[ステージ3周回1、ステージ3周回2、ステージ3周回3],
        #[ステージ4周回1、ステージ4周回2、ステージ4周回3],
        #[ステージ5周回1、ステージ5周回2、ステージ5周回3],
        #[ステージ6周回1、ステージ6周回2、ステージ6周回3]
        #]
        #みたいな感じで書きます
        
        self.game_event_list = [
                            [self.event_list_stage_mountain_region_l1,
                            self.event_list_stage_mountain_region_l1,
                            self.event_list_stage_mountain_region_l1],
                            
                            [self.event_list_stage_advance_base_l1,
                            self.event_list_stage_advance_base_l2,
                            self.event_list_stage_advance_base_l3]
                            ]
        
        #self.game_event_list = [self.event_list_no_enemy_mode,  self.event_list_no_enemy_mode,  self.event_list_no_enemy_mode]
        
        #各ステージのＢＧ書き換えによるアニメーションの為のデータリスト群
        #フォーマットの説明
        #[アニメーションさせたいマップチップのx座標(0~255(8の倍数にしてね)),
        #                            y座標(0~255(8の倍数にしてね)),
        #                           アニメスピード(1なら1フレーム毎 2だと2フレーム毎って感じ),
        #                           アニメ枚数(横一列に並べてください)]
        self.bg_animation_list_mountain_region = [
                            [192,192,6,8],                          
                            [144, 64,6,8],
                            ]
        
        if self.boss_test_mode == 1:
            self.event_list = self.event_list_boss_test_mode #ボステストモードが1の時はボスだけが出現するイベントリストを登録します
        else:
            self.event_list = self.game_event_list[self.stage_number - 1][self.stage_loop - 1] 
                                                                #self.event_list_stage_advance_base_l1        
                                                                #とりあえずイベントリストはadvance_baseステージのものをコピーして使用します
                                                                #将来的にはステージやループ回数を反映する・・・はず
        
        self.bg_animation_list = self.bg_animation_list_mountain_region    #とりあえずBGアニメーションパターンリストはmountain_regionのものをコピーして使用します
        
        #自機のXY座標をトレースクローのXY座標としてコピーし、初期化を行う(とりあえず60要素埋め尽くす)(60要素=60フレーム分=1秒過去分まで記録される)
        for _i in range(TRACE_CLAW_BUFFER_SIZE):
            new_traceclaw = Trace_coordinates()
            new_traceclaw.update(self.my_x,self.my_y)
            self.claw_coordinates.append(new_traceclaw)
        
        self.create_raster_scroll_data() #ラスタースクロール用のデータの初期化＆育成

