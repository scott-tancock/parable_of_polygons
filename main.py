import random
import pygame
import sys

def show_grid(screen, grid, happy):
	rows = len(grid)
	cols = len(grid[0])
	width = screen.get_width()/cols
	height = screen.get_height()/rows
	triangle = pygame.Surface((width, height))
	square = pygame.Surface((width, height))
	unhappy = pygame.Surface((width, height))
	ishappy = pygame.Surface((width, height))
	screen.fill((128,128,128)) # Neutral colour
	unhappy.fill((255,0,0)) # Unhappy colour
	ishappy.fill((0,255,0)) # Happy colour
	square = square.convert_alpha()
	square.fill((0,0,0,0))
	triangle = triangle.convert_alpha()
	triangle.fill((0,0,0,0))
	pygame.draw.rect(square, (0,0,255,255), (width/4, height/4, 2*width/4, 2*height/4))
	pygame.draw.polygon(triangle, (255,0,255,255), [(width/4, 3*height/4),(3*width/4, 3*height/4),(width/2,height/4)])
	for i in range(0, rows):
		for j in range(0, cols):
			if happy[i][j] == 'U':
				screen.blit(unhappy, (width*j, height*i))
			elif happy[i][j] == 'H':
				screen.blit(ishappy, (width*j, height*i))
			if grid[i][j] == 'T':
				screen.blit(triangle, (width*j, height*i))
			elif grid[i][j] == 'S':
				screen.blit(square, (width*j, height*i))
	pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

def make_rand_grid(rows, cols, lim_square, lim_triangle):
	grid = []
	for i in range(0,rows):
		grid.append([])
		for j in range(0,cols):
			r = random.random()
			if r < lim_square:
				grid[i].append('S')
			elif r < lim_square + lim_triangle:
				grid[i].append('T')
			else:
				grid[i].append('N')
	return grid

def eval_grid(grid, happy_same, happy_different):
	happy = []
	rows = len(grid)
	cols = len(grid[0])
	for i in range(0, rows):
		happy.append([])
		for j in range(0, cols):
			happy[i].append('N')
			s = 0
			t = 0
			n = 0
			me = grid[i][j]
			if me == 'N':
				continue
			for k in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
				ni = i+k[0]
				nj = j+k[1]
				if ni < 0 or ni >= rows or nj < 0 or nj >= cols:
					continue
				neighbour = grid[i+k[0]][j+k[1]]
				if neighbour == 'S':
					s += 1
				elif neighbour == 'T':
					t += 1
				else:
					n += 1
			same = s if me == 'S' else t
			different = t if me == 'S' else s
			diversity = same / (same+different)
			if different != 0:
				happy[i][j] = 'H'
			if diversity < happy_same:
				happy[i][j] = 'U'
			if diversity > happy_different:
				happy[i][j] = 'U'
	return happy
def main():
	random.seed()
	screen = pygame.display.set_mode((400,400))
	grid = make_rand_grid(20, 20, 0.40, 0.40)
	happy = eval_grid(grid, 0.2, 1.0)
	show_grid(screen, grid, happy)
	
if __name__ == '__main__':
	main()
