import pygame
#import numpy

from numpy import *

#Class representing a line segment
class Line():
	def __init__(self, p1, p2):
		#The points between which the line segment runs
		self.p1 = p1
		self.p2 = p2
	
	#Checks if this line segment intersects with another line segment
	#From: http://stackoverflow.com/questions/7069420/check-if-two-line-segments-are-colliding-only-check-if-they-are-intersecting-n
	def intersects(self, other) :
		AB = self.p2 - self.p1
		BC = other.p1 - self.p2
		sideC = cross(AB, BC)
		BD = other.p2 - self.p2
		sideD = cross(AB, BD)
		
		CD = other.p2 - other.p1
		DA = self.p1 - other.p2
		sideA = cross(CD, DA)
		DB = self.p2 - other.p2
		sideB = cross(CD, DB)
		
		if (sign(sideA) != sign(sideB)) and (sign(sideC) != sign(sideD)):
			return True;
		else:
			return False;
	
	#Calculates the intersection point between two infinite lines
	def intersectionPoint(self, other):
		(a, b) = self.calcAB()
		(c, d) = other.calcAB()
		x = (d - b) / (a - c)
		y = a * x + b
		return array([x,y])		
	
	#Returns the a and b of the (y = ax + b) representation of this line
	def calcAB(self):
		x1 = self.p1[0]
		y1 = self.p1[1]
		x2 = self.p2[0]
		y2 = self.p2[1]
		
		b = (y1*x2 - y2*x1) / (x2 - x1)
		if x1 != 0:
			a = (y1 - b) / x1
		else:
			a = (y2 - b) / x2
		
		#print "a and b are: (", a, ", ", b, ")"
		return (a, b)
	
	def getNormal(self):
		v = self.p2 - self.p1
		# Normal vector -> swap x and y, and multiply one of them by -1
		normal = array([-v[1], v[0]])
		return normal / linalg.norm(normal)
	
	#Draw the line in the specified color on the surface
	def draw(self, surface, color):
		pygame.draw.aaline(surface, color, self.p1.toList(), self.p2.toList())

# A superclass for everything that can be bounced against
class Obstacle(pygame.sprite.Sprite):
	def __init__(self, lines):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		#Subclasses should provide the rect and the image
		
		self.lines = lines
	
	# Check what line (if any) of the lines intersects with the given line
	def intersectingLine(self, other_line):
		for line in self.lines:
			if line.intersects(other_line):
				return line
		#In the case that no line intersects
		return None
	
	# Draw the line on the image
	def drawLines(self, color):
		for line in self.lines:
			line.draw(self.image, color)
	
	

#  l1 = Line(array([0.0, 0.0]),array([8.0, 1.0]))
#  l2 = Line(array([4.0, -5.0]),array([5.0, 2.0]))	
#  l3 = Line(array([2.0, 2.0]),array([4.0, 3.0]))	
#  l4 = Line(array([6.0, 0.0]),array([6.0, 3.0]))	
#  
#  l5 = Line(array([0.0, 0.0]),array([2.0, 2.0]))	
#  l6 = Line(array([0.0, 2.0]),array([2.0, 0.0]))

#print l1.intersectionPoint(l2)	
#print l5.intersectionPoint(l6)	

