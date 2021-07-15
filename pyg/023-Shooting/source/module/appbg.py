
from typing import List
import pyxel

class AppBg:

    stars: List[Star]

    def __init__(self):
        pass

    #背景の星の追加（発生＆育成）
    def update_append_star(self):
        if (pyxel.frame_count % 3) == 0:
            if len(self.stars) < 600:
                new_stars = Star()
                new_stars.update(WINDOW_W + 1,self.s_rndint(0,WINDOW_H),self.s_rndint(1,50))
                self.stars.append(new_stars)

    #背景の星の更新（移動）
    def update_star(self):
        stars_count = len(self.stars)
        for i in reversed(range (stars_count)):
            if 0 < self.stars[i].posx and self.stars[i].posx < WINDOW_W + 2:#背景の星が画面内に存在するのか判定

            #背景の星の位置を更新する
                self.stars[i].posx -= (self.stars[i].speed) / 12 * self.star_scroll_speed #左方向にspeedを１２で割った切り捨てドット分（star_scroll_speedは倍率です）星が左に流れます
            else:
                del self.stars[i]#背景の星が画面外に存在するときはインスタンスを破棄する （流れ星消滅）




    #背景の星の表示
    def draw_star(self):
        stars_count = len(self.stars)
        for i in range(stars_count):
            pyxel.pset(self.stars[i].posx, self.stars[i].posy,self.stars[i].posx  // 4 % 15) 
            #pyxel.pset(self.stars[i].posx, self.stars[i].posy,self.s_rndint(0,7)) 



class Star:#背景の流れる星のクラス設定
    def __init__(self):
        self.posx = 0
        self.posy = 0
        self.speed = 0

    def update(self,x , y, speed):
        self.posx = x
        self.posy = y
        self.speed = speed




