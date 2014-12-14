import pygame
import serial

import sys, pygame
import numpy
import serial
from player import Player
from constants import size, width, height
from particles import ParticleEmitter

from controlls import Controlls

ctrl = Controlls()
serConected = ctrl.serConected
moveConected = ctrl.moveConected

pygame.init()
screen = pygame.display.set_mode(size) 

class Menu:
	def __init__(self):
		self.img = pygame.image.load("Menu_Background.bmp")
		self.img = pygame.transform.smoothscale(self.img, (width, height))
		self.rect = self.img.get_rect()
		self.isInMenu=True

	def update(self):
		pass
	def draw(self,screen):
		if self.isInMenu:
			screen.blit(self.img, self.rect)
		

class Asteroid:
	def __init__(self):
		self.img = pygame.image.load("Jam_Asteroid_V2.bmp")
		self.img.set_colorkey((104,255,59))
		self.img = pygame.transform.scale(self.img, (100, 100))
		self.mask = pygame.mask.from_surface(self.img)

		self.rect = self.img.get_rect()
		self.rect.move_ip( numpy.random.randint(100, width),  height)
		self.vel = (numpy.random.randint(10,20)-15, -numpy.random.randint(10,20))


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

class Bird(Asteroid):
	def __init__(self):
		self.img = [pygame.image.load("Bird_aile_up.bmp"),pygame.image.load("Bird_aile_middle.bmp"),pygame.image.load("Bird_aile_down.bmp")]
		self.vel = (numpy.random.randint(10,20)-15, -numpy.random.randint(10,20))
		for img in self.img: img.set_colorkey((255,255,255))
		for i in range(0,3): self.img[i] = pygame.transform.scale(self.img[i], (40, 40))
		if self.vel[0]<0:
			for i in range(0,3): self.img[i] = pygame.transform.flip(self.img[i], True, False)
		self.mask = pygame.mask.from_surface(self.img[0])

		self.rect = self.img[0].get_rect()
		self.rect.move_ip( numpy.random.randint(100, width),  height)
		
		self.frame=0
		self.animDir=1
		self.time =0

	def update(self):
		self.rect = self.rect.move(self.vel)
		self.time+=1
		self.time=self.time%100
		if self.time%2==0:
			self.frame+=self.animDir
		if self.frame==3 or self.frame==-1:
			self.animDir*=-1
			self.frame+=self.animDir


	def draw(self, screen):
		screen.blit(self.img[self.frame], self.rect)





class HealthBar:
	def __init__(self, screen):
		self.brackets = pygame.image.load("Brackets_V2.bmp")
		self.brackets.set_colorkey((104,255,59))
		self.bRect = self.brackets.get_rect()
		self.bar = pygame.image.load("shield_barre.bmp")
		self.bar.set_colorkey((255,255,255))
		self.barRect = self.bar.get_rect()
		self.screen = screen

		self.bRect = self.bRect.move((width/2-300,0))
		self.barRect = self.barRect.move((width/2-300+35,25))
		
	def draw(self,screen, health):
		screen.blit(self.brackets, self.bRect)
		cropped = pygame.Surface((self.barRect.width*health/100, self.barRect.bottom-self.barRect.top))
		cropped.blit(self.bar,(0,0,80,80))
		screen.blit(cropped, (self.barRect.left,self.barRect.top,10,100))
				
class Background:
	def __init__(self):
		self.vel = [7,7,0]
		self.velBg2 = 10

		self.img = pygame.image.load("level_01_BG02Large.bmp")
		self.rect = self.img.get_rect()
		self.rocks = pygame.image.load("Level_01_BG01_Canyon.bmp")
		self.rocks.set_colorkey((104,255,59))
		self.rocksRect = self.rocks.get_rect()
		D = (self.rect.bottom/self.vel[0]) * (self.velBg2 - self.vel[0])
		self.rocksRect = self.rocksRect.move((0,self.rect.bottom - self.rocksRect.bottom + D))
		self.stage = 0
		self.y = 0
		
		self.lev1 = -2000
		self.lev15 = -4000
		self.lev2 = -self.rect.bottom + height

	def update(self):
		if self.stage!=2:
			self.rect = self.rect.move((0,-self.vel[0]))
			self.rocksRect = self.rocksRect.move((0,-self.velBg2))
		if self.rect.top<self.lev1:
			self.stage=0
		if self.rect.top<self.lev1 and self.rect.top>self.lev15:
			self.stage=1
		if self.rect.top<self.lev15 and self.rect.top>self.lev2:
			self.stage=1.5
		if self.rect.top<self.lev2:
			self.stage=2
		pass

	def draw(self, screen):
		screen.blit(self.img, self.rect)
		screen.blit(self.rocks, self.rocksRect)

class Environment:
	def __init__(self):
		
		self.rocks = pygame.image.load("Level_01_BG01_Canyon.bmp")
		self.rectRocks = self.rocks.get_rect()
		self.rocks.set_colorkey((104,255,59))
		self.mask = pygame.mask.from_surface(self.rocks)

		self.asteroids = []
		for i in range(0,7):
			self.asteroids.append(Asteroid())
		self.emitters=[]
		self.stage=0

	def update(self):
		for i in range(len(self.asteroids)-1,-1,-1):
			if self.asteroids[i].isOutOfWindow():
				del self.asteroids[i]
				if self.stage<=1.6: self.addAsteroid()
			else:
				self.asteroids[i].update()
		
		for i in range(len(self.emitters)-1,-1,-1):
			if self.emitters[i].done:
				del self.emitters[i]
			else:
				self.emitters[i].update()

		self.rocks

	def draw(self,screen):
		for ast in self.asteroids:
			ast.draw(screen)
		for par in self.emitters:
			par.draw(screen)

	def addAsteroid(self):
		if self.stage==0:
			self.asteroids.append(Asteroid())
		if self.stage==1:
			self.asteroids.append(Bird())

	def delAsteroid(self, i):
		if self.asteroids[i].__class__.__name__=='Asteroid':
			imageList=["Asteroid_Frag01.bmp", "Asteroid_Frag02.bmp", "Asteroid_Frag03.bmp"]
			scale = (50,50)
		if self.asteroids[i].__class__.__name__=='Bird':
			imageList=["feather_good.bmp"]
			scale = (20,20)
		pos = (self.asteroids[i].rect.left*0.5+self.asteroids[i].rect.right*0.5, self.asteroids[i].rect.bottom*0.5+self.asteroids[i].rect.top*0.5)
		angle = 90
		funnel = 180
		vel=3
		lifetime=100
		N=20
		finite=True
		self.emitters.append(ParticleEmitter(imageList, pos, angle, funnel, vel, lifetime, N, finite, scale))
		del self.asteroids[i]

	def addSmoke(self, pos):
		imageList=["Smoke1.bmp"]
		angle = 0
		funnel = 360
		vel=10
		lifetime=10
		N=40
		finite=True
		self.emitters.append(ParticleEmitter(imageList, pos, angle, funnel, vel, lifetime, N, finite))


player=None
env = None
healthBar = None
background = None
menu = Menu()
gameover = False
#print menu.__class__.__name__


while 1:
	if menu.isInMenu:
		menu.update()
		menu.draw(screen)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					if moveConected:
						ctrl.movePort.write('q')
					sys.exit()	
				else:
					if serConected:
						player = Player(ctrl.ser)
					else:
						player = Player(None)

					menu.isInMenu=False
					gameover=False
					env = Environment()
					healthBar = HealthBar(screen)
					background = Background()
					gameover = False
					if moveConected:
						ctrl.movePort.write('l')
						ctrl.calibrate()

			if event.type == pygame.QUIT: 
				if moveConected:
					ctrl.movePort.write('q')
				sys.exit()
	else:
		if moveConected and not gameover:
			ctrl.readAccelerometer()
			player.processMovement( (ctrl.ry)/100., (-ctrl.rx)/100.)

		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
				if moveConected:
					ctrl.movePort.write('q')

			if not gameover:
				if not moveConected:
					player.processEvent(event)
		
		if not gameover:
			env.update()
			env.rectRocks=background.rocksRect
			player.update()
			stageOld = background.stage
			background.update()
			if stageOld!=background.stage:
				player.setMode(background.stage)
				env.stage=background.stage

			player.processCollisions(env)
			
			background.draw(screen)

			player.draw(screen)

			env.draw(screen)

			healthBar.draw(screen,player.health)

			
			if player.health == 0:
				gameover=True

		else:
			if moveConected:
				ctrl.movePort.write('q')
			menu.isInMenu=True
			
	pygame.display.flip()