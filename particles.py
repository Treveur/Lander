import pygame
import numpy
from constants import width, height


class Particle:
	def __init__(self, image, emitterPos, emitterAngle, emitterFunnel, emitterVel, lifetime, posP=50):
		self.img = image
		self.rimg = self.img
		self.img.set_colorkey((104,255,59))

		self.rect = self.img.get_rect()
		self.rect.move_ip( emitterPos[0]+numpy.random.randint(0,posP)-posP/2, emitterPos[1]+numpy.random.randint(0,posP)-posP/2)
		velRand = emitterVel + 0.1*emitterVel*(numpy.random.rand()-0.5)
		self.rotVel=(numpy.random.rand()-0.5)*10
		self.angle=0

		angle = emitterAngle + emitterFunnel*(numpy.random.rand()-0.5)
		angle = angle*numpy.pi/180.0
		self.vel = (velRand*numpy.cos(angle), velRand*numpy.sin(angle))

		self.lifetime = lifetime
		self.life = self.lifetime




	def draw(self, screen):
		screen.blit(self.rimg, self.rect)

	def processEvent(self, event):
		pass

	def update(self):
		self.angle+=self.rotVel
		self.angle=self.angle%360
		self.rect = self.rect.move(self.vel)
		self.img.set_alpha(self.life*255/self.lifetime)
		self.rimg = pygame.transform.rotate(self.img, self.angle)
		self.life-=1

	def isOutOfWindow(self):
		if self.rect.left >= width or self.rect.right<=0:
			return True
		if self.rect.bottom <= 0 :
			return True

class ParticleEmitter:
	def __init__(self, imageList, pos, angle, funnel, vel, lifetime, N, finite, scaleSize=(50,50), posP=50):
		self.pos=pos
		self.angle=angle
		self.funnel=funnel
		self.vel = vel
		self.lifetime=lifetime
		self.finite=finite 
		self.particles = []
		self.images = []
		self.done = False
		self.imageList=[]
		self.N = N
		self.posP = posP
		
		for image in imageList:
			img = pygame.image.load(image)
			img.set_colorkey((104,255,59))
			img = pygame.transform.scale(img, scaleSize)
			img = pygame.transform.rotate(img, numpy.random.randint(0,270))
			img.set_alpha(255)
			self.imageList.append(img)

		for i in range(0,N): self.addParticle()

		

	def addParticle(self):
		img = self.imageList[numpy.random.randint(-1,len(self.imageList))]
		particle=Particle(img, self.pos, self.angle, self.funnel, self.vel, self.lifetime, self.posP)
		if not self.finite:
			particle.life += particle.lifetime*0.3*(numpy.random.rand()-0.5)
		self.particles.append(particle)
		


	def update(self):
		if len(self.particles)==0 and self.finite:
			self.done=True
		
		ndel=0
		for i in range(len(self.particles)-1,-1,-1):
			self.particles[i].update()
			if self.particles[i].life<0:
				del self.particles[i]
				ndel+=1
		if not self.finite:
			for i in range(0,self.N-len(self.particles)): self.addParticle()
		

	def draw(self,screen):
		for p in self.particles:
			p.draw(screen)
		
