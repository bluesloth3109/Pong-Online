import pygame
from network import Network
pygame.init()
WIDTH = 500
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Client")

clientNumber = 0

class Player():
	def __init__(self, x, y, width, height, colour):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.colour = colour
		self.rect = (x, y, width, height)
		self.vel = 2
	
	def draw(self, win):
		pygame.draw.rect(win, self.colour, self.rect)
	
	def move(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self.x -= self.vel

		if keys[pygame.K_RIGHT]:
			self.x += self.vel

		if keys[pygame.K_UP]:
			self.y -= self.vel

		if keys[pygame.K_DOWN]:
			self.y += self.vel
		self.update()
	def update(self):
		self.rect = (self.x, self.y, self.width, self.height)

def redrawWindow(win, player, player2):
	win.fill ((255,255,255))
	player.draw(win)
	player2.draw(win)
	pygame.display.update()

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tuple):
    return str(tuple[0]) + "," + str(tuple[1])

def main():
	run = True
	clock = pygame.time.Clock()
	n = Network()
	startpos = read_pos(n.get_pos())

	p1 = Player(startpos[0], startpos[1], 30, 30, (255, 0, 0))
	p2 = Player(100, 100, 30, 30, (0, 255, 0))


	while run:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
		p2pos = read_pos(n.send(make_pos((p1.x, p1.y))))
		p2.x = p2pos[0]
		p2.y = p2pos[1]
		p2.update()
		p1.move()
		redrawWindow(win, p1, p2)

main()