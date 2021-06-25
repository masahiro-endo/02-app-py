import pygame
import pygame.locals
import pygame.color
import pygame.display
import sys
 
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
DIRECTION_NORTH = 0
DIRECTION_EAST = 1
DIRECTION_SOUTH = 2
DIRECTION_WEST = 3
# |(x-2,y-3)|(x-1,y-3)|(x,y-3)|(x+1,y-3)|(x+2,y-3)|
#            |(x-1,y-2)|(x,y-2)|(x+1,y-2)|
#            |(x-1,y-1)|(x,y-1)|(x+1,y-1)|
#            |(x-1,y)  |(x,y)  |(x+1,y)  |
# 
# 　この座標増分データを、4方向それぞれに対して用意してやれば良いわけです。
#  　具体的には、以下のように2次元のタプル型で定義します。
# マップの参照先の定義
# 参照順のイメージは以下（上向きの場合。自分の位置はCとする）
# |0|1|2|3|4|
#   |5|6|7|
#   |8|9|A|
#   |B|C|D|
pos_x = (
    (-2,-1, 2, 1, 0,-1, 1, 0,-1, 1, 0,-1, 1, 0),
    ( 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
    ( 2, 1,-2,-1, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0),
    (-3,-3,-3,-3,-3,-2,-2,-2,-1,-1,-1, 0, 0, 0)
)
pos_y = (
    (-3,-3,-3,-3,-3,-2,-2,-2,-1,-1,-1, 0, 0, 0),
    (-2,-1, 2, 1, 0,-1, 1, 0,-1, 1, 0,-1, 1, 0),
    ( 3, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1, 0, 0, 0),
    ( 2, 1,-2,-1, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0)
)
# 自分の最初の座標と方向
x = 1
y = 1
direction = DIRECTION_SOUTH
# マップ
# 0 = 通路
# 1 = 壁
# 外周は必ず壁とする
map = [
    [ 1, 1, 1, 1, 1],
    [ 1, 0, 1, 0, 1],
    [ 1, 0, 1, 0, 1],
    [ 1, 0, 0, 0, 1],
    [ 1, 1, 1, 1, 1]
]


arr:list[str] = []
arr.append("|")
arr.append("/")
arr.append("―")
arr.append("\\")
 
def main():
	pygame.init()
	pygame.display.set_caption("***test***")
	screen = pygame.display.set_mode((400, 300))
	clock = pygame.time.Clock()
	font = pygame.font.Font(None, 80)
	tmr = 0
 
	while True:
		tmr = tmr + 1
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
 
		txt = font.render(str(arr[tmr % 4]), True, WHITE)
		screen.fill(BLACK)
		# screen.blit(txt, [100, 100])

        
		pygame.draw.line(screen, WHITE, (15,25), (25,30), 1)
		pygame.draw.line(screen, WHITE, (15,35), (25,30), 1)
		pygame.draw.rect(screen, WHITE, pygame.Rect(5,25,10,10), 1)
		pygame.draw.line(screen, WHITE, (25,25), (30,30), 1)
		pygame.draw.line(screen, WHITE, (25,35), (30,30), 1)
		pygame.draw.rect(screen, BLACK, pygame.Rect(15,25,10,10))

		pygame.display.update()
		clock.tick(2)


# 		for i in range(0, 14):
#             map_x = x + pos_x[direction][i]
#             map_y = y + pos_y[direction][i]
#             if map_x < 0 or map_x > 4 or map_y < 0 or map_y > 4:
#                 data = "1"
#             else:
#                 data = map[map_y][map_x]
# 
#             print(str(map_x) + ":" + str(map_y) + "=" + str(data))
 
if __name__ == '__main__':
	main()

