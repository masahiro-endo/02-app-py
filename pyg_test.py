import pygame
import sys
 
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
 
arr = []
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
		screen.blit(txt, [100, 100])
		pygame.display.update()
		clock.tick(2)
 
if __name__ == '__main__':
	main()
