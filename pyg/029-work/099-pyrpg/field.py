# -*- coding: utf-8 -*-
from parameter.monsters import monsterParams


class demotown:
    '''
     39 x  39
    '''
    floormap = (
        (1,1,1,1,1,1,1,1,1,1),
        (1,0,0,0,0,0,0,0,0,1),
        (1,0,1,1,1,1,1,1,0,1),
        (1,0,1,0,0,0,0,1,0,1),
        (1,0,1,0,0,0,0,2,0,1),
        (1,0,1,0,0,0,0,1,0,1),
        (1,0,1,0,0,0,0,1,1,1),
        (1,1,1,1,1,1,1,1,1,1),
        (0,0,0,0,0,0,0,0,0,0),
        (0,0,0,0,0,0,0,0,0,0)
    )

    enemy_set = (
        monsterParams["WOLF_LV1"],
        monsterParams["WOLF_LV1"],
        monsterParams["ZOMBIE_LV1"],
    )
