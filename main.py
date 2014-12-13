import pygame
import serial

import sys, pygame
import numpy
import serial

serConected = True
try:
	ser = serial.Serial('/dev/tty.usbserial-A50201O6', 9600) # Establish the connection on a specific port
except:
	serConected=False

moveConected = True
try:
	movePort = serial.Serial('/dev/tty.usbmodem411', 38400) # Establish the connection on a specific port
except:
	moveConected=False


pygame.init()

size = width, height = 768, 1024
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size) 
effect = pygame.mixer.Sound('sound.wav')



class Player:
	def __init__(self):
		self.img = pygame.image.load("spaceship_clean.bmp")
		self.img.set_colorkey((104,255,59))
		self.img = pygame.transform.scale(self.img, (100, 100))
		self.mask = pygame.mask.from_surface(self.img)

		self.rect = self.img.get_rect()
		self.rect = self.rect.move(width/2, 100)
		self.vel = (0,0)
		self.health = 100

	def draw(self, screen):
		screen.blit(self.img, self.rect)

	def processEvent(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				self.vel = (-5,0)
			if event.key == pygame.K_RIGHT and self.rect.left >= 0:
				self.vel = (5,0)
			if event.key == pygame.K_LEFT:
				self.vel = (-5,0)
			if event.key == pygame.K_RIGHT and self.rect.left >= 0:
				self.vel = (5,0)


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				self.vel = (0,0)
			if event.key == pygame.K_RIGHT:
				self.vel= (0,0)
	
	def processMovement(self, mx,my):
		self.vel = (mx/400,my/400)

	def update(self):
		if self.rect.right >= width and self.vel[0]>0:
			self.vel = (-5, self.vel[1])
		if self.rect.left <= 0 and self.vel[0]<0:
			self.vel = (5, self.vel[1])

		self.rect = self.rect.move(self.vel)

	def processCollisions(self, env):
		objects = env.asteroids
		for i in range(len(objects)-1,-1,-1):
			if objects[i].rect.colliderect(self.rect):
				offset = ( (objects[i].rect.left - self.rect.left), (objects[i].rect.top - self.rect.top) )
				print offset
				if self.mask.overlap(objects[i].mask, offset) != None:
					self.health -= 10
					del objects[i]
					env.addAsteroid()
					if serConected: ser.write('5')
					effect.play()




class Asteroid:
	def __init__(self):
		self.img = pygame.image.load("Jam_Asteroid.bmp")
		self.img.set_colorkey((104,255,59))
		self.img = pygame.transform.scale(self.img, (100, 100))
		self.mask = pygame.mask.from_surface(self.img)

		self.rect = self.img.get_rect()
		self.rect.move_ip( numpy.random.randint(100, width),  height)
		self.vel = (numpy.random.randint(3,7)-5, -numpy.random.randint(3,7))


	def draw(self, screen):
		screen.blit(self.img, self.rect)

	def processEvent(self, event):
		pass

	def update(self):
		self.rect = self.rect.move(self.vel)

	def isOutOfWindow(self):
		if self.rect.left >= width or self.rect.right<=0:
			return True
		if self.rect.bottom <= 0 :
			return True


class HealthBar:
	def __init__(self, screen):
		self.screen = screen
		self.color=(255,0,0)
		
	def draw(self,screen, health):
		pygame.draw.rect(screen, self.color, (width/2 - 300,0, health*6, 25), 0)
				
class Background:
	def __init__(self):
		self.img = pygame.image.load("level_01_background.bmp")
		#self.img = pygame.transform.scale(self.img, (width, height))
		self.rect = self.img.get_rect()

	def update(self):
		self.rect = self.rect.move((0,-2))
		pass
	def draw(self, screen):
		screen.blit(self.img, self.rect)

class Environment:
	def __init__(self):
		self.asteroids = []
		for i in range(0,7):
			self.asteroids.append(Asteroid())

	def update(self):
		for i in range(len(self.asteroids)-1,-1,-1):
			if self.asteroids[i].isOutOfWindow():
				del self.asteroids[i]
				self.asteroids.append(Asteroid())
			else:
				self.asteroids[i].update()

		# for i,ast1 in enumerate(self.asteroids):
		# 	x1 , y1 = (ast1.rect.right + ast1.rect.left)/2., (ast1.rect.bottom + ast1.rect.top)/2.
		# 	for j,ast2 in enumerate(self.asteroids):
		# 		if i==j: continue
		# 		x2 , y2 = (ast2.rect.right + ast2.rect.left)/2., (ast2.rect.bottom + ast2.rect.top)/2.
		# 		d = numpy.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
		# 		mx = 500.0*(x2 - x1)/(d+1)
		# 		my = 500.0*(y2 - y1)/(d+1)
		# 		ast2.rect.move(mx,my)


	def draw(self,screen):
		for ast in self.asteroids:
			ast.draw(screen)

	def addAsteroid(self):
		self.asteroids.append(Asteroid())



player = Player()
env = Environment()
healthBar = HealthBar(screen)
background = Background()

gameover = False

if moveConected:
	movePort.write('l')

while 1:
	if moveConected:
		line = movePort.readline()
		a=line.split()
		mx = float(a[4])
		my = float(a[5])
		print line
		player.processMovement(mx,my)
			

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			sys.exit()
			if moveConected:
				movePort.write('q')

		if not gameover:
			if not moveConected:
				player.processEvent(event)
	
	if not gameover:
		env.update()
		player.update()
		background.update()
		player.processCollisions(env)
		
		background.draw(screen)

		player.draw(screen)

		env.draw(screen)

		healthBar.draw(screen,player.health)

		
		if player.health == 0:
			gameover=True

	else:

		print "Game Over"
		if moveConected:
				movePort.write('q')
		
	pygame.display.flip()