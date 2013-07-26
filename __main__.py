import pygame
import math
import os
import re
import tiles

from numpy import array, dot, linalg
from Queue import Queue
from obstacles import *

#Simple point to display on the map
class Point(pygame.sprite.Sprite):
	def __init__(self, x, y):
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self)
		#The image will be a 32x32 square
		self.image = pygame.Surface((5,5))
		pygame.draw.circle(self.image, (0, 0, 150), [2,2], 2)
		#Collision box
		self.rect = self.image.get_rect()
		
		#Set position
		self.rect.x = x
		self.rect.y = y

class Unit(pygame.sprite.Sprite):
	def __init__(self, surface, pos, movement):
		super(Unit, self).__init__()	

		# Set the surface
		self.image = surface

		# Collision box
		self.rect = self.image.get_rect() 
		self.collision_point = self.rect.center
		#Set position
		self.pos = pos 
		# And movement
		self.movement = movement 

		self.path_calc = PathCalculator(self)
	
	@property
	def pos(self):
		return self._pos

	@pos.setter
	def pos(self, value):
		self._pos = value
		self.rect.x = self._pos[0]
		self.rect.y = self._pos[1]

	@property
	def center_pos( self ):
		return self.pos + array([self.collision_point[0], self.collision_point[1]])
	
	def update(self, x_offset):
		# First update position according to x_offset.
		self.path_calc.update( x_offset )
		self.pos = self.pos + array([x_offset, 0.0])

		if self.path_calc.is_collided():
			self.bounce()
			
		# Can't do +=
		self.pos = self.pos + self.movement
	
	# Called when the unit has collided with an obstacle
	def bounce(self):
		# Let the object know that one of its lines has been touched
		obstacle, line = self.path_calc.get_collision()
		obstacle.touched(line, self)
		# Change direction
		new_direction = self.path_calc.next()
		# Magnitude * normalized direction
		self.movement = linalg.norm(self.movement) * new_direction
	
	def __repr__(self):
		return "%s at pos: %s" % (self.__class__.__name__, self.pos )

class Player(Unit):
	def __init__(self, pos, movement):
		super(Player, self).__init__(pygame.Surface((32, 48)), pos, movement)

		#The image will be a 32x32 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, (255,0,0), [16,16], 16)
		pygame.draw.circle(self.image, (0,0,255), [16,16], 1)
		pygame.draw.rect(self.image, (0,255,0), pygame.Rect(0,0,32,48))

		self.bounce_angle = 0.0
		self.bounce_angles = Queue()

		# Manually change the collision point
		self.collision_point = (16, 32) 

		self.path_calc = PathCalculator(self, True)
		
		# Load image and settings
		self.images = self.loadImages()
		self.frame = 0
		self.delay = 6
		self.pause = 0

	def update(self, x_offset):
		# Collision with guard
		collision_sprite = pygame.sprite.spritecollideany( self, guard_list )
		if collision_sprite:
			testtesttest=5
			#print "Collided with guard"

		# Collision with target
		collision_sprite = pygame.sprite.spritecollideany( self, target_list )
		if collision_sprite:
			testtesttest=5
			#print "Collided with target"

		super(Player, self).update( x_offset )

		# Animate the sprite
		self.pause += 1
		if self.pause == self.delay:
			self.pause = 0
			self.frame = ( self.frame + 1 ) % len( self.images['front'] )
			angle = math.atan2(self.movement[1], self.movement[0])
			print self, angle
			#Right side
			if angle > -math.pi/4. and angle < math.pi/4.:
				side = 'right'
			#Front side
			elif angle >= math.pi/4. and angle <= 3.*math.pi/4.:
				side = 'front'
			#Back side
			elif angle >= -3.*math.pi/4. and angle <= -math.pi/4.:
				side = 'back'
			else:
				side = 'left'

			self.image = self.images[side][self.frame]
		
	def loadImages(self):
		images = { 'front': [0]*4, 'back': [0]*4, 'left': [0]*4, 'right': [0]*4 }
		image_directory = os.path.join('images','spy')
		
		#Regexes to extract the right strings.
		image_name_regex = re.compile(r"_[^\W\d_]+(\d)+")
		key_regex = re.compile(r"[^\W\d_]+")
		number_regex = re.compile(r"(\d)+")
		for image in os.listdir(image_directory):
			result = image_name_regex.search(image).group(0)
			# The key in the dictionary, the direction.
			key = key_regex.search( result ).group(0)
			# And the number of the animation frame.
			number = number_regex.search( result ).group(0)
			images[key][int(number)] = pygame.image.load(
				os.path.join(image_directory, image ))

		# Also generate the right images, from the left ones.
		for i, image in enumerate(images['left']):
			images['right'][i] = pygame.transform.flip(image, True, False)
		return images

class Guard(Unit):
	def __init__(self, pos, movement):
		super(Guard, self).__init__(pygame.Surface((32, 32)), pos, movement) 

		#The image will be a 32x32 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, (255,255,0), [16,16], 16)

class Target(Unit):
	def __init__(self, pos, movement):
		super(Target, self).__init__(pygame.Surface((32, 32)), pos, movement) 

		#The image will be a 32x32 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, ( 31, 196, 255 ), [16,16], 16)


class PathCalculator():
	MIN_ANGLE = -30
	MAX_ANGLE = 30
	MAX_DIRECTIONS = 3

	def __init__(self, unit, player=False):
		self.pos = unit.center_pos
		self.direction = unit.movement
		self.unit = unit 

		self.angle = 0
		self.ignore_lines = [] 
		self.direction_queue = Queue(maxsize=self.MAX_DIRECTIONS)
		self.calc_next()
	
	def update( self, x_offset ):
		self.pos = self.pos + array([x_offset, 0])
	
	def next(self):
		# Sync position so that drift is prevented.
		self.sync_position()
		
		# If the queue is empty, use the current direction.
		if self.direction_queue.empty():
			next_direction = self.direction
			self.calc_next()
		# Otherwise use the direction in the queue
		else:
			next_direction = self.direction_queue.get()
		#print "Next direction for %s: %s" % ( self.unit, next_direction )
		return next_direction

	def calc_next(self):
		""" Calculates the next direction of the Unit.
			returns: A normalized vector, which is the next direction.
			raises AssertionError: When the Path Calculator cannot
				find a line to jump to.
		"""
		# Only when self.direction is not the null-vector.
		if not linalg.norm( self.direction ) == 0.0:
			direction_line = Line( self.pos, self.pos + 1e10 * self.direction )
			intersecting_obstacle = direction_line.closest_intersecting_obstacle(
				self.pos, obstacles_list, ignore_lines=self.ignore_lines)
			intersecting_line = direction_line.closest_intersection_with_obstacle(
				self.pos, intersecting_obstacle, ignore_lines=self.ignore_lines)
			assert intersecting_line is not None, "PathCalculator couldn't find a line to jump to." #Truthy

			# Set new position to intersection point.
			intersecting_point = direction_line.intersection_point( intersecting_line ) 
			self.pos = intersecting_point
			self.ignore_lines = [intersecting_line]
			
			# Then figure out the outbound angle.
			outbound_direction = self.line_collision(direction_line, intersecting_line)
			self.direction = outbound_direction / linalg.norm( outbound_direction )
		# self.direction_queue.put( self.direction )

		# Reset player angle adjustments.
		self.angle = 0
	
	def is_collided( self ):
		movement_line = Line( self.unit.center_pos,
			self.unit.center_pos + self.unit.movement)
		intersecting_obstacle = movement_line.closest_intersecting_obstacle(
			self.unit.center_pos, obstacles_list)
		intersecting_line = movement_line.closest_intersection_with_obstacle(
			self.unit.center_pos, intersecting_obstacle)
		return intersecting_line is not None
	
	# Can be called after is_collided to get collided obstacle and line
	def get_collision( self ):
		movement_line = Line( self.unit.center_pos,
			self.unit.center_pos + self.unit.movement)
		intersecting_obstacle = movement_line.closest_intersecting_obstacle(
			self.unit.center_pos, obstacles_list)
		intersecting_line = movement_line.closest_intersection_with_obstacle(
			self.unit.center_pos, intersecting_obstacle)	
		return (intersecting_obstacle, intersecting_line)

	def sync_position( self, surface=None ):
		""" Sync the position of the PathCalculator with the self.unit.
			This repairs the drift in float calculation.
		"""
		# Save the current direction before syncing.
		previous_direction = self.direction
		previous_angle = self.angle

		# Start the sync
		self.pos = self.unit.center_pos
		self.direction = self.unit.movement
		self.ignore_lines = []

		new_direction_queue = Queue(maxsize=self.MAX_DIRECTIONS)
		while not self.direction_queue.empty():
			direction = self.direction_queue.get()
			new_direction_queue.put( direction )

			old_pos = self.pos
			# Jump to a line
			self.calc_next()
			# Draw a line if a surface is given.
			if surface:
				pygame.draw.aaline( surface, (255,0,255),
					[old_pos[0], old_pos[1]],
					[self.pos[0], self.pos[1]])
			# And set the direction as stored in the Queue.
			self.direction = direction

		self.direction_queue = new_direction_queue

		# Do the last jump to the latest position.
		old_pos = self.pos
		self.calc_next()
		self.direction = previous_direction
		self.angle = previous_angle
		# Draw the last line.
		if surface:
			pygame.draw.aaline( surface, (255,0,255),
				[old_pos[0], old_pos[1]],
				[self.pos[0], self.pos[1]])
	
	def increase_angle( self ):
		if self.angle + 10 <= self.MAX_ANGLE:
			print "Increase angle"
			self.angle += 10
			self.rotate_direction( 10.0/360.0 * 2.0 * math.pi )

	def decrease_angle( self ):
		if self.angle - 10 >= self.MIN_ANGLE:
			print "Decrease angle"
			self.angle -= 10
			self.rotate_direction( -10.0/360 * 2 * math.pi )
	
	def confirm_angle( self ):
		if not self.direction_queue.full():
			self.direction_queue.put( self.direction )
			self.calc_next()

	def rotate_direction( self, angle ):
		rot_matrix = array([[math.cos(angle), math.sin(angle)],
			[-math.sin(angle), math.cos(angle)]]) 
		self.direction = dot( rot_matrix, self.direction )

	def draw(self, surface):
		self.sync_position( surface = surface )

		# Draw the the outbound direction.
		point2 = 20 * self.direction + self.pos
		pygame.draw.aaline( surface, (255,0,255),
			[self.pos[0], self.pos[1]],
			[point2[0], point2[1]])

	def line_collision(self, direction, intersecting_line):
		""" Check collision with lines.
			returns: The new movement vector. 
		"""
		#http://stackoverflow.com/questions/573084/how-to-calculate-bounce-angle
		normal = intersecting_line.get_normal()
		u = dot( self.direction, normal ) * normal 
		w = self.direction - u
		return w - u
	
	def __repr__(self):
		return "PathCalculator for %s" % self.unit

#Initialize pygame
pygame.init()

#Set the screen
screen_width = 1240
screen_height = 900
screen = pygame.display.set_mode([screen_width, screen_height])

#Make instances to place in the world
all_sprites_list = pygame.sprite.Group()
obstacles_list = []
guard_list = pygame.sprite.Group()
target_list = pygame.sprite.Group()

#block_list = pygame.sprite.Group()

#Lets make a simple room
"""
room = SimpleRoom()
all_sprites_list.add(room)
obstacles_list = [room]
# Experiment: let's add some blocks too!

for block in [
Block(300, 250),
Block(300, 300),
Block(400, 250),
Block(270, 170),
Block(350, 250),
Block(400, 250),
#Evil cornercase block of doom
Block(screen_width/2 + 80.0, screen_height/2 + 80.0)
]:
	all_sprites_list.add(block)
	obstacles_list.append(block)
"""
polyframe1 = Polygon( array([0.0, 0.0]), array([1240.0, 900.0]), [
	array([50.000000, 43.000000]),
	array([386.000000, 46.000000]),
	array([396.000000, 330.000000]),
	array([253.000000, 336.000000]),
	array([240.000000, 757.000000]),
	array([405.000000, 750.000000]),
	array([410.000000, 476.000000]),
	array([799.000000, 461.000000]),
	array([798.000000, 611.000000]),
	array([943.000000, 618.000000]),
	array([1007.000000, 469.000000]),
	array([916.000000, 360.000000]),
	array([990.000000, 226.000000]),
	array([934.000000, 153.000000]),
	array([725.000000, 145.000000]),
	array([688.000000, 307.000000]),
	array([756.000000, 304.000000]),
	array([686.000000, 437.000000]),
	array([456.000000, 439.000000]),
	array([467.000000, 313.000000]),
	array([597.000000, 306.000000]),
	array([591.000000, 16.000000]),
	array([929.000000, 19.000000]),
	array([1031.000000, 22.000000]),
	array([1133.000000, 228.000000]),
	array([1083.000000, 364.000000]),
	array([1173.000000, 476.000000]),
	array([1120.000000, 641.000000]),
	array([1132.000000, 803.000000]),
	array([787.000000, 774.000000]),
	array([667.000000, 772.000000]),
	array([647.000000, 573.000000]),
	array([535.000000, 579.000000]),
	array([535.000000, 759.000000]),
	array([523.000000, 878.000000]),
	array([40.000000, 858.000000]),
	array([46.000000, 336.000000])
])
polyframe1.draw_lines((0, 0, 0))		
all_sprites_list.add(polyframe1)
obstacles_list = [polyframe1]

#And set the player
player = Player( array([119.000000, 120.000000]), array([ 2.0 , 2.0 ]))
all_sprites_list.add(player)

#Add guards
guard_list = pygame.sprite.Group()
guard_list.add( Guard( array([83.000000, 430.000000]), array([ 0.5, 2.0 ])))
# guard_list.add( Guard( array([461.000000, 817.000000]), array([ 0.5, 2.0 ])))
# guard_list.add( Guard( array([1069.000000, 480.000000]), array([ 0.5, 2.0 ])))

all_sprites_list.add( guard_list )

# Add Target
target_list = pygame.sprite.Group()
target_list.add( Target( array([575.000000, 375.000000]), array([ 0.0, 0.0 ])))

all_sprites_list.add( target_list )

# Add interactive elements
door1 = Door( array([253.000000, 336.000000]), array([46.000000, 336.000000]))
def trigger_door(unit):
	if unit == player:
		door1.open()
for element in [
	door1,
	Button(242.000000, 125.000000, trigger_door)
]:
	all_sprites_list.add(element)
	obstacles_list.append(element)

# Make a tile to start off with
"""
start_tile = tiles.get_tile(0)
start_tile.add_sprites_to(all_sprites_list)
start_tile.add_obstacles_to(obstacles_list)
start_tile.pos = array([0.0, 0.0])
"""

#Keep track of clicked points, for levelbuilding purposes
clicked = []
clicked_sprites = []

# Keep track of last added tile
#last_tile = start_tile

# THE GAME LOOP
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
done = False
speed = 0.0

while not done:
	#Event processing
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # Exit button presed.
			done=True # Flag that we are done so we exit this loop
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: # If user clicked close
				done=True # Flag that we are done so we exit this loop
			elif event.key == pygame.K_RIGHT:
				player.path_calc.decrease_angle()
			elif event.key == pygame.K_LEFT:
				player.path_calc.increase_angle()
			elif event.key == pygame.K_SPACE:
				player.path_calc.confirm_angle()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# Left mouse button remembers clicked points, for levelbuilding purposes
			if event.button == 1:
				point = Point(event.pos[0] - 3, event.pos[1] - 3)
				clicked.append( event.pos )
				print "Clicked: array([%f, %f])," % (event.pos)
				clicked_sprites.append(point)
				all_sprites_list.add(point)
			# Right mouse button prints the remembered points (so that no other prints can get inbetween)
			elif event.button == 3:
				print("REMEMBERED POINTS ----")
				for pos in clicked:
					print "array([%f, %f])," % (pos)
				print("END OF POINTS --------")
			# Middle mouse button can be used to remove wrongly placed points
			elif event.button == 2:
				clicked.pop()
				
				point = clicked_sprites.pop()
				
				if point != None:
					point.kill()
	
	#Game logic
	all_sprites_list.update(speed) 
	
	#Drawing
	screen.fill((255,255,255))
	all_sprites_list.draw(screen)
	player.path_calc.draw(screen)

	# Draw lines
	prev_pos = None
	for pos in clicked:
		if prev_pos:
			pygame.draw.aaline(screen, (0,0,0),
				[prev_pos[0], prev_pos[1]],
				[pos[0], pos[1]])
		prev_pos = pos

	#FPS limited to 60
	clock.tick(60)
	pygame.display.flip()

pygame.quit()
