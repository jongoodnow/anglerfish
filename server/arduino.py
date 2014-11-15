import serial

class Arduino(object):

	def __init__(self, dev, port=9600):
		self.ser = serial.Serial(dev, 9600)

	def read(self):
		return self.ser.readline()

	def write(self, buf):
		self.ser.write(buf)