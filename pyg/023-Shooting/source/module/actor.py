

class Ship:

    #自機の移動          キーボードとゲームパッド、または移動座標先を指定しての「自動移動モード」による自機の移動処理を行う関数です
    def update_my_ship(self):
        self.my_rolling_flag = 0  #自機ローリングフラグ(旋回フラグ)を0に初期化する
        self.my_moved_flag = 0    #自機が動いたかどうかのフラグを0に初期化する
        
        if self.game_status == SCENE_STAGE_CLEAR_MY_SHIP_BOOST: #ゲームステータスが「ステージクリア後、自機がブースト加速して右に過ぎ去っていく」なら
            self.my_x += self.my_vx
            self.my_vx += 0.025                #速度0.01で加速していく
            self.my_boost_injection_count += 1 #ステージクリア後のブースト噴射用のカウンターを1増やしていく
            self.my_moved_flag = 1             #トレースクローも動かしたいので自機移動フラグOnにする
            
        elif self.replay_status != REPLAY_PLAY and self.move_mode == MOVE_MANUAL: #リプレイステータスが(再生中)では無い & 移動モードが(MANUAL)の時は
            self.my_vx,self.my_vy = 0,0 #自機の自機の移動量(vx,vy)を0に初期化する
            
            # 左入力があったのなら  x座標を  1*my_speedの数値だけ減らす
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT) or pyxel.btn(pyxel.GAMEPAD_2_LEFT):
                self.my_moved_flag = 1#自機移動フラグOn
                self.my_vx = -1
                self.pad_data_l += PAD_LEFT
            
            # 右入力があったのなら  x座標を  1*my_speedの数値だけ増やす
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT) or pyxel.btn(pyxel.GAMEPAD_2_RIGHT):
                self.my_moved_flag = 1#自機移動フラグOn
                self.my_vx = 1
                self.pad_data_l += PAD_RIGHT
            
            # 上入力があったのなら  y座標を  1*my_speedの数値だけ減らす
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP) or pyxel.btn(pyxel.GAMEPAD_2_UP):
                self.my_rolling_flag = 2
                self.my_moved_flag = 1#自機移動フラグOn
                self.my_vy = -1
                self.pad_data_l += PAD_UP
            
            # 下入力があったのなら  y座標を  1*my_speedの数値だけ増やす
            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN) or pyxel.btn(pyxel.GAMEPAD_2_DOWN):
                self.my_rolling_flag = 1
                self.my_moved_flag = 1#自機移動フラグOn
                self.my_vy = 1
                self.pad_data_l += PAD_DOWN
            
            self.my_x += self.my_vx * self.my_speed #自機の移動量(vx,vy)と自機の速度(speed)を使って自機の座標を更新する（移動！）
            self.my_y += self.my_vy * self.my_speed
            
        elif self.replay_status == REPLAY_PLAY and self.move_mode == MOVE_MANUAL: #リプレイステータスが「PLAY」で移動モードが「MANUAL」のときは
            self.my_vx,self.my_vy = 0,0 #自機の自機の移動量(vx,vy)を0に初期化する
            #self.replay_frame_index    インデックス値のリストの内容はパッド入力データのHigh Byte
            #self.replay_frame_index + 1インデックス値のリストの内容はパッド入力データのLow Byte となります
            #リプレイデータを調べて左入力だったのなら  x座標を  my_speedの数値だけ減らす
            if self.replay_data[self.replay_stage_num][self.replay_frame_index + 1] & 0b00000100 == 0b00000100:  #LowByte
                self.my_moved_flag = 1#自機移動フラグOn
                self.my_vx = -1
            
            #リプレイデータを調べて右入力があったのなら x座標を  my_speedの数値だけ増やす
            if self.replay_data[self.replay_stage_num][self.replay_frame_index + 1] & 0b00001000 == 0b00001000:  #LowByte
                self.my_moved_flag = 1#自機移動フラグOn
                self.my_vx = 1
            
            #リプレイデータを調べて上入力があったのなら y座標を  my_speedの数値だけ減らす
            if self.replay_data[self.replay_stage_num][self.replay_frame_index + 1] & 0b00000001 == 0b00000001:  #LowByte
                self.my_rolling_flag = 2
                self.my_moved_flag = 1#自機移動フラグOn
                self.my_vy = -1
            
            #リプレイデータを調べて下入力があったのなら y座標を  my_speedの数値だけ増やす
            if self.replay_data[self.replay_stage_num][self.replay_frame_index + 1] & 0b00000010 == 0b00000010:  #LowByte
                self.my_rolling_flag = 1
                self.my_moved_flag = 1#自機移動フラグOn
                self.my_vy = 1
            
            self.my_x += self.my_vx * self.my_speed #自機の移動量(vx,vy)と自機の速度(speed)を使って自機の座標を更新する（移動！）
            self.my_y += self.my_vy * self.my_speed
            
        elif self.move_mode == MOVE_AUTO and self.move_mode_auto_complete == 0: #移動モード「AUTO」&まだ移動完了フラグが建っていなかったら・・・
            self.my_vx,self.my_vy = 0,0 #自機の自機の移動量(vx,vy)を0に初期化する
            
            if self.my_x > self.move_mode_auto_x:
                self.my_moved_flag = 1                #自機移動フラグOn
                self.my_vx = -0.5                     #左に自動移動
            else:
                self.my_moved_flag = 1                #自機移動フラグOn
                self.my_vx = 0.5                      #右に自動移動
            
            if self.my_y > self.move_mode_auto_y:
                self.my_rolling_flag = 2
                self.my_moved_flag = 1                #自機移動フラグOn
                self.my_vy = -0.5                     #上に自動移動
            else:
                self.my_rolling_flag = 1
                self.my_moved_flag = 1                #自機移動フラグOn
                self.my_vy = 0.5                      #下に自動移動
            
            self.my_x += self.my_vx #自機の移動量(vx,vy)を使って自機の座標を更新する（移動！）
            self.my_y += self.my_vy
            
            if -1 <= self.my_x - self.move_mode_auto_x <= 1 and -1 <= self.my_y - self.move_mode_auto_y <= 1: #自機座標(x,y)と移動目的先の座標の差が誤差+-1以内ならば
                self.move_mode_auto_complete = 1    #自動移動完了フラグをonにする
                if self.game_status == SCENE_STAGE_CLEAR_MOVE_MY_SHIP: #ゲームステータスが「ステージクリア後の自機自動移動」だったら
                    self.move_mode = MOVE_MANUAL    #自動移動モードを解除し手動移動モードに移行します
                    self.game_status = SCENE_STAGE_CLEAR_MY_SHIP_BOOST   #ゲームステータスを「ステージクリア後、自機がブーストして右へ過ぎ去っていくシーン」にする
                    self.my_vx = -1.3 #ブースト開始の初期スピードは左へ1ドット毎フレーム（ちょっと左に戻ってから加速し、右へ飛んでいく）
                    self.my_boost_injection_count = 1 #ステージクリア後のブースト噴射用のカウンターの数値を初期化
                    self.my_moved_flag = 1          #トレースクローも動かしたいので自機移動フラグOnにする
                    pyxel.playm(3)  #ブーストサウンド？再生

    #自機の座標を過去履歴リストに書き込んでいく関数（トレースクローの座標として使用します）
    def update_my_ship_record_coordinate(self):
        if self.my_moved_flag == 1:#自機が移動したフラグがonならＸＹ座標を過去履歴リストに書き込み一番古い物を削除する
            new_traceclaw = Trace_coordinates()#new_traceclawにTrace_coordinatesクラスの型を登録
            new_traceclaw.update(self.my_x,self.my_y)#クラス登録された（クラス設計された？）new_traceclawに自機のＸＹ座標データを入れてインスタンスを作成する
            self.claw_coordinates.append(new_traceclaw)#1フレームごとに自機のXY座標の入ったインスタンスをclaw_coordinatesリストに追加していく(append)
            
            del self.claw_coordinates[0]#一番古いXY座標データをdelする(一番古いXY座標のインデックス値は0)
            
            #自機が移動したフラグがonならリバースクロー用のショット方向ベクトルも書き込む
            self.reverse_claw_svx = -(self.my_vx)#リバースクロー用のショット方向ベクトルは自機移動ベクトルを反転したものとなります
            self.reverse_claw_svy = -(self.my_vy)

    #キーボードの1が推されたらショット経験値を増やしていく                              KEY 1
    def update_powerup_shot(self):
        if pyxel.btnp(pyxel.KEY_1):
            self.shot_exp += 1  #ショット経験値を１増やして武器をアップグレードさせていく
            self.level_up_my_shot() #自機ショットの経験値を調べ可能な場合レベルアップをさせる関数を呼び出す
            if self.shot_level > 10:
                self.shot_level = 0

    #キーボードの2が推されたらミサイル経験値を増やしていく                              KEY 2
    def update_powerup_missile(self):
        if pyxel.btnp(pyxel.KEY_2):
            self.missile_exp += 1#ミサイル経験値を１増やしてミサイルをアップグレードさせていく
            self.level_up_my_missile() #自機ミサイルの経験値を調べ可能な場合はレベルアップさせる関数を呼び出す
            if self.missile_level > 2:
                self.missile_level = 0

    #キーボードの3かゲームパッドの「SELECT」ボタンが入力されたボタンが押されたか？チェックする(スピードチェンジ)     KEY 3 GAMEPAD SELECT
    def update_check_change_speed(self):
        if self.replay_status == REPLAY_PLAY: #リプレイステータスが「再生中」の場合は
            if self.replay_data[self.replay_stage_num][self.replay_frame_index] & 0b00000001 == 0b00000001: #HighByte リプレイデータを調べてPAD SELECTが押された記録だったのなら...
                self.update_change_speed() #スピードチェンジ関数呼び出し！
        elif self.move_mode == MOVE_MANUAL: #手動移動モードの場合は
            if pyxel.btnp(pyxel.KEY_3) or pyxel.btnp(pyxel.GAMEPAD_1_SELECT) or pyxel.btnp(pyxel.GAMEPAD_2_SELECT):
                self.pad_data_h += PAD_SELECT #パッド入力データのSELECTボタンの情報ビットを立てる
                self.update_change_speed() #スピードチェンジ関数呼び出し！

    #自機のスピードチェンジ!!!!
    def update_change_speed(self):
        if self.my_speed == 1:
            self.my_speed = 1.5
        elif self.my_speed == 1.5:
            self.my_speed = 1.75
        else:
            self.my_speed = 1

    #スペースキーかゲームパッドAが押されたかどうか？もしくはリプレイモードでショット発射したのか調べる     KEY SPACE GAMEPAD A
    def update_check_fire_shot(self):
        if self.replay_status == REPLAY_PLAY: #リプレイステータスが「再生中」の場合は
            if self.replay_data[self.replay_stage_num][self.replay_frame_index + 1 ] & 0b00010000 == 0b00010000: #LowByte リプレイデータを調べてPAD Aが押された記録だったのなら...
                self.update_fire_shot() #ショット発射関数呼び出し！
        elif self.move_mode == MOVE_MANUAL: #手動移動モードの場合は
            if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_2_A): #パッドAかスペースキーが押されたか？
                self.pad_data_l += PAD_A #コントロールパッド入力記録にAボタンを押した情報ビットを立てて記録する
                self.update_fire_shot() #ショット発射関数呼び出し！

    #ショットを発射する!!!!!
    def update_fire_shot(self):
        if self.shot_level == SHOT_LV7_WAVE_CUTTER_LV1:#ウェーブカッターLv1発射
            if len(self.shots) < self.shot_rapid_of_fire:
            #if self.shot_type_count(self.shot_level) < 3: 
                if (pyxel.frame_count % 8) == 0:
                    pyxel.play(2,5) #チャンネル2でサウンドナンバー5を鳴らす
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 5,self.my_y -4,      3,0,  8,16,  0,   2,1)
                    
                    self.shots.append(new_shot)
        
        if self.shot_level == SHOT_LV8_WAVE_CUTTER_LV2:#ウェーブカッターLv2発射
            if len(self.shots) < self.shot_rapid_of_fire:
                if (pyxel.frame_count % 8) == 0:
                    pyxel.play(2,5)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 5,self.my_y -8,      3,0,  8,24,  0,   2,1)
                    self.shots.append(new_shot)
        
        if self.shot_level == SHOT_LV9_WAVE_CUTTER_LV3:#ウェーブカッターLv3発射
            if len(self.shots) < self.shot_rapid_of_fire:
                if (pyxel.frame_count % 8) == 0:
                    pyxel.play(2,5)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 5,self.my_y -12,      3,0,  8,32,  0,   2,1)
                    self.shots.append(new_shot)
        
        if self.shot_level == SHOT_LV10_WAVE_CUTTER_LV4:#ウェーブカッターLv4発射
            if len(self.shots) < self.shot_rapid_of_fire:
                if (pyxel.frame_count % 6) == 0:
                    pyxel.play(2,5)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 5,self.my_y -12,      4,0,  8,32,  0,   2,1)
                    self.shots.append(new_shot)
        
        if self.shot_level == SHOT_LV4_LASER:#レーザー発射
            if len(self.shots) < 20:
                if (pyxel.frame_count % 2) == 0:
                    pyxel.play(2,4)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 5,self.my_y,         3,1,  8,8,  0,   0.3,1)
                    self.shots.append(new_shot)
        
        if self.shot_level == SHOT_LV5_TWIN_LASER:#ツインレーザー発射
            if len(self.shots) < 40:
                if (pyxel.frame_count % 2) == 0:
                    pyxel.play(2,4)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 5,self.my_y - 3,     3,1,  8,8,  -3,  0.3,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 5,self.my_y + 3,     3,1,  8,8,    3, 0.3,1)
                    self.shots.append(new_shot)
        
        if self.shot_level == SHOT_LV6_3WAY_LASER:#３ＷＡＹレーザー発射
            if len(self.shots) < 80:
                if (pyxel.frame_count % 2) == 0:
                    pyxel.play(2,4)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 1,self.my_y  -1,    1,-1.08,   8,8,   -1,  0.2,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y,       3,1,      8,8,    0,  0.3,1)
                    self.shots.append(new_shot)
                    
                    pyxel.play(2,4)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y + 1,    2, 1.07,   8,8,    1,  0.2,1)
                    self.shots.append(new_shot)
        
        self.count_missile_type(5,5,5,5) #ミサイルタイプ5(ペネトレートロケット）がいくつ存在するのか調べる
        if self.type_check_quantity == 0 and self.select_sub_weapon_id == PENETRATE_ROCKET:#もしペネトレートロケットが全く存在しないのなら発射する！！！
            new_missile = Missile()
            new_missile.update(5,self.my_x + 4,self.my_y,   -0.8,-0.7,   6,    1   ,0,0,   0,1,   8,8, 0,0,  0,0) #ペネトレートロケット
            self.missile.append(new_missile)#ペネトレートロケット育成
            
            new_missile = Missile()
            new_missile.update(5,self.my_x + 4,self.my_y,   -0.8,-0.7,   6,    1   ,0,0,   0,-1,  8,8, 0,0,  0,0) #ペネトレートロケット
            self.missile.append(new_missile)#ペネトレートロケット育成
            
            new_missile = Missile()
            new_missile.update(5,self.my_x + 4,self.my_y,   -1,-0.8,   6,    1   ,0,0,   0,1,    8,8, 0,0,  0,0) #ペネトレートロケット
            self.missile.append(new_missile)#ペネトレートロケット育成
            
            new_missile = Missile()
            new_missile.update(5,self.my_x + 4,self.my_y,   -1,-0.8,   6,    1   ,0,0,   0,-1,    8,8, 0,0,  0,0) #ペネトレートロケット
            self.missile.append(new_missile)#ペネトレートロケット育成
        
        self.count_missile_type(4,4,4,4) #ミサイルタイプ4(テイルショット）がいくつ存在するのか調べる    
        if self.type_check_quantity < self.sub_weapon_tail_shot_level_data_list[self.sub_weapon_list[TAIL_SHOT]-1][1] and self.select_sub_weapon_id == TAIL_SHOT and (pyxel.frame_count % 6) == 0:#もしテイルショットが全く存在しないのなら発射する！！！
            level = self.sub_weapon_list[TAIL_SHOT] #現在のテイルショットのレベルを取得する
            #テイルショットのレベルデータリストから現時点のレベルに応じたデータを取得する
            speed = self.sub_weapon_tail_shot_level_data_list[level - 1][2] #スピード
            power = self.sub_weapon_tail_shot_level_data_list[level - 1][3] #攻撃力
            n_way = self.sub_weapon_tail_shot_level_data_list[level - 1][4] #n_way数
            if n_way == 1 or n_way == 3: #真後ろにテイルショット発射
                new_missile = Missile()
                new_missile.update(4,self.my_x - 4,self.my_y,   -2*speed,0,   power,1,   0,0,   0,0,   8,8,  0,0,  0,0) #テイルショット
                self.missile.append(new_missile)#真後ろに射出されるテイルショット育成
                if n_way == 3: #3wayの場合は更に斜め後ろ方向にテイルショット発射
                    new_missile = Missile()
                    new_missile.update(4,self.my_x - 4,self.my_y - 2,   -2*speed,-0.5,   power,1,   0,0,   0,0,   8,8,  0,0,  0,0) #テイルショット
                    self.missile.append(new_missile)#斜め後ろ(上)のテイルショット育成
                    
                    new_missile = Missile()
                    new_missile.update(4,self.my_x - 4,self.my_y + 2,   -2*speed, 0.5,   power,1,   0,0,   0,0,   8,8,  0,0,  0,0) #テイルショット
                    self.missile.append(new_missile)#斜め後ろ(下)のテイルショット育成
                
            elif n_way == 2: #ツインテイルショット発射
                new_missile = Missile()
                new_missile.update(4,self.my_x - 4,self.my_y - 2,   -2*speed,0,   power,1,   0,0,   0,0,   8,8,  0,0,  0,0) #テイルショット
                self.missile.append(new_missile)#ツインテイルショット(上)育成
                
                new_missile = Missile()
                new_missile.update(4,self.my_x - 4,self.my_y + 2,   -2*speed,0,   power,1,   0,0,   0,0,   8,8,  0,0,  0,0) #テイルショット
                self.missile.append(new_missile)#ツインテイルショット(下)育成
        
        self.count_missile_type(6,6,6,6) #ミサイルタイプ6(サーチレーザー）がいくつ存在するのか調べる
        if self.type_check_quantity <= 1 and self.select_sub_weapon_id == SEARCH_LASER and pyxel.frame_count % 32 == 0: #サーチレーザーが全く存在しないのなら発射する！！！
            new_missile = Missile()
            new_missile.update(6,self.my_x + 14,self.my_y,   2,0,   1,1,   0,1,   0,0,   16,8,  0,0,  0,0) #サーチレーザー(flag2=1なのでちょっとｘ軸前方向に対して索敵する)
            self.missile.append(new_missile)#サーチレーザー育成
            
            new_missile = Missile()
            new_missile.update(6,self.my_x    ,self.my_y,   2,0,   1,1,   0,0,   0,0,   16,8,  0,0,  0,0) #サーチレーザー
            self.missile.append(new_missile)#サーチレーザー育成
        
        self.count_missile_type(7,7,7,7) #ミサイルタイプ7(ホーミングミサイル）がいくつ存在するのか調べる
        if self.type_check_quantity <= self.sub_weapon_homing_missile_level_data_list[self.sub_weapon_list[HOMING_MISSILE]-1][1] - 4 and self.select_sub_weapon_id == HOMING_MISSILE and pyxel.frame_count % 8 == 0: #ホーミングミサイルの個数が1以下なら発射する！！！
            level = self.sub_weapon_list[HOMING_MISSILE] #現在のホーミングミサイルのレベルを取得する
            #ホーミングミサイルのレベルデータリストから現時点のレベルに応じたデータを取得する
            speed = self.sub_weapon_homing_missile_level_data_list[level - 1][2] #スピード
            power = self.sub_weapon_homing_missile_level_data_list[level - 1][3] #攻撃力
            new_missile = Missile()
            new_missile.update(7,self.my_x - 4,self.my_y,   -2*speed,1*speed,   power,1,   0,0,   0,0,   8,8,     200,60,   2,1)
            self.missile.append(new_missile)#ホーミングミサイル育成
            
            new_missile = Missile()
            new_missile.update(7,self.my_x - 4,self.my_y,   -2*speed,-1*speed,   power,1,   0,0,   0,0,   8,8,     200,60,   2,1)
            self.missile.append(new_missile)#ホーミングミサイル育成
            
            
            new_missile = Missile()
            new_missile.update(7,self.my_x + 4,self.my_y + 2,   0*speed,2*speed,   power,1,   0,0,   0,0,   8,8,     200,60,   2,1)
            self.missile.append(new_missile)#ホーミングミサイル育成
            
            new_missile = Missile()
            new_missile.update(7,self.my_x + 4,self.my_y - 2,   0*speed,-2*speed,   power,1,   0,0,   0,0,   8,8,     200,60,   2,1)
            self.missile.append(new_missile)#ホーミングミサイル育成
        
        if len(self.shots) < (self.shot_rapid_of_fire + (self.shot_level) * 2):#バルカンショットの発射
            if (pyxel.frame_count % 6) == 0:    
                if self.shot_level == SHOT_LV0_VULCAN_SHOT:#初期ショット バルカンショット1連装
                    pyxel.play(2,1)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 4,self.my_y    ,4,0,  8,8,    0, 1,1)
                    self.shots.append(new_shot)
                
                if self.shot_level == SHOT_LV1_TWIN_VULCAN_SHOT:#ツインバルカンショット 2連装
                    pyxel.play(2,1)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y - 2,4,0,  8,8,    0,  1,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y + 2,4,0,  8,8,     0,  1,1)
                    self.shots.append(new_shot)
                
                if self.shot_level == SHOT_LV2_3WAY_VULCAN_SHOT:#３ＷＡＹバルカンショット
                    pyxel.play(2,1)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y - 2  ,5,-0.3,  8,8,    0,  1,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y     ,5,0,    8,8,    0,  1,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y + 2  ,5,0.3,   8,8,    0,  1,1)
                    self.shots.append(new_shot)
                
                if self.shot_level == SHOT_LV3_5WAY_VULCAN_SHOT:#５ＷＡＹバルカンショット
                    pyxel.play(2,1)
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y - 2,    5,-1,    8,8,    0,  1,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y - 1,    5,-0.3,   8,8,    0,  1,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y,       5,0,     8,8,    0,  1,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y + 1,    5,0.3,    8,8,    0,  1,1)
                    self.shots.append(new_shot)
                    
                    new_shot = Shot()
                    new_shot.update(self.shot_level,self.my_x + 6,self.my_y + 2,    5,1,     8,8,    0,  1,1)
                    self.shots.append(new_shot)

    #スペースキーかゲームバットBボタンが押さたかどうか？もしくはリプレイモードでミサイル発射したのか調べる KEY SPACE GAMEPAD B
    def update_check_fire_missile(self):
        if self.replay_status == REPLAY_PLAY: #リプレイステータスが「再生中」の場合は
            if self.replay_data[self.replay_stage_num][self.replay_frame_index + 1] & 0b00100000 == 0b00100000: #LowByte リプレイデータを調べてPAD Bが押された記録だったのなら...
                self.update_fire_missile() #ミサイル発射関数呼び出し！
        elif self.move_mode == MOVE_MANUAL: #手動移動モードの場合は
            if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD_1_B) or pyxel.btn(pyxel.GAMEPAD_2_B): #パッドBかスペースキーが押されたか？
                self.pad_data_l += PAD_B #コントロールパッド入力記録にBボタンを押した情報ビットを立てて記録する
                self.update_fire_missile() #ミサイル発射関数呼び出し！

    #ミサイルを発射する!!!!!
    def update_fire_missile(self):
        if (pyxel.frame_count % 10) == 0:
            self.count_missile_type(0,1,2,3)#ミサイルタイプ0,1,2,3の合計数を数える
            if self.type_check_quantity < (self.missile_level + 1) * self.missile_rapid_of_fire:  #初期段階では２発以上は出せないようにする
                if self.missile_level == MISSILE_LV0_NORMAL_MISSILE:
                    pyxel.play(2,1)
                    
                    new_missile = Missile()
                    new_missile.update(0,self.my_x + 4,self.my_y,   0.7,0.7,   3,    1   ,0,0,    1,1,  8,8  ,0,0,   0,0) #前方右下に落ちていくミサイル
                    self.missile.append(new_missile)#ミサイル育成
                    
                elif self.missile_level == MISSILE_LV1_TWIN_MISSILE:
                    pyxel.play(2,1)
                    
                    new_missile = Missile()
                    new_missile.update(0,self.my_x + 2,self.my_y +2,   0.7,0.7,   3,    1   ,0,0,    1,1,  8,8,  0,0,   0,0) #前方右下に落ちていくミサイル
                    self.missile.append(new_missile)#ミサイル育成
                    
                    new_missile = Missile()
                    new_missile.update(1,self.my_x + 2,self.my_y -2,   0.7,0.7,   3,    1   ,0,0    ,1,-1,  8,8,  0,0,  0,0) #前方右上に飛んでいくミサイル
                    self.missile.append(new_missile)#ミサイル育成
                    
                elif self.missile_level == MISSILE_LV2_MULTI_MISSILE:
                    pyxel.play(2,1)
                    
                    new_missile = Missile()
                    new_missile.update(0,self.my_x +2,self.my_y +2,   0.7,0.7,    3,    1   ,0,0,    1,1,   8,8,  0,0,  0,0) #前方右下に落ちていくミサイル
                    self.missile.append(new_missile)#ミサイル育成
                    
                    new_missile = Missile()
                    new_missile.update(1,self.my_x +2,self.my_y -2,   0.7,0.7,    3,    1   ,0,0    ,1,-1,   8,8,  0,0,  0,0) #前方右上に飛んでいくミサイル
                    self.missile.append(new_missile)#ミサイル育成
                    
                    new_missile = Missile()
                    new_missile.update(2,self.my_x -2,self.my_y +2,   -0.7,0.7,   3,    1   ,0,0,    -1,1,    8,8,  0,0,   0,0) #後方左下に落ちていくミサイル
                    self.missile.append(new_missile)#ミサイル育成
                    
                    new_missile = Missile()
                    new_missile.update(3,self.my_x -2,self.my_y -2,   -0.7,0.7,   3,    1   ,0,0    ,-1,-1,   8,8,  0,0,   0,0) #後方左上に飛んでいくミサイル
                    self.missile.append(new_missile)#ミサイル育成

    #自機をはみ出さないようにする
    def update_clip_my_ship(self):
        if    self.game_status == SCENE_STAGE_CLEAR_MY_SHIP_BOOST\
            or self.game_status == SCENE_STAGE_CLEAR_FADE_OUT: #ステータスが「ブースト加速して去る」「ステージクリアフェードアウト」なら
            if self.my_x < 0:
                self.my_x = 0
            if self.my_x >= WINDOW_W + 80:
                self.my_x = WINDOW_W + 80
            return  #x軸はある程度まではみ出してok
        else:
            if self.my_x < 0:
                self.my_x = 0
            if self.my_x >= WINDOW_W - MOVE_LIMIT:
                self.my_x = WINDOW_W - MOVE_LIMIT - 1
        
        if self.my_y < 0:
            self.my_y = 0
        if self.my_y >= WINDOW_H - SHIP_H:
            self.my_y = WINDOW_H - SHIP_H - 1

    #################################自機弾関連の処理関数###############################################
    #自機弾の更新
    def update_my_shot(self):
        shot_count = len(self.shots)#弾の数を数える
        for i in reversed(range (shot_count)):
            #弾の位置を更新！
            if 0 <= self.shots[i].shot_type <= 3:#ショットタイプがバルカンショットの場合
                self.shots[i].posx += self.shots[i].vx * self.shot_speed_magnification #弾のX座標をVX*speed_magnification(倍率)分加減算して更新
                self.shots[i].posy += self.shots[i].vy                           #弾のY座標をVY分加減算して更新
                
            elif 4 <= self.shots[i].shot_type <= 6:#ショットタイプがレーザーの場合
                self.shots[i].posx += self.shots[i].vx#弾のX座標をVX分加減算して更新
                self.shots[i].offset_y = self.shots[i].offset_y * self.shots[i].vy#Ｙ軸オフセット値 vyの倍率ごと乗算して行って上下にずらしていく
                self.shots[i].posy = self.my_y + self.shots[i].offset_y#自機のｙ座標+Ｙ軸オフセット値をレーザーのＹ座標としてコピーする（ワインダー処理）
                self.shots[i].shot_hp = 1#レーザーなのでHPは減らず強制的にＨＰ＝１にする（ゾンビ化～みたいな）
                
            elif 7 <= self.shots[i].shot_type <= 10:#ショットタイプがウェーブカッターの場合
                self.shots[i].posx += self.shots[i].vx * self.shot_speed_magnification #弾のX座標をVX*speed_magnification(倍率)分加減算して更新
                self.shots[i].posy += self.shots[i].vy                           #弾のY座標をVY分加減算して更新
                self.shots[i].shot_hp = 1#ウェーブカッターはHPは減らず強制的にＨＰ＝１にする（ゾンビ化～みたいな）
            
            if self.shots[i].shot_hp == 0:
                del self.shots[i]#自機弾のHPがゼロだったらインスタンスを破棄する（弾消滅） 

    #自機弾のはみだしチェック（はみ出て画面外に出てしまったら消去する)
    def update_clip_my_shot(self):
        shot_count = len(self.shots)#弾の数を数える
        for i in reversed(range (shot_count)):
            if (-16 < self.shots[i].posx < WINDOW_W + 16 ) and (-16 <self.shots[i].posy < WINDOW_H + 16):
                continue
            else:
                del self.shots[i]

    #自機弾と敵の当たり判定
    def update_collision_my_shot_enemy(self):
        shot_hit = len(self.shots)
        for h in reversed(range (shot_hit)):
            enemy_hit = len(self.enemy)
            for e in reversed(range (enemy_hit)):#ウェーブカッターの分も含めてＹ軸方向の幅の大きさも考えた当たり判定にする、Ｘ軸方向の当たり判定は普通に8ドット単位で行う
                if      self.enemy[e].posx                    <= self.shots[h].posx + 4 <= self.enemy[e].posx + self.enemy[e].width\
                    and self.enemy[e].posy - self.shots[h].height <= self.shots[h].posy + 4 <= self.enemy[e].posy + self.enemy[e].height:
                    self.enemy[e].enemy_hp -= self.shots[h].shot_power #敵の耐久力をShot_powerの分だけ減らす
                    if self.enemy[e].enemy_hp <= 0:
                        self.enemy_destruction(e) #敵破壊処理関数呼び出し！
                        #パーティクル生成
                        for _number in range(5):
                            self.update_append_particle(PARTICLE_DOT,self.enemy[e].posx + 4,self.enemy[e].posy + 4,self.shots[h].vx / 2,self.shots[h].vy / 2, 0,0,0)
                        
                        #スコア加算
                        if   self.enemy[e].status == ENEMY_STATUS_NORMAL:   #ステータスが「通常」ならscore_normalをpointとしてスコアを加算する
                            point = self.enemy[e].score_normal
                        elif self.enemy[e].status == ENEMY_STATUS_ATTACK: #ステータスが「攻撃中」ならscore_attackをpointとしてスコアを加算する
                            point = self.enemy[e].score_attack
                        elif self.enemy[e].status == ENEMY_STATUS_ESCAPE: #ステータスが「撤退中」ならscore_escapeをpointとしてスコアを加算する
                            point = self.enemy[e].score_escape
                        elif self.enemy[e].status == ENEMY_STATUS_AWAITING: #ステータスが「待機中」ならscore_awaitingをpointとしてスコアを加算する
                            point = self.enemy[e].score_awaiting
                        elif self.enemy[e].status == ENEMY_STATUS_DEFENSE: #ステータスが「防御中」ならscore_defenseをpointとしてスコアを加算する
                            point = self.enemy[e].score_defense
                        elif self.enemy[e].status == ENEMY_STATUS_BERSERK: #ステータスが「怒り状態」ならscore_berserkをpointとしてスコアを加算する
                            point = self.enemy[e].score_berserk
                        else:                                     #ステータスが以上に当てはまらないときはscore_normalとする
                            point = self.enemy[e].score_normal
                        self.add_score(point) #スコアを加算する関数の呼び出し
                        del self.enemy[e] #敵リストから破壊した敵をdel消去破壊するっ！
                        
                    self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させるため
                    pyxel.play(0,2)#変な爆発音を出すのだ～～～☆彡

    #自機弾とボスとの当たり判定
    def update_collision_my_shot_boss(self):
        shot_hit = len(self.shots)
        for h in reversed(range (shot_hit)):
            boss_hit = len(self.boss)
            for e in reversed(range (boss_hit)):#ウェーブカッターの分も含めてＹ軸方向の幅の大きさも考えた当たり判定にする、Ｘ軸方向の当たり判定は普通に8ドット単位で行う
                if self.boss[e].invincible != 1: #もしボスが無敵状態で無いのならば
                    #ボス本体の当たり判定1(弾を消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main1_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main1_x + self.boss[e].col_main1_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_main1_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main1_y + self.boss[e].col_main1_h\
                        and self.boss[e].col_main1_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.shots[h].posx,self.shots[h].posy,0,0, 0,0,0)#自機弾の位置に消滅エフェクト育成
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定2(弾を消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main2_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main2_x + self.boss[e].col_main2_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_main2_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main2_y + self.boss[e].col_main2_h\
                        and self.boss[e].col_main2_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.shots[h].posx,self.shots[h].posy,0,0, 0,0,0)#自機弾の位置に消滅エフェクト育成
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定3(弾を消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main3_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main3_x + self.boss[e].col_main3_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_main3_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main3_y + self.boss[e].col_main3_h\
                        and self.boss[e].col_main3_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.shots[h].posx,self.shots[h].posy,0,0, 0,0,0)#自機弾の位置に消滅エフェクト育成
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定4(弾を消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main4_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main4_x + self.boss[e].col_main4_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_main4_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main4_y + self.boss[e].col_main4_h\
                        and self.boss[e].col_main4_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.shots[h].posx,self.shots[h].posy,0,0, 0,0,0)#自機弾の位置に消滅エフェクト育成
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定5(弾を消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main5_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main5_x + self.boss[e].col_main5_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_main5_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main5_y + self.boss[e].col_main5_h\
                        and self.boss[e].col_main5_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.shots[h].posx,self.shots[h].posy,0,0, 0,0,0)#自機弾の位置に消滅エフェクト育成
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定6(弾を消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main6_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main6_x + self.boss[e].col_main6_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_main6_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main6_y + self.boss[e].col_main6_h\
                        and self.boss[e].col_main6_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.shots[h].posx,self.shots[h].posy,0,0, 0,0,0)#自機弾の位置に消滅エフェクト育成
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定7(弾を消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main7_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main7_x + self.boss[e].col_main7_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_main7_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main7_y + self.boss[e].col_main7_h\
                        and self.boss[e].col_main7_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.shots[h].posx,self.shots[h].posy,0,0, 0,0,0)#自機弾の位置に消滅エフェクト育成
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定8(弾を消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main8_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main8_x + self.boss[e].col_main8_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_main8_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main8_y + self.boss[e].col_main8_h\
                        and self.boss[e].col_main8_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.shots[h].posx,self.shots[h].posy,0,0, 0,0,0)#自機弾の位置に消滅エフェクト育成
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    
                    
                    #パーツ１との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts1_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts1_x + self.boss[e].col_parts1_w\
                        and self.boss[e].posy + self.boss[e].col_parts1_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts1_y + self.boss[e].col_parts1_h\
                        and self.boss[e].parts1_flag == 1:
                        
                        self.boss[e].parts1_hp -= self.shots[h].shot_power #パーツ1の耐久力をShot_powerの分だけ減らす
                        if self.boss[e].parts1_hp <= 0: #パーツ1の耐久力が0以下になったのなら
                            self.boss[e].parts1_flag = 0 #パーツ1の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts1_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ1耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y   = self.shots[h].posx,self.shots[h].posy
                        hit_vx,hit_vy = self.shots[h].vx,self.shots[h].vx
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにショットを当てた後の処理の関数を呼び出す！
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する   
                    #パーツ2との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts2_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts2_x + self.boss[e].col_parts2_w\
                        and self.boss[e].posy + self.boss[e].col_parts2_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts2_y + self.boss[e].col_parts2_h\
                        and self.boss[e].parts2_flag == 1:
                        
                        self.boss[e].parts2_hp -= self.shots[h].shot_power #パーツ2の耐久力をShot_powerの分だけ減らす
                        if self.boss[e].parts2_hp <= 0: #パーツ2の耐久力が0以下になったのなら
                            self.boss[e].parts2_flag = 0 #パーツ2の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts2_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ2耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y   = self.shots[h].posx,self.shots[h].posy
                        hit_vx,hit_vy = self.shots[h].vx,self.shots[h].vx
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにショットを当てた後の処理の関数を呼び出す！
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる 
                        continue #これ以下の処理はせず次のループへと移行する                    
                    #パーツ3との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts3_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts3_x + self.boss[e].col_parts3_w\
                        and self.boss[e].posy + self.boss[e].col_parts3_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts3_y + self.boss[e].col_parts3_h\
                        and self.boss[e].parts3_flag == 1:
                        
                        self.boss[e].parts3_hp -= self.shots[h].shot_power #パーツ3の耐久力をShot_powerの分だけ減らす
                        if self.boss[e].parts3_hp <= 0: #パーツ3の耐久力が0以下になったのなら
                            self.boss[e].parts3_flag = 0 #パーツ3の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts3_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ3耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y   = self.shots[h].posx,self.shots[h].posy
                        hit_vx,hit_vy = self.shots[h].vx,self.shots[h].vx
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにショットを当てた後の処理の関数を呼び出す！
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する                  
                    #パーツ4との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts4_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts4_x + self.boss[e].col_parts4_w\
                        and self.boss[e].posy + self.boss[e].col_parts4_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts4_y + self.boss[e].col_parts4_h\
                        and self.boss[e].parts4_flag == 1:
                        
                        self.boss[e].parts4_hp -= self.shots[h].shot_power #パーツ4の耐久力をShot_powerの分だけ減らす
                        if self.boss[e].parts4_hp <= 0: #パーツ4の耐久力が0以下になったのなら
                            self.boss[e].parts4_flag = 0 #パーツ4の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts4_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ4耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y   = self.shots[h].posx,self.shots[h].posy
                        hit_vx,hit_vy = self.shots[h].vx,self.shots[h].vx
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにショットを当てた後の処理の関数を呼び出す！
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する                  
                    
                    #ダメージポイント1との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point1_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point1_x + self.boss[e].col_damage_point1_w\
                        and self.boss[e].posy - self.shots[h].height  + self.boss[e].col_damage_point1_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point1_y + self.boss[e].col_damage_point1_h\
                        and self.boss[e].col_damage_point1_w != 0:
                        
                        self.boss[e].main_hp -= self.shots[h].shot_power #ボスの耐久力をShot_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y   = self.shots[h].posx,self.shots[h].posy
                        hit_vx,hit_vy = self.shots[h].vx,self.shots[h].vx
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにショットを当てた後の処理の関数を呼び出す！
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント2との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point2_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point2_x + self.boss[e].col_damage_point2_w\
                        and self.boss[e].posy - self.shots[h].height + self.boss[e].col_damage_point2_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point2_y + self.boss[e].col_damage_point2_h\
                        and self.boss[e].col_damage_point2_w != 0:
                        
                        self.boss[e].main_hp -= self.shots[h].shot_power #ボスの耐久力をShot_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y   = self.shots[h].posx,self.shots[h].posy
                        hit_vx,hit_vy = self.shots[h].vx,self.shots[h].vx
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにショットを当てた後の処理の関数を呼び出す！
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント3との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point3_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point3_x + self.boss[e].col_damage_point3_w\
                        and self.boss[e].posy - self.shots[h].height + self.boss[e].col_damage_point3_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point3_y + self.boss[e].col_damage_point3_h\
                        and self.boss[e].col_damage_point3_w != 0:
                        
                        self.boss[e].main_hp -= self.shots[h].shot_power #ボスの耐久力をShot_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y   = self.shots[h].posx,self.shots[h].posy
                        hit_vx,hit_vy = self.shots[h].vx,self.shots[h].vx
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにショットを当てた後の処理の関数を呼び出す！
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント4との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point4_x <= self.shots[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point4_x + self.boss[e].col_damage_point4_w\
                        and self.boss[e].posy - self.shots[h].height + self.boss[e].col_damage_point4_y <= self.shots[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point4_y + self.boss[e].col_damage_point4_h\
                        and self.boss[e].col_damage_point4_w != 0:
                        
                        self.boss[e].main_hp -= self.shots[h].shot_power #ボスの耐久力をShot_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y   = self.shots[h].posx,self.shots[h].posy
                        hit_vx,hit_vy = self.shots[h].vx,self.shots[h].vx
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにショットを当てた後の処理の関数を呼び出す！
                        self.shots[h].shot_hp = 0#自機弾のＨＰをゼロにして自機弾移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する    

    #自機弾と背景障害物の当たり判定
    def update_collision_my_shot_bg(self):
        if  0 <= self.shot_level <= 6:#ウェーブカッターの場合は背景は貫通する
            shot_count = len(self.shots)
            for i in reversed(range(shot_count)):
                self.check_bg_collision(self.shots[i].posx,self.shots[i].posy + 4,0,0)
                if self.collision_flag == 1:
                    self.update_append_particle(PARTICLE_LINE,self.shots[i].posx,self.shots[i].posy,0,0, 0,0,0)
                    del self.shots[i]    

    #################################自機ミサイル関連の処理関数##########################################
    #自機ミサイルのはみだしチェック（はみ出て画面外に出てしまったら消去する）
    def update_clip_my_missile(self):
        missile_count = len(self.missile)#ミサイルリストの総数を数える
        for i in reversed(range (missile_count)):
            if (-24 < self.missile[i].posx < WINDOW_W + 18 ) and (-18 <self.missile[i].posy < WINDOW_H + 18):
                continue
            else:
                del self.missile[i]

    #自機ミサイルと敵の当たり判定
    def update_collision_missile_enemy(self):
        missile_hit = len(self.missile)
        for h in reversed(range (missile_hit)):
            enemy_hit = len(self.enemy)
            for e in reversed(range (enemy_hit)):
                if     self.enemy[e].posx <= self.missile[h].posx + 4 <= self.enemy[e].posx +   self.enemy[e].width  + self.missile[h].width  / 2\
                    and self.enemy[e].posy <= self.missile[h].posy + 4 <= self.enemy[e].posy +   self.enemy[e].height + self.missile[h].height / 2:
                    
                    self.enemy[e].enemy_hp -= self.missile[h].missile_power #敵の耐久力をミサイルパワーの分だけ減らす
                    if self.enemy[e].enemy_hp <= 0:
                        self.enemy_destruction(e) #敵破壊処理関数呼び出し！
                        #パーティクル生成
                        for _number in range(5):
                            self.update_append_particle(PARTICLE_DOT,self.enemy[e].posx + 4,self.enemy[e].posy + 4,self.missile[h].vx / 2,self.missile[h].vy / 2,   0,0,0)    
                        
                        del self.enemy[e]#敵リストから破壊した敵をＤＥＬ消去破壊！
                        self.score += 1#スコア加算（あとあといろんなスコアシステム実装する予定だよ）
                    
                    self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロにしてミサイル移動時にチェックしリストから消去させるため
                    pyxel.play(0,2)#ミサイルが敵を破壊した音！

    #自機ミサイルとボスとの当たり判定
    def update_collision_missile_boss(self):
        missile_hit = len(self.missile)
        for h in reversed(range (missile_hit)):
            boss_hit = len(self.boss)
            for e in reversed(range (boss_hit)):
                if self.boss[e].invincible != 1: #もしボスが無敵状態で無いのならば
                    #ボス本体の当たり判定1(ミサイルを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main1_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main1_x + self.boss[e].col_main1_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_main1_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main1_y + self.boss[e].col_main1_h\
                        and self.boss[e].col_main1_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.missile[h].posx,self.missile[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定2(ミサイルを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main2_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main2_x + self.boss[e].col_main2_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_main2_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main2_y + self.boss[e].col_main2_h\
                        and self.boss[e].col_main2_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.missile[h].posx,self.missile[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定3(ミサイルを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main3_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main3_x + self.boss[e].col_main3_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_main3_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main3_y + self.boss[e].col_main3_h\
                        and self.boss[e].col_main3_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.missile[h].posx,self.missile[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定4(ミサイルを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main4_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main4_x + self.boss[e].col_main4_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_main4_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main4_y + self.boss[e].col_main4_h\
                        and self.boss[e].col_main4_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.missile[h].posx,self.missile[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定5(ミサイルを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main5_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main5_x + self.boss[e].col_main5_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_main5_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main5_y + self.boss[e].col_main5_h\
                        and self.boss[e].col_main5_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.missile[h].posx,self.missile[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定6(ミサイルを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main6_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main6_x + self.boss[e].col_main6_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_main6_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main6_y + self.boss[e].col_main6_h\
                        and self.boss[e].col_main6_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.missile[h].posx,self.missile[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定7(ミサイルを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main7_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main7_x + self.boss[e].col_main7_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_main7_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main7_y + self.boss[e].col_main7_h\
                        and self.boss[e].col_main7_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.missile[h].posx,self.missile[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定8(ミサイルを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main8_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main8_x + self.boss[e].col_main8_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_main8_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main8_y + self.boss[e].col_main8_h\
                        and self.boss[e].col_main8_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.missile[h].posx,self.missile[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    
                    
                    #パーツ１との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts1_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts1_x + self.boss[e].col_parts1_w\
                        and self.boss[e].posy + self.boss[e].col_parts1_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts1_y + self.boss[e].col_parts1_h\
                        and self.boss[e].parts1_flag == 1:
                        
                        self.boss[e].parts1_hp -= self.missile[h].missile_power #パーツ1の耐久力をmissile_powerの分だけ減らす
                        if self.boss[e].parts1_hp <= 0: #パーツ1の耐久力が0以下になったのなら
                            self.boss[e].parts1_flag = 0 #パーツ1の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts1_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ1耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.missile[h].posx,self.missile[h].posy
                        hit_vx,hit_vy = self.missile[h].vx,self.missile[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにミサイルを当てた後の処理の関数を呼び出す！
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する   
                    #パーツ2との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts2_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts2_x + self.boss[e].col_parts2_w\
                        and self.boss[e].posy + self.boss[e].col_parts2_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts2_y + self.boss[e].col_parts2_h\
                        and self.boss[e].parts2_flag == 1:
                        
                        self.boss[e].parts2_hp -= self.missile[h].missile_power #パーツ2の耐久力をmissile_powerの分だけ減らす
                        if self.boss[e].parts2_hp <= 0: #パーツ2の耐久力が0以下になったのなら
                            self.boss[e].parts2_flag = 0 #パーツ2の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts2_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ2耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.missile[h].posx,self.missile[h].posy
                        hit_vx,hit_vy = self.missile[h].vx,self.missile[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにミサイルを当てた後の処理の関数を呼び出す！
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する                    
                    #パーツ3との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts3_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts3_x + self.boss[e].col_parts3_w\
                        and self.boss[e].posy + self.boss[e].col_parts3_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts3_y + self.boss[e].col_parts3_h\
                        and self.boss[e].parts3_flag == 1:
                        
                        self.boss[e].parts3_hp -= self.missile[h].missile_power #パーツ3の耐久力をmissile_powerの分だけ減らす
                        if self.boss[e].parts3_hp <= 0: #パーツ3の耐久力が0以下になったのなら
                            self.boss[e].parts3_flag = 0 #パーツ3の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts3_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ3耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.missile[h].posx,self.missile[h].posy
                        hit_vx,hit_vy = self.missile[h].vx,self.missile[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにミサイルを当てた後の処理の関数を呼び出す！
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する                  
                    #パーツ4との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts4_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts4_x + self.boss[e].col_parts4_w\
                        and self.boss[e].posy + self.boss[e].col_parts4_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts4_y + self.boss[e].col_parts4_h\
                        and self.boss[e].parts4_flag == 1:
                        
                        self.boss[e].parts4_hp -= self.missile[h].missile_power #パーツ4の耐久力をmissile_powerの分だけ減らす
                        if self.boss[e].parts4_hp <= 0: #パーツ4の耐久力が0以下になったのなら
                            self.boss[e].parts4_flag = 0 #パーツ4の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts4_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ4耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.missile[h].posx,self.missile[h].posy
                        hit_vx,hit_vy = self.missile[h].vx,self.missile[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにミサイルを当てた後の処理の関数を呼び出す！
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する                  
                    
                    #ダメージポイント1との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point1_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point1_x + self.boss[e].col_damage_point1_w\
                        and self.boss[e].posy - self.missile[h].height  + self.boss[e].col_damage_point1_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point1_y + self.boss[e].col_damage_point1_h\
                        and self.boss[e].col_damage_point1_w != 0:
                        
                        self.boss[e].main_hp -= self.missile[h].missile_power #ボスの耐久力をmissile_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.missile[h].posx,self.missile[h].posy
                        hit_vx,hit_vy = self.missile[h].vx,self.missile[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにミサイルを当てた後の処理の関数を呼び出す！
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント2との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point2_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point2_x + self.boss[e].col_damage_point2_w\
                        and self.boss[e].posy - self.missile[h].height + self.boss[e].col_damage_point2_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point2_y + self.boss[e].col_damage_point2_h\
                        and self.boss[e].col_damage_point2_w != 0:
                        
                        self.boss[e].main_hp -= self.missile[h].missile_power #ボスの耐久力をmissile_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.missile[h].posx,self.missile[h].posy
                        hit_vx,hit_vy = self.missile[h].vx,self.missile[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにミサイルを当てた後の処理の関数を呼び出す！
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント3との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point3_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point3_x + self.boss[e].col_damage_point3_w\
                        and self.boss[e].posy - self.missile[h].height + self.boss[e].col_damage_point3_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point3_y + self.boss[e].col_damage_point3_h\
                        and self.boss[e].col_damage_point3_w != 0:
                        
                        self.boss[e].main_hp -= self.missile[h].missile_power #ボスの耐久力をmissile_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.missile[h].posx,self.missile[h].posy
                        hit_vx,hit_vy = self.missile[h].vx,self.missile[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにミサイルを当てた後の処理の関数を呼び出す！
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント4との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point4_x <= self.missile[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point4_x + self.boss[e].col_damage_point4_w\
                        and self.boss[e].posy - self.missile[h].height + self.boss[e].col_damage_point4_y <= self.missile[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point4_y + self.boss[e].col_damage_point4_h\
                        and self.boss[e].col_damage_point4_w != 0:
                        
                        self.boss[e].main_hp -= self.missile[h].missile_power #ボスの耐久力をmissile_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.missile[h].posx,self.missile[h].posy
                        hit_vx,hit_vy = self.missile[h].vx,self.missile[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにミサイルを当てた後の処理の関数を呼び出す！ 
                        self.missile[h].missile_hp = 0#ミサイルのＨＰをゼロしてミサイル移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する    

    #自機ミサイルの更新（背景障害物との当たり判定も行っています）
    def update_my_missile(self):
        missile_count = len(self.missile)#ミサイルの総数を数える
        for i in reversed(range (missile_count)):
            if 0 <= self.missile[i].missile_type <= 3:#通常ミサイルの処理
                self.missile[i].vy = self.missile[i].y_reverse * 0.7#ミサイルの落下スピードを標準の0.7にしておく（ｙ軸反転を掛けて反転もさせる）
                #ミサイルの真下（もしくは真上）が地形かどうか？チェック
                self.check_bg_collision(self.missile[i].posx,(((self.missile[i].posy ) // 8) * 8) + self.missile[i].y_reverse + 8,  0,0)#これで上手くいった・・なんでや・・どうしてや？
                
                if self.collision_flag == 1:#障害物に当たった時の処理
                    self.missile[i].missile_flag1 = 1#もしミサイルの真下(y_reverseが-1なら真上）が障害物ならmissile_flag1を１にして
                    self.missile[i].vy = 0#縦方向の移動量vyを0にして横方向だけに進むようにする
                    if  2 <= self.missile[i].missile_type <= 3:
                        self.missile[i].vx = -1
                
                #ミサイルの進行先が地形かどうか？チェック
                self.check_bg_collision(self.missile[i].posx + (self.missile[i].x_reverse * 8),self.missile[i].posy + 4,0,0)
                
                if self.missile[i].missile_hp == 0:
                    del self.missile[i]#ミサイルのＨＰが0だったらインスタンスを破棄する(ミサイル消滅)
                elif self.collision_flag == 1:
                    self.update_append_particle(PARTICLE_MISSILE_DEBRIS,self.missile[i].posx + (self.missile[i].missile_type // 2) * 2 - 8,self.missile[i].posy,0,0, 7,0,0)
                    #(self.missile[i].missile_type // 2) * 2 - 8の計算結果は
                    #ミサイルタイプが0右下ミサイルの場合は 0 // 2 * 2 - 8で -8
                    #ミサイルタイプが1右上ミサイルの場合は 1 // 2 * 2 - 8で -8
                    #ミサイルタイプが2左下ミサイルの場合は 2 // 2 * 2 - 8で +8
                    #ミサイルタイプが3左上ミサイルの場合は 3 // 2 * 2 - 8で +8となる よって補正値は右向きのミサイルの場合は-8 左向きのミサイルは+8となる
                    #
                    #う～ん、後方のミサイルは別にx+8の補正を入れなくても良いかもしれない・・・
                    #スクロールスピードの関係でミサイルデブリを表示した瞬間にスクロールして表示位置ずれるし
                    del self.missile[i]#ミサイルの右側が障害物だったらインスタンスを破棄する（ミサイル消滅）
                else:
                    #進行先が地形ではなく尚且つミサイルのＨＰがまだ残っていたのなら、ミサイルの位置を更新！
                    if self.missile[i].vy == 0: #地面に設置して横方向動くときだけ倍率補正値を掛け合わせたvxとする
                        self.missile[i].posx += self.missile[i].vx * self.missile_speed_magnification #ミサイルのX座標を(VX*倍率補正)分加減算して更新
                    else:   
                        self.missile[i].posx += self.missile[i].vx #上下に落ちていくときはミサイルのX座標をVXだけ加減算して更新
                    
                    self.missile[i].posy += self.missile[i].vy                             #ミサイルのY座標をVY分加減算して更新
                
            elif    self.missile[i].missile_type == 4:#テイルショットの処理        
                #テイルショットの位置が地形かどうか？チェック
                self.check_bg_collision(self.missile[i].posx,self.missile[i].posy,0,0)
                if self.collision_flag == 1 or self.missile[i].missile_hp == 0:
                    del self.missile[i]#テイルショットの位置が障害物かもしくはテイルショットのＨＰが0だったらインスタンスを破棄する（テイルショット消滅） 
                else:
                    #進行先が地形ではなく尚且つテイルショットのＨＰがまだ残っていたのなら位置を更新！
                    self.missile[i].posx += self.missile[i].vx#テイルショットのX座標をVX分加減算して更新
                    self.missile[i].posy += self.missile[i].vy#テイルショットのY座標をVY分加減算して更新                 
            elif    self.missile[i].missile_type == 5:#ペネトレートロケットの処理
                #進行先が地形ではなく尚且つペネトレートロケットのＨＰがまだ残っていたのなら位置を更新！
                self.missile[i].vx += 0.02 #vxをだんだんと増加させていく
                self.missile[i].posx += self.missile[i].vx #ペネトレートロケットのx座標をvxと足し合わせて更新
                
                self.missile[i].vy += 0.01 #vyをだんだんと増加させていく
                self.missile[i].posy += self.missile[i].vy * self.missile[i].y_reverse #ペネトレートロケットのx,y座標をvx,vyと足し合わせて更新(y_reverseが-1ならy軸の補正が逆となる)           
            elif    self.missile[i].missile_type == 6:#サーチレーザーの処理        
                #サーチレーザーの位置が地形かどうか？チェック
                self.check_bg_collision(self.missile[i].posx,self.missile[i].posy,0,0)
                if self.collision_flag == 1 or self.missile[i].missile_hp == 0:
                    del self.missile[i]#サーチレーザーの位置が障害物かもしくはサーチレーザーのＨＰが0だったらインスタンスを破棄する（サーチレーザー消滅） 
                else:
                    self.missile[i].posx += self.missile[i].vx          #サーチレーザーのX座標をVX分加減算して更新
                    
                    if self.missile[i].missile_flag1 == 0:#状態遷移が(敵索敵中=0)なら
                        if self.missile[i].posx > self.my_x + 16:#サーチレーザーは自機より前方16ドット進んでから索敵を始める
                            #索敵用関数の呼び出し(missile_flag2*16のぶんだけｘ方向の先で敵とのＸ座標を比較する)
                            self.search_laser_enemy_cordinate(self.missile[i].posx + self.missile[i].missile_flag2 * 8,self.missile[i].posy)
                            if self.search_laser_flag == 1:#敵機索敵ＯＫ！のフラグが立っていたのなら
                                self.missile[i].missile_flag1 = 1 #状態遷移を(屈折中=1)にする                  
                                self.missile[i].y_reverse = self.search_laser_y_direction #Y軸加算用の反転フラグ(-1=上方向 1=下方向)もそのまま代入
                        
                    elif self.missile[i].missile_flag1 == 1:#状態遷移が（屈折中=1)なら
                        self.missile[i].vx = 0 #x軸（横）に移動はさせないようvxに0を強制代入
                        self.missile[i].missile_flag1 = 2 #状態遷移を（縦に進行中=2)にする
                        
                        self.missile[i].width  = 8   #レーザーは縦長になるので当たり判定は16x16に変化する(本当は8x16何だけど甘めに16x16にしちゃう)
                        self.missile[i].height = 16
                        
                    elif self.missile[i].missile_flag1 == 2:#状態遷移が（縦に進行中=2)なら
                        self.missile[i].vx = 0 #x軸（横）に移動はさせないようvxに0を強制代入
                        #self.missile[i].posx += self.missile[i].vx          #サーチレーザーのX座標をVX分加減算して更新
                        self.missile[i].posy += self.missile[i].y_reverse * 2#サーチレーザーのY座標をy_reverse分加減算して更新
                
            elif    self.missile[i].missile_type == 7:#ホーミングミサイルの処理        
                if self.missile[i].missile_hp == 0:
                    del self.missile[i]#ホーミングミサイルのＨＰが0だったらインスタンスを破棄する（ホーミングミサイル消滅） 
                else:
                    self.search_homing_missile_enemy_cordinate(self.missile[i].posx,self.missile[i].posy)#ホーミングミサイルのposx.posyを元に一番近距離の敵の座標を見つけ出す
                    if self.search_homing_missile_flag == 1:#もし狙い撃つ敵を見つけたのなら
                        self.missile[i].tx = self.search_homing_missile_tx #ターゲットとなる敵の座標をミサイルリストのTargetX,TargetYに代入する
                        self.missile[i].ty = self.search_homing_missile_ty
                        
                    #ホーミングミサイルを目標位置まで追尾させる
                    vx0 = self.missile[i].vx
                    vy0 = self.missile[i].vy #ホーミングミサイルの速度(vx,vy)を(vx0,vy0)に退避する
                    
                    #目標までの距離を求める dに距離が入る
                    #狙うターゲットとなる座標(tx,ty)
                    self.d = math.sqrt((self.missile[i].tx - self.missile[i].posx) * (self.missile[i].tx - self.missile[i].posx) + (self.missile[i].ty - self.missile[i].posy) * (self.missile[i].ty - self.missile[i].posy))
                    
                    #ホーミングミサイルの速度 vx,vyを求める
                    #速さが一定値speedになるようにする
                    #目標までの距離dが0の時は速度を左方向にする
                    #theta(Θ)は旋回できる角度の上限
                    #ターゲット方向の速度ベクトル(vx1,vy1)を求める
                    if self.d == 0:#目標（ターゲット）までの距離は0だった？（重なっていた？）
                        vx1= 0
                        vy1 = self.missile[i].speed #目標までの距離dが0の時は速度を左方向にする
                    else:
                        #ホーミングミサイルとターゲットとの距離とＸ座標、Ｙ座標との差からＶＸ，ＶＹの増分を計算する
                    
                     vx1 = ((self.missile[i].tx - self.missile[i].posx) / (self.d * self.missile[i].speed))
                     vy1 = ((self.missile[i].ty - self.missile[i].posy) / (self.d * self.missile[i].speed))
                    #右回り旋回角度上限の速度ベクトル(vx2,vy2)を求める
                    #math.piはπ（円周率3.141592......)
                    #ううううぅ・・・難しい・・・・数学赤点の私には難しい・・・・
                    self.rad = 3.14 / 180 * self.missile[i].theta #rad = 角度degree（theta）をラジアンradianに変換
                    
                    self.missile[i].theta += 0.2 #旋回できる角度を増やしていく
                    if self.missile[i].theta > 360:
                        self.missile[i].theta = 360 #旋回可能角度は360度を超えないようにする
                    
                    vx2 = math.cos(self.rad) * vx0 - math.sin(self.rad) * vy0
                    vy2 = math.sin(self.rad) * vx0 + math.cos(self.rad) * vy0
                    
                    #ターゲット方向に曲がるのか？ それとも旋回角度上限一杯（面舵一杯！とか取り舵一杯！とかそういう表現）で曲がるのか判別する
                    if vx0 * vx1 + vy0 * vy1 >= vx0 * vx2 + vy0 * vy2:
                        #ターゲット方向が旋回可能範囲内の場合の処理
                        #ターゲット方向に曲がるようにする
                        self.missile[i].vx = vx1
                        self.missile[i].vy = vy1
                    else:
                        #ターゲットが旋回可能範囲を超えている場合（ハンドルをいっぱいまで切ってもターゲットに追いつけないよ～）ハンドル一杯まで切る！
                        #左回り（取り舵方向）の旋回角度上限の速度ベクトルvx3,vy3を求める
                        vx3 =  math.cos(self.rad) * vx0 + math.sin(self.rad) * vy0
                        vy3 = -math.sin(self.rad) * vx0 + math.cos(self.rad) * vy0
                        
                        #ホーミングミサイルからターゲットへの相対ベクトル(px,py)を求める
                        px = self.missile[i].tx - self.missile[i].posx
                        py = self.missile[i].ty - self.missile[i].posy
                        
                        #右回りか左回りを決める
                        #右回りの速度ベクトルの内積(p,v2)と左回りの速度ベクトルの内積(p,v3)の比較で右回りか左回りか判断する
                        #旋回角度が小さいほうが内積が大きくなるのでそちらの方に曲がるようにする
                        if px * vx2 + py * vy2 >= px * vx3 + py * vy3:
                            #右回り（面舵方向）の場合
                            self.missile[i].vx = vx2
                            self.missile[i].vy = vy2
                        else:
                            #左回り（取り舵方向）の場合
                            self.missile[i].vx = vx3
                            self.missile[i].vy = vy3
                    
                    #ホーミングミサイルの座標(posx,posy)を増分(vx,vy)を加減算更新して敵を移動させる(座標更新！)
                    self.missile[i].posx += self.missile[i].vx#ホーミングミサイルのX座標をVX分加減算して更新
                    self.missile[i].posy += self.missile[i].vy#ホーミングミサイルのY座標をVY分加減算して更新

    #################################クロー関連の処理関数################################################
    #クローの更新
    def update_claw(self):
        if   self.claw_type == 0:#ローリングクローの時のみ実行
            #ひとつ前を回るクローとの回転角度の差の計算処理
            if self.claw_number == 4:#クロー4機の時の処理
                self.claw[0].angle_difference = self.claw[1].degree - self.claw[0].degree
                self.claw[1].angle_difference = self.claw[2].degree - self.claw[1].degree
                self.claw[2].angle_difference = self.claw[3].degree - self.claw[2].degree
                self.claw[3].angle_difference = self.claw[0].degree - self.claw[3].degree
            elif self.claw_number == 3:#クロー3機の時の処理
                self.claw[0].angle_difference = self.claw[1].degree - self.claw[0].degree
                self.claw[1].angle_difference = self.claw[2].degree - self.claw[1].degree
                self.claw[2].angle_difference = self.claw[0].degree - self.claw[2].degree
            elif self.claw_number == 2:#クロー2機の時の処理
                self.claw[0].angle_difference = self.claw[1].degree - self.claw[0].degree
                self.claw[1].angle_difference = self.claw[0].degree - self.claw[1].degree
                #クローが1機と0機の時は角度計算しないのです
            
            #クローの回転処理
            claw_count = len(self.claw)#クローの数を数える
            for i in range(claw_count):
                if self.claw[i].status == 0:#ステータスが(0)の場合は回転開始の初期位置まで動いていく（自機の真上）
                    #self.claw[i].offset_x += self.claw[i].roll_vx
                    #self.claw[i].offset_y += self.claw[i].roll_vy#現在のオフセット座標値をroll_vx,roll_vyの分だけ加減算させていく
                    #
                    #self.claw[i].posx = self.my_x + self.claw[i].offset_x
                    #self.claw[i].posy = self.my_y + self.claw[i].offset_y#クローのX,Y座標をオフセット分だけ加減算させていって回転開始位置まで移動させてやる
                    #if  self.claw[i].offset_x == self.claw[i].offset_roll_x and self.claw[i].offset_y == self.claw[i].offset_roll_y:
                    #      self.claw[i].status = 1#回転開始初期位置のオフセット値まで行ったのならステータスを回転開始(1)にする
                    if self.claw[i].offset_x < self.claw[i].offset_roll_x:#offset_xとyをoffset_fix_xとyに+1ドット単位で増減させて同じ値に近づけていく
                        self.claw[i].offset_x += 1
                    elif self.claw[i].offset_x > self.claw[i].offset_roll_x:
                        self.claw[i].offset_x -= 1
                    
                    if self.claw[i].offset_y < self.claw[i].offset_roll_y:
                        self.claw[i].offset_y += 1
                    elif self.claw[i].offset_y > self.claw[i].offset_roll_y:
                        self.claw[i].offset_y -= 1
                    
                    self.claw[i].posx = self.my_x + self.claw[i].offset_x
                    self.claw[i].posy = self.my_y + self.claw[i].offset_y#クローのX,Y座標をオフセット分だけ加減算させていって回転開始位置まで移動させてやる
                    if  int(self.claw[i].offset_x) == int(self.claw[i].offset_roll_x) and int(self.claw[i].offset_y) == int(self.claw[i].offset_roll_y):
                        self.claw[i].status = 1#ローリングクロー回転開始初期位置のオフセット値まで行ったのならステータスを回転開始！！(1)にする 比較するときはint()を使って切り捨てた整数値で比較する
                    
                elif  self.claw[i].status == 1:#ステータスが(1)の場合は回転開始！
                    if self.claw[i].angle_difference == self.claw_difference:
                        self.claw[i].degree -= self.claw[i].speed#クローの個数に応じた回転間隔
                    elif self.claw[i].angle_difference > self.claw_difference:
                        self.claw[i].degree -= self.claw[i].speed - 1
                    else:
                        self.claw[i].degree -= self.claw[i].speed + 1
                    
                    self.claw[i].degree = self.claw[i].degree % 360#角度は３６０で割った余りとする(0~359)
                    #極座標(r,θ)から直交座標(x,y)への変換は
                    #     x = r cos θ
                    #     y = r sin θ
                    self.claw[i].offset_x = self.claw[i].radius *   math.cos(math.radians(self.claw[i].degree))
                    self.claw[i].offset_y = self.claw[i].radius *  -math.sin(math.radians(self.claw[i].degree))
                    
                    #クローの座標を自機の座標を中心としオフセット値を足した物とする
                    #線形補間値0.2で線形補間してやる（ピッタリ自機に付いてくる）
                    self.claw[i].posx = self.claw[i].posx + 0.2 * ((self.my_x + self.claw[i].offset_x) - self.claw[i].posx)
                    self.claw[i].posy = self.claw[i].posy + 0.2 * ((self.my_y + self.claw[i].offset_y) - self.claw[i].posy)
            
        elif self.claw_type == 1:#トレースクローの時のみ実行
            for i in range(self.claw_number):#iの値は0からクローの数まで増えてイクです  ハイ！
                self.claw[i].status = 1#トレースクローは出現と同時に移動開始のステータスにする
                self.claw[i].posx = self.claw_coordinates[self.trace_claw_index + (TRACE_CLAW_BUFFER_SIZE - self.trace_claw_distance) - self.trace_claw_distance * i].posx#クローの座標をオフセット値のＸＹ座標とする
                self.claw[i].posy = self.claw_coordinates[self.trace_claw_index + (TRACE_CLAW_BUFFER_SIZE - self.trace_claw_distance) - self.trace_claw_distance * i].posy
            
        elif self.claw_type == 2:#フィックスクローの時のみ実行
            claw_count = len(self.claw)#クローの数を数える
            for i in range(claw_count):
                if self.claw[i].status == 0:#ステータスが(0)の場合はフイックスクローの初期位置まで動いていく（自機の上か下）
                    if self.claw[i].offset_x < self.claw[i].offset_fix_x:#offset_xとyをoffset_fix_xとyに0.5単位で増減させて同じ値に近づけていく
                        self.claw[i].offset_x += 0.5
                    elif self.claw[i].offset_x > self.claw[i].offset_fix_x:
                        self.claw[i].offset_x -= 0.5
                    
                    if self.claw[i].offset_y < self.claw[i].offset_fix_y:
                        self.claw[i].offset_y += 0.5
                    elif self.claw[i].offset_y > self.claw[i].offset_fix_y:
                        self.claw[i].offset_y -= 0.5
                    
                    self.claw[i].posx = self.my_x + self.claw[i].offset_x
                    self.claw[i].posy = self.my_y + self.claw[i].offset_y#クローのX,Y座標をオフセット分だけ加減算させていってクロ―固定位置まで移動させてやる
                    
                    if  -0.5 <= self.claw[i].offset_x - self.claw[i].offset_fix_x <= 0.5 and -0.5 <= self.claw[i].offset_y - self.claw[i].offset_fix_y <= 0.5:
                        self.claw[i].status = 1#クロー固定位置のオフセット値付近(+-0.5)まで行ったのならステータスをクロー固定完了！！(1)にする
                    
                elif self.claw[i].status == 1:#ステータスが(1)の場合はフイックスクローの固定は完了したので弾を発射とかしちゃう
                    if i <=1:
                        #クローの座標を自機の座標を中心としオフセット値を足した物とする
                        #クローナンバー0と1（内側のクロー）は線形補間値0.2で線形補間してやる（ピッタリ自機に付いてくる）
                        self.claw[i].posx = self.claw[i].posx + 0.2 * (self.my_x + self.claw[i].offset_x - self.claw[i].posx)
                        self.claw[i].posy = self.claw[i].posy + 0.2 * (self.my_y + (self.claw[i].offset_y * self.fix_claw_magnification) - self.claw[i].posy)
                    else:
                        #クローの座標を自機の座標を中心としオフセット値を足した物とする
                        #クローナンバー2と3（外側のクロー）は線形補間値0.1で線形補間してやる（ちょっと遅れて自機に引っ付いてくる）
                        self.claw[i].posx = self.claw[i].posx + 0.1 * (self.my_x + self.claw[i].offset_x - self.claw[i].posx)
                        self.claw[i].posy = self.claw[i].posy + 0.1 * (self.my_y + (self.claw[i].offset_y * self.fix_claw_magnification) - self.claw[i].posy)
            
        elif self.claw_type == 3:#リバースクローの時のみ実行
            claw_count = len(self.claw)#クローの数を数える
            for i in range(claw_count):
                if self.claw[i].status == 0:#ステータスが(0)の場合はリバースクローの初期位置まで動いていく（自機の上か下）
                    if self.claw[i].offset_x < self.claw[i].offset_reverse_x:#offset_xとyをoffset_reverse_xとyに0.5単位で増減させて同じ値に近づけていく
                        self.claw[i].offset_x += 0.5
                    elif self.claw[i].offset_x > self.claw[i].offset_reverse_x:
                        self.claw[i].offset_x -= 0.5
                    
                    if self.claw[i].offset_y < self.claw[i].offset_reverse_y:
                        self.claw[i].offset_y += 0.5
                    elif self.claw[i].offset_y > self.claw[i].offset_reverse_y:
                        self.claw[i].offset_y -= 0.5
                    
                    self.claw[i].posx = self.my_x + self.claw[i].offset_x
                    self.claw[i].posy = self.my_y + self.claw[i].offset_y#クローのX,Y座標をオフセット分だけ加減算させていってクロ―固定位置まで移動させてやる
                    
                    if  -0.5 <= self.claw[i].offset_x - self.claw[i].offset_reverse_x <= 0.5 and -0.5 <= self.claw[i].offset_y - self.claw[i].offset_reverse_y <= 0.5:
                        self.claw[i].status = 1#リバースクローの開始のオフセット値付近(+-0.5)まで行ったのならステータスをクロー固定完了！！(1)にする
                    
                elif self.claw[i].status == 1:#ステータスが(1)の場合はリバースクローの固定は完了したので弾を発射とかしちゃう
                    if i == 1 or i == 2:
                        #クローの座標を自機の座標を中心としオフセット値を足した物とする
                        #クローナンバー1と2（上下のクロー）は線形補間値0.3で線形補間してやる（ピッタリ自機に付いてくる）
                        self.claw[i].posx = self.claw[i].posx + 0.3 * (self.my_x + self.claw[i].offset_x - self.claw[i].posx)
                        self.claw[i].posy = self.claw[i].posy + 0.3 * (self.my_y + self.claw[i].offset_y - self.claw[i].posy)
                    else:
                        #クローの座標を自機の座標を中心としオフセット値を足した物とする
                        #クローナンバー0と3（後部についてくるクロー）は線形補間値0.2で線形補間してやる（ちょっと遅れて自機に引っ付いてくる）
                        self.claw[i].posx = self.claw[i].posx + 0.2 * (self.my_x + self.claw[i].offset_x - self.claw[i].posx)
                        if self.claw_number == 4:#クローが4機の場合は定着させるＹ座標をそれぞれ変化させる
                            self.claw[i].posy = self.claw[i].posy + 0.2 * (self.my_y + self.claw[i].offset_y + ((i * 3) - 4) - self.claw[i].posy)
                            #クローナンバーi=0の時は(i*3)-4=0*3-4=-4で Y軸の補正値が-4になる
                            #クローナンバーi=3の時は(i*3)-4=3*3-4=+5で Y軸の補正値が+5になる
                        else:#クローが１～３機のときは固定位置は変化させない
                            self.claw[i].posy = self.claw[i].posy + 0.2 * (self.my_y + self.claw[i].offset_y - self.claw[i].posy)

    #クローが弾を発射するのか調べる関数
    def update_check_fire_claw_shot(self):
        if self.replay_status == REPLAY_PLAY: #リプレイステータスが「再生中」の場合は
            if self.replay_data[self.replay_stage_num][self.replay_frame_index + 1] & 0b00010000 == 0b00010000: #LowByte リプレイデータを調べてPAD Aが押された記録だったのなら...
                self.update_fire_claw_shot() #クローショット発射関数呼び出し！
        elif self.move_mode == MOVE_MANUAL: #手動移動モードの場合は
            if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_2_A): #パッドAかスペースキーが押されたか？
                self.update_fire_claw_shot() #クローショット発射関数呼び出し！

    #クローが弾を発射!!!!!!
    def update_fire_claw_shot(self):
            if (pyxel.frame_count % 16) == 0: #16フレーム毎だったら クローショットを育成する
                if len(self.claw_shot) < CLAW_RAPID_FIRE_NUMBER * (self.claw_number):#クローショットの要素数がクローの数x２以下なら弾を発射する
                    #ここからクローが弾を発射する実処理
                    claw_count = len(self.claw)#クローの数を数える
                    for i in range(claw_count):
                        if self.claw[i].status != 0:#ステータスが0の時は初期回転位置や初期固定位置に移動中なので弾は発射しない
                            new_claw_shot = Shot()
                            if self.claw_type == 3:#クロータイプがリバースクローの時はクローショットの方向をreverse_claw_svx,reverse_claw_svyにして8方向弾にする
                                new_claw_shot.update(0,self.claw[i].posx,self.claw[i].posy,    self.reverse_claw_svx,self.reverse_claw_svy,   8,8,   0,  1,1)
                                self.claw_shot.append(new_claw_shot)
                            else:#リバースクロー以外のクローは全て前方に弾を撃つ
                                new_claw_shot.update(0,self.claw[i].posx,self.claw[i].posy,    3,0,   8,8,   0,  1,1)
                                self.claw_shot.append(new_claw_shot)

    #クローショットの更新
    def update_claw_shot(self):
        claw_shot_count = len(self.claw_shot)#クローの弾の数を数える
        for i in reversed(range (claw_shot_count)):
            #クローの弾の位置を更新！
            self.claw_shot[i].posx += self.claw_shot[i].vx * self.claw_shot_speed #弾のX座標をVX*claw_shot_speed分加減算して更新
            self.claw_shot[i].posy += self.claw_shot[i].vy * self.claw_shot_speed #弾のY座標をVY*claw_shot_speed分加減算して更新
            
            if self.claw_shot[i].shot_hp != 0:
                if (-16 < self.claw_shot[i].posx < WINDOW_W + 16 ) and (-16 <self.claw_shot[i].posy < WINDOW_H + 16):
                    continue
                else:
                    del self.claw_shot[i]#クローショットが画面外まで飛んで行ってはみ出ていたのならインスタンス破棄（クローショット消滅）
            else:
                del self.claw_shot[i]#クローショットのHPがゼロだったらインスタンスを破棄する（クローショット消滅）

    #クローショットと敵の当たり判定
    def update_collision_claw_shot_enemy(self):
        claw_shot_hit = len(self.claw_shot)#クローの弾の数を数える
        for h in reversed(range (claw_shot_hit)):
            enemy_hit = len(self.enemy)
            for e in reversed(range (enemy_hit)):
                if     self.enemy[e].posx <= self.claw_shot[h].posx + 4 <= self.enemy[e].posx + self.enemy[e].width\
                    and self.enemy[e].posy <= self.claw_shot[h].posy + 4 <= self.enemy[e].posy + self.enemy[e].height:
                    
                    self.enemy[e].enemy_hp -= self.claw_shot[h].shot_power #敵の耐久力をクローショットパワーの分だけ減らす
                    if self.enemy[e].enemy_hp <= 0:
                        self.enemy_destruction(e) #敵破壊処理関数呼び出し！
                        #パーティクル生成
                        for _number in range(5):
                            self.update_append_particle(PARTICLE_DOT,self.enemy[e].posx + 4,self.enemy[e].posy + 4,self.claw_shot[h].vx / 2,self.claw_shot[h].vy / 2,    0,0,0)
                        
                        del self.enemy[e]#敵リストから破壊した敵をＤＥＬ消去破壊！
                        self.score += 1#スコア加算（あとあといろんなスコアシステム実装する予定だよ）
                    
                    self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにしてクローショット移動時にチェックしリストから消去させるため
                    pyxel.play(0,2)#クローショットが敵を破壊した音！

    #クローショットとボスとの当たり判定
    def update_collision_claw_shot_boss(self):
        claw_shot_hit = len(self.claw_shot)#クローの弾の数を数える
        for h in reversed(range (claw_shot_hit)):
            boss_hit = len(self.boss)
            for e in reversed(range (boss_hit)):
                if self.boss[e].invincible != 1: #もしボスが無敵状態で無いのならば
                    #ボス本体の当たり判定1(クローショットを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main1_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main1_x + self.boss[e].col_main1_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_main1_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main1_y + self.boss[e].col_main1_h\
                        and self.boss[e].col_main1_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.claw_shot[h].posx,self.claw_shot[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定2(クローショットを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main2_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main2_x + self.boss[e].col_main2_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_main2_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main2_y + self.boss[e].col_main2_h\
                        and self.boss[e].col_main2_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.claw_shot[h].posx,self.claw_shot[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定3(クローショットを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main3_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main3_x + self.boss[e].col_main3_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_main3_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main3_y + self.boss[e].col_main3_h\
                        and self.boss[e].col_main3_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.claw_shot[h].posx,self.claw_shot[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定4(クローショットを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main4_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main4_x + self.boss[e].col_main4_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_main4_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main4_y + self.boss[e].col_main4_h\
                        and self.boss[e].col_main4_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.claw_shot[h].posx,self.claw_shot[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定5(クローショットを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main5_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main5_x + self.boss[e].col_main5_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_main5_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main5_y + self.boss[e].col_main5_h\
                        and self.boss[e].col_main5_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.claw_shot[h].posx,self.claw_shot[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定6(クローショットを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main6_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main6_x + self.boss[e].col_main6_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_main6_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main6_y + self.boss[e].col_main6_h\
                        and self.boss[e].col_main6_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.claw_shot[h].posx,self.claw_shot[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定7(クローショットを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main7_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main7_x + self.boss[e].col_main7_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_main7_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main7_y + self.boss[e].col_main7_h\
                        and self.boss[e].col_main7_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.claw_shot[h].posx,self.claw_shot[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ボス本体の当たり判定8(クローショットを消滅させる)との判定
                    if        self.boss[e].posx                   + self.boss[e].col_main8_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_main8_x + self.boss[e].col_main8_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_main8_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_main8_y + self.boss[e].col_main8_h\
                        and self.boss[e].col_main8_w != 0:
                        
                        self.update_append_particle(PARTICLE_LINE,self.claw_shot[h].posx,self.claw_shot[h].posy,0,0, 0,0,0)#ミサイルの位置に消滅エフェクト育成
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    
                    
                    #パーツ１との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts1_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts1_x + self.boss[e].col_parts1_w\
                        and self.boss[e].posy + self.boss[e].col_parts1_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts1_y + self.boss[e].col_parts1_h\
                        and self.boss[e].parts1_flag == 1:
                        
                        self.boss[e].parts1_hp -= self.claw_shot[h].shot_power #パーツ1の耐久力をshot_powerの分だけ減らす
                        if self.boss[e].parts1_hp <= 0: #パーツ1の耐久力が0以下になったのなら
                            self.boss[e].parts1_flag = 0 #パーツ1の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts1_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ1耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.claw_shot[h].posx,self.claw_shot[h].posy
                        hit_vx,hit_vy = self.claw_shot[h].vx,self.claw_shot[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにクローショットを当てた後の処理の関数を呼び出す！
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する   
                    #パーツ2との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts2_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts2_x + self.boss[e].col_parts2_w\
                        and self.boss[e].posy + self.boss[e].col_parts2_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts2_y + self.boss[e].col_parts2_h\
                        and self.boss[e].parts2_flag == 1:
                        
                        self.boss[e].parts2_hp -= self.claw_shot[h].shot_power #パーツ2の耐久力をshot_powerの分だけ減らす
                        if self.boss[e].parts2_hp <= 0: #パーツ2の耐久力が0以下になったのなら
                            self.boss[e].parts2_flag = 0 #パーツ2の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts2_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ2耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.claw_shot[h].posx,self.claw_shot[h].posy
                        hit_vx,hit_vy = self.claw_shot[h].vx,self.claw_shot[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにクローショットを当てた後の処理の関数を呼び出す！
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する                    
                    #パーツ3との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts3_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts3_x + self.boss[e].col_parts3_w\
                        and self.boss[e].posy + self.boss[e].col_parts3_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts3_y + self.boss[e].col_parts3_h\
                        and self.boss[e].parts3_flag == 1:
                        
                        self.boss[e].parts3_hp -= self.claw_shot[h].shot_power #パーツ3の耐久力をshot_powerの分だけ減らす
                        if self.boss[e].parts3_hp <= 0: #パーツ3の耐久力が0以下になったのなら
                            self.boss[e].parts3_flag = 0 #パーツ3の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts3_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ3耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.claw_shot[h].posx,self.claw_shot[h].posy
                        hit_vx,hit_vy = self.claw_shot[h].vx,self.claw_shot[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにクローショットを当てた後の処理の関数を呼び出す！
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する                  
                    #パーツ4との当たり判定
                    if        self.boss[e].posx + self.boss[e].col_parts4_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_parts4_x + self.boss[e].col_parts4_w\
                        and self.boss[e].posy + self.boss[e].col_parts4_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_parts4_y + self.boss[e].col_parts4_h\
                        and self.boss[e].parts4_flag == 1:
                        
                        self.boss[e].parts4_hp -= self.claw_shot[h].shot_power #パーツ4の耐久力をshot_powerの分だけ減らす
                        if self.boss[e].parts4_hp <= 0: #パーツ4の耐久力が0以下になったのなら
                            self.boss[e].parts4_flag = 0 #パーツ4の生存フラグを0にして破壊したことにする
                        
                        self.boss[e].display_time_parts4_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #パーツ4耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.claw_shot[h].posx,self.claw_shot[h].posy
                        hit_vx,hit_vy = self.claw_shot[h].vx,self.claw_shot[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにクローショットを当てた後の処理の関数を呼び出す！
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する                  
                    
                    #ダメージポイント1との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point1_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point1_x + self.boss[e].col_damage_point1_w\
                        and self.boss[e].posy - self.claw_shot[h].height  + self.boss[e].col_damage_point1_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point1_y + self.boss[e].col_damage_point1_h\
                        and self.boss[e].col_damage_point1_w != 0:
                        
                        self.boss[e].main_hp -= self.claw_shot[h].shot_power #ボスの耐久力をshot_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.claw_shot[h].posx,self.claw_shot[h].posy
                        hit_vx,hit_vy = self.claw_shot[h].vx,self.claw_shot[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにクローショットを当てた後の処理の関数を呼び出す！
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント2との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point2_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point2_x + self.boss[e].col_damage_point2_w\
                        and self.boss[e].posy - self.claw_shot[h].height + self.boss[e].col_damage_point2_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point2_y + self.boss[e].col_damage_point2_h\
                        and self.boss[e].col_damage_point2_w != 0:
                        
                        self.boss[e].main_hp -= self.claw_shot[h].shot_power #ボスの耐久力をshot_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.claw_shot[h].posx,self.claw_shot[h].posy
                        hit_vx,hit_vy = self.claw_shot[h].vx,self.claw_shot[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにクローショットを当てた後の処理の関数を呼び出す！
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント3との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point3_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point3_x + self.boss[e].col_damage_point3_w\
                        and self.boss[e].posy - self.claw_shot[h].height + self.boss[e].col_damage_point3_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point3_y + self.boss[e].col_damage_point3_h\
                        and self.boss[e].col_damage_point3_w != 0:
                        
                        self.boss[e].main_hp -= self.claw_shot[h].shot_power #ボスの耐久力をshot_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.claw_shot[h].posx,self.claw_shot[h].posy
                        hit_vx,hit_vy = self.claw_shot[h].vx,self.claw_shot[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにクローショットを当てた後の処理の関数を呼び出す！
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する
                    #ダメージポイント4との判定
                    if        self.boss[e].posx                  + self.boss[e].col_damage_point4_x <= self.claw_shot[h].posx + 4 <= self.boss[e].posx + self.boss[e].col_damage_point4_x + self.boss[e].col_damage_point4_w\
                        and self.boss[e].posy - self.claw_shot[h].height + self.boss[e].col_damage_point4_y <= self.claw_shot[h].posy + 4 <= self.boss[e].posy + self.boss[e].col_damage_point4_y + self.boss[e].col_damage_point4_h\
                        and self.boss[e].col_damage_point4_w != 0:
                        
                        self.boss[e].main_hp -= self.claw_shot[h].shot_power #ボスの耐久力をshot_powerの分だけ減らす
                        self.boss[e].display_time_main_hp_bar = BOSS_HP_BAR_DISPLAY_TIME #耐久力バーを表示するカウントタイマーを初期値の定数に戻す
                        hit_x,hit_y = self.claw_shot[h].posx,self.claw_shot[h].posy
                        hit_vx,hit_vy = self.claw_shot[h].vx,self.claw_shot[h].vy
                        self.boss_processing_after_hitting(e,hit_x,hit_y,hit_vx,hit_vy) #ボスにクローショットを当てた後の処理の関数を呼び出す！ 
                        self.claw_shot[h].shot_hp = 0#クローショットのＨＰをゼロにして移動時にチェックしリストから消去させる
                        continue #これ以下の処理はせず次のループへと移行する    

    #クローショットと背景との当たり判定
    def update_collision_claw_shot_bg(self):
        claw_shot_count = len(self.claw_shot)
        for i in reversed(range(claw_shot_count)):
            self.check_bg_collision(self.claw_shot[i].posx,(self.claw_shot[i].posy) + 4,0,0)
            if self.collision_flag == 1:#背景と衝突したのならクローショットを消滅させる
                del self.claw_shot[i]        




class Shot:#自機弾のクラス設定
    def __init__(self) -> None:
        self.shot_type: int = 0
        self.posx: int = 0
        self.posy: int = 0
        self.vx: int = 0
        self.vy: int = 0
        self.width: int = 0
        self.height: int = 0
        self.offset_y: int = 0
        self.shot_power: int = 0
        self.shot_hp: int = 0

    def update(self,shot_type: int, x: int, y: int, vx: int, vy: int, width: int, height: int, offset_y: int, shot_power: int, shot_hp: int) -> None:
        self.shot_type = shot_type
        self.posx = x
        self.posy = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.offset_y = offset_y
        self.shot_power = shot_power
        self.shot_hp = shot_hp


class Missile(Shot):#自機ミサイルのクラス設定
    def __init__(self) -> None:
        self.missile_type: int = 0 #0=右下ミサイル 1=右上ミサイル 2=左下ミサイル 3=左上ミサイル 4=テイルショット 5=ぺネトレートロケット 6=サーチレーザー 7=ホーミングミサイル
        self.posx: int = 0
        self.posy: int = 0
        self.vx: int = 0
        self.vy: int = 0
        self.missile_power: int = 0
        self.missile_hp: int = 0
        self.missile_flag1: int = 0
        self.missile_flag2: int = 0
        self.x_reverse: int = 0
        self.y_reverse: int = 0
        self.width: int = 0
        self.height: int = 0
        self.tx: int = 0
        self.ty: int = 0
        self.theta: int = 0
        self.speed: int = 0

    def update(self,missile_type: int, x: int, y: int, vx: int, vy: int, missile_power: int, missile_hp: int,missile_flag1: int,missile_flag2: int,x_reverse: int,y_reverse: int,width: int,height: int,tx: int,ty: int,theta: int,speed: int) -> None:
        self.missile_type = missile_type
        self.posx = x
        self.posy = y
        self.vx = vx
        self.vy = vy
        self.missile_power = missile_power
        self.missile_hp = missile_hp
        self.missile_flag1 = missile_flag1
        self.missile_flag2 = missile_flag2
        self.x_reverse = x_reverse
        self.y_reverse = y_reverse
        self.width = width
        self.height = height
        self.tx = tx
        self.ty = ty
        self.theta = theta
        self.speed = speed


class Claw(Shot):#クローのクラス設定
    def __init__(self):
        self.number = 0 #クローのIDナンバー 0~3まで
        self.claw_type = 0 #0=ローリングタイプ 1=トレースタイプ 2=フックスタイプ 3=リバースタイプ
        self.status = 0 #0=回転開始や固定開始の初期位置まで動いていく #1==回転中もしくは固定完了
        self.posx = 0#インスタンス育成時は自機のX座標が入る
        self.posy = 0#インスタンス育成時は自機のY座標が入る
        self.roll_vx = 0
        self.roll_vy = 0
        self.fix_vx = 0
        self.fix_vy = 0
        
        self.reverse_vx = 0
        self.reverse_vy = 0
        
        self.offset_x = 0#クローの現時点での座標オフセット値
        self.offset_y = 0
        self.offset_roll_x = 0      #ローリングクローの処理開始の座標（オフセット値）
        self.offset_roll_y = 0
        self.offset_fix_x = 0        #フックスクローの処理開始の間隔倍率を掛けた座標（オフセット値）実際に比較対象になるのはこっちのほう
        self.offset_fix_y = 0
        self.offset_fix_origin_x = 0  #フックスクローの処理開始の間隔倍率を掛ける前の元の座標（オフセット値）
        self.offset_fix_origin_y = 0
        self.offset_reverse_x = 0    #リバースクローの処理開始の座標（オフセット値）
        self.offset_reverse_y = 0
        self.intensity = 0
        self.timer = 0
        self.degree = 0 #回転角度 度数法（主にこちらを使用するのです！）
        self.radian = 0 #回転角度 弧度法
        self.speed = 0 #回転スピード(弧度法0~360度)
        self.radius = 0 #半径
        self.degree_interval = 0 #クローの個数に応じた回転間隔(1個=設定なし 2個=180度 3個=120度 4個=90度)
        self.angle_difference = 0 #ひとつ前のクローとの回転角度の差（この値がdegree_intarvalと同じ数値になるまで回転スピードを増減させていく）
        self.shot_type = 0
        self.shot_power = 0
        self.animation_number = 0

    def update(self,number,claw_type,status,x,y,roll_vx,roll_vy,fix_vx,fix_vy,reverse_vx,reverse_vy,offset_x,offset_y,offset_roll_x,offset_roll_y,offset_fix_x,offset_fix_y,offset_fix_origin_x,offset_fix_origin_y,offset_reverse_x,offset_reverse_y,intensity,timer,degree,radian,speed,radius,degree_interval,angle_difference,shot_type,shot_power,animation_number):
        self.number = number
        self.claw_type = claw_type
        self.status = status
        self.posx = x
        self.posy = y
        self.roll_vx = roll_vx
        self.roll_vy = roll_vy
        self.fix_vx = fix_vx
        self.fix_vy = fix_vy
        self.reverse_vx = reverse_vx
        self.reverse_vy = reverse_vy
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_roll_x = offset_roll_x
        self.offset_roll_y = offset_roll_y
        self.offset_fix_x = offset_fix_x
        self.offset_fix_y = offset_fix_y
        self.offset_fix_origin_x = offset_fix_origin_x
        self.offset_fix_origin_y = offset_fix_origin_y
        self.offset_reverse_x = offset_reverse_x
        self.offset_reverse_y = offset_reverse_y
        self.intensity = intensity
        self.timer = timer
        self.degree = degree
        self.radian = radian
        self.speed = speed
        self.radius = radius
        self.degree_interval = degree_interval
        self.angle_difference = angle_difference
        self.shot_type = shot_type
        self.shot_power = shot_power
        self.animation_number = animation_number

class Trace_coordinates:#トレースクロー（オプション）座標のクラス設定
    def __init__(self):
        self.posx = 0 #自機のx座標をオプションのx座標としてコピーして使用する
        self.posy = 0 #自機のy座標をオプションのy座標としてコピーして使用する

    def update(self, ox, oy):
        self.posx = ox
        self.posy = oy

class Claw_shot:#クローショット（クローの弾）のクラス設定
    def __init__(self):
        self.shot_type = 0
        self.posx = 0
        self.posy = 0
        self.vx = 0
        self.vy = 0
        self.width = 0
        self.height = 0
        self.offset_x = 0
        self.offset_y = 0
        self.shot_power = 0
        self.shot_hp = 0

    def update(self,shot_type, x , y, vx, vy, width, height, offset_x, offset_y, shot_power, shot_hp):
        self.shot_type = shot_type
        self.posx = x
        self.posy = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.offseet_x = offset_x
        self.offset_y = offset_y
        self.shot_power = shot_power
        self.shot_hp = shot_hp


class Enemy(Ship):#敵キャラ達のクラス設定
    def __init__(self):
        self.enemy_type = 0    #敵のタイプ
        self.enemy_id = 0     #敵のIDナンバー
        self.status = 0       #敵の状態
        self.attack_method = 0 #敵の攻撃方法
        self.posx = 0 #敵の位置座標(x,y)
        self.posy = 0
        self.offset_x = 0 #座標オフセット値
        self.offset_y = 0
        self.offset_p1x = 0 #パーツ1のオフセット座標値(p1x,p1y)
        self.offset_p1y = 0
        self.offset_p2x = 0 #パーツ2のオフセット座標値(p2x,p2y)
        self.offset_p2y = 0
        self.offset_p3x = 0 #パーツ3のオフセット座標値(p3x,p3y)
        self.offset_p3y = 0
        self.offset_p4x = 0 #パーツ4のオフセット座標値(p4x,p4y)
        self.offset_p4y = 0
        
        self.ax = 0 #移動元の座標
        self.ay = 0
        self.bx = 0 #予約座標1
        self.by = 0
        self.cx = 0 #予約座標2
        self.cy = 0 
        self.dx = 0 #移動先の座標(destination_x,y)
        self.dy = 0
        self.qx = 0 #2次ベジェ曲線の制御点qとして使用
        self.qy = 0
        self.vx = 0 #敵の速度ベクトル(vx,vy)
        self.vy = 0
        
        
        self.o1x = 0 #移動元の座標1(origin1_x,y)(リストを使わずにインスタンス育成時に座標を指定してベジェ曲線移動するときに使うメンバ変数)とりあえず5点まで移動できるように変数を確保してます
        self.o1y = 0 
        self.d1x = 0 #移動先の座標1(destination1_x,y)
        self.d1y = 0
        self.q1x = 0 #2次ベジェ曲線の制御点q1として使用
        self.q1y = 0
        self.a1  = 0 #加速度(acceleration1)
        
        self.o2x = 0 #移動元の座標2(origin2_x,y)
        self.o2y = 0 
        self.d2x = 0 #移動先の座標2(destination2_x,y)
        self.d2y = 0
        self.q2x = 0 #2次ベジェ曲線の制御点q2として使用
        self.q2y = 0
        self.a2  = 0 #加速度(acceleration2)
        
        self.o3x = 0 #移動元の座標3(origin3_x,y)
        self.o3y = 0 
        self.d3x = 0 #移動先の座標3(destination3_x,y)
        self.d3y = 0
        self.q3x = 0 #2次ベジェ曲線の制御点q3として使用
        self.q3y = 0
        self.a3  = 0 #加速度(acceleration3)
        
        self.o4x = 0 #移動元の座標4(origin4_x,y)
        self.o4y = 0 
        self.d4x = 0 #移動先の座標4(destination4_x,y)
        self.d4y = 0
        self.q4x = 0 #2次ベジェ曲線の制御点q4として使用
        self.q4y = 0
        self.a4  = 0 #加速度(acceleration4)
        
        self.o5x = 0 #移動元の座標5(origin5_x,y)
        self.o5y = 0 
        self.d5x = 0 #移動先の座標5(destination5_x,y)
        self.d5y = 0
        self.q5x = 0 #2次ベジェ曲線の制御点q5として使用
        self.q5y = 0
        self.a5  = 0 #加速度(acceleration5)      
        
        self.width = 0  #敵の横幅
        self.height = 0 #敵の縦幅
        self.move_speed       = 0 #敵の全体的な移動スピード
        self.move_speed_offset = 0 #敵の全体的な移動スピード(オフセット値)move_speedとかけ合わせたり加減算したりしてスピードを変化とか出来そう
        self.direction = 0    #敵の移動方向
        self.enemy_hp = 0    #敵の耐久力
        self.enemy_flag1 = 0  #フラグ用その1
        self.enemy_flag2 = 0  #フラグ用その２
        self.enemy_size = 0   #敵の全体的な大きさ
        self.enemy_count1 = 0 #汎用カウンタその1
        self.enemy_count2 = 0 #汎用カウンタその2
        self.enemy_count3 = 0 #汎用カウンタその3
        self.parts1_flag = 0 #各部位用のフラグ
        self.parts2_flag = 0
        self.parts3_flag = 0
        self.parts4_flag = 0
        self.item = 0         #0=パワーアップアイテム未所持 1=ショットアイテム 2=ミサイルアイテム 3=シールドアイテム
                            #これ以外の項目については敵キャラが持っているアイテム類のＩＤを参照してね
        self.formation_id = 0   #単独機の場合は0 1番最初に出現した編隊群は1 2番目に出現した編隊群2 3番目の編隊は3 みたいな感じで数値が代入される
        self.timer       = 0   #時間(三角関数系で使用)
        self.speed       = 0   #速度(三角関数系で使用)
        self.intensity    = 0   #振れ幅(三角関数系で使用)
        self.acceleration  = 0  #加速度
        self.move_index    = 0  #2次ベジェ曲線での移動用リストを参照するときに使用するインデックス値（リストの添え字に入る数値）
        self.obj_time     = 0  #2次ベジェ曲線での移動用のtime（現在のタイムフレーム番号が入る）(0~totaltimeまで変化する)ピエール・ベジェさんありがとう・・・
        self.obj_totaltime = 0  #2次ベジェ曲線での移動用のtotaltime（移動元から移動先までに掛けるトータルフレーム数が入る60なら1秒掛けて移動元から移動先まで移動するって事,120なら2秒かかる)
        self.color        = 0  #色
        self.floating_flag = 0  #地上物か空中物かどうかのフラグ 0=空中物 1=地上物 2=地上を移動する物体(装甲車とか)
        self.score_normal  = 0  #通常時の得点
        self.score_attack  = 0  #攻撃時の得点
        self.score_escape  = 0  #撤退時の得点
        self.score_awaiting = 0 #待機中の得点
        self.score_defense  = 0 #防御中の得点
        self.score_berserk  = 0 #怒り状態の得点

    def update(self,enemy_type,enemy_id,status,attack_method,
            x, y,
            offset_x,offset_y,
            offset_p1x,offset_p1y,
            offset_p2x,offset_p2y,
            offset_p3x,offset_p3y,
            offset_p4x,offset_p4y,
            ax,ay,bx,by,cx,cy,dx,dy,qx,qy,
            vx, vy,
            
            o1x,o1y,d1x,d1y,q1x,q1y,a1,
            o2x,o2y,d2x,d2y,q2x,q2y,a2,
            o3x,o3y,d3x,d3y,q3x,q3y,a3,
            o4x,o4y,d4x,d4y,q4x,q4y,a4,
            o5x,o5y,d5x,d5y,q5x,q5y,a5,
            
            width, height,
            move_speed,move_speed_offset,
            direction,
            enemy_hp,
            enemy_flag1, enemy_flag2,
            enemy_size,
            enemy_count1, enemy_count2, enemy_count3,
            parts1_flag,parts2_flag,parts3_flag,parts4_flag,
            
            item,formation_id,
            timer,speed,intensity,
            acceleration,
            move_index,obj_time,obj_totaltime,
            color,floating_flag,
            score_normal,score_attack,score_escape,score_awaiting,score_defense,score_berserk):
        self.enemy_type = enemy_type
        self.enemy_id = enemy_id
        self.status = status
        self.attack_method = attack_method
        self.posx = x
        self.posy = y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.offset_p1x = offset_p1x
        self.offset_p1y = offset_p1y
        self.offset_p2x = offset_p2x
        self.offset_p2y = offset_p2y
        self.offset_p3x = offset_p3x
        self.offset_p3y = offset_p3y
        self.offset_p4x = offset_p4x
        self.offset_p4y = offset_p4y
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.cx = cx
        self.cy = cy        
        self.dx = dx
        self.dy = dy
        self.qx = qx
        self.qy = qy
        self.vx = vx
        self.vy = vy
        
        self.o1x = o1x
        self.o1y = o1y 
        self.d1x = d1x
        self.d1y = d1y
        self.q1x = q1x
        self.q1y = q1y
        self.a1  = a1
        
        self.o2x = o2x
        self.o2y = o2y 
        self.d2x = d2x
        self.d2y = d2y
        self.q2x = q2x
        self.q2y = q2y
        self.a2  = a2
        
        self.o3x = o3x
        self.o3y = o3y 
        self.d3x = d3x
        self.d3y = d3y
        self.q3x = q3x
        self.q3y = q3y
        self.a3  = a3
        
        self.o4x = o4x
        self.o4y = o4y 
        self.d4x = d4x
        self.d4y = d4y
        self.q4x = q4x
        self.q4y = q4y
        self.a4  = a4
        
        self.o5x = o5x
        self.o5y = o5y 
        self.d5x = d5x
        self.d5y = d5y
        self.q5x = q5x
        self.q5y = q5y
        self.a5  = a5
        
        self.width = width
        self.height = height
        self.move_speed = move_speed
        self.move_speed_offset = move_speed_offset
        self.direction = direction
        self.enemy_hp = enemy_hp
        self.enemy_flag1 = enemy_flag1
        self.enemy_flag2 = enemy_flag2
        self.enemy_size = enemy_size
        self.enemy_count1 = enemy_count1
        self.enemy_count2 = enemy_count2
        self.enemy_count3 = enemy_count3
        self.parts1_flag = parts1_flag
        self.parts2_flag = parts2_flag
        self.parts3_flag = parts3_flag
        self.parts4_flag = parts4_flag
        self.item = item
        self.formation_id = formation_id
        self.timer = timer
        self.speed = speed
        self.intensity = intensity
        self.acceleration  = acceleration
        self.move_index    = move_index
        self.obj_time     = obj_time
        self.obj_totaltime = obj_totaltime
        self.color = color
        self.floating_flag  = floating_flag
        self.score_normal   = score_normal
        self.score_attack   = score_attack
        self.score_escape   = score_escape
        self.score_awaiting = score_awaiting
        self.score_defense  = score_defense
        self.score_berserk  = score_berserk

class Boss:#ボスキャラのクラス設定
    def __init__(self):
        self.boss_id = 0
        self.boss_type = 0
        self.status = 0
        self.parts_number = 0 #破壊可能部位の数 0なら本体のみ 1なら破壊可能部位が1箇所あり 4なら4箇所あるという事です
        self.main_hp   = 0    #本体の耐久力
        self.parts1_hp = 0    #各部位の耐久力(1~4)
        self.parts2_hp = 0
        self.parts3_hp = 0
        self.parts4_hp = 0
        self.parts5_hp = 0
        self.parts6_hp = 0
        self.parts7_hp = 0
        self.parts8_hp = 0
        self.parts9_hp = 0
        self.parts1_score = 0 #各パーツを破壊した時の得点
        self.parts2_score = 0
        self.parts3_score = 0
        self.parts4_score = 0
        self.parts5_score = 0
        self.parts6_score = 0
        self.parts7_score = 0
        self.parts8_score = 0
        self.parts9_score = 0
        self.level = 0 #レベル
        self.weapon1_status,self.weapon1_interval,self.weapon1_rapid_num,self.weapon1_cool_down_time,self.weapon1_omen_count = 0,0,0,0,0 #武器1の状態,発射間隔,連射数,次に発射できるまでの時間(クールタイム),予兆エフェクトカウンター
        self.weapon2_status,self.weapon2_interval,self.weapon2_rapid_num,self.weapon2_cool_down_time,self.weapon2_omen_count = 0,0,0,0,0 #武器2の状態,発射間隔,連射数,次に発射できるまでの時間(クールタイム),予兆エフェクトカウンター
        self.weapon3_status,self.weapon3_interval,self.weapon3_rapid_num,self.weapon3_cool_down_time,self.weapon3_omen_count = 0,0,0,0,0 #武器3の状態,発射間隔,連射数,次に発射できるまでの時間(クールタイム),予兆エフェクトカウンター
        self.weapon4_status,self.weapon4_interval,self.weapon4_rapid_num,self.weapon4_cool_down_time,self.weapon4_omen_count = 0,0,0,0,0 #武器4の状態,発射間隔,連射数,次に発射できるまでの時間(クールタイム),予兆エフェクトカウンター
        self.weapon5_status,self.weapon5_interval,self.weapon5_rapid_num,self.weapon5_cool_down_time,self.weapon5_omen_count = 0,0,0,0,0 #武器5の状態,発射間隔,連射数,次に発射できるまでの時間(クールタイム),予兆エフェクトカウンター
        self.posy = 0
        self.offset_x = 0 #座標オフセット値
        self.offset_y = 0
        self.ax = 0 #移動元の座標
        self.ay = 0
        self.bx = 0
        self.by = 0
        self.cx = 0
        self.cy = 0 
        self.dx = 0 #移動先の座標(destination_x,y)
        self.dy = 0
        self.qx = 0 #2次ベジェ曲線の制御点qとして使用
        self.qy = 0
        self.vx = 0 #速度
        self.vy = 0
        self.width = 0  #画像の横の大きさ
        self.height = 0 #画像の縦の大きさ
        
        self.col_damage_point1_x,self.col_damage_point1_y = 0,0 #ボスの弱点位置1 始点x,y座標
        self.col_damage_point1_w,self.col_damage_point1_h = 0,0 #    弱点位置1 横の長さ,縦の長さ w=0の場合は当たり判定として使用しない
        
        self.col_damage_point2_x,self.col_damage_point2_y = 0,0 #ボスの弱点位置2 始点x,y座標
        self.col_damage_point2_w,self.col_damage_point2_h = 0,0 #    弱点位置2 横の長さ,縦の長さ w=0の場合は当たり判定として使用しない
        
        self.col_damage_point3_x,self.col_damage_point3_y = 0,0 #ボスの弱点位置3 始点x,y座標
        self.col_damage_point3_w,self.col_damage_point3_h = 0,0 #    弱点位置3 横の長さ,縦の長さ w=0の場合は当たり判定として使用しない
        
        self.col_damage_point4_x,self.col_damage_point4_y = 0,0 #ボスの弱点位置3 始点x,y座標
        self.col_damage_point4_w,self.col_damage_point4_h = 0,0 #    弱点位置3 横の長さ,縦の長さ w=0の場合は当たり判定として使用しない
        
        self.col_main1_x = 0 #本体1当たり判定の始点x
        self.col_main1_y = 0 #             始点y          
        self.col_main1_w = 0 #            横の長さ 横の長さが0の場合は当たり判定として使用しない
        self.col_main1_h = 0 #            縦の長さ
        
        self.col_main2_x = 0 #本体2当たり判定の始点x
        self.col_main2_y = 0 #             始点y          
        self.col_main2_w = 0 #            横の長さ 横の長さが0の場合は当たり判定として使用しない
        self.col_main2_h = 0 #            縦の長さ
        
        self.col_main3_x = 0 #本体3当たり判定の始点x
        self.col_main3_y = 0 #             始点y          
        self.col_main3_w = 0 #            横の長さ 横の長さが0の場合は当たり判定として使用しない
        self.col_main3_h = 0 #            縦の長さ
        
        self.col_main4_x = 0 #本体4当たり判定の始点x
        self.col_main4_y = 0 #             始点y          
        self.col_main4_w = 0 #            横の長さ 横の長さが0の場合は当たり判定として使用しない
        self.col_main4_h = 0 #            縦の長さ
        
        self.col_main5_x = 0 #本体5当たり判定の始点x
        self.col_main5_y = 0 #             始点y          
        self.col_main5_w = 0 #            横の長さ 横の長さが0の場合は当たり判定として使用しない
        self.col_main5_h = 0 #            縦の長さ
        
        self.col_main6_x = 0 #本体6当たり判定の始点x
        self.col_main6_y = 0 #             始点y          
        self.col_main6_w = 0 #            横の長さ 横の長さが0の場合は当たり判定として使用しない
        self.col_main6_h = 0 #            縦の長さ
        
        self.col_main7_x = 0 #本体7当たり判定の始点x
        self.col_main7_y = 0 #             始点y          
        self.col_main7_w = 0 #            横の長さ 横の長さが0の場合は当たり判定として使用しない
        self.col_main7_h = 0 #            縦の長さ
        
        self.col_main8_x = 0 #本体8当たり判定の始点x
        self.col_main8_y = 0 #             始点y          
        self.col_main8_w = 0 #            横の長さ 横の長さが0の場合は当たり判定として使用しない
        self.col_main8_h = 0 #            縦の長さ
        
        
        self.col_parts1_x = 0 #パーツ1当たり判定の始点x
        self.col_parts1_y = 0 #パーツ1当たり判定の始点y          
        self.col_parts1_w = 0 #パーツ1当たり判定(横の長さ）
        self.col_parts1_h = 0 #パーツ1当たり判定(縦の長さ)
        
        self.col_parts2_x = 0 #パーツ2当たり判定の始点x
        self.col_parts2_y = 0 #パーツ2当たり判定の始点y          
        self.col_parts2_w = 0 #パーツ2当たり判定(横の長さ）
        self.col_parts2_h = 0 #パーツ2当たり判定(縦の長さ)
        
        self.col_parts3_x = 0 #パーツ3当たり判定の始点x
        self.col_parts3_y = 0 #パーツ3当たり判定の始点y          
        self.col_parts3_w = 0 #パーツ3当たり判定(横の長さ）
        self.col_parts3_h = 0 #パーツ3当たり判定(縦の長さ)
        
        self.col_parts4_x = 0 #パーツ4当たり判定の始点x
        self.col_parts4_y = 0 #パーツ4当たり判定の始点y          
        self.col_parts4_w = 0 #パーツ4当たり判定(横の長さ）
        self.col_parts4_h = 0 #パーツ4当たり判定(縦の長さ)
        
        self.col_parts5_x = 0 #パーツ5当たり判定の始点x
        self.col_parts5_y = 0 #パーツ5当たり判定の始点y          
        self.col_parts5_w = 0 #パーツ5当たり判定(横の長さ）
        self.col_parts5_h = 0 #パーツ5当たり判定(縦の長さ)
        
        self.col_parts6_x = 0 #パーツ6当たり判定の始点x
        self.col_parts6_y = 0 #パーツ6当たり判定の始点y          
        self.col_parts6_w = 0 #パーツ6当たり判定(横の長さ）
        self.col_parts6_h = 0 #パーツ6当たり判定(縦の長さ)
        
        self.col_parts7_x = 0 #パーツ7当たり判定の始点x
        self.col_parts7_y = 0 #パーツ7当たり判定の始点y          
        self.col_parts7_w = 0 #パーツ7当たり判定(横の長さ）
        self.col_parts7_h = 0 #パーツ7当たり判定(縦の長さ)
        
        self.col_parts8_x = 0 #パーツ8当たり判定の始点x
        self.col_parts8_y = 0 #パーツ8当たり判定の始点y          
        self.col_parts8_w = 0 #パーツ8当たり判定(横の長さ）
        self.col_parts8_h = 0 #パーツ8当たり判定(縦の長さ)
        
        self.col_parts9_x = 0 #パーツ9当たり判定の始点x
        self.col_parts9_y = 0 #パーツ9当たり判定の始点y          
        self.col_parts9_w = 0 #パーツ9当たり判定(横の長さ）
        self.col_parts9_h = 0 #パーツ9当たり判定(縦の長さ)
        
        self.main_hp_bar_offset_x,  self.main_hp_bar_offset_y   = 0,0 #本体のHPバーを表示する座標のオフセット値
        
        self.parts1_hp_bar_offset_x,self.parts1_hp_bar_offset_y = 0,0 #パーツ1のHPバーを表示する座標のオフセット値
        self.parts2_hp_bar_offset_x,self.parts2_hp_bar_offset_y = 0,0 #パーツ2のHPバーを表示する座標のオフセット値
        self.parts3_hp_bar_offset_x,self.parts3_hp_bar_offset_y = 0,0 #パーツ3のHPバーを表示する座標のオフセット値
        self.parts4_hp_bar_offset_x,self.parts4_hp_bar_offset_y = 0,0 #パーツ4のHPバーを表示する座標のオフセット値
        self.parts5_hp_bar_offset_x,self.parts5_hp_bar_offset_y = 0,0 #パーツ5のHPバーを表示する座標のオフセット値
        self.parts6_hp_bar_offset_x,self.parts6_hp_bar_offset_y = 0,0 #パーツ6のHPバーを表示する座標のオフセット値
        self.parts7_hp_bar_offset_x,self.parts7_hp_bar_offset_y = 0,0 #パーツ7のHPバーを表示する座標のオフセット値
        self.parts8_hp_bar_offset_x,self.parts8_hp_bar_offset_y = 0,0 #パーツ8のHPバーを表示する座標のオフセット値
        self.parts9_hp_bar_offset_x,self.parts9_hp_bar_offset_y = 0,0 #パーツ9のHPバーを表示する座標のオフセット値
        
        self.size = 0        #大きさ
        self.priority = 0     #画像表示時の優先度
        self.attack_method = 0 #攻撃方法
        self.direction = 0    #方向
        self.acceleration = 0  #加速度
        self.timer = 0    #時間
        self.degree = 0   #回転角度 度数法（主にこちらを使用するのです！）
        self.radian = 0   #回転角度 弧度法
        self.speed = 0    #回転スピード(弧度法0~360度)
        self.radius = 0   #半径
        self.flag1 = 0    #フラグ類
        self.flag2 = 0
        self.flag3 = 0
        self.flag4 = 0
        self.count1 = 0   #カウンター類
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.parts1_flag = 0 #各部位用のフラグ
        self.parts2_flag = 0
        self.parts3_flag = 0
        self.parts4_flag = 0
        self.parts5_flag = 0
        self.parts6_flag = 0
        self.parts7_flag = 0
        self.parts8_flag = 0
        self.parts9_flag = 0
        self.animation_number1 = 0 #アニメーションパターンナンバー用
        self.animation_number2 = 0
        self.animation_number3 = 0
        self.animation_number4 = 0
        self.move_index = 0    #移動用のインデックス（リストの添え字に入る数値）
        self.obj_time = 0      #2次ベジェ曲線での移動用のtime（現在のタイムフレーム番号が入る）(0~totaltimeまで変化する)ピエール・ベジェさんありがとう・・・
        self.obj_totaltime = 0  #2次ベジェ曲線での移動用のtotaltime（移動元から移動先までに掛けるトータルフレーム数が入る60なら1秒掛けて移動元から移動先まで移動するって事,120なら2秒かかる)
        self.invincible = 0    #無敵状態かどうかのフラグ(出現時は無敵にするとかで使うかも？)
        self.display_time_main_hp_bar   = 0 #耐久力ゲージをどれだけの時間表示させるかのカウント 1=60ミリ秒
        self.display_time_parts1_hp_bar = 0
        self.display_time_parts2_hp_bar = 0
        self.display_time_parts3_hp_bar = 0
        self.display_time_parts4_hp_bar = 0
        self.display_time_parts5_hp_bar = 0
        self.display_time_parts6_hp_bar = 0
        self.display_time_parts7_hp_bar = 0
        self.display_time_parts8_hp_bar = 0
        self.display_time_parts9_hp_bar = 0

    def update(self,boss_id,boss_type,status,parts_number,
            main_hp,
            parts1_hp,parts2_hp,parts3_hp,
            parts4_hp,parts5_hp,parts6_hp,
            parts7_hp,parts8_hp,parts9_hp,
            parts1_score,parts2_score,parts3_score,
            parts4_score,parts5_score,parts6_score,
            parts7_score,parts8_score,parts9_score,
            level,
            
            weapon1_status,weapon1_interval,weapon1_rapid_num,weapon1_cool_down_time,weapon1_omen_count,
            weapon2_status,weapon2_interval,weapon2_rapid_num,weapon2_cool_down_time,weapon2_omen_count,
            weapon3_status,weapon3_interval,weapon3_rapid_num,weapon3_cool_down_time,weapon3_omen_count,
            weapon4_status,weapon4_interval,weapon4_rapid_num,weapon4_cool_down_time,weapon4_omen_count,
            weapon5_status,weapon5_interval,weapon5_rapid_num,weapon5_cool_down_time,weapon5_omen_count,
            x,y,offset_x,offset_y,ax,ay,bx,by,cx,cy,dx,dy,qx,qy,vx,vy,
            width,height,
            
            col_damage_point1_x,col_damage_point1_y,col_damage_point1_w,col_damage_point1_h,
            col_damage_point2_x,col_damage_point2_y,col_damage_point2_w,col_damage_point2_h,
            col_damage_point3_x,col_damage_point3_y,col_damage_point3_w,col_damage_point3_h,
            col_damage_point4_x,col_damage_point4_y,col_damage_point4_w,col_damage_point4_h,
            
            col_main1_x ,col_main1_y ,col_main1_w ,col_main1_h,
            col_main2_x ,col_main2_y ,col_main2_w ,col_main2_h,
            col_main3_x ,col_main3_y ,col_main3_w ,col_main3_h,
            col_main4_x ,col_main4_y ,col_main4_w ,col_main4_h,
            col_main5_x ,col_main5_y ,col_main5_w ,col_main5_h,
            col_main6_x ,col_main6_y ,col_main6_w ,col_main6_h,
            col_main7_x ,col_main7_y ,col_main7_w ,col_main7_h,
            col_main8_x ,col_main8_y ,col_main8_w ,col_main8_h,
            
            col_parts1_x,col_parts1_y,col_parts1_w,col_parts1_h,
            col_parts2_x,col_parts2_y,col_parts2_w,col_parts2_h,
            col_parts3_x,col_parts3_y,col_parts3_w,col_parts3_h,
            col_parts4_x,col_parts4_y,col_parts4_w,col_parts4_h,
            col_parts5_x,col_parts5_y,col_parts5_w,col_parts5_h,
            col_parts6_x,col_parts6_y,col_parts6_w,col_parts6_h,
            col_parts7_x,col_parts7_y,col_parts7_w,col_parts7_h,
            col_parts8_x,col_parts8_y,col_parts8_w,col_parts8_h,
            col_parts9_x,col_parts9_y,col_parts9_w,col_parts9_h,
            
            main_hp_bar_offset_x,main_hp_bar_offset_y,
            
            parts1_hp_bar_offset_x,parts1_hp_bar_offset_y,
            parts2_hp_bar_offset_x,parts2_hp_bar_offset_y,
            parts3_hp_bar_offset_x,parts3_hp_bar_offset_y,
            parts4_hp_bar_offset_x,parts4_hp_bar_offset_y,
            parts5_hp_bar_offset_x,parts5_hp_bar_offset_y,
            parts6_hp_bar_offset_x,parts6_hp_bar_offset_y,
            parts7_hp_bar_offset_x,parts7_hp_bar_offset_y,
            parts8_hp_bar_offset_x,parts8_hp_bar_offset_y,
            parts9_hp_bar_offset_x,parts9_hp_bar_offset_y,
            
            size,priority,attack_method,direction,acceleration,timer,degree,radian,speed,radius,
            flag1,flag2,flag3,flag4,
            count1,count2,count3,count4,
            parts1_flag,parts2_flag,parts3_flag,
            parts4_flag,parts5_flag,parts6_flag,
            parts7_flag,parts8_flag,parts9_flag,
            animation_number1,animation_number2,animation_number3,animation_number4,
            move_index,
            obj_time,obj_totaltime,
            invincible,
            display_time_main_hp_bar,
            display_time_parts1_hp_bar,display_time_parts2_hp_bar,display_time_parts3_hp_bar,
            display_time_parts4_hp_bar,display_time_parts5_hp_bar,display_time_parts6_hp_bar,
            display_time_parts7_hp_bar,display_time_parts8_hp_bar,display_time_parts9_hp_bar,
            ):
        self.boss_id = boss_id
        self.boss_type = boss_type
        self.status = status
        self.parts_number = parts_number
        self.main_hp = main_hp
        self.parts1_hp = parts1_hp
        self.parts2_hp = parts2_hp
        self.parts3_hp = parts3_hp
        self.parts4_hp = parts4_hp
        self.parts5_hp = parts5_hp
        self.parts6_hp = parts6_hp
        self.parts7_hp = parts7_hp
        self.parts8_hp = parts8_hp
        self.parts9_hp = parts9_hp
        self.parts1_score = parts1_score
        self.parts2_score = parts2_score
        self.parts3_score = parts3_score
        self.parts4_score = parts4_score
        self.parts5_score = parts5_score
        self.parts6_score = parts6_score
        self.parts7_score = parts7_score
        self.parts8_score = parts8_score
        self.parts9_score = parts9_score
        self.level = level
        
        self.weapon1_status        = weapon1_status
        self.weapon1_interval      = weapon1_interval
        self.weapon1_rapid_num     = weapon1_rapid_num
        self.weapon1_cool_down_time = weapon1_cool_down_time
        self.weapon1_omen_count    = weapon1_omen_count  
        
        self.weapon2_status        = weapon2_status
        self.weapon2_interval      = weapon2_interval
        self.weapon2_rapid_num     = weapon2_rapid_num
        self.weapon2_cool_down_time = weapon2_cool_down_time
        self.weapon2_omen_count    = weapon2_omen_count  
        
        self.weapon3_status        = weapon3_status
        self.weapon3_interval      = weapon3_interval
        self.weapon3_rapid_num     = weapon3_rapid_num
        self.weapon3_cool_down_time = weapon3_cool_down_time
        self.weapon3_omen_count    = weapon3_omen_count  
        
        self.weapon4_status        = weapon4_status
        self.weapon4_interval      = weapon4_interval
        self.weapon4_rapid_num     = weapon4_rapid_num
        self.weapon4_cool_down_time = weapon4_cool_down_time
        self.weapon4_omen_count    = weapon4_omen_count  
        
        self.weapon5_status        = weapon5_status
        self.weapon5_interval      = weapon5_interval
        self.weapon5_rapid_num     = weapon5_rapid_num
        self.weapon5_cool_down_time = weapon5_cool_down_time
        self.weapon5_omen_count    = weapon5_omen_count  
        
        self.posx = x
        self.posy = y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.ax = ax
        self.ay = ay
        self.bx = bx
        self.by = by
        self.cx = cx
        self.cy = cy        
        self.dx = dx
        self.dy = dy
        self.qx = qx
        self.qy = qy
        self.vx = vx
        self.vy = vy
        self.width = width 
        self.height = height
        
        self.col_damage_point1_x = col_damage_point1_x
        self.col_damage_point1_y = col_damage_point1_y
        self.col_damage_point1_w = col_damage_point1_w
        self.col_damage_point1_h = col_damage_point1_h
        
        self.col_damage_point2_x = col_damage_point2_x
        self.col_damage_point2_y = col_damage_point2_y
        self.col_damage_point2_w = col_damage_point2_w
        self.col_damage_point2_h = col_damage_point2_h
        
        self.col_damage_point3_x = col_damage_point3_x
        self.col_damage_point3_y = col_damage_point3_y
        self.col_damage_point3_w = col_damage_point3_w
        self.col_damage_point3_h = col_damage_point3_h
        
        self.col_damage_point4_x = col_damage_point4_x
        self.col_damage_point4_y = col_damage_point4_y
        self.col_damage_point4_w = col_damage_point4_w
        self.col_damage_point4_h = col_damage_point4_h
        
        self.col_main1_x = col_main1_x
        self.col_main1_y = col_main1_y
        self.col_main1_w = col_main1_w
        self.col_main1_h = col_main1_h
        
        self.col_main2_x = col_main2_x
        self.col_main2_y = col_main2_y
        self.col_main2_w = col_main2_w
        self.col_main2_h = col_main2_h
        
        self.col_main3_x = col_main3_x
        self.col_main3_y = col_main3_y
        self.col_main3_w = col_main3_w
        self.col_main3_h = col_main3_h
        
        self.col_main4_x = col_main4_x
        self.col_main4_y = col_main4_y
        self.col_main4_w = col_main4_w
        self.col_main4_h = col_main4_h
        
        self.col_main5_x = col_main5_x
        self.col_main5_y = col_main5_y
        self.col_main5_w = col_main5_w
        self.col_main5_h = col_main5_h
        
        self.col_main6_x = col_main6_x
        self.col_main6_y = col_main6_y
        self.col_main6_w = col_main6_w
        self.col_main6_h = col_main6_h
        
        self.col_main7_x = col_main7_x
        self.col_main7_y = col_main7_y
        self.col_main7_w = col_main7_w
        self.col_main7_h = col_main7_h
        
        self.col_main8_x = col_main8_x
        self.col_main8_y = col_main8_y
        self.col_main8_w = col_main8_w
        self.col_main8_h = col_main8_h
        
        self.col_parts1_x = col_parts1_x
        self.col_parts1_y = col_parts1_y
        self.col_parts1_w = col_parts1_w
        self.col_parts1_h = col_parts1_h
        
        self.col_parts2_x = col_parts2_x
        self.col_parts2_y = col_parts2_y
        self.col_parts2_w = col_parts2_w
        self.col_parts2_h = col_parts2_h
        
        self.col_parts3_x = col_parts3_x
        self.col_parts3_y = col_parts3_y
        self.col_parts3_w = col_parts3_w
        self.col_parts3_h = col_parts3_h
        
        self.col_parts4_x = col_parts4_x
        self.col_parts4_y = col_parts4_y
        self.col_parts4_w = col_parts4_w
        self.col_parts4_h = col_parts4_h
        
        self.col_parts5_x = col_parts5_x
        self.col_parts5_y = col_parts5_y
        self.col_parts5_w = col_parts5_w
        self.col_parts5_h = col_parts5_h
        
        self.col_parts6_x = col_parts6_x
        self.col_parts6_y = col_parts6_y
        self.col_parts6_w = col_parts6_w
        self.col_parts6_h = col_parts6_h
        
        self.col_parts7_x = col_parts7_x
        self.col_parts7_y = col_parts7_y
        self.col_parts7_w = col_parts7_w
        self.col_parts7_h = col_parts7_h
        
        self.col_parts8_x = col_parts8_x
        self.col_parts8_y = col_parts8_y
        self.col_parts8_w = col_parts8_w
        self.col_parts8_h = col_parts8_h
        
        self.col_parts9_x = col_parts9_x
        self.col_parts9_y = col_parts9_y
        self.col_parts9_w = col_parts9_w
        self.col_parts9_h = col_parts9_h
        
        self.main_hp_bar_offset_x = main_hp_bar_offset_x  
        self.main_hp_bar_offset_y = main_hp_bar_offset_y
        
        self.parts1_hp_bar_offset_x = parts1_hp_bar_offset_x
        self.parts1_hp_bar_offset_y = parts1_hp_bar_offset_y
        
        self.parts2_hp_bar_offset_x = parts2_hp_bar_offset_x
        self.parts2_hp_bar_offset_y = parts2_hp_bar_offset_y
        
        self.parts3_hp_bar_offset_x = parts3_hp_bar_offset_x
        self.parts3_hp_bar_offset_y = parts3_hp_bar_offset_y
        
        self.parts4_hp_bar_offset_x = parts4_hp_bar_offset_x
        self.parts4_hp_bar_offset_y = parts4_hp_bar_offset_y
        
        self.parts5_hp_bar_offset_x = parts5_hp_bar_offset_x
        self.parts5_hp_bar_offset_y = parts5_hp_bar_offset_y
        
        self.parts6_hp_bar_offset_x = parts6_hp_bar_offset_x
        self.parts6_hp_bar_offset_y = parts6_hp_bar_offset_y
        
        self.parts7_hp_bar_offset_x = parts7_hp_bar_offset_x
        self.parts7_hp_bar_offset_y = parts7_hp_bar_offset_y
        
        self.parts8_hp_bar_offset_x = parts8_hp_bar_offset_x
        self.parts8_hp_bar_offset_y = parts8_hp_bar_offset_y
        
        self.parts9_hp_bar_offset_x = parts9_hp_bar_offset_x
        self.parts9_hp_bar_offset_y = parts9_hp_bar_offset_y
        
        self.size = size
        self.priority = priority
        self.attack_method = attack_method
        self.direction = direction
        self.acceleration = acceleration
        self.timer = timer
        self.degree = degree
        self.radian = radian
        self.speed = speed
        self.radius = radius
        self.flag1 = flag1
        self.flag2 = flag2
        self.flag3 = flag3
        self.flag4 = flag4
        self.count1 = count1
        self.count2 = count2
        self.count3 = count3
        self.count4 = count4
        self.parts1_flag = parts1_flag
        self.parts2_flag = parts2_flag
        self.parts3_flag = parts3_flag
        self.parts4_flag = parts4_flag
        self.parts5_flag = parts5_flag
        self.parts6_flag = parts6_flag
        self.parts7_flag = parts7_flag
        self.parts8_flag = parts8_flag
        self.parts9_flag = parts9_flag
        self.animation_number1 = animation_number1
        self.animation_number2 = animation_number2
        self.animation_number3 = animation_number3
        self.animation_number4 = animation_number4
        self.move_index = move_index
        self.obj_time = obj_time
        self.obj_totaltime = obj_totaltime
        self.invincible = invincible
        self.display_time_main_hp_bar = display_time_main_hp_bar
        self.display_time_parts1_hp_bar = display_time_parts1_hp_bar
        self.display_time_parts2_hp_bar = display_time_parts2_hp_bar
        self.display_time_parts3_hp_bar = display_time_parts3_hp_bar
        self.display_time_parts4_hp_bar = display_time_parts4_hp_bar
        self.display_time_parts5_hp_bar = display_time_parts5_hp_bar
        self.display_time_parts6_hp_bar = display_time_parts6_hp_bar
        self.display_time_parts7_hp_bar = display_time_parts7_hp_bar
        self.display_time_parts8_hp_bar = display_time_parts8_hp_bar
        self.display_time_parts9_hp_bar = display_time_parts9_hp_bar  

class Enemy_shot:#敵弾のクラス設定
    def __init__(self):
        self.enemy_shot_type = 0 #敵弾の種類
        self.enemy_shot_id   = 0 #敵弾に振られたIDナンバー
        self.posx = 0          #敵弾の座標x,y
        self.posy = 0
        self.collision_type = 0 #自機との当たり判定の種類 0=単純な小さな正方形で自機との距離を比べて当たったか判断 1=長方形でwidth,heightを見て自機と当たったかどうか判断する
        self.width  = 0 #弾の横幅
        self.height = 0 #弾の縦幅
        self.cx = 0    #回転弾で使用する回転の中心cx,cy
        self.cy = 0
        self.vx = 0    #速度ベクトルvx,vy
        self.vy = 0
        self.accel = 0    #加速度
        self.power = 0    #弾のパワー
        self.hp = 0       #弾のヒットポイント
        self.count1 = 0    #汎用カウンタ1
        self.count2 = 0    #汎用カウンタ2
        self.timer = 0    #時間(三角関数系で使用)
        self.speed = 0    #速度(三角関数系で使用)
        self.intensity = 0 #振れ幅(三角関数系で使用)
        self.aim = 0      #狙い撃つ方向
        self.disappearance_count = 0 #消滅するまでのカウントタイマー
        self.stop_count = 0        #その場に止まり続ける時に使用するカウンタ
        self.priority = 0          #描画優先度 0=1番最前面に表示 1=ボスより奥&敵より手前 2=ボスより奥&敵よりも奥
        self.turn_theta = 0        #誘導弾やホーミングミサイル,レーザーでの最大旋回可能角度(これ以上の角度では曲がることが出来ません)
        self.search_flag = 0             #サーチレーザーなどで自機の位置を調べて曲がる位置を確定させたかどうかのフラグ
        self.rotation_omega = 0           #回転弾などで使用する角度が入ります(現在値)
        self.rotation_omega_incremental = 0 #回転弾などで使用する,1フレームで増加する角度が入ります
        self.radius = 0        #回転弾などで使用する半径(現在値)
        self.radius_max = 0     #回転弾などで使用する半径(目標となる最大値)
        self.division_type = 0  #分裂弾かどうかのフラグとそのタイプ
                                #0=分裂はしない 1=自機狙いの3way 2=自機狙いの5way 3=自機狙いの7way 4=16方向弾 5=誘導弾4個
                                #6=誘導弾8個
        self.division_count = 0       #分裂するまでのカウント
        self.radius_incremental = 0    #回転弾などで使用する半径の増分
        self.division_count_origin = 0 #分裂するまでのカウント(元となる数値です変化はしません)
        self.division_num = 0        #分裂する回数(0なら1回だけ分裂して通常弾に戻る 1なら2分裂(孫分裂),2なら3分裂(ひ孫)後通常弾に戻ります)
        self.angle = 0              #グラフイック表示時に使用する回転角の数値
        self.expansion = 0           #だんだんと広がっていくウェーブやレーザーの広がっていくドット数(毎フレーム)
        self.expansion_flag = 0       #ウェーブやレーザーが最大まで広がったら立てるフラグ
        self.width_max = 0           #拡大ウェーブや拡大レーザーリップルレーザーの横幅の最大値
        self.height_max = 0          #拡大ウェーブや拡大レーザーリップルレーザーの縦幅の最大値
        self.color = 0              #色
        self.anime = 0              #アニメーション用カウンター

    def update(self,enemy_shot_type,enemy_shot_id, x, y,collision_type,width,height, cx,cy, vx,vy,accel,power, hp, count1, count2, timer, speed, intensity, aim,disappearance_count,stop_count,priority,turn_theta,search_flag,rotation_omega,rotation_omega_incremental,radius,radius_max,division_type,division_count,radius_incremental,division_count_origin,division_num,angle,expansion,expansion_flag,width_max,height_max,color,anime):
        self.enemy_shot_type = enemy_shot_type
        self.enemy_shot_id   = enemy_shot_id
        self.posx = x
        self.posy = y
        self.collision_type = collision_type
        self.width = width
        self.height = height
        self.cx = cx
        self.cy = cy
        self.vx = vx
        self.vy = vy
        self.accel = accel
        self.power = power
        self.hp = hp
        self.count1 = count1
        self.count2 = count2
        self.timer = timer
        self.speed = speed
        self.intensity = intensity
        self.aim = aim
        self.disappearance_count = disappearance_count
        self.stop_count = stop_count
        self.priority = priority
        self.turn_theta = turn_theta
        self.search_flag = search_flag
        self.rotation_omega = rotation_omega
        self.rotation_omega_incremental = rotation_omega_incremental
        self.radius = radius
        self.radius_max = radius_max
        self.division_type = division_type
        self.division_count = division_count
        self.radius_incremental = radius_incremental
        self.division_count_origin = division_count_origin
        self.division_num = division_num
        self.angle = angle
        self.expansion = expansion
        self.expansion_flag = expansion_flag
        self.width_max = width_max
        self.height_max = height_max
        self.color = color
        self.anime = anime

class Explosion:#爆発のクラス設定
    def __init__(self):
        self.explosion_type = 0 #爆発の種類
        self.priority = 0      #描画優先度
        self.posx = 0 #x座標
        self.posy = 0 #y座標
        self.vx = 0   #速度(ベクトル)
        self.vy = 0
        self.explotion_count = 0 #アニメーションパターン数
        self.return_bullet_type = 0  #打ち返し弾の種類 0=打ち返しなし 1=爆発直後に自機狙い弾1個 2=爆発直後に自機狙い弾1個+爆発の終わりに自機を狙う弾1個
        self.return_buller_count = 0 #打ち返し弾を生み出すまでのカウントタイマー(0になったら打ち返し弾を育成する)
        self.x_reverse = 0         #x軸方向(横)反転フラグ1=通常表示 -1=横に反転する
        self.y_reverse = 0         #y軸方向(横)反転フラグ1=通常表示 -1=縦に反転する

    def update(self,explosion_type,priority,x,y,vx,vy,explosion_count,return_bullet_type,return_buller_count,x_reverse,y_reverse):
        self.explosion_type = explosion_type
        self.priority = priority
        self.posx = x
        self.posy = y
        self.vx = vx
        self.vy = vy
        self.explosion_count = explosion_count
        self.return_bullet_type = return_bullet_type
        self.return_buller_count = return_buller_count
        self.x_reverse = x_reverse
        self.y_reverse = y_reverse

class Particle:#パーティクル（粒子）クラスの設定
    def __init__(self):
        self.particle_type = 0 #パーティクルの種類
        self.posx = 0 #x座標
        self.posy = 0 #y座標
        self.size = 0 #大きさ
        self.vx = 0 #速度(ベクトル)
        self.vy = 0
        self.life = 0 #パーティクルの生存期間
        self.wait = 0 #ウェイト(どれだけその場所に停止し続けるのかのウェイトカウンター)
        self.color = 0 #パーティクルの色

    def update(self,particle_type,x,y,size,vx,vy,life,wait,color):
        self.particle_type = particle_type
        self.posx = x
        self.posy = y
        self.size = size
        self.vx = vx
        self.vy = vy
        self.life = life
        self.wait = wait
        self.color = color

class Background_object:#背景の物体(背景オブジェクト）クラスの設定 (雲や鳥や泡や木葉や背景を移動する艦隊とか当たり判定の無い大き目の物体)
    def __init__(self):
        self.background_object_type = 0 #背景オブジェクトの種類
        self.posx,self.posy = 0,0 #x,y座標
        self.size         = 0   #大きさ
        self.ax,self.ay    = 0,0 #加速度
        self.bx,self.by    = 0,0
        self.cx,self.cy    = 0,0
        self.dx,self.dy    = 0,0
        self.vx,self.vy    = 0,0 #速度(ベクトル)
        self.width        = 0   #横
        self.height        = 0   #縦
        self.life         = 0   #生存時間
        self.wait         = 0   #停止時間
        self.color        = 0   #色
        self.speed        = 0   #速度(倍率)
        self.direction     = 0   #方向
        self.flag1,self.flag2,self.flag3    = 0,0,0 #フラグ1~3
        self.count1,self.count2,self.count3 = 0,0,0 #カウント1~3
        self.animation_number1,self.animation_number2,self.animation_number3 = 0,0,0 #アニメーション番号1~3

    def update(self,background_object_type,
            posx,posy,
            size,
            ax,ay, bx,by, cx,cy, dx,dy, vx,vy,
            width,height,
            life,wait,color,speed,direction,
            flag1,flag2,flag3,
            count1,count2,count3,
            animation_number1,animation_number2,animation_number3
            ):
        self.background_object_type = background_object_type
        self.posx,self.posy = posx,posy
        self.size         = size
        self.ax,self.ay    = ax,ay
        self.bx,self.by    = bx,by
        self.cx,self.cy    = cx,cy
        self.dx,self.dy    = dx,dy
        self.vx,self.vy    = vx,vy
        self.width        = width
        self.height        = height
        self.life         = life
        self.wait         = wait
        self.color        = color
        self.speed        = speed
        self.direction     = direction
        self.flag1,self.flag2,self.flag3    = flag1,flag2,flag3
        self.count1,self.count2,self.count3 = count1,count2,count3
        self.animation_number1,self.animation_number2,self.animation_number3 = animation_number1,animation_number2,animation_number3


class Window: #メッセージ表示ウィンドウのクラスの設定
    def __init__(self):
        self.window_id = 0          #それぞれのウィンドウに与えられるIDです
        self.window_id_sub = 0      #ウィンドウIDに対しての補助的なIDです(はい」「いいえ」などの2択メニューとかで使用)
        self.window_type = 0        #ウィンドウの種類です
        self.window_bg = 0          #ウィンドウの下地(主に背景の事です) 0=シースルー 1=完全な青地 2=ちょっとシースルー
        self.window_status = 0      #ウィンドウの現在の状態を表しますステータスです WINDOW_OPEN=ウィンドウ開き中 WINDOW_CLOSE=ウィンドウ閉じ中
                                    #                                           WINDOW_WRITE_MESSAGE=メッセージテキスト表示中
        self.between_line = 0       #テキスト表示時の行と行の間隔(通常は7ドット)
        self.title_text = []                      #タイトルが入ります
        self.item_text    = [[] for i in range(12)] #アイテムテキスト(選択メニューの項目文章)が入ります 
        self.edit_text    = []                      #編集できるテキストが入ります
        self.scroll_text  = []                      #スクロール表示されるテキストが入ります
        self.script       = []                      #スクリプト(書記系)が入ります
        
        self.posx = 0          #現在のウィンドウの座標(posx,posy)
        self.posy = 0
        self.dx = 0            #移動先の座標(destination_x,y)
        self.dy = 0
        self.width = 0         #現在のウィンドウの横幅と縦幅(width,height)最初は0でだんだんと(open_width,open_height)に近づいていきます
        self.height = 0
        self.open_width = 0    #ウィンドウが完全に開いた状態の横幅と縦幅(width,heighがこの値になったらウィンドウオープン完了)
        self.open_height = 0   
        self.change_x = 0      #ウィンドウを開閉する時の変化ドット数
        self.change_y = 0
        self.open_speed  = 0   #ウィンドウを開くスピード (change_x,change_y)に掛け合わされます
        self.close_speed = 0   #ウィンドウを閉じるスピード(change_x,change_y)に掛け合わされます
        self.open_accel  = 0   #ウィンドウオープン時の加速度(毎フレームごとopen_speedと掛け合わされた数値がopen_speedに入ります)
        self.close_accel = 0   #ウィンドウクローズ時の加速度(毎フレームごとclose_speedと掛け合わされた数値がclose_speedに入ります)
        self.marker = 0        #マーカー(印)用フラグ      予約用
        self.color = 0         #ウィンドウの色            予約用
        self.vx = 0            #ウィンドウの速度(vx,vy)
        self.vy = 0
        self.vx_accel = 0      #速度に掛け合わせる加速度(accel)
        self.vy_accel = 0
        
        self.ok_button_disp_flag = 0  #OKボタン(決定ボタン)を表示するかどうかのフラグ DISP_OFF=0=表示しない DISP_ON=1=表示する
        self.ok_button_x = 0          #OKボタンを表示する座標(オフセット値)
        self.ok_button_y = 0
        self.ok_button_size = 0       #OKボタンのサイズ
        
        self.no_button_disp_flag = 0  #NOボタン(決定ボタン)を表示するかどうかのフラグ DISP_OFF=0=表示しない DISP_ON=1=表示する
        self.no_button_x = 0          #NOボタンを表示する座標(オフセット値)
        self.no_button_y = 0
        self.no_button_size = 0       #NOボタンのサイズ
        
        self.cursor_move_se   = 0  #カーソルを動かしたときの効果音
        self.cursor_push_se   = 0  #カーソルでボタンを押したときの効果音
        self.cursor_ok_se     = 0  #カーソルでokボタンを押したときの効果音
        self.cursor_cancel_se = 0  #カーソルでキャンセルボタンを押したときの効果音
        self.cursor_bounce_se = 0  #カーソルが障害物に当たった時の跳ね返り効果音
        
        
        self.ship_list              = []
        self.ship_graph_list        = []
        self.weapon_list            = []
        self.weapon_graph_list      = []
        self.sub_weapon_list        = []
        self.sub_weapon_graph_list  = []
        self.missile_list           = []
        self.missile_graph_list     = []
        self.medal_list             = []
        self.medal_graph_list       = []
        self.item_list              = [[] for i in range(128)]
        self.item_graph_list        = [[] for i in range(128)]
        self.flag_list              = [[] for i in range(128)]
        self.graph_list             = [[] for i in range(128)]
        
        self.comment_flag           = 0   #カーソルが現在指し示しているアイテムの説明文を表示するかどうかのフラグ(全体管理)
        self.comment_ox_eng         = 0   #アイテムの説明文を表示する座標(英語)(comment_ox_eng,comment_oy_eng)(ウィンドウの座標からのオフセット値となります)
        self.comment_oy_eng         = 0
        self.comment_ox_jpn         = 0   #アイテムの説明文を表示する座標(日本語)(comment_ox_jpn,comment_oy_jpn)(ウィンドウの座標からのオフセット値となります)
        self.comment_oy_jpn         = 0
        self.comment_disp_flag      = []  #個々のアイテムの説明文を表示するかのフラグcomment_list_eng,comment_list_jpnと1対1で対応し対となります
        self.comment_list_eng       = []  #アイテムの説明文(英語)
        self.comment_list_jpn       = []  #アイテムの説明文(日本語)

    def update(self,window_id,window_id_sub,window_type,window_bg,window_status,\
        between_line,\
        
        title_text,\
        item_text,\
        edit_text,\
        scroll_text,\
        script,\
        
        x,y,dx,dy,width,height,open_width,open_height,change_x,change_y,open_speed,close_speed,open_accel,close_accel,marker,color,\
        vx,vy,vx_accel,vy_accel,\
        ok_button_disp_flag,ok_button_x,ok_button_y,ok_button_size,\
        no_button_disp_flag,no_button_x,no_button_y,no_button_size,\
        cursor_move_se,cursor_push_se,cursor_ok_se,cursor_cancel_se,cursor_bounce_se,\
        
        
        ship_list,ship_graph_list,\
        weapon_list,weapon_graph_list,\
        sub_weapon_list,sub_weapon_graph_list,\
        missile_list,missile_graph_list,\
        medal_list,medal_graph_list,\
        item_list,item_graph_list,\
        flag_list,graph_list,\
        
        comment_flag,comment_ox_eng,comment_oy_eng,comment_ox_jpn,comment_oy_jpn,comment_disp_flag,comment_list_eng,comment_list_jpn):
        
        self.window_id = window_id
        self.window_id_sub = window_id_sub
        self.window_type = window_type
        self.window_bg = window_bg
        self.window_status = window_status
        
        self.between_line = between_line
        
        self.title_text   = title_text
        self.item_text    = item_text
        self.edit_text    = edit_text
        self.scroll_text  = scroll_text
        self.script       = script
        
        self.posx = x
        self.posy = y
        self.dx = dx
        self.dy = dy
        self.width  = width
        self.height = height
        self.open_width  = open_width
        self.open_height = open_height
        self.change_x = change_x
        self.change_y = change_y
        self.open_speed  = open_speed
        self.close_speed = close_speed
        self.open_accel  = open_accel
        self.close_accel = close_accel
        self.marker = marker
        self.color = color
        self.vx = vx
        self.vy = vy
        self.vx_accel = vx_accel
        self.vy_accel = vy_accel
        
        self.ok_button_disp_flag = ok_button_disp_flag   
        self.ok_button_x = ok_button_x      
        self.ok_button_y = ok_button_y
        self.ok_button_size = ok_button_size       
        
        self.no_button_disp_flag = no_button_disp_flag  
        self.no_button_x = no_button_x 
        self.no_button_y = no_button_y
        self.no_button_size = no_button_size
        
        self.cursor_move_se   = cursor_move_se
        self.cursor_push_se   = cursor_push_se
        self.cursor_ok_se     = cursor_ok_se
        self.cursor_cancel_se = cursor_cancel_se
        self.cursor_bounce_se = cursor_bounce_se
        
        
        self.ship_list             = ship_list
        self.ship_graph_list       = ship_graph_list
        self.weapon_list           = weapon_list
        self.weapon_graph_list     = weapon_graph_list
        self.sub_weapon_list       = sub_weapon_list
        self.sub_weapon_graph_list = sub_weapon_graph_list
        self.missile_list          = missile_list
        self.missile_graph_list    = missile_graph_list
        self.medal_list            = medal_list
        self.medal_graph_list      = medal_graph_list
        self.item_list             = item_list
        self.item_graph_list       = item_graph_list
        self.flag_list             = flag_list
        self.graph_list            = graph_list
        
        self.comment_flag      = comment_flag
        self.comment_ox_eng    = comment_ox_eng
        self.comment_oy_eng    = comment_oy_eng
        self.comment_ox_jpn    = comment_ox_jpn
        self.comment_oy_jpn    = comment_oy_jpn
        self.comment_disp_flag = comment_disp_flag
        self.comment_list_eng  = comment_list_eng
        self.comment_list_jpn  = comment_list_jpn
        
class Cursor: #メッセージ表示ウィンドウで使用するカーソルのデータ群のクラス設定
    def __init__(self): #コンストラクタ
        self.window_id = 0         #このウィンドウIDがアクティブになったらこのカーソルデータを使用してカーソルを表示開始します
        self.cursor_type = 0       #セレクトカーソルの種類
        self.posx = 0              #セレクトカーソルのx座標
        self.posy = 0              #セレクトカーソルのy座標
        self.step_x = 0            #横方向の移動ドット数
        self.step_y = 0            #縦方向の移動ドット数
        self.page = 0              #いま指し示しているページナンバー
        self.page_max = 0          #セレクトカーソルで捲ることが出来る最多ページ数
        self.item_x = 0            #いま指し示しているアイテムナンバーx軸方向
        self.item_y = 0            #いま指し示しているアイテムナンバーy軸方向
        self.max_item_x = 0        #x軸の最大項目数 5の場合(0~4)の5項目分カーソルが移動することになります 3だったら(0~2)って感じで
        self.max_item_y = 0        #y軸の最大項目数 5の場合(0~4)の5項目分カーソルが移動することになります 3だったら(0~2)って感じで
        self.decision_item_x = -1  #ボタンが押されて「決定」されたアイテムのナンバーx軸方向 -1は未決定 ここをチェックしてどのアイテムが選択されたのか判断する
        self.decision_item_y = -1  #ボタンが押されて「決定」されたアイテムのナンバーy軸方向 -1は未決定 ここをチェックしてどのアイテムが選択されたのか判断する
        self.color = 0             #セレクトカーソルの色
        self.menu_layer = 0        #現在選択中のメニューの階層の数値が入ります
        self.move_direction = 0    #セレクトカーソルがどう動かせることが出来るのか？の状態遷移変数です

    def update(self,window_id,cursor_type,x,y,step_x,step_y,page,page_max,item_x,item_y,max_item_x,max_item_y,decision_item_x,decision_item_y,color,menu_layer,move_direction):
        self.window_id = window_id
        self.cursor_type = cursor_type
        self.posx = x
        self.posy = y
        self.step_x = step_x
        self.step_y = step_y
        self.page = page
        self.page_max = page_max
        self.item_x = item_x
        self.item_y = item_y
        self.max_item_x = max_item_x
        self.max_item_y = max_item_y
        self.decision_item_x = decision_item_x
        self.decision_item_y = decision_item_y
        self.color = color
        self.menu_layer = menu_layer
        self.move_direction = move_direction


class Obtain_item:#手に入れるアイテム類（パワーアップ勲章とかコインアイテムとか）のクラス設定
    def __init__(self):
        self.item_type = 0                  #アイテムのタイプ 1=ショットパワーアップ 2=ミサイルパワーアップ 3=シールドパワーアップ
                                            #これ以外はパワーアップアイテム類のtype定数の定義を参照してください
        self.posx = 0                       #x座標
        self.posy = 0                       #y座標
        self.vx = 0                         #速度ベクトル
        self.vy = 0
        self.width = 0                      #横の大きさ
        self.height = 0                     #縦の大きさ
        self.color = 0                      #色
        self.intensity = 0                  #振れの度合い
        self.timer = 0                      #時間
        self.degree = 0                     #回転角度 度数法（主にこちらを使用するのです！）
        self.radian = 0                     #回転角度 弧度法
        self.speed = 0                      #回転スピード(弧度法0~360度)
        self.radius = 0                     #半径
        self.radius_max = 0                 #半径の最大値(回転半径が変化する物ではこの数値を最大値として設定することにします)
        self.animation_number = 0           #アニメーションパターンのオフセット指定番号用
        self.score = 0                      #得点
        self.shot = 0                       #ショットパワーの増加量
        self.missile = 0                    #ミサイルパワーの増加量
        self.shield = 0                     #シールドパワーの増加量
        self.flag1 = 0                      #フラグ用その１
        self.flag2 = 0                      #フラグ用その２
        self.flag3 = 0                      #フラグ用その３
        self.bounce = 0                     #画面左端で跳ね返って戻ってくる回数(バウンス回数)
        self.status = 0                     #状態遷移用（ステータス）

    def update(self,item_type,x,y,vx,vy,width,height,color,intensity,timer,degree,radian,speed,radius,radius_max,animation_number,score,shot,missile,shield,flag1,flag2,flag3,bounce,status):
        self.item_type = item_type
        self.posx = x
        self.posy = y
        self.vx = vx
        self.vy = vy
        self.width = width
        self.height = height
        self.color = color
        self.intensity = intensity
        self.timer = timer
        self.degree = degree
        self.radian = radian
        self.speed = speed
        self.radius = radius
        self.radius_max = radius_max
        self.animation_number = animation_number
        self.score = score
        self.shot = shot
        self.missile = missile
        self.shield = shield
        self.flag1 = flag1
        self.flag2 = flag2
        self.flag3 = flag3
        self.bounce = bounce
        self.status = status


class Enemy_formation: #敵の編隊数のリストのクラス設定
    def __init__(self):
        self.formation_id = 0            #それぞれの編隊に与えられたidナンバー(1~?)(0は単独機で使用してるので編隊では未使用です) 
        self.formation_number = 0         #何機編隊なのか編隊の総数が入ります
        self.on_screen_formation_number = 0 #画面上に存在する編隊数(撃墜されたり画面からいなくなったらだんだん数が減ってきます0になったらリストからインスタンス破棄します)
        self.shoot_down_number = 0        #撃墜するべき編隊総数 (7機編隊なら最初は7で1機撃墜すると1減らしていく、この値が0になったらパワーアップアイテム出現！って事ね)

    def update(self,formation_id,formation_number,on_screen_formation_number,shoot_down_number):
        self.formation_id               = formation_id
        self.formation_number           = formation_number
        self.on_screen_formation_number = on_screen_formation_number
        self.shoot_down_number          = shoot_down_number


class Event_append_request: #早回しなどの敵の追加や乱入中ボス,臨時のスクロールスピードや方向の調整などの追加リクエストが入るリストのクラス設定です
    def __init__(self):
        self.timer = 0      #イベントが開始されるカウントタイマー
        self.event_type = 0 #イベントのタイプ
        self.enemy_type = 0 #敵の種類
        self.posx = 0       #x座標
        self.posy = 0       #y座標
        self.number = 0     #敵の数

    def update(self,timer,event_type,enemy_type,x,y,number):
        self.timer = timer
        self.event_type = event_type
        self.enemy_type = enemy_type
        self.posx = x
        self.posy = y
        self.number = number


class Raster_scroll: #背景でラスタースクロールするときに使用する横ラインのデータ設定値のクラス
    def __init__(self):
        self.scroll_id = 0       #複数のラスタースクロールを動作させる時に使用するidナンバー
        self.raster_type = 0     #ラスタースクロールの種類
        self.priority  = 0       #描画時の優先度
        self.display = 0         #描画するかどうかの判定用 (0=描画しない 1=描画する)
        self.scroll_line_no = 0  #ラスタースクロール時に使用するそれぞれの横ラインの割り当てられた番号(上方向から0~任意の数値)
        self.total_line_num = 0  #どこまでラスタスクロールさせるかの縦軸総ライン数 (scroll_line_noに入る最大値(任意の数値)が入る)
        self.posx = 0            #x座標
        self.posy = 0            #y座標
        self.offset_x = 0        #現在のx座標値に対してのオフセット値
        self.offset_y = 0        #現在の垂直スクロールカウント数に対してのy軸オフセット値
        self.img_bank = 0        #グラフイックパターンのあるイメージバンクの数値
        self.posu = 0            #グラフイックパターンが記録されている横座標(pyxelのblt命令のuの値)
        self.posv = 0            #グラフイックパターンが記録されている縦座標(pyxelのblt命令のvの値)
        self.width = 0           #各ラインを描画するときの横幅の数値(単位はドット)
        self.height = 0          #縦幅(通常は1だけど上下スクロールするときに1ドットだと隙間が出来る可能性があるので2ドットでもいいかも？)
        self.speed = 0           #スクロールスピード
        self.transparent_color=0 #透明色の指定
        self.wave_timer = 0      #ウェーブラスタースクロール用のタイマー
        self.wave_speed = 0      #ウェーブラスタースクロール用のスピード
        self.wave_intensity = 0  #ウェーブラスタースクロール用の振れ幅

    def update(self,scroll_id,raster_type,priority,display,scroll_line_no,total_line_num,
            x,y,offset_x,offset_y,img_bank,u,v,width,height,speed,transparent_color,
            wave_timer,wave_speed,wave_intensity):
        self.scroll_id = scroll_id
        self.raster_type = raster_type
        self.priority = priority
        self.display = display
        self.scroll_line_no = scroll_line_no
        self.total_line_num = total_line_num
        self.posx = x
        self.posy = y
        self.offsrt_x = offset_y
        self.offset_y = offset_y
        self.img_bank = img_bank
        self.posu = u
        self.posv = v
        self.width = width
        self.height = height
        self.speed = speed
        self.transparent_color = transparent_color
        self.wave_timer = wave_timer
        self.wave_speed = wave_speed
        self.wave_intensity = wave_intensity
    


