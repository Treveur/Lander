import numpy
import serial
from collections import deque
import time

class Controlls:
	def __init__(self):
		self.serConected = True
		try:
			self.ser = serial.Serial('/dev/tty.usbserial-A50201O6', 9600) # Establish the connection on a specific port
		except:
			self.serConected=False

		self.moveConected = True
		try:
			self.movePort = serial.Serial('/dev/tty.usbmodem621', 38400) # Establish the connection on a specific port
		except:
			try:
				self.movePort = serial.Serial('/dev/tty.usbmodem411', 38400) # Establish the connection on a specific port
			except:
				self.moveConected=False
		self.t = 0 
		self.avgT = 10
		self.data = [deque() for i in range(0,6)]

	def readAccelerometer(self):
		line = self.movePort.readline()
		a=line.split()
		if len(a)==7:
			self.ax = float(a[1])
			self.ay = float(a[2])
			self.az = float(a[3])
			
			self.rx = float(a[4])
			self.ry = float(a[5])
			self.rz = float(a[6])
			
		else:
			print 'Something is wrong!'
		self.t+=1
		self.getAverage()

	def getAverage(self):
		self.data[0].append(self.ax)
		self.data[1].append(self.ay)
		self.data[2].append(self.az)
		self.data[3].append(self.rx)
		self.data[4].append(self.ry)
		self.data[5].append(self.rz)
		self.aax = numpy.mean(self.data[0])
		self.aay = numpy.mean(self.data[1])
		self.aaz = numpy.mean(self.data[2])
		self.arx = numpy.mean(self.data[3])
		self.ary = numpy.mean(self.data[4])
		self.arz = numpy.mean(self.data[5])

	def calibrate(self):
		stop=False
		start = time.time()
		while not stop:
			self.readAccelerometer()
			ctime = time.time()
			if ctime-start>1.0:
				stop=True
		self.zeroax=self.aax
		self.zeroay=self.aay
		self.zeroaz=self.aaz

		self.zerorx=self.arx
		self.zerory=self.ary
		self.zerorz=self.arz

	def getGuestes(self):
		if (self.aax-self.zeroax)<0 and (self.arx-self.zerorx)<0:
			self.left=1
			print 'left'
		else:
			self.left=0

		if (self.aax-self.zeroax)>0 and (self.arx-self.zerorx)>0:
			print 'right'
			self.right=1
		else:
			self.right=0


		
