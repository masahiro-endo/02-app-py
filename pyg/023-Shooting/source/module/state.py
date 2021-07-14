

#定数の定義関連##################################################################################################
WINDOW_W = 160    #ゲームウィンドウの横サイズ
WINDOW_H = 120    #ゲームウィンドウの縦サイズ
SHIP_H = 8        #自機の縦サイズ
SHIP_W = 8        #自機の横サイズ
MOVE_LIMIT = 20   #前方に進める限界距離

ALL_STAGE_NUMBER = 10 #全ステージ数(撃ち返し弾を出すとき ループ数×ALL_STAGE_NUMBER+ステージ数を計算して撃ち返すのか撃ち返さないのか判断します)

SHOT_EXP_MAXIMUM = 71 #自機ショットの最大経験値（この数値を超えちゃダメだよ）
                #例 self.j_python_shot_table_listのy軸の最大値がこの数と一致します
                #これより大きい数値にしちゃうとindex erroerになっちゃうからね
MISSILE_EXP_MAXIMUM = 71 #自機ミサイルの最大経験値（この数値を超えちゃダメだよ）
                #例 self.j_python_missile_table_listのy軸の最大値がこの数と一致します
                #これより大きい数値にしちゃうとindex erroerになっちゃうからね
SUB_WEAPON_LEVEL_MAXIMUM = 10 #自機サブウェポンのレベルの最大値
                    #例 self.sub_weapon_tail_shot_level_data_listのy軸の最大値がこの数と一致します
                    #これより大きい数値にしちゃうとindex out of range erroerになっちゃうからね

#!ゲームステータス関連の定数定義 game_statusに代入されます#######################################################################
SCENE_IPL               =  0    #IPL(Initial Program Load)
SCENE_SPLASH_LOGO       =  1    #起動処理中（スプラッシュロゴ表示）

SCENE_TITLE_INIT        = 10    #タイトル表示に必要な初期化をする
SCENE_TITLE             = 11    #タイトル表示中
SCENE_TITLE_MENU_SELECT = 12    #タイトルメニュー選択中
SCENE_SELECT_LOAD_SLOT  = 13    #リプレイ再生に必要なリプレイファイルをどのスロットからロードするのか？選択待ち
SCENE_CREDIT            = 14    #クレジットタイトル表示中

SCENE_CONFIG            = 20    #設定メニュー表示中

SCENE_DEBUG_CONGIG      = 30    #デバッグモード設定メニュー表示中

SCENE_TITLE_DEMO        = 40    #タイトルデモ表示中（ストーリーとかのビジュアルシーン）
SCENE_ADVERTISE_DEMO    = 41    #アドバタイズデモ（コンピュータによるゲームの宣伝の為のリプレイ再生）
SCENE_MIDDLE_DEMO       = 42    #中間デモ中

SCENE_GAME_START_INIT   = 50    #ゲーム開始前の初期化    スコアやシールド値、ショットレベルやミサイルレベルなどの初期化
SCENE_STAGE_START_INIT  = 51    #ステージ開始前の初期化   自機の座標や各リストの初期化、カウンター類の初期化
SCENE_START             = 52    #ゲーム開始(スタートダイアログを出したり、自機の出現アニメーションとか)
SCENE_PLAY              = 53    #ゲームプレイ中
SCENE_BOSS_APPEAR       = 54    #ボスキャラ現れる！
SCENE_BOSS_BATTLE       = 55    #ボスキャラと戦闘中
SCENE_BOSS_EXPLOSION    = 56    #ボスキャラ爆発中！
SCENE_PAUSE             = 57    #一時中断中
SCENE_EXPLOSION         = 58    #被弾して爆発中（ゲーム自体はまだ進行している）
SCENE_RESTORATION       = 59    #復活中(自機は点滅状態で無敵状態だよ)

SCENE_GAME_OVER           = 60 #ゲームオーバーメッセージ表示中（ゲームはまだ進行している）
SCENE_GAME_OVER_FADE_OUT  = 61 #ゲームオーバーメッセージ表示中（ゲーム自体は停止、画面をフェードアウトさせていく）
SCENE_GAME_OVER_SHADOW_IN = 62 #ゲームオーバーメッセージ表示中（ゲーム自体は停止、画面をシャドウインさせていく）
SCENE_GAME_OVER_STOP      = 63 #ゲームオーバーメッセージ表示中（ゲーム自体は停止している）
SCENE_RETURN_TITLE        = 64 #ゲームオーバーになりタイトルに戻るかどうかカーソルを出して選択待ち
SCENE_SELECT_SAVE_SLOT    = 65 #タイトルに戻る前にリプレイファイルどのスロットにセーブするのか選択待ち

SCENE_STAGE_CLEAR               = 70 #ステージクリア
SCENE_STAGE_CLEAR_MOVE_MY_SHIP  = 71 #ステージクリア後、自機がステージクリア画像左上まで自動に動いていくシーン
SCENE_STAGE_CLEAR_MY_SHIP_BOOST = 72 #ステージクリア後、自機がブーストして右へ過ぎ去っていくシーン
SCENE_STAGE_CLEAR_FADE_OUT      = 73 #ステージクリア後のフェードアウト

SCENE_CONTINUE    = 80   #コンティニューメッセージ表示中

SCENE_ENDING      = 90   #エンディング表示中

SCENE_STAFF_ROLL  = 99   #スタッフロール表示中

#!自機のIDナンバー定義 ##########################################################################
J_PYTHON          =  0   #Justice Python
PYTHON_FORCE      =  1   #Python4.0(4th.force)
E_PERL            =  2   #Elegant Perl(practical extraction and report language)
C_FORTRAN         =  3   #Classical FORTRAN 1954
AI_LOVE_LISP      =  4   #AI love LISP 1958
ECLIPSING_ALGOL   =  5   #Eclipsing Binary ALGOL 1958
AUNT_COBOL        =  6   #Aunt COBOL more better 1959
BEGINNING_ADA     =  7   #Beginning programmer Ada 1815-1983
FIRST_BASIC       =  8   #First Beginners All purpose Symbolic Instruction Code 1964
CUTTER_SHARP_2000 =  9   #Cutter # 2000
LEGEND_ASM        = 10   #Legend Assembler
LAST_RUST         = 11   #Last Rust
GAMBA_RUBY        = 12   #GAMBA Ruby New Generation IDOL
SHIFT_SWIFT       = 13   #SHIFT timer SWIFT space
MAGI_FORCE        = 14   #MAGI FORCE power is dream
LOOK_AT_LOGO      = 15   #LOOK AT THE TURTLE LOGO! 1967

#自機、機体分類
SHIP_FIRST_STEP      = 0 #初期機体
SHIP_STANDARD        = 1 #標準機体
SHIP_ANCENT          = 2 #古代機体
SHIP_EXTRA           = 3 #特殊機体
SHIP_NEXT_GENERATION = 4 #次世代機体

#言語選択
LANGUAGE_ENG         = 0 #英語
LANGUAGE_JPN         = 1 #日本語

#!キーアイテムの定数定義 ########################################################
KEY_ITEM_PUNCHED_CARD               =  0 #パンチカード
KEY_ITEM_MAGNETIC_CORE_MEMORY       =  1 #磁気コアメモリ
KEY_ITEM_MAGNETIC_BUBBLE_MEMORY     =  2 #磁気バブルメモリ
KEY_ITEM_CASSETLE_TAPE_IEC_TYPE_I   =  3 #ノーマルテープ
KEY_ITEM_CASSETLE_TAPE_IEC_TYPE_II  =  4 #ハイポジションテープ
KEY_ITEM_CASSETLE_TAPE_IEC_TYPE_III =  5 #フェリクロームカセットテープ
KEY_ITEM_CASSETLE_TAPE_IEC_TYPE_IV  =  6 #メタルカセットテープ
KEY_ITEM_QUICK_DISC                 =  7 #クイックディスク
KEY_ITEM_JAZ                        =  8 #JAZ
KEY_ITEM_DAT                        =  9 #DAT デジタルオーディオテープ
KEY_ITEM_3INCH_FLOPPY_DISK          = 10 #3インチフロッピーディスク
KEY_ITEM_PD                         = 11 #PD Phase-change Dual or Phase-change Disc
KEY_ITEM_MD                         = 12 #Micro Drive
KEY_ITEM_KANJI_ROM_CARTRIDGE        = 13 #漢字ROMカートリッジ HBI-K21

#称号
NOVICE        = 0 #ノービス        入門者
ASPIRANT      = 1 #アスパイラント   志を持つ者
BATTLER       = 2 #バトラー        兵士
FIGHTER       = 3 #ファイター      闘士
ADEPT         = 4 #アデプト        熟練者
CHEVALIER     = 5 #シェバリアー    騎士
VETERAN       = 6 #ベテラン        軍人
WARRIOR       = 7 #ウォーリア      勇士
SWORDMAN      = 8 #ソードマン      剣士
HERO          = 9 #ヒーロー        英雄
SWASHBUCKLER  =10 #スワッシュバックラー 暴れ者
CHAMPION      =12 #チャンピオン    勝者
MYRMIDON      =11 #マーミダン      忠臣
SUPERHERO     =13 #スーパーヒーロー 勇者
PALADIN       =14 #パラディン      親衛隊騎士
LOAD          =15 #ロード          君主
MASTER_LOAD   =16 #マスターロード   大君主

#勲章(メダル)自機のオプションスロットにはめ込むことが出来るメダル 色々な効果を付加することが出来る
MEDAL_BEFOREHAND_1SHOT_ITEM     = 0 #ゲームスタート時点で事前にショットアイテムを1個入手した状態から始まる 1個目のショットアイテムは得点アイテムに変化する それ以降は通常となる
MEDAL_BEFOREHAND_2SHOT_ITEM     = 1 #ゲームスタート時点で事前にショットアイテムを2個入手した状態から始まる 1~2個目までのショットアイテムは得点アイテムに変化する それ以降は通常となる
MEDAL_BEFOREHAND_3SHOT_ITEM     = 2 #ゲームスタート時点で事前にショットアイテムを3個入手した状態から始まる 1~3個目までのショットアイテムは得点アイテムに変化する それ以降は通常となる
MEDAL_BEFOREHAND_4SHOT_ITEM     = 3 #ゲームスタート時点で事前にショットアイテムを4個入手した状態から始まる 1~4個目までのショットアイテムは得点アイテムに変化する それ以降は通常となる
MEDAL_EQUIPMENT_LS_SHIELD       = 4 #L'sシールドが装備される
MEDAL_PLUS_MEDALLION            = 5 #はめ込むことで2つのオプションスロットが作られる(実質スロットが1増える)

#ショットレベル(というか種類？)の定数定義
SHOT_LV0_VULCAN_SHOT      =  0 #バルカンショット1連装
SHOT_LV1_TWIN_VULCAN_SHOT =  1 #ツインバルカンショット2連装
SHOT_LV2_3WAY_VULCAN_SHOT =  2 #3WAYバルカンショット
SHOT_LV3_5WAY_VULCAN_SHOT =  3 #5WAYバルカンショット
SHOT_LV4_LASER            =  4 #レーザー
SHOT_LV5_TWIN_LASER       =  5 #ツインレーザー
SHOT_LV6_3WAY_LASER       =  6 #3WAYレーザー
SHOT_LV7_WAVE_CUTTER_LV1  =  7 #ウェーブカッターLv1
SHOT_LV8_WAVE_CUTTER_LV2  =  8 #ウェーブカッターLv2
SHOT_LV9_WAVE_CUTTER_LV3  =  9 #ウェーブカッターLv3
SHOT_LV10_WAVE_CUTTER_LV4 = 10 #ウェーブカッターLv4

#ミサイルレベル(というか種類？)の定数定義
MISSILE_LV0_NORMAL_MISSILE = 0 #初期装備右下ミサイル
MISSILE_LV1_TWIN_MISSILE   = 1 #ツインミサイル(右下と右上方向)
MISSILE_LV2_MULTI_MISSILE  = 2 #マルチミサイル(右下右上左下左上4方向)

#!サブウェポン関連のIDナンバー定数定義 #############################################
TAIL_SHOT        = 0 #テイルショットＩＤナンバー
PENETRATE_ROCKET = 1 #ペネトレートロケットＩＤナンバー
SEARCH_LASER     = 2 #サーチレーザーＩＤナンバー
HOMING_MISSILE   = 3 #ホーミングミサイルＩＤナンバー
SHOCK_BUMPER     = 4 #ショックバンパーＩＤナンバー

#難易度リストを参照するときに使用するインデックスナンバー定数定義
LIST_DIFFICULTY                   = 0 #難易度(難しさ)
LIST_START_BONUS_SHOT             = 1 #ゲーム開始時のショットボーナス
LIST_START_BONUS_MISSILE          = 2 #ゲーム開始時のミサイルボーナス
LIST_START_BONUS_SHIELD           = 3 #ゲーム開始時のシールドボーナス
LIST_START_CLAW                   = 4 #ゲーム開始時のクローの数
LIST_REPAIR_SHIELD                = 5 #ステージクリア後に回復するシールド値
LIST_RETURN_BULLET                = 6 #撃ち返し弾の有無と有の時の種類
LIST_SCORE_MAGNIFICATION          = 7 #スコア倍率
LIST_RANK_UP_FRAME                = 8 #ランク上昇フレーム数
LIST_START_RANK                   = 9 #ゲームスタート時のランク数
LIST_DAMAGE_AFTER_INVINCIBLE_TIME =10 #被弾後の無敵時間
LIST_GET_ITEM_INVINCIBLE_TIME     =11 #アイテム取得後の無敵時間
LIST_ITEM_ERACE_BULLET            =12 #パワーアップアイテムが敵弾を消去するかどうか？のフラグ
LIST_RANK_LIMIT                   =13 #ランク数の上限値
LIST_RETURN_BULLET_START_LOOP     =14 #撃ち返しを始めてくるループ数
LIST_RETURN_BULLET_START_STAGE    =15 #撃ち返しを始めてくるステージ数
LIST_RANK_DOWN_NEED_DAMAGE        =16 #1ランクダウンに必要なダメージ数
LIST_LOOP_POWER_CONTROL           =17 #次のループに移る時のパワーアップ調整関連の動作の仕方とか
LIST_ITEM_RANGE_OF_ATTRACTION     =18 #アイテムを引き寄せる範囲
LIST_ITEM_BOUNCE_NUM              =19 #アイテムの跳ね返り回数(左端に当たったら何回まで跳ね返るかの数値)

#難易度名の定数定義
GAME_VERY_EASY = 0
GAME_EASY      = 1
GAME_NORMAL    = 2
GAME_HARD      = 3
GAME_VERY_HARD = 4
GAME_INSAME    = 5 #狂ってる・・・・・

#ランクリストを参照するときに使用するインデックスナンバー定数定義
LIST_RANK                           = 0  #ランク数
LIST_RANK_E_SPEED_MAG               = 1  #敵スピード倍率
LIST_RANK_BULLET_SPEED_MAG          = 2  #敵狙い撃ち弾スピード倍率
LIST_RANK_RETURN_BULLET_PROBABILITY = 3  #敵撃ち返し弾発射確率
LIST_RANK_E_HP_MAG                  = 4  #敵耐久力倍率
LIST_RANK_E_BULLET_APPEND           = 5  #弾追加数
LIST_RANK_E_BULLET_INTERVAL         = 6  #弾発射間隔減少パーセント
LIST_RANK_NWAY_LEVEL                = 7  #nWAY弾のレベル(レベルが上がると扇状の幅が広がる)

#スコアリストを参照するときに使用するインデックスナンバー定数定義
LIST_SCORE_DIFFICULTY               =  0 #難易度
LIST_SCORE_RANKING                  =  1 #順位
LIST_SCORE_NAME                     =  2 #名前
LIST_SCORE_CLEAR_STAGE              =  3 #クリアしたステージ数
LIST_SCORE_SHIP_USED                =  4 #使用した機体
#ゲーム開始時に追加されるクロー数の定数定義
NO_CLAW      = 0
ONE_CLAW     = 1
TWO_CLAW     = 2
THREE_CLAW   = 3

#ステージクリア時に回復するシールド値
REPAIR_SHIELD0 = 0
REPAIR_SHIELD1 = 1
REPAIR_SHIELD2 = 2
REPAIR_SHIELD3 = 3

#次の周回に移る時のパワーアップアイテム関連の動作
LOOP_POWER_CONTINUE            = 0    #全てのメインウェポンとミサイルの状態は次週にもそのまま引き継がれます
LOOP_ONE_LEVEL_DOWN            = 1    #メインウェポンが1レベルダウンします
LOOP_TWO_LEVEL_DOWN            = 2    #メインウェポンが2レベルダウンします
LOOP_THREE_LEVEL_DOWN          = 3    #メインウェポンが3レベルダウンします
LOOP_FOUR_LEVEL_DOWN           = 4    #メインウェポンが4レベルダウンします
LOOP_FIVE_LEVEL_DOWN           = 5    #メインウェポンが5レベルダウンします
LOOP_MAIN_WEAPON_TYPE_RESET    = 10   #メインウェポンのタイプのみ初期化されます 例 5WAYバルカンショット→初期バルカンショット  3WAYレーザー→通常のレーザー ウェーブカッターLV4→ウェーブカッターLV1
LOOP_MAIN_WEAPON_MISSILE_TYPE_RESET = 90   #メインウェポンとミサイルのタイプが初期化されます 例 5WAYバルカンショット→初期バルカンショット ツインミサイル4段階目→ツインミサイル1段階目
LOOP_ALL_RESET                 = 100  #メインウェポンもミサイルもゲーム開始時と同じ初期状態に戻ります

#!ステージの名称関連の定数定義################################################################
STAGE_MOUNTAIN_REGION         =  1 #ステージ1 山岳地帯          Mountain Region
STAGE_ADVANCE_BASE            =  2 #ステージ2 前線基地          Advance Base
STAGE_VOLCANIC_BELT           =  3 #ステージ3 火山地帯          Volcanic Belt
STAGE_NIGHT_SKYSCRAPER        =  4 #ステージ4 夜間超高層ビル地帯 Night Skyscraper
STAGE_AMPHIBIOUS_ASSAULT_SHIP =  5 #ステージ5 強襲揚陸艦襲撃     Amphibious Assault Ship
STAGE_DEEP_SEA_TRENCH         =  6 #ステージ6 深海海溝          Deep Sea Trench
STAGE_INTERMEDIATE_FORTRESS   =  7 #ステージ7 中間要塞          Intermediate Fortress
STAGE_ESCAPE_FORTRESS         =  8 #ステージ8 要塞脱出          Escape Fortress
SATGE_BOSS_RUSH               =  9 #ステージ9 連続強敵襲来       Boss Rush

#クロー関連の定数定義（主にトレースクロー）
TRACE_CLAW_COUNT       =  4 #トレースクローの数
TRACE_CLAW_INTERVAL    = 60 #トレースクローの間隔
TRACE_CLAW_BUFFER_SIZE = 60 #トレースクローのバッファーサイズ   1フレームは60分の1秒 60フレームで1秒分となります
CLAW_RAPID_FIRE_NUMBER =  2 #クローの最大連射数

SHIP_EXPLOSION_TIMER_LIMIT = 180 #自機が爆発した後、まだどれだけゲームが進行し続けるかのタイマー限界数
GAME_OVER_TIMER_LIMIT      = 180 #ゲームオーバーダイアログを表示した後まだどれだけゲームが進行し続けるのかのタイマー限界数

FADE_IN  = 0               #フェードインアウト用エフェクトスクリーン用の定数定義 0=in 1=out
FADE_OUT = 1

#イメージバンクの定数定義
IMG0 = 0 #イメージバンク0
IMG1 = 1 #イメージバンク1
IMG2 = 2 #イメージバンク2

#移動モードに入る定数定義 self.move_modeに入ります
MOVE_MANUAL = 0   #手動移動モード   パッドやキーボード入力によって移動
MOVE_AUTO   = 1   #自動移動モード   イベントによる自動移動モードとなり設定された位置まで自動で移動して行きます

#リプレイ機能のステータスです self.replay_statusに入ります
REPLAY_STOP   = 0 #何も作動してない状態です リプレイデータ記録無し,再生無し
REPLAY_RECORD = 1 #リプレイデータを記録中です
REPLAY_PLAY   = 2 #リプレイデータを再生中です

#パッド入力でのリプレイデータ記録に使用する定数定義
PAD_UP      =    1 #0b 0000 0001 Low byte
PAD_DOWN    =    2 #0b 0000 0010
PAD_LEFT    =    4 #0b 0000 0100
PAD_RIGHT   =    8 #0b 0000 1000
PAD_A       =   16 #0b 0001 0000
PAD_B       =   32 #0b 0010 0000
PAD_X       =   64 #0b 0100 0000
PAD_Y       =  128 #0b 1000 0000

PAD_SELECT  =    1 #0b 0000 0001 Hige byte
PAD_START   =    2 #0b 0000 0010 
PAD_LEFT_S  =    4 #0b 0000 0100 
PAD_RIGHT_S =    8 #0b 0000 1000 

#リプレイモードでの毎ステージ開始時の自機データの記録用で使用する定数
ST_SCORE                       =  0   #毎ステージごとのスコア
ST_MY_SHIELD                   =  1   #自機のシールド耐久値
ST_MY_SPEED                    =  2   #自機のスピード
ST_SELECT_SHOT_ID              =  3   #現在使用しているショットのIDナンバー
ST_SHOT_EXP                    =  4   #自機ショットの経験値
ST_SHOT_LEVEL                  =  5   #自機ショットのレベル
ST_SHOT_SPEED_MAGNIFICATION    =  6   #自機ショットのスピードに掛ける倍率
ST_SHOT_RAPID_OF_FIRE          =  7   #自機ショットの連射数
ST_MISSILE_EXP                 =  8   #自機ミサイルの経験値
ST_MISSILE_LEVEL               =  9   #自機ミサイルのレベル
ST_MISSILE_SPEED_MAGNIFICATION = 10   #自機ミサイルのスピードに掛ける倍率
ST_MISSILE_RAPID_OF_FIRE       = 11   #自機ミサイルの連射数
ST_SELECT_SUB_WEAPON_ID        = 12   #現在使用しているサブウェポンのIDナンバー
ST_CLAW_TYPE                   = 13   #クローのタイプ
ST_CLAW_NUMBER                 = 14   #クローの装備数
ST_CLAW_DIFFERENCE             = 15   #クロ―同士の角度間隔
ST_TRACE_CLAW_INDEX            = 16   #トレースクロー（オプション）時のトレース用配列のインデックス値
ST_TRACE_CLAW_DISTANCE         = 17   #トレースクロー同士の間隔
ST_FIX_CLAW_MAGNIFICATION      = 18   #フイックスクロー同士の間隔の倍率
ST_REVERSE_CLAW_SVX            = 19   #リバースクロー用の攻撃方向ベクトル(x軸)
ST_REVERSE_CLAW_SVY            = 20   #リバースクロー用の攻撃方向ベクトル(y軸)
ST_CLAW_SHOT_SPEED             = 21   #クローショットのスピード
ST_LS_SHIELD_HP                = 22   #L'sシールドの耐久力

#パーティクルの種類
PARTICLE_DOT            =  0 #パーティクルタイプ 1~2ドット描画タイプ(破壊後のエフェクト)
PARTICLE_CIRCLE         =  1 #パーティクルタイプ 円形パーティクル   (破壊後のエフェクト)
PARTICLE_LINE           =  2 #パーティクルタイプ ラインパーティクル (跳ね返りエフェクト)
PARTICLE_FIRE_SPARK     =  3 #パーティクルタイプ 大気圏突入時の火花 (火花が飛び散るエフェクト)

PARTICLE_SHOT_DEBRIS    =  4 #パーティクルタイプ 自機ショットの破片(デブリ)(障害物に当たったエフェクト)
PARTICLE_MISSILE_DEBRIS =  5 #パーティクルタイプ 自機ミサイルの破片(デブリ)(障害物に当たったエフェクト)

PARTICLE_BOSS_DEBRIS1   =  6 #パーティクルタイプ ボスの破片1(破壊後のエフェクト)かなり大きい金属プレート
PARTICLE_BOSS_DEBRIS2   =  7 #パーティクルタイプ ボスの破片2(破壊後のエフェクト)回転するブロック状な物
PARTICLE_BOSS_DEBRIS3   =  8 #パーティクルタイプ ボスの破片3(破壊後のエフェクト)ホワイト系のスパーク 
PARTICLE_BOSS_DEBRIS4   =  9 #パーティクルタイプ ボスの破片4(破壊後のエフェクト)橙色系の落下する火花
PARTICLE_BOSS_DEBRIS5   = 10 #パーティクルタイプ ボスの破片5(破壊後のエフェクト)
PARTICLE_BOSS_DEBRIS6   = 11 #パーティクルタイプ ボスの破片6(破壊後のエフェクト)

#背景オブジェクトの種類
BG_OBJ_CLOUD1,BG_OBJ_CLOUD2,BG_OBJ_CLOUD3,BG_OBJ_CLOUD4,BG_OBJ_CLOUD5      = 0,1,2,3,4     #雲小1~5
BG_OBJ_CLOUD6,BG_OBJ_CLOUD7,BG_OBJ_CLOUD8,BG_OBJ_CLOUD9,BG_OBJ_CLOUD10     = 5,6,7,8,9     #雲小6~10

BG_OBJ_CLOUD11,BG_OBJ_CLOUD12,BG_OBJ_CLOUD13,BG_OBJ_CLOUD14,BG_OBJ_CLOUD15   = 10,11,12,13,14  #雲中11~15
BG_OBJ_CLOUD16,BG_OBJ_CLOUD17,BG_OBJ_CLOUD18                                 = 15,16,17        #雲中16~18

BG_OBJ_CLOUD19,BG_OBJ_CLOUD20,BG_OBJ_CLOUD21                                 = 18,19,20        #雲大19~21

BG_OBJ_CLOUD22                                                               = 21              #雲特大22

#爆発パターンの種類
EXPLOSION_NORMAL =   0  #標準サイズ(8x8サイズ)の敵を倒したときの爆発パターン
EXPLOSION_MIDDLE =   1  #スクランブルハッチや重爆撃機系の敵を倒したときの中くらいの爆発パターン 
EXPLOSION_MY_SHIP = 10  #自機の爆発パターン

#ウィンドウのidの定数定義 windowクラスの window[i].window_idに入ります
WINDOW_ID_NO_MENU                  =  0 #ダミー用 ノーメニュー
WINDOW_ID_MAIN_MENU                =  1 #タイトル画面からのメインメニュー
WINDOW_ID_SELECT_STAGE_MENU        =  2 #ステージ選択メニュー
WINDOW_ID_SELECT_LOOP_MENU         =  3 #ループ数選択メニュー
WINDOW_ID_BOSS_MODE_MENU           =  4 #ボスモードオンオフメニュー
WINDOW_ID_HITBOX_MENU              =  5 #ヒットボックス(当たり判定)表示オンオフメニュー(ボスのみ)
WINDOW_ID_SELECT_DIFFICULTY        =  6 #難易度選択メニュー
WINDOW_ID_SELECT_REPLAY_SLOT       =  7 #どのスロットのリプレイデータをロードするのかのメニュー
WINDOW_ID_GAME_OVER_RETURN         =  8 #ゲームオーバーから戻る時のメニュー
WINDOW_ID_GAME_OVER_RETURN_NO_SAVE =  9 #ゲームオーバーから戻る時のメニュー(リプレイデータのセーブは無し)
WINDOW_ID_SELECT_FILE_SLOT         = 10 #リプレイデータをセーブするスロットを選択するメニュー
WINDOW_ID_SCORE_BOARD              = 11 #スコアボードウィンドウ
WINDOW_ID_INPUT_YOUR_NAME          = 12 #名前入力ウィンドウ
WINDOW_ID_CONFIG                   = 13 #各種設定ウィンドウ(CONFIGウィンドウ)
WINDOW_ID_CONFIG_GRAPHICS          = 14 #グラフイック設定ウィンドウ
WINDOW_ID_CONFIG_SOUND             = 15 #サウンド設定ウィンドウ
WINDOW_ID_CONFIG_CONTROL           = 16 #コントロール設定ウィンドウ
WINDOW_ID_CONFIG_SETTING           = 17 #ゲーム設定ウィンドウ
WINDOW_ID_STATUS                   = 18 #ステータスウィンドウ
WINDOW_ID_DUMMY_TEST               = 19 #ダミーテスト用ウィンドウ
WINDOW_ID_ACHIEVEMENT_LIST         = 20 #アチーブメント(功績)リストウィンドウ
WINDOW_ID_MEDAL_LIST               = 21 #メダルウィンドウリスト
WINDOW_ID_EQUIPMENT                = 22 #装備ウィンドウ
WINDOW_ID_ITEM_LIST                = 23 #アイテムリストウィンドウ

#ウィンドウのid_subの定数定義 windowクラスの window[i].window_id_subに入ります
WINDOW_ID_SUB_NORMAL_MENU            = 0 #通常の選択メニュー
WINDOW_ID_SUB_YES_NO_MENU            = 1 #「はい」「いいえ」の2択式メニュー
WINDOW_ID_SUB_ON_OFF_MENU            = 2 #「ON」「OFF」の2択式メニュー        (フラグオン時は選択されている物がハイライトされた色となります)
WINDOW_ID_SUB_SELECT_NUM_MENU        = 3 #数値を横方向の操作で増減させて決めるメニュー
WINDOW_ID_SUB_TOGGLE_MENU            = 4 #押すことでオンオフを切り替えることが出来るトグルスイッチメニュー
WINDOW_ID_SUB_FULL_4WAY_MENU         = 5 #4方向入力による自由なデザインでのメニュー
WINDOW_ID_SUB_RIGHT_LEFT_PAGE_MENU   = 6 #左右の頁送りで切り替えるメニュー(スコアボードとかで使用)
WINDOW_ID_SUB_MULTI_SELECT_MENU      = 7 #通常の選択メニューと基本は同じだがあらかじめ選択された物がハイライトされた色で表示される
WINDOW_ID_SUB_SWITCH_TEXT_MENU       = 8 #上下操作でカーソルが上下し左右でそれぞれの項目に対応したテキストが切り替わり表示されるメニュータイプ

#ウィンドウの種類の定数定義 windowクラスのwindow[i].window_typeに入ります
WINDOW_TYPE_NORMAL                   = 0 #メッセージを表示するだけのタイプ
WINDOW_TYPE_EDIT_TEXT                = 1 #メッセージを表示しさらにテキスト編集の入力待ちするタイプ
WINDOW_TYPE_SCROLL_TEXT              = 1 #カーソルキーで上下スクロールできる長文を読ませる時に使用するタイプ


#ウィンドウの下地の定数定義 windowクラスの window[i].window_bgに入ります
WINDOW_BG_TRANSLUCENT     = 0 #半透明
WINDOW_BG_BLUE_BACK       = 1 #青地
WINDOW_BG_LOW_TRANSLUCENT = 2 #ちょっと半透明

#メッセージウィンドウ関連の定数定義 windowクラスの window[i].window_statusに入ります
WINDOW_OPEN            =  0    #ウィンドウ開き進行中
WINDOW_WRITE_TITLE_BAR =  4    #ウィンドウのタイトルバー表示中
WINDOW_WRITE_MESSAGE   =  5    #メッセージの表示中
WINDOW_SELECT_YES_NO   =  8    #「はい」「いいえ」の2択表示中
WINDOW_OPEN_COMPLETED  =  9    #ウィンドウ開き完了！
WINDOW_CLOSE           = 10    #ウィンドウ閉め進行中
WINDOW_CLOSE_COMPLETED = 11    #ウィンドウ閉め完了！
WINDOW_MOVE            = 12    #ウィンドウ移動中

#ウィンドウのテキスト行間ドット数 windowクラスのbetween_lineに入ります
WINDOW_BETWEEN_LINE_7   =  7     #行間 7ドット
WINDOW_BETWEEN_LINE_8   =  8     #行間 8ドット
WINDOW_BETWEEN_LINE_9   =  9     #行間 9ドット
WINDOW_BETWEEN_LINE_10  = 10     #行間10ドット
#ウィンドウで表示されるボタンのサイズ
WINDOW_BUTTON_SIZE_1X1    = 0      #1x1キャラ分(8x8ドット)
WINDOW_BUTTON_SIZE_1TEXT  = 1      #半角文字サイズ4*6ドット
WINDOW_BUTTON_SIZE_1X2    = 2      #1x2キャラ分(8x16ドット)

#メッセージ,ボタンの表示の仕方 windowクラスのwindow[i].title_text[LIST_WINDOW_TEXT_ALIGN],またはwindow[i].item_text[j][LIST_WINDOW_TEXT_ALIGN]に入ります
BUTTON_DISP_OFF    = 0 #0=表示しない
DISP_OFF           = 0 #0=表示しない

BUTTON_DISP_ON     = 1 #1=表示する
DISP_ON            = 1 #1=表示する 

DISP_CENTER        = 2 #2=中央表示
DISP_LEFT_ALIGN    = 3 #3=左揃え
DISP_RIGHT_ALIGN   = 4 #4=右揃え

#ウィンドウテキストのリストの2次元配列のインデックスナンバーとして使用する定数定義 windowクラスのwindow[i].title_text[ここで定義した定数],またはwindow[i].item_text[j][ここで定義した定数]またはwindow[i].scroll_text[ここで定義した定数]に入ります
LIST_WINDOW_TEXT                    =  0 #ウィンドウテキスト
LIST_WINDOW_TEXT_ALIGN              =  1 #ウィンドウテキストの揃え方(アライメント)(整列の仕方)
LIST_WINDOW_TEXT_OX                 =  2 #ウィンドウテキスト表示x軸のオフセット値
LIST_WINDOW_TEXT_OY                 =  3 #ウィンドウテキスト表示y軸のオフセット値
LIST_WINDOW_TEXT_COLOR              =  4 #ウィンドウテキストの表示色

LIST_WINDOW_TEXT_FLASH              =  5 #ウィンドウテキストの点滅のしかた
LIST_WINDOW_TEXT_TYPE               =  6 #ウィンドウテキストのタイプ
LIST_WINDOW_TEXT_STATUS             =  7 #ウィンドウテキストのステータス(状態)
LIST_WINDOW_TEXT_LENGTH             =  8 #ウィンドウテキストの長さ
LIST_WINDOW_TEXT_LINEFEED_WIDTH     =  9 #ウィンドウテキストの折り返し改行幅

LIST_WINDOW_TEXT_LINEFEED_HEIGHT    = 10 #ウィンドウテキストの折り返し改行幅(縦書きモードの時)
LIST_WINDOW_TEXT_DISP_TYPE          = 11 #ウィンドウテキストの文字の表示のしかた
LIST_WINDOW_TEXT_DISP_SPEED         = 12 #ウィンドウテキストの文字の表示スピード(一文字ずつ表示する場合のみ)
LIST_WINDOW_TEXT_SCROLL_SPEED       = 13 #ウィンドウテキストの上下スクロールスピード値
LIST_WINDOW_TEXT_SLIDE_IN_WAY       = 14 #ウィンドウテキストがスライドインしてくる方向

LIST_WINDOW_TEXT_SLIDE_OUT_WAY      = 15 #ウィンドウテキストをスライドアウトさせる方向
LIST_WINDOW_TEXT_SLIDE_NOW_SPEED    = 16 #ウィンドウテキストをスライドインアウトさせる時の現在のスピード値
LIST_WINDOW_TEXT_SLIDE_START_SPEED  = 17 #ウィンドウテキストをスライドインアウトさせる時の初期スピード値
LIST_WINDOW_TEXT_SLIDE_END_SPEED    = 18 #ウィンドウテキストをスライドインアウトさせる時の最後のスピード値(目標となるスピード値ですの)
LIST_WINDOW_TEXT_SLIDE_MAG_SPEED    = 19 #ウィンドウテキストをスライドインアウトさせる時のスピード値に掛ける加速度

LIST_WINDOW_TEXT_OPE_OBJ            = 20 #ウィンドウテキストで編集対象となるオブジェクトを指示します(windowクラスのflag_list[i][対象オブジェクト]の対象オブジェクトとなります)
LIST_WINDOW_TEXT_OPE_OBJ_TYPE       = 21 #ウィンドウテキストで編集対象となるオブジェクトの種類分類
LIST_WINDOW_TEXT_OPE_OBJ_TEXT       = 22 #ウィンドウテキストで編集対象となるオブジェクトのタイトルテキスト「ON」とか「OFF」とか
LIST_WINDOW_TEXT_OPE_OBJ_TEXT_ALIGN = 23 #ウィンドウテキストで編集対象となるオブジェクトのタイトルテキストの揃え方(アライメント)(整列の仕方)アラ～イイアラ～～イイ
LIST_WINDOW_TEXT_OPE_OBJ_COMPARE    = 24 #対象オブジェクトと比較するパラメータ数値(この数値とOPE_OBJの数値を比較してTrueかFalseか判定します)

LIST_WINDOW_TEXT_OPE_OBJ_TEXT_OX    = 25 #ウィンドウテキストで編集対象となるオブジェクトのタイトルテキスト x軸のオフセット値
LIST_WINDOW_TEXT_OPE_OBJ_TEXT_OY    = 26 #ウィンドウテキストで編集対象となるオブジェクトのタイトルテキスト y軸のオフセット値
LIST_WINDOW_TEXT_OPE_OBJ_OFF_COLOR  = 27 #対象オブジェクトがFalse(OFF)になった時の文字色
LIST_WINDOW_TEXT_OPE_OBJ_ON_COLOR   = 28 #対象オブジェクトがTrue(ON)になった時の文字色
LIST_WINDOW_TEXT_OPE_OBJ_MIN_NUM    = 29 #ウィンドウテキストで編集対象となるオブジェクトの最小値(数値の場合)

LIST_WINDOW_TEXT_OPE_OBJ_MAX_NUM        = 30 #ウィンドウテキストで編集対象となるオブジェクトの最大値(数値の場合)
LIST_WINDOW_TEXT_OPE_OBJ_SWITCH_TEXT    = 31 #ウィンドウテキストで編集対象となるオブジェクトテキスト(切り替え表示タイプ「VERYEASY」「EASY」「NORMAL」「HARD」とか表示テキストがボタンまたは左右カーソルセレクトで切り替わる
LIST_WINDOW_TEXT_OPE_OBJ_MARKER_TYPE    = 32 #ウィンドウテキストで編集対象となるオブジェクトが増減できる数値とかの場合増加減出来るかどうかの矢印マーカーの種別（矢印マーカを表示するしないの判断はLIST_WINDOW_TEXT_OPE_OBJ_TYPEをみて行う,LIST_WINDOW_TEXT_OPE_OBJ_MARKER_TYPEは複数の表示パターンを持てるようにするためのリザーブ）

LIST_WINDOW_TEXT_OPE_OBJ_UP_MARKER_FLAG    = 33 #増減表示（上矢印）を表示するかのフラグ
LIST_WINDOW_TEXT_OPE_OBJ_DOWN_MARKER_FLAG  = 34 #増減表示（下矢印）を表示するかのフラグ
LIST_WINDOW_TEXT_OPE_OBJ_RIGHT_MARKER_FLAG = 35 #増減表示（右矢印）を表示するかのフラグ
LIST_WINDOW_TEXT_OPE_OBJ_LEFT_MARKER_FLAG  = 36 #増減表示（左矢印）を表示するかのフラグ

LIST_WINDOW_TEXT_OPE_OBJ_UP_MARKER_X    = 37 #対象が数値とかで増加減出来るかどうかの、上矢印の座標(x,y)
LIST_WINDOW_TEXT_OPE_OBJ_UP_MARKER_Y    = 38
LIST_WINDOW_TEXT_OPE_OBJ_DOWN_MARKER_X  = 39 #対象が数値とかで増加減出来るかどうかの、下矢印の座標(x,y)
LIST_WINDOW_TEXT_OPE_OBJ_DOWN_MARKER_Y  = 40
LIST_WINDOW_TEXT_OPE_OBJ_RIGHT_MARKER_X = 41 #対象が数値とかで増加減出来るかどうかの、右矢印の座標(x,y)
LIST_WINDOW_TEXT_OPE_OBJ_RIGHT_MARKER_Y = 42
LIST_WINDOW_TEXT_OPE_OBJ_LEFT_MARKER_X  = 43 #対象が数値とかで増加減出来るかどうかの、左矢印の座標(x,y)
LIST_WINDOW_TEXT_OPE_OBJ_LEFT_MARKER_Y  = 44

#ウィンドウフラグリストの２次元配列のインデックスナンバーとして使用する定数定義 windowクラスのwindow[i].flag_list[ここで定義した定数]に入ります
LIST_WINDOW_FLAG_DEBUG_MODE        =  0 #デバッグモードのon/offフラグ
LIST_WINDOW_FLAG_GOD_MODE          =  1 #ゴッドモードの
LIST_WINDOW_FLAG_HIT_BOX           =  2 #ヒットボックス(当たり判定)の
LIST_WINDOW_FLAG_BOSS_MODE         =  3 #ボスモード(ボス戦闘のみのモード)の
LIST_WINDOW_FLAG_START_STAGE       =  4 #開始ステージ数
LIST_WINDOW_FLAG_START_LOOP        =  5 #開始ループ数
LIST_WINDOW_FLAG_START_AGE         =  6 #開始時代数
LIST_WINDOW_FLAG_DIFFICULTY        =  7 #難易度
LIST_WINDOW_FLAG_SCREEN_MODE       =  8 #画面スクリーンモード(ウィンドウ表示、全画面表示切替)
LIST_WINDOW_FLAG_BGM_VOL           =  9 #BGMボリューム値
LIST_WINDOW_FLAG_SE_VOL            = 10 #SE(サウンドエフェクト)ボリューム値
LIST_WINDOW_FLAG_CTRL_TYPE         = 11 #パッド入力パターン
LIST_WINDOW_FLAG_LANGUAGE          = 12 #選択言語
'''
LIST_WINDOW_FLAG_                  = 13 #
LIST_WINDOW_FLAG_                  = 14 #
LIST_WINDOW_FLAG_                  = 15 #
LIST_WINDOW_FLAG_                  = 16 #
LIST_WINDOW_FLAG_                  = 17 #
LIST_WINDOW_FLAG_                  = 18 #
LIST_WINDOW_FLAG_                  = 19 #
LIST_WINDOW_FLAG_                  = 20 #
LIST_WINDOW_FLAG_                  = 21 #
LIST_WINDOW_FLAG_                  = 22 #
LIST_WINDOW_FLAG_                  = 23 #
LIST_WINDOW_FLAG_                  = 24 #
'''
#ウィンドウグラフイック群リストの２次元配列のインデックスナンバーとして使用する定数定義 windowクラスのwindow[i].graph_list[ここで定義した定数]に入ります
LIST_WINDOW_GRAPH_OX               =  0 #グラフイックキャラを表示する座標(ox,oy)ウィンドウ表示座標からのオフセット値となります
LIST_WINDOW_GRAPH_OY               =  1 #
LIST_WINDOW_GRAPH_IMGB             =  2 #表示するグラフイックキャラが入っているイメージバンクの数値
LIST_WINDOW_GRAPH_U                =  3 #表示するグラフイックキャラが入っている場所を示した座標(u,v)
LIST_WINDOW_GRAPH_V                =  4 #
LIST_WINDOW_GRAPH_W                =  5 #表示するグラフイックキャラの縦幅、横幅(width,height)マイナス値の場合は反転します
LIST_WINDOW_GRAPH_H                =  6 #
LIST_WINDOW_GRAPH_COLKEY           =  7 #透明色の指定
LIST_WINDOW_GRAPH_ANIME_FRAME_NUM  =  8 #アニメーションパターンの枚数(1の場合はアニメーション無し)
LIST_WINDOW_GRAPH_ANIME_SPEED      =  9 #アニメーションのスピード(1が速く数値が増えるにつれて遅くなる4位が良いかも？)
LIST_WINDOW_GRAPH_ITEM_X           = 10 #このグラフイックキャラはアイテムとしてどこに位置するのかを指定する(x座標)
LIST_WINDOW_GRAPH_ITEM_Y           = 11 #このグラフイックキャラはアイテムとしてどこに位置するのかを指定する(y座標)(0,0)だったらdecision_item_x=0,decision_item_y=0
                                        #                                                                   (2,1)だったらdecision_item_x=2,decision_item_y=1って事になります

#ウィンドウスクリプトリストのリストの2次元配列のインデックスナンバーとして使用する定数定義 windowクラスのwindow[i].script[ここで定義した定数]に入ります(一つだけだよ=1個だけ)(リスト表記=複数の数値が入ります)
LIST_WINDOW_SCRIPT_TEXT            =  0 #スクリプト文本文が入ります(文字列型)
LIST_WINDOW_SCRIPT_OX              =  1 #スクリプト内のテキストの表示オフセット座標(OX,OY)
LIST_WINDOW_SCRIPT_OY              =  2 #
LIST_WINDOW_SCRIPT_DISP_TYPE       =  3 #スクリプトテキストの表示タイプ
LIST_WINDOW_SCRIPT_DISP_SPEED      =  4 #スクリプトテキストの表示スピード
LIST_WINDOW_SCRIPT_TEXT_WIDTH      =  5 #現在のスクリプトテキストの最大表示幅(はみ出したとき折り返すかどうかは〇〇の値で判断する)
LIST_WINDOW_SCRIPT_TEXT_HEIGHT     =  6 #現在のスクリプトテキストの最大表示行数
LIST_WINDOW_SCRIPT_ALIGN           =  7 #現在のスクリプトテキストの表示揃えの仕方
LIST_WINDOW_SCRIPT_COLOR           =  8 #現在のスクリプトテキストの表示色
LIST_WINDOW_SCRIPT_SCROLL_TYPE     =  9 #現在のスクリプトテキストのスクロールタイプ
LIST_WINDOW_SCRIPT_SCROLL_SPEED    = 10 #現在のスクリプトテキストのスクロールスピード
LIST_WINDOW_SCRIPT_WAIT            = 11 #スクリプトテキスト用のウェイトタイマー wait**
LIST_WINDOW_SCRIPT_COUNT           = 12 #スクリプトテキスト用のカウンター      count**
LIST_WINDOW_SCRIPT_FLAG            = 13 #スクリプトテキスト用のフラグ          FLAG** 
LIST_WINDOW_SCRIPT_VAR             = 14 #スクリプトテキスト用の変数リスト群(整数)[["@変数名",整数],[@EGG,123],[@HUM,456667],.........[@PULIN,467890]]
LIST_WINDOW_SCRIPT_STR             = 15 #スクリプトテキスト用の変数リスト群(文字列型)[["$変数名","文字列"],["$STR1","AAA"],["$STR_A3","BBB"],["$STR_3456","CDE"]....["$STR_3414","ZZzzz"]]
LIST_WINDOW_SCRIPT_LABEL           = 16 #スクリプトテキスト用のラベル定義リスト群(文字列型)[["#ラベル名",プログラムカウント数],["#HYOUZI_KAISI",34],.......["#HOGEHOGE",46]]
LIST_WINDOW_SCRIPT_PROGRAM_COUNTER = 17 #スクリプトテキスト用の処理用実行位置カウンター(一つだけだよ)プログラムカウンターPC
LIST_WINDOW_SCRIPT_STACK_MEMORY    = 18 #スクリプトテキスト用スタックメモリー(リスト表記)スタックメモリエリア
LIST_WINDOW_SCRIPT_STACK_POINTER   = 19 #スクリプトテキスト用スタックポインタ(一つだけだよ)SP
LIST_WINDOW_SCRIPT_RETURN_MEMORY   = 20 #スクリプトテキスト用リターンメモリー(リスト表記)RETURN文で戻るべきプログラムカウンターがスタックされる
LIST_WINDOW_SCRIPT_RETURN_POINTER  = 21 #スクリプトテキスト用リターンポインタ(一つだけだよ)RP
LIST_WINDOW_SCRIPT_FOR_START_NUM   = 22 #スクリプトテキスト用FOR文での開始値(リスト表記)
LIST_WINDOW_SCRIPT_FOR_END_NUM     = 23 #スクリプトテキスト用FOR文での終了値(リスト表記)
LIST_WINDOW_SCRIPT_FOR_STEP_NUM    = 24 #スクリプトテキスト用FOR文での増分値(リスト表記) 


#メッセージを点滅させるかのフラグ windowクラスのwindow[i].item_text[j][LIST_WINDOW_TEXT_FLASH]に入ります
MES_NO_FLASH         = 0 #点滅しない
MES_BLINKING_FLASH   = 1 #点滅
MES_RED_FLASH        = 2 #赤い点滅
MES_GREEN_FLASH      = 3 #緑で点滅
MES_YELLOW_FLASH     = 4 #黄色で点滅
MES_MONOCHROME_FLASH = 5 #白黒で点滅
MES_RAINBOW_FLASH    = 6 #虹色に点滅

#ウィンドウテキストで編集対象となるオブジェクトの種類分類ですwindowクラスのwindow[i].item_text[j][LIST_WINDOW_TEXT_OPE_OBJ_TYPE]に入ります
OPE_OBJ_TYPE_NONE    = 0 #操作テキストオブジェクトの指定は無し
OPE_OBJ_TYPE_ON_OFF  = 1 #操作テキストオブジェクトは「ON」「OFF」の二つから選ぶシンプルなタイプです
OPE_OBJ_TYPE_NUM     = 2 #操作テキストオブジェクトは数値を増減させて選択するタイプ
OPE_OBJ_MULTI_ITEM   = 3 #操作テキストオブジェクトは多項目から選択するタイプ

#セレクトカーソルのタイプ
CURSOR_TYPE_NO_DISP   = 0 #セレクトカーソルは表示しない
CURSOR_TYPE_NORMAL    = 1 #通常の横向きのクロー回転アニメーションカーソル
CURSOR_TYPE_UNDER_BAR = 2 #アンダーバータイプ
CURSOR_TYPE_BOX_FLASH = 3 #点滅囲み矩形タイプ

#セレクトカーソルの移動音 pyxelのsndの番号を使って定義してね～～♪
CURSOR_MOVE_SE_NORMAL   = 16
CURSOR_MOVE_SE_TYPE1    = 1
CURSOR_MOVE_SE_TYPE2    = 2
CURSOR_MOVE_SE_TYPE3    = 3
CURSOR_MOVE_SE_TYPE4    = 4

CURSOR_PUSH_SE_NORMAL   = 19
CURSOR_PUSH_SE_TYPE1    = 1
CURSOR_PUSH_SE_TYPE2    = 2
CURSOR_PUSH_SE_TYPE3    = 3
CURSOR_PUSH_SE_TYPE4    = 4

CURSOR_OK_SE_NORMAL     = 17
CURSOR_OK_SE_TYPE1      = 1
CURSOR_OK_SE_TYPE2      = 2
CURSOR_OK_SE_TYPE3      = 3
CURSOR_OK_SE_TYPE4      = 4

CURSOR_CANCEL_SE_NORMAL   = 18
CURSOR_CANCEL_SE_TYPE1    = 1
CURSOR_CANCEL_SE_TYPE2    = 2
CURSOR_CANCEL_SE_TYPE3    = 3
CURSOR_CANCEL_SE_TYPE4    = 4

CURSOR_BOUNCE_SE_NORMAL     = 20
CURSOR_BOUNCE_SE_TYPE1      = 1
CURSOR_BOUNCE_SE_TYPE2      = 2
CURSOR_BOUNCE_SE_TYPE3      = 3
CURSOR_BOUNCE_SE_TYPE4      = 4

#カーソルが現在指し示しているアイテムの説明文を表示するかどうかのフラグ
COMMENT_FLAG_OFF            = 0 #表示しない
COMMENT_FLAG_ON             = 1 #表示する

#セレクトカーソルの動き方
CURSOR_MOVE_UD               =  0 #セレクトカーソルの動きは上下のみです UD=Up Down
CURSOR_MOVE_UD_SLIDER        =  1 #セレクトカーソルは上下に動かすことができ、左右の入力でスライダーを動かせます
CURSOR_MOVE_UD_SLIDER_BUTTON =  2 #セレクトカーソルは上下に動かすことができ、左右の入力でスライダーを動かせます ON/OFF切り替えの項目ではボタンを押すことでも切り替えができます
CURSOR_MOVE_LR               =  3 #セレクトカーソルの動きは左右のみです LR=Left Right
CURSOR_MOVE_LR_SLIDER        =  4 #セレクトカーソルは左右に動かすことができ、上下の入力でスライダーを動かせます
CURSOR_MOVE_LR_SLIDER_BUTTON =  5 #セレクトカーソルは左右に動かすことができ、上下の入力でスライダーを動かせます ON/OFF切り替えの項目ではボタンを押すことでも切り替えができます
CURSOR_MOVE_4WAY             =  6 #上下左右4方向に動かせます
CURSOR_MOVE_4WAY_BUTTON      =  7 #上下左右4方向に動かせます(ボタンを押すと現在のカーソル位置のアイテムがアクティブとなります)
CURSOR_MOVE_8WAY             =  8 #斜め移動も含んだ8方向に動かせます
CURSOR_MOVE_8WAY_BUTTON      =  9 #斜め移動も含んだ8方向に動かせます(ボタンを押すと現在のカーソル位置のアイテムがアクティブとなります)
CURSOR_MOVE_SHOW_PAGE        = 10 #セレクトカーソルは表示せずLRキーもしくはLショルダーRショルダーで左右に頁をめくる動作です

#カーソルの移動量
STEP3,STEP4,STEP5,STEP6,STEP7,STEP8,STEP9,STEP10 = 3,4,5,6,7,8,9,10

#メニューのレイヤー数定数定義
MENU_LAYER0                  = 0 #レイヤー数0でメニュー階層は0
MENU_LAYER1                  = 1 #レイヤー数1でメニュー階層は1
MENU_LAYER2                  = 2 #レイヤー数2でメニュー階層は2

#メニューで選ばれたアイテムの定数定義
UNSELECTED                   = -1  #まだ未選択なので-1

#火花エフェクトの表示の仕方(大気圏突入シーンなどのエフェクトで使用)
SPARK_OFF = 0              #火花表示なし
SPARK_ON  = 1              #火花表示あり

#パワーアップアイテム類のtype定数の定義 obtain_itemクラスのitem_typeに代入されます
ITEM_SHOT_POWER_UP     = 1      #ショットアイテム
ITEM_MISSILE_POWER_UP  = 2      #ミサイルアイテム
ITEM_SHIELD_POWER_UP   = 3      #シールドアイテム

ITEM_CLAW_POWER_UP     = 4      #クローアイテム
ITEM_TRIANGLE_POWER_UP = 5      #トライアングルアイテム（ショット、ミサイル、シールド）

ITEM_TAIL_SHOT_POWER_UP        = 10    #テイルショットアイテム
ITEM_PENETRATE_ROCKET_POWER_UP = 11    #ペネトレートロケットアイテム
ITEM_SEARCH_LASER_POWER_UP     = 12    #サーチレーザーアイテム
ITEM_HOMING_MISSILE_POWER_UP   = 13    #ホーミングミサイルアイテム
ITEM_SHOCK_BUMPER_POWER_UP     = 14    #ショックバンパーアイテム 

#!ステージのイベントリストで使う定数の定義
EVENT_ENEMY              = 0  #敵出現
EVENT_ADD_APPEAR_ENEMY   = 1  #敵出現（早回しによる敵の追加出現）
EVENT_FAST_FORWARD_NUM   = 2  #早回しに関する編隊群のパラメーターを設定するイベント

EVENT_SCROLL                      = 60 #スクロール制御
EVENT_DISPLAY_STAR                = 61 #星のスクロールのon/off
EVENT_CHANGE_BG_CLS_COLOR         = 62 #背景でまず最初に塗りつぶす色を指定する(初期状態は黒で塗り潰してます) CLSカラーの指定
EVENT_CHANGE_BG_TRANSPARENT_COLOR = 63 #背景マップを敷き詰める時の透明色を指定する(初期状態は黒)        TRANSPARENTカラーの指定
EVENT_CLOUD                       = 64 #背景雲の表示設定
EVENT_RASTER_SCROLL               = 65 #ラスタースクロールの制御
EVENT_BG_SCREEN_ON_OFF            = 66 #各BGスクリーンの表示のオンオフ
EVENT_ENTRY_SPARK_ON_OFF          = 67 #大気圏突入の火花エフェクト表示のオンオフ

EVENT_DISPLAY_CAUTION    = 70 #CAUTION.注意表示
EVENT_COMMANDER_MESSSAGE = 71 #司令からの通信メッセージ

EVENT_MIDDLE_BOSS   = 80 #中ボス出現
EVENT_WARNING       = 90 #WARNING.警告表示
EVENT_BOSS          = 100#ボスキャラ出現

#イベントリスト・スクロール制御関連の定数定義
SCROLL_NUM_SET               = 0  #スクロール関連のパラメーター設定
SCROLL_START                 = 1  #スクロール開始
SCROLL_STOP                  = 2  #スクロールストップ
SCROLL_SPEED_CHANGE          = 3  #スクロールスピードチェンジ
SCROLL_SPEED_CHANGE_VERTICAL = 4  #縦スクロールスピードチェンジ

SCROLL_SPEED            = 5  #スクロールスピード直接指定
SCROLL_REVERSE          = 6  #逆スクロール開始
SCROLL_UP               = 7  #上方向にスクロール開始
SCROLL_DOWN             = 8  #下方向にスクロール開始

#イベントリスト・雲のスクロール制御関連の定数定義
CLOUD_NUM_SET          = 0  #雲のパラメータ設定
CLOUD_START            = 1  #雲を流すのを開始する
CLOUD_STOP             = 2  #雲を流すのを停止する

#イベントリスト BGスクロールオンオフの制御関連の定数定義
BG_BACK   = 0 #BGスクリーン奥
BG_MIDDLE = 1 #BGスクリーン真ん中
BG_FRONT  = 2 #BGスクリーン手前

#背景スクロールの種類
SCROLL_TYPE_TRIPLE_SCROLL_AND_STAR     = 0 #横3重スクロール+星スクロール
SCROLL_TYPE_8FREEWAY_SCROLL_AND_RASTER = 1 #8方向自由スクロール+ラスタースクロール

#背景の星のスクロールの有無
STAR_SCROLL_ON      = 1 #星スクロールあり
STAR_SCROLL_OFF     = 0 #        なし

#背景ラスタスクロールの有無
RASTER_SCROLL_ON    = 1 #ラスタースクロールあり
RASTER_SCROLL_OFF   = 0 #           なし

#背景ラスタスクロールの種類
RASTER_NORMAL      = 0 #奥と手前のラインごとのスクロールスピードの差で奥行き感を出すタイプ (流れるスピードはスクロールスピードに依存します)
RASTER_WAVE        = 1 #x軸にたいして波打つラスタースクロールタイプ(x座標オフセット値を加減算して波打つ感じを表現します)

#!敵キャラの名前(タイプナンバー)定数定義####################################
CIR_COIN           =  1  #無人編隊戦闘機 サーコイン（サークルコイン）
SAISEE_RO          =  2  #回転戦闘機サイシーロ(サインカーブを描く敵)
HOUDA_UNDER        =  3  #固定砲台ホウダ 下
HOUDA_UPPER        =  4  #固定砲台ホウダ 上
HOPPER_CHAN2       =  5  #はねるホッパーチャンmk2
MIST_M54           =  6  #謎の回転飛翔体M54
TWIN_ARROW_SIN     =  7  #真！(SIN)ツインアロー
TWIN_ARROW         =  8  #自機を追尾してくるツインアロー
ROLBOARD           =  9  #ロルボードＹ軸を合わせた後突っ込んで来る怖い
KURANBURU_UNDER    = 10  #クランブルアンダー(スクランブルハッチ)
KURANBURU_UPPER    = 11  #クランブルアッパー(スクランブルハッチ)
RAY_BLASTER        = 12  #レイブラスター 直進して画面前方のどこかで停止→レーザービーム射出→急いで後退するレーザー系
GREEN_LANCER       = 13  #3way弾を出してくるグリーンランサー・翠の硬い奴(ミサイルパワーアップアイテムを持っている！)
TEMI               = 14  #テミー(アイテムキャリアー)
MUU_ROBO           = 15  #ムーロボ 地面を左右に動きながらチョット進んできて弾を撃つ移動砲台
CLAMPARION         = 16  #2機一体で挟みこみ攻撃をしてくるクランパリオン
ROLL_BLITZ         = 17  #ロールブリッツ 画面内のあらかじめ決められた場所へスプライン曲線で移動,そこについたら狙い撃ち弾を出して画面外へ高速離脱
VOLDAR             = 18  #ボルダー 硬めの弾バラマキ重爆撃機
ROLL_BLITZ_POINTER = 19  #ロールブリッツポインター(最大5定点を滑らかに通過していくロールブリッツ)

#敵キャラの大きさの定数定義(この定数を見て敵を破壊した後に育成する爆発パターンの種類を決定しています)
E_SIZE_NORMAL         = 4  #敵サイズノーマル（8ドット）四方の当たり判定
E_SIZE_MIDDLE22       = 6  #敵サイズ2x2チップタイプ  中型16ドットx16ドットの当たり判定
E_SIZE_MIDDLE32       = 8  #敵サイズ3x2チップタイプ  中型24ドットx16ドットの当たり判定
E_SIZE_MIDDLE32_Y_REV = 9  #敵サイズ3x2チップタイプ  中型24ドットx16ドットの当たり判定(上下反転版)(天井に固定されてるハッチとかです)
E_SIZE_HI_MIDDLE53    =10  #敵サイズ5x3チップタイプ  準中型40ドットx24ドットの当たり判定（重爆撃機とか)
#敵キャラのIDナンバー定数定義
ID00,ID01,ID02,ID03,ID04,ID05,ID06,ID07,ID08,ID09,ID10 = 0,1,2,3,4,5,6,7,8,9,10
#敵キャラのステータス(状態)
ENEMY_STATUS_NORMAL    = 0 #通常 破壊時はscore_normalを加算
ENEMY_STATUS_ATTACK    = 1 #攻撃 破壊時はscore_attackを加算
ENEMY_STATUS_ESCAPE    = 2 #撤退 破壊時はscore_escapeを加算
ENEMY_STATUS_AWAITING  = 3 #待機 破壊時はscore_awaitingを加算
ENEMY_STATUS_DEFENSE   = 4 #防御 破壊時はscore_defenseを加算
ENEMY_STATUS_BERSERK   = 5 #怒り 破壊時はscore_berserkを加算

ENEMY_STATUS_MOVE_COORDINATE_INIT  = 10 #移動用座標初期化
ENEMY_STATUS_MOVE_BEZIER_CURVE     = 11 #ベジェ曲線で移動

#敵の攻撃方法(enemyクラスのattack_methodに入る)の定数定義
ENEMY_ATTCK_ANY                = 0  #任意攻撃(移動ルートで攻撃方法が変わるのではなく体力や自機の位置などによって攻撃方法が変化します)
ENEMY_ATTACK_NO_FIRE           = 1  #なにも攻撃しないよ
ENEMY_ATTACK_AIM_BULLET        = 2  #狙い撃ち弾
ENEMY_ATTACK_FRONT_5WAY        = 3  #前方に5way弾を撃ってきます
ENEMY_ATTACK_FRONT_GREEN_LASER = 4  #前方に細いグリーンレーザーを撃ってきます
#ヒットポイント(耐久力)の定数定義
HP00,HP01,HP02,HP03,HP04,HP05,HP06,HP07,HP08,HP09 =  0, 1, 2, 3, 4, 5, 6, 7, 8, 9
HP10,HP11,HP12,HP13,HP14,HP15,HP16,HP17,HP18,HP19 = 10,11,12,13,14,15,16,17,18,19
HP20,HP21,HP22,HP23,HP24,HP25,HP26,HP27,HP28,HP29 = 20,21,22,23,24,25,26,27,28,29
HP30,HP31,HP32,HP33,HP34,HP35,HP36,HP37,HP38,HP39 = 30,31,32,33,34,35,36,37,38,39
HP40,HP41,HP42,HP43,HP44,HP45,HP46,HP47,HP48,HP49 = 40,41,42,43,44,45,46,47,48,49
HP50,HP51,HP52,HP53,HP54,HP55,HP56,HP57,HP58,HP59 = 50,51,52,53,54,55,56,57,58,59
#ShotPower(ショットパワー)攻撃力の定数定義
SP00,SP01,SP02,SP03,SP04,SP05,SP06,SP07,SP08,SP09 =  0, 1, 2, 3, 4, 5, 6, 7, 8, 9
SP10,SP11,SP12,SP13,SP14,SP15,SP16,SP17,SP18,SP19 = 10,11,12,13,14,15,16,17,18,19
SP20,SP21,SP22,SP23,SP24,SP25,SP26,SP27,SP28,SP29 = 20,21,22,23,24,25,26,27,28,29
SP30,SP31,SP32,SP33,SP34,SP35,SP36,SP37,SP38,SP39 = 30,31,32,33,34,35,36,37,38,39
SP40,SP41,SP42,SP43,SP44,SP45,SP46,SP47,SP48,SP49 = 40,41,42,43,44,45,46,47,48,49
SP50,SP51,SP52,SP53,SP54,SP55,SP56,SP57,SP58,SP59 = 50,51,52,53,54,55,56,57,58,59
#得点の定数定義
PT01,PT02,PT03,PT04,PT05,PT06,PT07,PT08,PT09,PT10 =  1, 2, 3, 4, 5, 6, 7, 8, 9,10
PT11,PT12,PT13,PT14,PT15,PT16,PT17,PT18,PT19,PT20 = 11,12,13,14,15,16,17,18,19,20
PT21,PT22,PT23,PT24,PT25,PT26,PT27,PT28,PT29,PT30 = 21,22,23,24,25,26,27,28,29,30
PT31,PT32,PT33,PT34,PT35,PT36,PT37,PT38,PT39,PT40 = 31,32,33,34,35,36,37,38,39,40
PT41,PT42,PT43,PT44,PT45,PT46,PT47,PT48,PT49,PT50 = 41,42,43,44,45,46,47,48,49,50

PT1000 = 1000
#レベルの定数定義
LV00,LV01,LV02,LV03,LV04,LV05,LV06,LV07,LV08,LV09,LV10 = 0,1,2,3,4,5,6,7,8,9,10
#サイズ(大きさ)の定数定義 おもに画像表示用、当たり判定用としてwidthやheightに入ります
SIZE_1, SIZE_2, SIZE_3, SIZE_4, SIZE_5  =  1, 2, 3, 4, 5
SIZE_6, SIZE_7, SIZE_8, SIZE_9, SIZE_10 =  6, 7, 8, 9,10
SIZE_11,SIZE_12,SIZE_13,SIZE_14,SIZE_15 = 11,12,13,14,15
SIZE_16,SIZE_17,SIZE_18,SIZE_19,SIZE_20 = 16,17,18,19,20
SIZE_21,SIZE_22,SIZE_23,SIZE_24,SIZE_25 = 21,22,23,24,25
SIZE_26,SIZE_27,SIZE_28,SIZE_29,SIZE_30 = 26,27,28,29,30
SIZE_31,SIZE_32,SIZE_33,SIZE_34,SIZE_35 = 31,32,33,34,35
SIZE_36,SIZE_37,SIZE_38,SIZE_39,SIZE_40 = 36,37,38,39,40
SIZE_41,SIZE_42,SIZE_43,SIZE_44,SIZE_45 = 41,42,43,44,45
SIZE_46,SIZE_47,SIZE_48,SIZE_49,SIZE_50 = 46,47,48,49,50

#空中物か地上物かの判定用定数定義 enemyクラスのfloating_flagに入ります
AERIAL_OBJ = 0 #空中物(飛行物体)
GROUND_OBJ = 1 #地上物
MOVING_OBJ = 2 #地上を移動する物体(装甲車とか)

#!敵弾のタイプ定数定義
ENEMY_SHOT_NORMAL            =  0 #通常弾
ENEMY_SHOT_SIN               =  1 #サインカーブ弾
ENEMY_SHOT_COS               =  2 #コサインカーブ弾
ENEMY_SHOT_LASER             =  3 #レーザービーム
ENEMY_SHOT_GREEN_LASER       =  4 #ボスのグリーンレーザー
ENEMY_SHOT_RED_LASER         =  5 #ボスのレッドレーザー
ENEMY_SHOT_YELLOW_LASER      =  6 #ボスのイエローレーザー
ENEMY_SHOT_BLUE_LASER        =  7 #ボスのブルーレーザー
ENEMY_SHOT_RAINBOW_LASER     =  8 #ボスのレインボーレーザー
ENEMY_SHOT_HOMING_LASER      =  9 #ホーミングレーザー(レイフォースみたいなの)
ENEMY_SHOT_HOMING_LASER_TAIL = 10 #ホーミングレーザーの尻尾
ENEMY_SHOT_LOCKON_LASER      = 11 #ロックオンレーザー(レイフォースみたいなの)
ENEMY_SHOT_LOCKON_LASER_TAIL = 12 #ロックオンレーザーの尻尾
ENEMY_SHOT_SEARCH_LASER      = 13 #サーチレーザー(イメージファイトみたいなの)
ENEMY_SHOT_SEARCH_LASER_TAIL = 14 #サーチレーザーの尻尾
ENEMY_SHOT_WAVE              = 15 #ウェーブカッター(ダライアスみたいなの)
ENEMY_SHOT_RIPPLW_LASER      = 16 #リップルレーザー(グラディウスⅡみたいなの)
ENEMY_SHOT_WAINDER_LASER     = 17 #ワインダーレーザー(グラディウスみたいなの)
ENEMY_SHOT_CIRCLE_LASER      = 18 #サークルレーザー(イメージファイトみたいなの)
ENEMY_SHOT_2TURN_LASER       = 19 #2回屈折サーチレーザー(ダライアスバーストみたいなの)
ENEMY_SHOT_BOUND_LASER       = 20 #反射レーザー(R-TYPEみたいなの)
ENEMY_SHOT_DROP_BULLET       = 21 #落下弾
ENEMY_SHOT_CIRCLE_BULLET     = 22 #回転弾
ENEMY_SHOT_SPLIT_BULLET      = 21 #分裂弾
ENEMY_SHOT_HOMING_BULLET     = 23 #誘導弾
ENEMY_SHOT_UP_LASER          = 24 #アップレーザー
ENEMY_SHOT_DOWN_LASER        = 25 #ダウンレーザー
ENEMY_SHOT_SPREAD_BOMB       = 26 #スプレッドボム
ENEMY_SHOT_VECTOR_LASER      = 27 #ベクトルレーザー(グラ２みたいなの)
ENEMY_SHOT_GREEN_CUTTER      = 28 #「ブリザーディア」が尾翼部から射出するグリーンカッター

#!分裂弾の種類の定数定義
ENEMY_SHOT_DIVISION_3WAY    = 1 #3way分裂弾
ENEMY_SHOT_DIVISION_5WAY    = 2 #5way分裂弾
ENEMY_SHOT_DIVISION_7WAY    = 3 #7way分裂弾
ENEMY_SHOT_DIVISION_9WAY    = 4 #9way分裂弾

#育成する打ち返し弾の種類 Explosionクラスのreturn_bullet_typeに入る,難易度リスト(game_difficulty_list)でも使用してます
RETURN_BULLET_NONE      = 0 #撃ち返ししない
RETURN_BULLET_AIM       = 1 #自機狙い弾を1発撃ち返す
RETURN_BULLET_DELAY_AIM = 2 #自機狙い撃ち返し＆遅れて更に自機狙い弾を撃ち返す 2発
RETURN_BULLET_3WAY      = 3 #自機狙いの3way弾を撃ち返してくる


#敵弾クラスで使用する定数定義 主にcollision_typeやwidth,heightに入る
ESHOT_COL_MIN88 = 0 #最小の正方形8x8ドットでの当たり判定タイプ    collision_typeに入る
ESHOT_COL_BOX   = 1 #長方形での当たり判定タイプ                  collision_typeに入る 判定はwidth,heightを見て行います

ESHOT_SIZE1  =  1 #敵ショットのサイズ  1ドット width,heightに入ります
ESHOT_SIZE2  =  2 #敵ショットのサイズ  2ドット
ESHOT_SIZE3  =  3 #敵ショットのサイズ  3ドット
ESHOT_SIZE4  =  4 #敵ショットのサイズ  4ドット
ESHOT_SIZE5  =  5 #敵ショットのサイズ  5ドット
ESHOT_SIZE6  =  6 #敵ショットのサイズ  6ドット
ESHOT_SIZE7  =  7 #敵ショットのサイズ  7ドット
ESHOT_SIZE8  =  8 #敵ショットのサイズ  8ドット
ESHOT_SIZE9  =  9 #敵ショットのサイズ  9ドット
ESHOT_SIZE10 = 10 #敵ショットのサイズ 10ドット
ESHOT_SIZE11 = 11 #敵ショットのサイズ 11ドット
ESHOT_SIZE12 = 12 #敵ショットのサイズ 12ドット
ESHOT_SIZE13 = 13 #敵ショットのサイズ 13ドット
ESHOT_SIZE14 = 14 #敵ショットのサイズ 14ドット
ESHOT_SIZE15 = 15 #敵ショットのサイズ 15ドット
ESHOT_SIZE16 = 16 #敵ショットのサイズ 16ドット 

#敵や爆発関連の表示用のプライオリティレベルの定数定義
PRIORITY_SEND_TO_BACK  = 0  #最背面(スクロールしない背景が多いです)
PRIORITY_BACK          = 1  #背面
PRIORITY_MIDDLE        = 2  #中面
PRIORITY_BOSS_BACK     = 3  #ボスキャラの真後ろ
PRIORITY_BOSS          = 4  #ボスキャラと同面
PRIORITY_BOSS_FRONT    = 5  #ボスキャラの直ぐ手前
PRIORITY_FRONT_SCROLL  = 6  #前面スクロールのすぐ手前
PRIORITY_FRONT         = 7  #前面
PRIORITY_MORE_FRONT    = 8  #さらに前面
PRIORITY_TOP           = 9  #最前面(すべてにおいて最後の描画されるため最前面となる！)

#ボスキャラのboss_type定数定義
BOSS_BREEZARDIA        = 0 #MOUNTAIN_REGIONのボス「ブリザーディア」
BOSS_FATTY_VALGUARD    = 1 #ADVANCED_BASEのボス  「ファッティバルガード」


#敵キャラが持っているアイテム類のID enemyクラスのitemに代入されます
E_NO_POW      = 0           #敵は何もパワーアップアイテムを持っていないです・・・涙
E_SHOT_POW    = 1           #敵が持っているショットアイテム定数定義
E_MISSILE_POW = 2           #敵が持っているミサイルアイテム定数定義
E_SHIELD_POW  = 3           #敵が持っているシールドアイテム定数定義

E_CLAW_POW        = 4        #敵が持っているクローアイテム定数定義

E_TRIANGLE_POW    = 5        #敵が持っている正三角形アイテム（ショット、ミサイル、シールド）アイテム定数定義

E_DESTRUCTION_POW = 6        #敵が持っている破壊アイテム定数定義（ザコ敵を殲滅させるアイテム）
E_SCORE_POW       = 7        #敵が持っている得点アップアイテムの定数定義
E_INVINCIBLE_POW  = 8        #敵が持っている無敵アイテムの定数定義

E_TAIL_SHOT_POW        = 10     #敵が持っているテイルショットアイテム定数定義
E_PENETRATE_ROCKET_POW = 11     #敵が持っているペネトレートロケットアイテム定数定義
E_SEARCH_LASER_POW     = 12     #敵が持っているサーチレーザーアイテム定数定義
E_HOMING_MISSILE_POW   = 13     #敵が持っているホーミングミサイルアイテム定数定義
E_SHOCK_BUMPER_POW     = 14     #敵が持っているショックバンパーアイテム定数定義 

#!bossクラスのstatusに入る定数定義   (状態遷移フラグとして使用します)
BOSS_STATUS_MOVE_COORDINATE_INIT  =  0  #ボス用のステータス定数定義 移動用座標初期化
BOSS_STATUS_MOVE_BEZIER_CURVE     = 10  #ボス用のステータス定数定義 ベジェ曲線で移動
BOSS_STATUS_MOVE_LEMNISCATE_CURVE = 11  #ボス用のステータス定数定義 レムニスケート曲線で移動

BOSS_STATUS_EXPLOSION_START    = 80  #ボス撃破！爆発開始！
BOSS_STATUS_EXPLOSION          = 81  #ボス爆発中！
BOSS_STATUS_BLAST_SPLIT_START  = 82  #ボス爆破分裂開始
BOSS_STATUS_BLAST_SPLIT        = 83  #ボス爆破分裂中
BOSS_STATUS_DISAPPEARANCE      = 89  #ボス消滅・・・・・

#bossクラスのattack_methodに入る定数定義 (ボスの攻撃方法)
BOSS_ATTACK_NO_FIRE               = 0 #なにも攻撃しないよ
BOSS_ATTACK_FRONT_5WAY            = 1 #前方に5way弾を撃ってきます
BOSS_ATTACK_RIGHT_GREEN_LASER     = 2 #後方に細いグリーンレーザーを撃ってきます
BOSS_ATTACK_FRONT_5WAY_AIM_BULLET = 3 #前方5way+狙い撃ち弾
BOSS_ATTACK_FRONT_5WAY_HOMING     = 4 #前方5way+ホーミング弾

BOSS_HP_BAR_DISPLAY_TIME = 32         #ボスの耐久力バーを表示する時間(弾が当たるたびにこの数値がカウンターに入る)

#bossクラスのweapon_statusに入る定数定義(ボスの持つ武器の状態)
WEAPON_READY          = 0    #何もしていない準備万端な状態
WEAPON_ROCK_ON        = 1    #目標を定めた状態（予兆エフェクトを表示)
WEAPON_FIRE           = 2    #武器発射中


