import sys, pygame
import numpy
from constants import width, height
from particles import ParticleEmitter

class Player:
	def __init__(self, serial):
		self.img = pygame.image.load("spaceship_clean_CLEAN.bmp")
		self.img.set_colorkey((104,255,59))
		self.img = pygame.transform.scale(self.img, (100, 100))
		self.mask = pygame.mask.from_surface(self.img)
		self.fimg = self.img

		self.rect = self.img.get_rect()
		self.rect = self.rect.move(width/2, 100)
		self.vel = (0,0)
		self.health = 100

		self.type = 0
		self.ser = serial

		self.angle=0
		self.angleVel=0
		self.angleMin=0
		self.angleMax=0
		self.emitter=None
		self.setMode(0)
		

	def draw(self, screen):
		screen.blit(self.fimg, self.rect)
		if not self.emitter is None:
			self.emitter.draw(screen)

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
		if self.rect.right >= width and mx>0:
			mx=0
		if self.rect.left <= 0 and mx<0:
			mx=0
		if self.rect.top <= 50 and my<0:
			my=0
		if self.rect.bottom >= height/2 and my>0:
			my=0
		self.vel = (mx,my)

	def update(self):
		if self.rect.right >= width and self.vel[0]>0:
			self.vel = (-5, self.vel[1])
		if self.rect.left <= 0 and self.vel[0]<0:
			self.vel = (5, self.vel[1])
		if self.rect.top <= 50 and self.vel[0]<0:
			self.rect.move((0,-self.rect.top+50+10))
			self.vel = (self.vel[0], 5)
		if self.rect.bottom >= height/2 and self.vel[0]>0:
			self.rect.move((0,-self.rect.bottom+height/2-10))
			self.vel = (self.vel[0], -5)


		self.rect = self.rect.move(self.vel)

		self.fimg = pygame.transform.rotate(self.img, self.angle)
		self.mask = pygame.mask.from_surface(self.fimg)
		self.angle+=self.angleVel
		if self.angle<self.angleMin and self.angleVel<0:
			self.angle = self.angleMin
			self.angleVel=-self.angleVel
		if self.angle>self.angleMax and self.angleVel>0:
			self.angle = self.angleMax
			self.angleVel=-self.angleVel

		if not self.emitter is None:
			h= (self.rect.bottom - self.rect.top)/2.0
			self.emitter.pos = (self.rect.left*0.5+self.rect.right*0.5 + h*numpy.sin(self.angle*numpy.pi/180.), self.rect.bottom*0.5+self.rect.top*0.5  + h*numpy.cos(self.angle*numpy.pi/180.))
			self.emitter.update()


	def processCollisions(self, env):
		objects = env.asteroids
		for i in range(len(objects)-1,-1,-1):
			if objects[i].rect.colliderect(self.rect):
				offset = ( (objects[i].rect.left - self.rect.left), (objects[i].rect.top - self.rect.top) )
				if self.mask.overlap(objects[i].mask, offset) != None:
					self.health -= 10
					env.delAsteroid(i)
					env.addAsteroid()

					if not self.ser is None: self.ser.write('5')

		if env.rectRocks.colliderect(self.rect):
			offset = ( (env.rectRocks.left - self.rect.left), (env.rectRocks.top - self.rect.top) )
			if self.mask.overlap(env.mask, offset) != None:
				self.health -= 10	
				minx = 100000
				for i in range(-10,10):
					if self.mask.overlap(env.mask, (offset[0]+i*10, offset[1]))==None:
						x = i*10
						if x<minx:
							minx=x
				self.rect = self.rect.move((-minx,0))
				if not self.ser is None: self.ser.write('5')
				env.addSmoke((self.rect.left*0.5+self.rect.right*0.5, self.rect.bottom*0.5+self.rect.top*0.5))


	def setMode(self, mode):
		if mode==0:
			#self.angle = 180
			self.angleVel=3
			self.angleMin=170
			self.angleMax=190
			imageList=["Smoke2.bmp"]
			pos = (self.rect.left*0.5+self.rect.right*0.5, self.rect.bottom*0.5+self.rect.top*0.5)
			angle = 270
			funnel = 20
			vel=10
			lifetime=30
			N=40
			finite=False
			self.emitter=ParticleEmitter(imageList, pos, angle, funnel, vel, lifetime, N, finite, (20,20), 50)
		
		if mode==1:
			#self.angle = 0
			self.angleVel=1
			self.angleMin=340
			self.angleMax=380
			imageList=["Smoke1.bmp"]
			pos = (self.rect.left*0.5+self.rect.right*0.5, self.rect.bottom*0.5+self.rect.top*0.5)
			angle = 90
			funnel = 10
			vel=10
			lifetime=10
			N=40
			finite=False
			if not self.emitter is None:
				del self.emitter
			self.emitter=ParticleEmitter(imageList, pos, angle, funnel, vel, lifetime, N, finite, (20,20), 50)



		if mode==2:
			#self.angle = 0
			self.angleVel=1
			self.angleMin=-2
			self.angleMax=2
			imageList=["Smoke2.bmp"]
			pos = (self.rect.left*0.5+self.rect.right*0.5, self.rect.bottom*0.5+self.rect.top*0.5)
			angle = 90
			funnel = 10
			vel=20
			lifetime=10
			N=40
			finite=False
			if not self.emitter is None:
				del self.emitter
			self.emitter=ParticleEmitter(imageList, pos, angle, funnel, vel, lifetime, N, finite, (20,20), 50)


