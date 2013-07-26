import pygame
import math
import objects

from numpy import array, dot, linalg
from Queue import Queue

class Block(objects.Obstacle):
	def __init__(self, x, y):
		#The lines surrounding this 16x16 block
		lines = [
			objects.Line(array([0.0, 0.0]), array([15.0, 0.0])),
			objects.Line(array([15.0, 0.0]), array([15.0, 15.0])),
			objects.Line(array([15.0, 15.0]), array([0.0, 15.0])),
			objects.Line(array([0.0, 15.0]), array([0.0, 0.0]))
		]
		# Call the parent class (Obstacle) constructor
		super(Block, self).__init__(lines)
		#The image will be a 16x16 square
		self.image = pygame.Surface((16,16))
		self.image.fill((255,170,0))
		#Let's draw lines on top of the image for debugging
		self.draw_lines((80, 0, 0))
		#Collision box
		self.rect = self.image.get_rect()
		
		#Set position
		self.rect.x = x
		self.rect.y = y

class SimpleRoom(objects.Obstacle):
	def __init__(self):
		#The lines of which this room consists
		lines = [
			objects.Line(array([201.0,150.0]), array([200.0,400.0])),
			objects.Line(array([501.0, 150.0]), array([500.0,400.0])),
			objects.Line(array([201.0, 150.0]), array([501.0,150.0])),
			objects.Line(array([200.0, 400.0]), array([500.0,400.0]))
		]
		# Call the parent class (Obstacle) constructor
		super(SimpleRoom, self).__init__(lines)
		#The image will be as big as the screen, and transparent
		self.image = pygame.Surface((640,480))
		self.image.fill((255, 255, 255))
		self.image.set_colorkey((255,255,255))
		#Let's draw lines on top of the image for debugging
		self.draw_lines((0,0,0))
		#Collision box
		self.rect = self.image.get_rect()
		
		#Set position
		self.rect.x = 0
		self.rect.y = 0

class Unit(pygame.sprite.Sprite):
	def __init__(self, surface, pos, movement):
		super(Unit, self).__init__()	

		# Set the surface
		self.image = surface

		# Collision box
		self.rect = self.image.get_rect()
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
		return self.pos + array([self.rect.width/2, self.rect.height/2])
	
	def update(self):
		if self.path_calc.is_collided():
			new_direction = self.path_calc.next()
			# Magnitude * normalized direction
			self.movement = linalg.norm(self.movement) * new_direction

		# Can't do +=
		self.pos = self.pos + self.movement
	
	def __repr__(self):
		return "%s at pos: %s" % (self.__class__.__name__, self.pos )

class Player(Unit):
	def __init__(self, pos, movement):
		super(Player, self).__init__(pygame.Surface((16, 16)), pos, movement)

		#The image will be a 16x16 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, (255,0,0), [8,8], 8)
		pygame.draw.circle(self.image, (0,0,255), [8,8], 1)

		self.bounce_angle = 0.0
		self.bounce_angles = Queue()

		self.path_calc = PathCalculator(self, True)

	def update(self):
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


		if self.path_calc.is_collided():
			print "Collision with line."
			new_direction = self.path_calc.next()
			# Magnitude * normalized direction
			new_movement = linalg.norm(self.movement) * new_direction
			# Adjust the angle of the new_movement, according to bounce input.
			if not self.bounce_angles.empty():
				angle = self.bounce_angles.get()
				rot_matrix = array([[math.cos(angle), math.sin(angle)],
					[-math.sin(angle), math.cos(angle)]]) 
				new_movement = dot( rot_matrix, new_movement )
			self.movement = new_movement

		self.pos = self.pos + self.movement

	def increase_bounce_angle( self ):
		self.bounce_angle += 10.0/360.0 * 2.0 * math.pi
		print "Increased bounce angle to %s" % self.bounce_angle
	
	def decrease_bounce_angle( self ):
		self.bounce_angle -= 10.0/360.0 * 2.0 * math.pi
		print "Decreased bounce angle to %s" % self.bounce_angle
	
	def confirm_bounce_angle( self ):
		print "Bounce angle set to %s" % self.bounce_angle
		self.bounce_angles.put( self.bounce_angle )
		self.bounce_angle = 0.0

class Guard(Unit):
	def __init__(self, pos, movement):
		super(Guard, self).__init__(pygame.Surface((16, 16)), pos, movement) 

		#The image will be a 16x16 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, (255,255,0), [8,8], 8)

class Target(Unit):
	def __init__(self, pos, movement):
		super(Target, self).__init__(pygame.Surface((16, 16)), pos, movement) 

		#The image will be a 16x16 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, ( 31, 196, 255 ), [8,8], 8)

class PathCalculator():
	def __init__(self, unit, player=False):
		self.pos = unit.center_pos
		self.direction = unit.movement
		self.unit = unit 

		self.ignore_lines = [] 
		self.direction_queue = Queue()
		self.direction_queue.put( self.calc_next())
	
	def next(self):
		next_direction = self.direction_queue.get()
		if self.direction_queue.empty():
			self.direction_queue.put( self.calc_next())
		print "Next direction for %s: %s" % ( self.unit, next_direction )
		return next_direction

	def calc_next(self):
		""" Calculates the next direction of the Unit.
			returns: A normalized vector, which is the next direction.
		"""
		print "Next calculated for %s" % self.unit
		# Only when self.direction is not the null-vector.
		if not linalg.norm( self.direction ) == 0.0:
			direction_line = objects.Line( self.pos, self.pos + 1e10 * self.direction )
			intersecting_obstacle = direction_line.closest_intersecting_obstacle(
				self.pos, obstacles_list, ignore_lines=self.ignore_lines)
			intersecting_line = direction_line.closest_intersection_with_obstacle(
				self.pos, intersecting_obstacle, ignore_lines=self.ignore_lines)
			assert intersecting_line is not None, "PathCalculator couldn't find a line to jump to." #Truthy
			print "Intersecting with: ", intersecting_line

			# Set new position to intersection point.
			intersecting_point = direction_line.intersection_point( intersecting_line ) 
			print "%s intersects at: %s" % (self, intersecting_point)
			self.pos = intersecting_point
			self.ignore_lines = [intersecting_line]
			
			# Then figure out the outbound angle.
			outbound_direction = self.line_collision(direction_line, intersecting_line)
			self.direction = outbound_direction / linalg.norm( outbound_direction )
		return self.direction
	
	def is_collided( self ):
		movement_line = objects.Line( self.unit.center_pos,
			self.unit.center_pos + self.unit.movement)
		intersecting_obstacle = movement_line.closest_intersecting_obstacle(self.unit.pos, obstacles_list)
		intersecting_line = movement_line.closest_intersection_with_obstacle(self.unit.pos, intersecting_obstacle)
		return intersecting_line is not None

	def draw(self, surface):
		# Draw the the outbound direction.
		point2 = 20 * self.direction + self.pos
		pygame.draw.aaline( surface, (255,0,255),
			[self.pos[0], self.pos[1]],
			[point2[0], point2[1]])

	def line_collision(self, direction, intersecting_line):
		""" Check collision with lines.
			returns: The new movement vector. 
		"""
		print "Intersects line at %s" % self.pos
		#http://stackoverflow.com/questions/573084/how-to-calculate-bounce-angle
		normal = intersecting_line.get_normal()
		u = dot( self.direction, normal ) * normal 
		w = self.direction - u
		print normal, u, self.direction
		return w - u
	
	def __repr__(self):
		return "PathCalculator for %s" % self.unit

#Initialize pygame
pygame.init()

#Set the screen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode([screen_width, screen_height])

#Make instances to place in the world
all_sprites_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()

#Lets make a simple room
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

#Add guards
guard_list = pygame.sprite.Group()
guard_list.add( Guard( array([ 5*screen_width/8, screen_height/2 ]), array([ 0.25, 1.0 ])))

all_sprites_list.add( guard_list )

# Add Target
target_list = pygame.sprite.Group()
target_list.add( Target( array([ 3*screen_width/8, screen_height/2 ]), array([ 0.0, 0.0 ])))

all_sprites_list.add( target_list )

#And set the player
player = Player( array([ screen_width/2, screen_height/2 ]), array([ -1.0, -1.0 ]))
all_sprites_list.add(player)


# THE GAME LOOP
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
done = False

while not done:
	#Event processing
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # Exit button presed.
			done=True # Flag that we are done so we exit this loop
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE: # If user clicked close
				done=True # Flag that we are done so we exit this loop
			elif event.key == pygame.K_LEFT:
				player.decrease_bounce_angle()
			elif event.key == pygame.K_RIGHT:
				player.increase_bounce_angle()
			elif event.key == pygame.K_SPACE:
				player.confirm_bounce_angle()
	
	#Game logic
	all_sprites_list.update()
	
	#Drawing
	screen.fill((255,255,255))
	all_sprites_list.draw(screen)
	player.path_calc.draw(screen)

	#FPS limited to 60
	clock.tick(60)
	pygame.display.flip()

pygame.quit()
