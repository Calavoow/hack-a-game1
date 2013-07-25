import pygame
#import numpy

from numpy import *

#Class representing a line segment
class Line:
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
		
		return (sign(sideA) != sign(sideB)) and (sign(sideC) != sign(sideD))
	
	#Calculates the intersection point between two infinite lines
	def intersection_point(self, other):
		#Vertical lines
		if self.p1[0] == self.p2[0] and other.p1[0] == other.p2[0]:
			return None;
		elif self.p1[0] == self.p2[0]:
			x = self.p1[0]
			(a, b) = other.calcAB()
			y = a * x + b
			return array([x, y])
		elif other.p1[0] == other.p2[0]:
			x = other.p1[0]
			(a, b) = self.calcAB()
			y = a * x + b
			return array([x, y])

		(a, b) = self.calcAB()
		(c, d) = other.calcAB()
		#In case the lines are parallel
		if (a == c): return None
		x = (d - b) / (a - c)
		y = a * x + b
		return array([x, y])		
	
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
	
	def get_normal(self):
		v = self.p2 - self.p1
		# Normal vector -> swap x and y, and multiply one of them by -1
		normal = array([-v[1], v[0]])
		return normal / linalg.norm(normal)
	
	#Draw the line in the specified color on the surface
	def draw(self, surface, color):
		pygame.draw.aaline(surface, color, self.p1.tolist(), self.p2.tolist())
	
	#Translate a line by a vector t
	def translate(self, t):
		self.p1 += t
		self.p2 += t

# A superclass for everything that can be bounced against
class Obstacle(pygame.sprite.Sprite):
	def __init__(self, lines):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		#Subclasses should provide the rect and the image
		
		self.lines = lines
	
	# Check what line (if any) of the lines intersects with the given line
	def intersecting_line(self, other_line):
		isc_lines = []
		for line in self.translated_lines:
			if line.intersects(other_line):
				isc_lines.append(line)
		#In the case that no line intersects
		if isc_lines.length == 0: None
		#Else, select the line closest to the other line's first point
		else:
			mindist = linalg.norm((isc_lines[0].intersectionPoint(other_line) - other_line.p1))
			closest = isc_lines[0]
			for line in isc_lines:
				dist = linalg.norm((line[0].intersectionPoint(other_line) - other_line.p1))
				if dist < mindist:
					mindist = dist
					closest = line
		return closest
	
	# Draw the line on the image
	def draw_lines(self, color):
		for line in self.lines:
			line.draw(self.image, color)
	
	# Call this method to get the lines, translated according to rect.x and rect.y
	def translated_lines(self):
		def translate(line): return line.translate(array([self.rect.x, self.rect.y]))
		return map(translate, self.lines)
	
	

#  l1 = Line(array([0.0, 0.0]),array([8.0, 1.0]))
#  l2 = Line(array([4.0, -5.0]),array([5.0, 2.0]))	
#  l3 = Line(array([2.0, 2.0]),array([4.0, 3.0]))	
#  l4 = Line(array([6.0, 0.0]),array([6.0, 3.0]))	
#  
#  l5 = Line(array([0.0, 0.0]),array([2.0, 2.0]))	
#  l6 = Line(array([0.0, 2.0]),array([2.0, 0.0]))

# l7 = Line(array([0.0, 0.0]),array([4, 0]))
# l8 = Line(array([2,-1]),array([2.0,5]))
#print l1.intersectionPoint(l2)	
#print l5.intersectionPoint(l6)	
# print l7.intersects(l8)
# print l7.intersectionPoint(l8)

