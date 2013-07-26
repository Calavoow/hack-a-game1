import pygame
#import numpy

from numpy import *

#Class representing a line segment
class Line:
	def __init__(self, p1, p2):
		#The points between which the line segment runs
		self.p1 = p1
		self.p2 = p2
	
	# custom toString method (called __repr__ in python)
	def __repr__(self):
		return  "LINE[(%f, %f), (%f, %f)]" % (self.p1[0], self.p1[1], self.p2[0], self.p2[1])
	
	def __eq__(self, other):
		if type(self) != type(other):
			return False
		else:
			if (self.p1[0] == other.p1[0]) and (self.p1[1] == other.p1[1]) and (self.p2[0] == other.p2[0]) and (self.p2[1] == other.p2[1]):
				return True
			else:
				return False

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
			(a, b) = other.calc_ab()
			y = a * x + b
			return array([x, y])
		elif other.p1[0] == other.p2[0]:
			x = other.p1[0]
			(a, b) = self.calc_ab()
			y = a * x + b
			return array([x, y])

		(a, b) = self.calc_ab()
		(c, d) = other.calc_ab()
		#In case the lines are parallel
		if (a == c): return None
		x = (d - b) / (a - c)
		y = a * x + b
		return array([x, y])		
	
	def closest_intersection(self, pos, other_lines, ignore_lines = []):
		"""Find the closest other intersecting line with self.
		""" 		
		if other_lines == None:
			return None
		
		closest_line = None
		smallest_dist = float("inf")
		
		for line in other_lines:
			if line not in ignore_lines:
				if line.intersects( self ):
					intersection_point = line.intersection_point( self )
					dist = linalg.norm( intersection_point - pos )
					if dist < smallest_dist:
							smallest_dist = dist
							closest_line = line
					elif dist == smallest_dist:
						# SUPER DUPER CORNERCASE, the line intersects a place where two lines overlap/touch (probably a corner)
						print "Extreme corner bounce, intersection point = ", intersection_point
						print "		-> closest = " , closest_line, ", new = ", line
						print "			-> #lines to check = ", len(other_lines)
					
		return closest_line
	
	#Returns the closest intersecting obstacle to pos
	def closest_intersecting_obstacle(self, pos, obstacle_list, ignore_lines = []):
		closest_obstacle = None
		smallest_dist = float("inf")
		
		for obstacle in obstacle_list:
			# Get the closest line in the obstacle
			closest_line = self.closest_intersection_with_obstacle(pos, obstacle, ignore_lines = ignore_lines )
			if closest_line != None:
				intersection_point = closest_line.intersection_point( self )
				dist = linalg.norm( intersection_point - pos )
				# Check if this object has the smallest distance so far
				if dist < smallest_dist:
					smallest_dist = dist
					closest_obstacle = obstacle
		
		return closest_obstacle
	
	#Returns the closest intersecting line of the obstacle
	def closest_intersection_with_obstacle(self, pos, obstacle, ignore_lines = []):
		if obstacle == None: 
			return None
		else:
			return self.closest_intersection(pos, obstacle.translated_lines(), ignore_lines = ignore_lines)
		
	
	#Returns the a and b of the (y = ax + b) representation of this line
	def calc_ab(self):
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
		pygame.draw.line(surface, color, self.p1.tolist(), self.p2.tolist())
	
	#Translate a line by a vector t
	def translate(self, t):
		return Line(self.p1 + t, self.p2 + t)

# A superclass for everything that can be bounced against
class Obstacle(pygame.sprite.Sprite):
	def __init__(self, lines):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		#Subclasses should provide the rect and the image
		
		self.lines = lines
		#By default, the lines are defined relative to the top left of the rect
		self.translation_point = array([0.0, 0.0])
	
	#def closest_intersection(self, pos, line):
	#	line.closest_intersection(pos, self.lines)
	
# 	# Check what line (if any) of the lines intersects with the given line
# 	def intersecting_line(self, other_line):
# 		isc_lines = []
# 		for line in self.translated_lines:
# 			if line.intersects(other_line):
# 				isc_lines.append(line)
# 		#In the case that no line intersects
# 		if isc_lines.length == 0: None
# 		#Else, select the line closest to the other line's first point
# 		else:
# 			mindist = linalg.norm((isc_lines[0].intersection_point(other_line) - other_line.p1))
# 			closest = isc_lines[0]
# 			for line in isc_lines:
# 				dist = linalg.norm((line[0].intersection_point(other_line) - other_line.p1))
# 				if dist < mindist:
# 					mindist = dist
# 					closest = line
# 		return closest
	
	# Called when a line of the obstacle is touched by a unit
	def touched(self, line, unit):
		# Does not do anything for a typical object
		pass
	
	# Draw the line on the image
	def draw_lines(self, color):
		for line in self.lines:
			line.draw(self.image, color)
	
	# Call this method to get the lines, translated according to rect.x and rect.y
	def translated_lines(self):
		def translate(line): return line.translate(array([self.rect.x, self.rect.y]) + self.translation_point)
		return map(translate, self.lines)

"""
The Polygon class represents an obstacle that consists of a simple closed polygon of lines,
	with possibly an underlying image. Basically, it uses a set of points to make a set of lines
	forming a closed polygon.
"""
class Polygon(Obstacle):
	def __init__(self, points):
		# The lines should connect the points
		lines = []
		if len( points ) == 2:
			#The special case of a line
			lines.append(Line(points[0], points[1]))
		elif len( points ) > 1:
			# Meanwhile keep track of the bounds of the figure
			#### --- this could be implemented in the future
# 			left = float("inf")
# 			right = -float("inf")
# 			top = -float("inf")
# 			bottom = float("inf")
			
			lastpoint = points[len(points) - 1]
			for point in points:
				line = Line(lastpoint, point)
				lines.append(line)
				lastpoint = point

		# Call the parent class (Obstacle) constructor
		super(Polygon, self).__init__(lines)

"""
The PolygonFrame class represents an obstacle that consists of a simple closed polygon of lines,
	without NO IMAGE. Only the lines are visible.
"""
class PolygonFrame(Polygon):
	def __init__(self, points, size = [1240, 900]):
		# Call the parent class (Polygon) constructor
		super(PolygonFrame, self).__init__(points)
		#The image will be completely transparent
		self.image = pygame.Surface(size)
		self.image.fill((255,255,255))
		self.image.set_colorkey((255,255,255))
		#Let's draw lines on top of the image for debugging
		self.draw_lines((0, 0, 0))
		#Collision box
		self.rect = self.image.get_rect()
		
		#Set position to (0, 0)
		self.rect.x = 0
		self.rect.y = 0


# l1 = Line(array([0.0, 0.0]), array([3.0, 3.0]))
# l2 = Line(array([1.0, -1.0]), array([1.0, 2.0]))
# l2c = Line(array([1.0, -1.0]), array([1.0, 2.0]))
# 
# obs = Obstacle([l2])
# obs.rect = pygame.Rect([0,0,1,1])
# 
# 
# print "closest_intersection : ", l1.closest_intersecting_obstacle(array([0.0, 0.0]), [obs])

