# -*- coding: utf-8 -*-

class dungeonB3:
    '''
    dungeonB3
     39 x  39
    '''
    map = (
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,8,521,512,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,8,520,512,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,8,520,512,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,64,0,8,520,512,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,521,512,8,520,512,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,8,520,576,64,64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,64,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,8,576,65,65,137,576,64,0,0,0,0,0,0,0,0,0,0,0,0,0,8,521,512,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,8,513,1,1,2,1,9,512,0,0,0,0,0,0,0,0,0,0,0,0,72,648,576,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,8,512,0,0,0,0,8,512,0,0,0,0,0,0,0,0,0,0,0,8,513,2,9,512,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,8,512,0,0,0,0,8,576,64,64,64,64,64,64,0,0,0,0,0,8,512,0,8,512,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,8,512,0,0,0,0,16,1089,65,65,65,193,193,9,576,64,64,64,0,8,512,0,8,512,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,8,512,0,0,0,0,8,513,1,9,536,192,0,1536,65,65,65,9,512,8,576,128,72,512,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,8,576,64,128,64,64,72,576,64,72,536,3,0,1544,513,1,9,520,512,0,9,522,513,64,64,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,0,1,9,578,65,65,65,65,65,65,1024,3,11,520,512,0,8,520,576,64,8,520,584,513,9,512,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,0,0,0,1,65,65,65,65,65,73,576,64,72,648,576,64,72,577,65,9,520,576,81,1088,72,512,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,0,0,0,72,513,1,9,513,9,521,1563,1730,27,577,65,65,513,2,9,520,512,1,1,1,1,0,0,0,0,0,0,0,0,0,),
        (0,0,8,520,512,0,0,8,529,1024,0,16,584,520,528,536,1539,24,513,65,81,512,0,8,520,512,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,8,584,512,0,64,72,520,576,64,72,577,64,72,1728,152,1752,576,73,585,576,128,72,520,512,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,1,0,8,513,65,72,513,74,577,65,65,73,513,1,9,513,2,9,513,1,9,648,512,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,8,520,513,97,584,585,521,1089,65,73,1024,0,16,512,0,8,1024,0,16,521,512,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,8,592,520,521,585,641,72,585,586,585,576,64,72,576,128,72,576,64,72,520,512,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,9,520,584,513,1,9,513,2,9,513,2,9,513,2,9,513,2,9,520,512,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,8,520,521,1024,0,16,512,0,16,1024,0,16,1024,0,16,512,0,8,1088,73,512,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,8,520,520,576,64,72,576,128,72,576,128,72,576,128,72,576,128,72,521,522,512,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,8,520,520,513,2,9,585,521,577,65,66,73,513,65,73,513,193,9,584,520,512,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,8,528,528,512,0,8,1089,72,521,1089,65,73,1032,513,73,1048,1755,1552,577,72,512,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,8,520,520,576,128,72,1089,65,72,521,513,9,584,648,585,576,67,72,513,1,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,8,520,576,65,73,585,513,65,65,1032,520,576,65,73,521,513,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,8,576,65,65,65,65,72,513,9,576,64,65,65,65,72,512,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
        (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,),
    )
