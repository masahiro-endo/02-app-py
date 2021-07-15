# from random import randint   #random.randint(n,m) と呼ぶと、nからm(m自身を含む)までの間の整数が 等しい確率で、ランダムに返される
from random import random    #random.random() と呼ぶと、0から1の範囲(1は含まない)のランダムな実数が返される(主にパーティクル系で使用します)
import math
import pyxel
import pygame.mixer #MP3再生するためだけに使用する予定・・・予定は未定・・・そして未定は確定に！やったあぁ！
from source.module.state import *
from source.module.appconfig import *
from source.module.actor import *


class App:
    
    def __init__(self):
        pygame.mixer.init()  #pygameミキサー関連の初期化 pyxel.initよりも先にpygameをinitしないと上手く動かないみたい・・・
        pyxel.init(WINDOW_W,WINDOW_H,caption="CODE OF PYTHON",fps = 60) #ゲームウィンドウのタイトルバーの表示とfpsの設定(60fpsにした)
        
        self.load_system_data()        #システムデータをロードする関数の呼び出し
        if self.fullscreen_mode == 1:  #フルスクリーン起動モードフラグが立っていたのなら
            pyxel.init(WINDOW_W,WINDOW_H,caption="CODE OF PYTHON",fps = 60,fullscreen = True) #フルスクリーンでpyxelを再起動する
        pyxel.mouse(False)             #マウスカーソルを非表示にする
        
        self.load_kanji_font_data()            #漢字フォントデータのローディング
        self.select_cursor_flag = 0            #セレクトカーソルの移動更新フラグはoffにして初期化しておく
        
        #毎フレームごとにupdateとdrawを呼び出す
        pyxel.run(self.update,self.draw)#この命令でこれ以降は１フレームごとに自動でupdate関数とdraw関数が交互に実行されることとなります
                                        #近年のゲームエンジンはみんなこんな感じらしい？？？unityやUEもこんな感じなのかな？？使ったことないけど



    def update(self):
        ################################起動処理中 IPL ###################################################################
        if self.game_status == SCENE_IPL:         #ゲームステータスが「SCENE_IPL」の場合IPLメッセージの更新を行う
            self.update_ipl()                     #IPLの更新
        
        ################################ タイトル関連の変数を初期化 ###################################################################
        if self.game_status == SCENE_TITLE_INIT:  #ゲームステータスが「SCENE_TITLE_INIT」の場合タイトル関連の変数を初期化する関数を呼び出す
            self.update_title_init()              #タイトル関連の変数の初期化関数を呼び出す
        
        ################################ タイトル ###################################################################
        if self.game_status == SCENE_TITLE:       #ゲームステータスが「SCENE_TITLE」の場合タイトルの更新を行う
            self.update_title()                   #タイトルの更新
            self.update_append_star()             #背景の星の追加＆発生育成関数呼び出し
            self.update_star()                    #背景の星の更新（移動）関数呼び出し
        
        ################################ タイトルでメニュー選択中 ###################################################################
        if self.game_status == SCENE_TITLE_MENU_SELECT:
            self.update_title_menu_select()       #タイトルでのメニュー選択処理をする関数の呼び出し
            self.update_append_star()             #背景の星の追加＆発生育成関数呼び出し
            self.update_star()                    #背景の星の更新（移動）関数呼び出し
            self.update_window()                  #ウィンドウの更新（ウィンドウの開き閉じ画面外に消え去っていくとか）関数を呼び出し
            self.update_clip_window()             #画面外にはみ出たウィンドウを消去する関数の呼び出し
            self.update_active_window()           #現在アクティブ(最前面)になっているウィンドウのインデックス値(i)を求める関数の呼び出し
            self.update_select_cursor()           #セレクトカーソルでメニューを選択する関数を呼び出す
        
        ############################### ロード用リプレイデータスロットの選択中 #######################################################
        if self.game_status == SCENE_SELECT_LOAD_SLOT:#「SCENE_SELECT_LOAD_SLOT」の時は
            self.update_append_star()                 #背景の星の追加＆発生育成関数呼び出し
            self.update_star()                        #背景の星の更新（移動）関数呼び出し
            self.update_window()                      #ウィンドウの更新（ウィンドウの開き閉じ画面外に消え去っていくとか）関数を呼び出し
            self.update_clip_window()                 #画面外にはみ出たウィンドウを消去する関数の呼び出し
            self.update_active_window()               #現在アクティブ(最前面)になっているウィンドウのインデックス値(i)を求める関数の呼び出し
            self.update_select_cursor()               #セレクトカーソルでメニューを選択する関数を呼び出す
            if   self.cursor_decision_item_y == 0:      #メニューでアイテムナンバー0の「1」が押されたら
                self.replay_slot_num = 0              #スロット番号は0   (以下はほぼ同じ処理です)
            elif self.cursor_decision_item_y == 1:
                self.replay_slot_num = 1
            elif self.cursor_decision_item_y == 2:
                self.replay_slot_num = 2
            elif self.cursor_decision_item_y == 3:
                self.replay_slot_num = 3
            elif self.cursor_decision_item_y == 4:
                self.replay_slot_num = 4
            elif self.cursor_decision_item_y == 5:
                self.replay_slot_num = 5
            elif self.cursor_decision_item_y == 6:
                self.replay_slot_num = 6
            elif self.cursor_decision_item_y == 7:
                self.replay_slot_num = 7
            
            if self.cursor_decision_item_y != -1: #決定ボタンが押されてアイテムが決まったのなら
                self.cursor_type = False                 #セレクトカーソルの表示をoffにする
                self.move_mode = MOVE_MANUAL             #移動モードを「手動移動」にする
                self.replay_status = REPLAY_PLAY         #リプレイ機能の状態を「再生中」にします
                self.replay_stage_num = 0                #リプレイデータを最初のステージから再生できるように0初期化
                self.update_replay_data_file_load()      #リプレイデータファイルのロードを行います
                self.active_window_id = WINDOW_ID_MAIN_MENU #メインメニューウィンドウIDを最前列でアクティブなものとする
                self.game_status = SCENE_GAME_START_INIT #ゲームステータスを「SCENE_GAME_START_INIT」にしてゲームスタート時の初期化にする
        
        ################################ ゲームスタート時の初期化 #################################################################
        if self.game_status == SCENE_GAME_START_INIT: #ゲームステータスが「GAME_START_INIT」の場合（ゲームスタート時の状態遷移）は以下を実行する
            self.update_game_start_init()             #ゲーム開始前の初期化    スコアやシールド値、ショットレベルやミサイルレベルなどの初期化
            self.update_replay_data_status()          #リプレイデータ(ステータス関連)をバックアップする関数の呼び出し
            self.game_status = SCENE_STAGE_START_INIT #ゲームステータスを「STAGE_START_INIT」にする
        
        ################################ステージスタート時の初期化 #################################################################
        if self.game_status == SCENE_STAGE_START_INIT: #ゲームステータスが「GAME_START_INIT」の場合（ゲームスタート時の状態遷移）は以下を実行する
            self.update_stage_start_init()             #ステージ開始前の初期化   自機の座標や各リストの初期化、カウンター類の初期化
            self.game_status = SCENE_PLAY              #ゲームステータスを「STAGE_START_INIT」にする
        
        ################################ ゲームプレイ中！！！！！！ ###############################################################
        if     self.game_status == SCENE_PLAY\
            or self.game_status == SCENE_EXPLOSION\
            or self.game_status == SCENE_STAGE_CLEAR\
            or self.game_status == SCENE_GAME_OVER\
            or self.game_status == SCENE_BOSS_APPEAR\
            or self.game_status == SCENE_BOSS_BATTLE\
            or self.game_status == SCENE_BOSS_EXPLOSION\
            or self.game_status == SCENE_STAGE_CLEAR\
            or self.game_status == SCENE_STAGE_CLEAR_MOVE_MY_SHIP\
            or self.game_status == SCENE_STAGE_CLEAR_MY_SHIP_BOOST\
            or self.game_status == SCENE_STAGE_CLEAR_FADE_OUT:
            #自機関連の処理######################################################################################
            # ##################################################################################################
            self.update_my_ship()                  #自機の更新処理（移動処理）関数を呼び出す
            self.update_my_ship_record_coordinate()#自機の座標を過去履歴リストに書き込んでいく関数（トレースクローの座標として使用します）を呼び出す
            self.update_clip_my_ship()             #自機をはみ出さないようにする関数を呼び出す
            #パワーアップ関連の処理################################################
            self.update_powerup_shot()             #ショットのパワーアップ処理関数を呼び出し
            self.update_powerup_missile()          #ミサイルのパワーアップ処理関数の呼び出し
            #自機スピードチェンジ###################################################
            self.update_check_change_speed()       #自機スピードチェンジボタンが押されたか調べる関数呼び出し
            #自機ショット関連の処理#################################################
            self.update_my_shot()                  #自機弾の更新関数を呼び出す
            self.update_clip_my_shot()             #自機弾をはみ出さないようにする関数を呼び出す
            self.update_collision_my_shot_bg()     #自機弾と背景との当たり判定を行う関数を呼び出す
            self.update_collision_my_shot_enemy()  #自機弾と敵の当たり判定を行う関数を呼び出す
            self.update_collision_my_shot_boss()   #自機弾とボスの当たり判定を行う関数を呼び出す
            #ミサイル関連の処理###################################################################
            self.update_my_missile()               #自機ミサイルの更新（移動処理）関数を呼び出す
            self.update_clip_my_missile()          #自機ミサイルをはみ出さないようにする関数を呼び出す
            self.update_collision_missile_enemy()  #自機ミサイルと敵との当たり判定を行う関数の呼び出す
            self.update_collision_missile_boss()   #自機ミサイルとボスとの当たり判定を行う関数を呼び出す
            #クロー関連の処理 ####################################################################
            self.update_claw()                      #クローの更新（移動処理）関数を呼び出す
            self.update_claw_shot()                 #クローの弾の更新（移動処理）を呼び出す
            self.update_collision_claw_shot_enemy() #クローの弾と敵との当たり判定関数を呼び出す
            self.update_collision_claw_shot_boss()  #クローの弾とボスとの当たり判定関数を呼び出す
            self.update_collision_claw_shot_bg()    #クローの弾と背景との当たり判定関数を呼び出す
            #敵の弾関連の処理 ###################################################################################
            ####################################################################################################
            self.update_enemy_shot()               #敵の弾の更新（移動処理とか）＆自機と敵弾と自機との当たり判定の関数の呼び出し
            self.update_clip_enemy_shot()          #敵の弾が画面からはみ出したら消去する関数の呼び出し
            self.update_collision_enemy_shot_bg()  #敵の弾と背景との当たり判定を行う関数の呼び出し
            #クロー関連の処理###########################################################################################################
            self.update_delete_claw()                    #クローの消滅関数の呼び出し
            self.update_check_change_fix_claw_interval() #フイックスクロー間隔変化ボタンが押されたか調べる関数を呼び出す
            self.update_check_change_claw_style()        #クロースタイル変更ボタンが押されたか調べる関数を呼び出す    
            #敵関連の処理###############################################################################################################
            self.update_enemy_append_event_system() #イベントリストシステムによる敵の発生関数を呼び出す
            self.update_enemy_append_map_scroll()   #マップスクロールによる敵の発生関数を呼び出す
            self.update_event_append_request()      #イベントアペンドリストによる敵の追加発生関数を呼び出す（早回しなどの追加注文発生とかの処理）(イベント追加依頼）
            self.update_enemy()                     #敵の更新（移動とか）関数を呼び出す
            self.update_clip_enemy()                #画面からはみ出た敵を消去する関数を呼び出し
            #ボス関連の処理#############################################################################################################
            self.update_boss()                      #ボスの更新移動とかを行う関数を呼び出す
            #パワーアップアイテム類の処理################################################################################################
            self.update_obtain_item()                      #パワーアップアイテム類の更新（移動とか）する関数を呼び出します
            self.update_collision_obtain_item_enemy_shot() #パワーアップアイテムと敵弾の当たり判定を行う関数を呼び出します
            self.update_clip_obtain_item()                 #画面からはみ出したパワーアップアイテム類を消去する関数を呼び出します
            self.stage_count += 1                          #ステージ開始から経過したフレームカウント数を1増加させる
            #ランクアップ処理#############################################################################################################
            self.update_rank_up_look_at_playtime()   #時間経過によるランクアップ関数を呼び出します
            #スクロール関連の処理#########################################################################################################
            if self.boss_test_mode == 0:                                 #ボス戦テストモードオフの時だけ
                self.scroll_count += self.side_scroll_speed              #スクロールカウント数をスクロールスピード分(通常は1)増加させていく
                self.vertical_scroll_count += self.vertical_scroll_speed #縦スクロールカウント数を縦スクロールスピード分(大抵のステージは縦スクロールしないので0)増加させていく
            
            #横スクロールのスピード調整##################################################################################################
            if self.side_scroll_speed != self.side_scroll_speed_set_value:         #現在の横スクロールスピードと設定値が違っていたのならば
                self.side_scroll_speed += self.side_scroll_speed_variation #スピード変化量を加算減算してやって設定値まで近づけていきます
                if  -0.01 <= self.side_scroll_speed - self.side_scroll_speed_set_value <= 0.01:
                    self.side_scroll_speed = self.side_scroll_speed_set_value #横スクロールスピードが設定値の近似値(誤差-0.01~0.01)なら強制的に現在スピードを設定値にしちゃうのだ！
            
            #縦スクロールのスピード調整###################################################################################################
            if self.vertical_scroll_speed != self.vertical_scroll_speed_set_value: #現在の縦スクロールスピードと設定値が違っていたのならば
                self.vertical_scroll_speed += self.vertical_scroll_speed_variation #スピード変化量を加算減算してやって設定値まで近づけていきます
                if  -0.01 <= self.vertical_scroll_speed - self.vertical_scroll_speed_set_value <= 0.01:
                    self.vertical_scroll_speed = self.vertical_scroll_speed_set_value #縦スクロールスピードが設定値の近似値(誤差-0.01~0.01)なら強制的に現在スピードを設定値にしちゃうのだ！
            
            #ラスタスクロールの更新#######################################################################################################
            self.update_raster_scroll()               #ラスタースクロールの更新関数の呼び出し
            #マップチップナンバー書き換えによるアニメーション関連の更新######################################################################
            self.update_bg_rewrite_animation()        #BG書き換えによるアニメーション関数の呼び出し
            # self.update_dummy_bg_animation()        #BG 座標直接指定による書き換えダミーテスト
            #リプレイデータの記録と再生###################################################################################################
            self.update_record_replay_data()          #パッド＆キーボード入力によるリプレイデータの記録を行う関数を呼び出します
            self.update_replay_frame_index()          #リプレイ用のフレームインデックス値を1進めていく関数を呼びますぅ
            #乱数ルーレットの更新########################################################################################################
            self.update_rnd0_9()                    #乱数ルーレット( 0~9)の更新
            self.update_rnd0_99()                   #乱数ルーレット(0~99)の更新
        
        if     self.game_status == SCENE_PLAY\
            or self.game_status == SCENE_BOSS_APPEAR\
            or self.game_status == SCENE_BOSS_BATTLE\
            or self.game_status == SCENE_BOSS_EXPLOSION :#「プレイ中」とボス関連の時だけ自機の当たり判定関連とシールド値のチェック&ボタンを押したら何かをする処理を実行する
            #自機と色んなオブジェクトとの当たり判定処理#############################
            self.update_collision_my_ship_enemy()       #自機と敵との当たり判定関数を呼び出す             
            self.update_collision_my_ship_bg()          #自機と背景障害物との当たり判定関数を呼び出す
            self.update_collision_my_ship_obtain_item() #自機とパワーアップアイテム類の当たり判定（パワーアップゲットしたかな？どうかな？）
            self.update_collision_my_ship_boss()        #自機とボスとの当たり判定を行う関数を呼び出す
            #自機シールドのチェック###############################################
            self.update_check_my_shield()         #自機のシールドが残っているのかチェックする関数を呼び出す
            #武器発射関連の処理###################################################
            self.update_check_fire_shot()         #ショット発射ボタンが押されたかどうか？を調べる関数を呼び出す
            self.update_check_fire_missile()      #ミサイル発射ボタンが押されたかどうか？を調べる関数を呼び出す
            self.update_check_fire_claw_shot()    #クローが弾を発射するボタンが押された？かどうかを調べる関数を呼び出す
            self.update_check_change_sub_weapon() #サブウェポンの切り替えボタンが押されたか？どうかを調べる関数を呼び出す
            #デバッグモードによる敵や敵弾の追加発生（ボタンを押したら敵が出てくる！？）###################################################
            # self.update_debug_mode_enemy_append()  #デバッグモードによる敵＆敵弾追加発生
            #プレイ時間の計算#####################################################
            self.update_calc_playtime()        #プレイ時間を計算する関数を呼び出す
            #ハイスコアの更新チェック##############################################
            self.update_check_hi_score()       #ハイスコアが更新されているか調べる関数を呼び出す
            #タイマーフレア放出###################################################
            self.update_timer_flare()          #タイマーフレア放出の更新処理関数を呼び出す
            #大気圏突入時の火花の発生##########################################################
            self.update_atmospheric_entry_spark()   #大気圏突入時の火花を発せさせる関数の呼び出し
        
        if self.game_status == SCENE_BOSS_EXPLOSION:         #「BOSS_EXPLOSION」の時は
            self.uddate_present_repair_item()              #リペアアイテムを出現させる関数の呼び出し
        
        if self.game_status == SCENE_EXPLOSION:              #「EXPLOSION」の時は
            self.my_ship_explosion_timer += 1              # my_ship_explosionタイマーを加算していき
            if self.my_ship_explosion_timer >= SHIP_EXPLOSION_TIMER_LIMIT:#リミット値まで行ったのなら
                self.game_status = SCENE_GAME_OVER         #「GAME_OVER」にする
                pygame.mixer.music.fadeout(6000)           #BGMフェードアウト開始
        
        #######ゲームオーバー後の処理#############################################################
        if self.game_status == SCENE_GAME_OVER:              #「GAME_OVER」の時は
            self.game_over_timer += 1                         # game_overタイマーを加算していき
            if self.game_over_timer >= GAME_OVER_TIMER_LIMIT: #リミット値まで行ったのなら
                self.game_status = SCENE_GAME_OVER_FADE_OUT   #「ゲームオーバーフェードアウト開始」にする
        
        if self.game_status == SCENE_GAME_OVER_FADE_OUT:     #「GAME_OVER_FADE_OUT」の時は
            if self.fade_complete_flag == 1:                 #フェードアウト完了のフラグが建ったのなら
                self.bg_cls_color = 0                        #クリアスクリーン時の塗りつぶし色を初期値の0(黒)に戻す（イベントとかで変化する場合があるため） 
                self.star_scroll_flag = 1                    #背景星のスクロール表示をonにする（イベントとかで変化する場合があるため） 
                self.game_status = SCENE_GAME_OVER_SHADOW_IN #「GAME_OVER_SHADOW_IN」状態にする
        
        if self.game_status == SCENE_GAME_OVER_SHADOW_IN:    #「GAME_OVER_SHADOW_IN」の時は
            if self.shadow_in_out_complete_flag == 1:        #シャドウイン完了のフラグが建ったのなら
                self.game_status = SCENE_GAME_OVER_STOP      #「GAME_OVER_STOP」状態にする
        
        if self.game_status == SCENE_GAME_OVER_STOP:         #「GAME_OVER_STOP」の時は
            if self.replay_status == REPLAY_RECORD: #リプレイ録画中の時のリターンタイトルウィンドウ表示
                self.create_window(WINDOW_ID_GAME_OVER_RETURN)    #RETRN? SAVE&RETURNウィンドウの作成
                self.cursor_type = CURSOR_TYPE_NORMAL             #選択カーソル表示をonにする
                self.select_cursor_flag = 1                       #セレクトカーソルの移動更新フラグをオン
                self.cursor_move_direction = CURSOR_MOVE_UD       #カーソルは上下移動のみ
                self.cursor_x = 46                                #セレクトカーソルの座標を設定します
                self.cursor_y = 80
                self.cursor_item_y = 0                            #いま指示しているアイテムナンバーは0の「RETURN」
                self.cursor_decision_item_y = -1                  #まだボタンも押されておらず未決定状態なのでdecision_item_yは-1
                self.cursor_max_item_y = 1                        #最大項目数は「RETURN」「SAVE & RETURN」の2項目なので 2-1=1を代入
                self.active_window_id = WINDOW_ID_GAME_OVER_RETURN#このウィンドウIDを最前列でアクティブなものとする
                self.game_status = SCENE_RETURN_TITLE             #ゲームステータスを「RETURN_TITLE」にする
            elif self.replay_status == REPLAY_PLAY: #リプレイ再生中の時のリターンタイトルウィンドウ表示(SAVE&RETURN項目は表示しない)  
                self.create_window(WINDOW_ID_GAME_OVER_RETURN_NO_SAVE)     #RETRN?ウィンドウの作成
                self.cursor_type = CURSOR_TYPE_NORMAL                      #選択カーソル表示をonにする
                self.select_cursor_flag = 1                                #セレクトカーソルの移動更新フラグをオン
                self.cursor_move_direction = CURSOR_MOVE_UD                #カーソルは上下移動のみ
                self.cursor_x = 46                                         #セレクトカーソルの座標を設定します
                self.cursor_y = 80
                self.cursor_item_y = 0                                     #いま指示しているアイテムナンバーは0の「RETURN」
                self.cursor_decision_item_y = -1                           #まだボタンも押されておらず未決定状態なのでdecision_item_yは-1
                self.cursor_max_item_y = 0                                 #最大項目数は「RETURN」の1項目なので 1-1=0を代入
                self.active_window_id = WINDOW_ID_GAME_OVER_RETURN_NO_SAVE #このウィンドウIDを最前列でアクティブなものとする
                self.game_status = SCENE_RETURN_TITLE                      #ゲームステータスを「RETURN_TITLE」にする
        
        if self.game_status == SCENE_RETURN_TITLE:           #「RETURN_TITLE」の時は        
            if   self.cursor_decision_item_y == 0:             #メニューでアイテムナンバー0の「RETURN」が押されたら
                self.game_playing_flag = 0                     #ゲームプレイ中のフラグを降ろす
                self.select_cursor_flag = 0                    #セレクトカーソルの移動更新は行わないのでフラグを降ろす
                self.save_system_data()                        #システムデータをセーブする関数の呼び出し
                self.recoard_score_board()                     #スコアボードに点数書き込み
                self.score_board_bubble_sort(self.game_difficulty) #現在選択している難易度を引数として書き込んだスコアデータをソートする関数の呼び出し
                self.game_status = SCENE_TITLE_INIT            #ゲームステータスを「SCENE_TITLE_INIT」にしてタイトルの初期化工程にする
                
            elif self.cursor_decision_item_y == 1:             #メニューでアイテムナンバー1の「SAVE & RETURN」が押されたら
                self.window_replay_data_slot_select()          #リプレイデータファイルスロット選択ウィンドウの表示
                self.cursor_type = CURSOR_TYPE_NORMAL               #選択カーソル表示をonにする
                self.cursor_move_direction = CURSOR_MOVE_UD         #カーソルは上下移動のみ
                self.cursor_x = 67                                  #セレクトカーソルの座標を設定します
                self.cursor_y = 55
                self.cursor_step_x = 4                              #横方向の移動ドット数は4ドット
                self.cursor_step_y = 7                              #縦方向の移動ドット数は7ドット
                self.cursor_item_y = 0                              #いま指示しているアイテムナンバーは0の「1」
                self.cursor_decision_item_y = -1                    #まだボタンも押されておらず未決定状態なのでdecision_item_yは-1
                self.cursor_max_item_y = 6                          #最大項目数は「1」「2」「3」「4」「5」「6」「7」の7項目なので 7-1=6を代入
                self.cursor_menu_layer = 0                          #メニューの階層は最初は0にします
                self.active_window_id = WINDOW_ID_SELECT_FILE_SLOT  #このウィンドウIDを最前列でアクティブなものとする
                self.game_status = SCENE_SELECT_SAVE_SLOT    #ゲームステータスを「SCENE_SELECT_SAVE_SLOT」にしてセーブスロット選択にする
            
        if self.game_status == SCENE_SELECT_SAVE_SLOT:       #「SCENE_SELECT_SAVE_SLOT」の時は
            if   self.cursor_decision_item_y == 0:             #メニューでアイテムナンバー0の「1」が押されたら
                self.replay_slot_num = 0                     #スロット番号は0   (以下はほぼ同じ処理です)
            elif self.cursor_decision_item_y == 1:
                self.replay_slot_num = 1
            elif self.cursor_decision_item_y == 2:
                self.replay_slot_num = 2
            elif self.cursor_decision_item_y == 3:
                self.replay_slot_num = 3
            elif self.cursor_decision_item_y == 4:
                self.replay_slot_num = 4
            elif self.cursor_decision_item_y == 5:
                self.replay_slot_num = 5
            elif self.cursor_decision_item_y == 6:
                self.replay_slot_num = 6
            elif self.cursor_decision_item_y == 7:
                self.replay_slot_num = 7
            
            if self.cursor_decision_item_y != -1: #決定ボタンが押されてアイテムが決まったのなら
                self.game_playing_flag = 0                   #ゲームプレイ中のフラグを降ろす
                self.select_cursor_flag = 0                  #セレクトカーソルの移動更新は行わないのでフラグを降ろす
                
                self.save_system_data()                    #システムデータをセーブする関数の呼び出し
                self.recoard_score_board()                   #スコアボードに点数書き込み
                self.score_board_bubble_sort(self.game_difficulty) #現在選択している難易度を引数として書き込んだスコアデータをソートする関数の呼び出し
                self.update_replay_data_list()             #録画したリプレイデータを登録します
                
                self.update_replay_data_file_save()          #リプレイデータファイルのセーブ
                
                self.replay_recording_data = []            #録画したリプレイデータは登録したので元のデータは消去します
                self.replay_mode_stage_data_backup = self.replay_mode_stage_data #各ステージ開始時のデータ履歴をバックアップ
                self.game_status = SCENE_TITLE_INIT        #ゲームステータスを「SCENE_TITLE_INIT」にしてタイトルの初期化工程にする
        
        #########ステージクリア後の処理#############################################################
        if self.game_status == SCENE_STAGE_CLEAR_FADE_OUT:   #「SCENE_STAGE_CLEAR_FADE_OUT」の時は
            if self.fade_complete_flag == 1:                 #フェードアウト完了のフラグが建ったのなら
                self.stage_number += 1    #ステージ数を1増やす
                self.replay_stage_num += 1#リプレイ再生記録用のステージ数も1増やします
                if self.replay_stage_num > 50:            #リプレイ記録用のファイルは50ステージ分しか今の所用意していないので
                    self.replay_status = REPLAY_STOP      #リプレイの記録はストップさせるようにします
                    self.replay_stage_num = 50            #念のため記録ステージ数は最高の50で丸めておきます
                
                if self.stage_number == STAGE_VOLCANIC_BELT:  #ステージ3 火山地帯はまだ未完成なので・・・
                    self.stage_number = STAGE_MOUNTAIN_REGION #ステージ1 山岳地帯に戻してやります
                    self.stage_loop += 1     #ループ数を1増やします
                    if self.stage_loop >= 4: #4周目以降は作っていないので\\\
                        self.stage_loop = 1  #1周目に戻ります
                
                self.game_status = SCENE_STAGE_START_INIT    #ゲームステータスを「STAGE_START_INIT」にして次のステージへ・・・・
        
        if self.game_playing_flag == 1: #ゲームプレイ中のフラグが立っていたのなら以下の処理を行う(主にゲーム進行に関与しない映像処理関連)
            self.update_debug_status()      #デバッグステータス表示＆非表示の切り替え
            #映像オブジェクト関連の処理################################################################################################
            self.update_append_star()       #背景の星の追加＆発生育成関数呼び出し
            self.update_append_cloud()      #背景の雲の追加＆発生育成関数呼び出し
            self.update_star()              #背景の星の更新（移動）関数呼び出し
            self.update_particle()          #パーティクルの更新関数呼び出し
            self.update_background_object() #背景オブジェクトの更新関数の呼び出し
            self.update_explosion()         #爆発パターンの更新関数呼び出し 
            #一時停止(pause)の処理###################################################################################################
            self.update_game_pause()        #ボタンが押されたらポーズをかける関数を呼び出し
            #ウィンドウ＆メニューカーソル関連の処理###############################################################################################
            self.update_window()            #ウィンドウの更新（ウィンドウの開き閉じ画面外に消え去っていくとか）関数を呼び出し
            self.update_clip_window()       #画面外にはみ出たウィンドウを消去する関数の呼び出し
            self.update_active_window()     #現在アクティブ(最前面)になっているウィンドウのインデックス値(i)を求める関数の呼び出し
        
        if self.select_cursor_flag == 1:  #セレクトカーソルを動かすフラグが立っているのならカーソルの移動更新を行う
            self.update_select_cursor()     #セレクトカーソルでメニューを選択する関数を呼び出す
        

    def draw(self):
        pyxel.cls(self.bg_cls_color)                #背景を指定色で消去する(初期値は0なので真っ黒になります)
        if self.game_status == SCENE_IPL:
            self.draw_ipl()
        
        if self.game_status == SCENE_TITLE or self.game_status == SCENE_TITLE_MENU_SELECT or self.game_status == SCENE_SELECT_LOAD_SLOT:
            self.draw_star()          #背景の星を表示する関数の呼び出し
            self.draw_title()         #タイトルロゴの表示関数の呼び出し
            self.draw_window()        #メニューウィンドウの表示関数の呼び出し
            self.draw_select_cursor() #セレクトカーソルの表示関数の呼び出し
        
        if self.game_playing_flag == 1 and self.star_scroll_flag == 1:#ゲームプレイ中フラグon,星スクロールフラグonの時は背景の星を表示する
            self.draw_star()          #背景の星を表示する関数の呼び出し 
        
        if     self.game_status == SCENE_PLAY\
            or self.game_status == SCENE_BOSS_APPEAR\
            or self.game_status == SCENE_BOSS_BATTLE\
            or self.game_status == SCENE_BOSS_EXPLOSION\
            or self.game_status == SCENE_EXPLOSION\
            or self.game_status == SCENE_STAGE_CLEAR\
            or self.game_status == SCENE_STAGE_CLEAR_MOVE_MY_SHIP\
            or self.game_status == SCENE_STAGE_CLEAR_MY_SHIP_BOOST\
            or self.game_status == SCENE_STAGE_CLEAR_FADE_OUT\
            or self.game_status == SCENE_GAME_OVER\
            or self.game_status == SCENE_GAME_OVER_FADE_OUT\
            or self.game_status == SCENE_PAUSE:
            
            #一番奥の背景の表示
            if   self.stage_number == STAGE_MOUNTAIN_REGION:
                #雲ウェーブラスタースクロールの表示
                self.draw_raster_scroll(0)  #ラスタースクロール描画関数呼び出し 山より奥で描画します
                
                #奥の雲スクロールの表示
                if self.disp_flag_bg_back == DISP_ON:
                    pyxel.bltm(-int(self.scroll_count  // 10 % (256*8 - 160)),-(self.vertical_scroll_count // 28) + 97,  1,    0,235,    256,7,    1)
                
                #影が強めの奥の山を描画
                if self.disp_flag_bg_middle == DISP_ON:
                    pyxel.bltm(-int(self.scroll_count  // 8  % (256*8 - 160)),-(self.vertical_scroll_count // 24) + 116,  1,    0,243,    256,5,    self.bg_transparent_color)
                
                #手前の小さめの山を描画
                if self.disp_flag_bg_front == DISP_ON:
                    pyxel.bltm(-int(self.scroll_count  // 4  % (256*8 - 160)),-(self.vertical_scroll_count // 16) + 160,  1,    0,248,    256,5,    self.bg_transparent_color)
                
                #湖面のラスタースクロールの表示、成層圏と大気圏の境目のラスタースクロールの表示
                self.draw_raster_scroll(1)  #ラスタースクロール描画関数呼び出し 山より手前で描画しますっ！
                
            elif self.stage_number == STAGE_ADVANCE_BASE:
                pyxel.bltm(-(self.scroll_count // 8) + 250,0,0,0,240,256,120,self.bg_transparent_color)
            
            ####################背景表示
            ###################pyxel.bltm(-(pyxel.frame_count // 8),0,0,((pyxel.frame_count / 2) - 160) ,0,160,120,0)最初はこれで上手くいかなかった・・・・なぜ？
            ###################奥の背景表示
            ###################pyxel.bltm(-(pyxel.frame_count // 4) + 400,0,0,0,16,256,120,0)
            
            if self.stage_number == STAGE_ADVANCE_BASE:
                pyxel.bltm(-(self.scroll_count // 4) + 400,0,0,0,224,256,120,self.bg_transparent_color)
            elif self.stage_number == STAGE_MOUNTAIN_REGION:
                    if self.disp_flag_bg_front == DISP_ON:
                        pyxel.bltm(-int(self.scroll_count % (256*8 - 160)),     -self.vertical_scroll_count,  1,    0,0,    256,256,    self.bg_transparent_color)
            
            self.draw_background_object()    #背景オブジェクトの描画関数の呼び出し
            
            self.draw_enemy_shot(PRIORITY_BOSS_BACK)   #敵の弾を表示する関数を呼び出す(ボスキャラの真後ろ)---------------------------
            self.draw_boss()         #ボスを表示する関数を呼び出す
            self.draw_boss_hp()      #ボスの耐久力を表示する関数を呼び出す
            self.draw_enemy_shot(PRIORITY_BOSS_FRONT)   #敵の弾を表示する関数を呼び出す(ボスキャラのすぐ手前)-------------------------
            
            self.draw_obtain_item()  #パワーアップアイテム類の表示
            
            self.draw_enemy()        #敵を表示する関数を呼び出す
            self.draw_enemy_shot(PRIORITY_FRONT)       #敵の弾を表示する関数を呼び出す (前面)---------------------------------------
            self.draw_enemy_shot(PRIORITY_MORE_FRONT)  #敵の弾を表示する関数を呼び出す (敵弾の中でもさらに前面)-----------------------
            PRIORITY_MORE_FRONT
            self.draw_particle()     #パーティクルを表示する関数の呼び出し
            
            self.draw_my_shot()      #自機弾の表示
            self.draw_missile()      #ミサイルの表示
            self.draw_claw_shot()    #クローショットの表示
            
            #手前の背景表示
            #結局なんでこれでキチンとスクロール表示されたのか謎・・・結局はじめは-1024ドットのx座標位置からスクロール開始していくことに・・
            #pyxel.bltm(-(pyxel.frame_count // 2) + 1024,0,0,0,0,256,120,0)
            if self.stage_number == STAGE_ADVANCE_BASE:
                if   self.stage_loop == 1:
                    pyxel.bltm(-(self.scroll_count // 2) + 1024,0,  0,    0,0,    256,120,    self.bg_transparent_color) #1周目マップ
                elif self.stage_loop == 2:
                    pyxel.bltm(-(self.scroll_count // 2) + 1024,0,  0,    0,16,   256,120,    self.bg_transparent_color) #2周目マップ
                elif self.stage_loop == 3:
                    pyxel.bltm(-(self.scroll_count // 2) + 1024,0,  0,    0,32,   256,120,    self.bg_transparent_color) #3周目マップ
            self.draw_enemy_shot(PRIORITY_TOP)        #敵の弾を表示する関数を呼び出す (最前面)-------------------------------------
        #自機、クロー、シールドの表示###############################################
        if     self.game_status == SCENE_PLAY\
            or self.game_status == SCENE_BOSS_APPEAR\
            or self.game_status == SCENE_BOSS_BATTLE\
            or self.game_status == SCENE_BOSS_EXPLOSION\
            or self.game_status == SCENE_STAGE_CLEAR\
            or self.game_status == SCENE_STAGE_CLEAR_MOVE_MY_SHIP\
            or self.game_status == SCENE_STAGE_CLEAR_MY_SHIP_BOOST\
            or self.game_status == SCENE_STAGE_CLEAR_FADE_OUT\
            or self.game_status == SCENE_PAUSE:
            
            self.draw_my_ship()     #自機表示
            self.draw_claw()        #クローの表示
            self.draw_ls_shield()   #Ｌ'sシールドシステムの表示
        
        if self.game_playing_flag == 1:              #「ゲームプレイ中」の時は爆発パターン表示
            self.draw_explosion(PRIORITY_FRONT)      #爆発パターン(前面)の表示
            self.draw_explosion(PRIORITY_MORE_FRONT) #爆発パターン(さらに前面)の表示
        
        #フェードアウトスクリーンの表示###############################################
        if    self.game_status == SCENE_GAME_OVER_FADE_OUT\
            or self.game_status == SCENE_STAGE_CLEAR_FADE_OUT:
            
            self.draw_fade_in_out_screen(FADE_OUT,0)        #フェードイン＆フェードアウト用のエフェクトスクリーンの描画表示
        
        #画面中央80ドットだけ表示する処理###########################################
        if    self.game_status == SCENE_GAME_OVER_SHADOW_IN\
            or self.game_status == SCENE_GAME_OVER_STOP\
            or self.game_status == SCENE_RETURN_TITLE:
            
            self.draw_shadow_out_screen(40,0)  #中央付近80ドット分だけ残してシャドウアウトする
        
        if self.game_playing_flag == 1:             #「ゲームプレイ中」の時は以下の処理も行う
            self.draw_sub_weapon_select_guidebox()  #選択中のサブウェポンのカーソルガイドボックスの表示
            self.draw_sub_weapon_select_gauge()     #サブウェポン一覧表示
            
            self.draw_status()             #スコアやスピード、自機耐久力などの表示関数の呼び出し （通常ステータス表示）
            self.draw_debug_status()       #デバッグ用ステータスの表示関数の呼び出し          （デバック用ステータス表示）
            self.draw_window()             #メッセージウィンドウの表示
            self.draw_select_cursor()      #セレクトカーソルの表示
            
            self.draw_warning_dialog()     #WARNINGダイアログの表示
            self.draw_stage_clear_dialog() #STAGE CLEARダイアログの表示
            
            # self.draw_dummy_put_bg_xy()  #BG Get&Put dummy test
        
        #一時停止・ポーズメッセージの表示#########################################
        if self.game_status == SCENE_PAUSE:
            self.draw_pause_message()      #一時停止・ポーズメッセージの表示
        
        #ゲームオーバー画像の表示##################################################
        if     self.game_status == SCENE_GAME_OVER\
            or self.game_status == SCENE_GAME_OVER_FADE_OUT\
            or self.game_status == SCENE_GAME_OVER_SHADOW_IN\
            or self.game_status == SCENE_GAME_OVER_STOP\
            or self.game_status == SCENE_RETURN_TITLE:
            self.draw_gameover_dialog()          #ゲームオーバー表示をする関数呼び出し


if __name__ == "__main__":
    App()