import pygame
import math
import objects

from numpy import array, dot, linalg
from Queue import Queue

class Block(objects.Obstacle):
	def __init__(self, x, y):
		#The lines surrounding this 16x16 block
		lines = [
			objects.Line(array([1, 1]), array([14, 1])),
			objects.Line(array([14, 1]), array([14, 14])),
			objects.Line(array([14, 14]), array([1, 14])),
			objects.Line(array([1, 14]), array([1, 1]))
		]
		# Call the parent class (Obstacle) constructor
		super(Block, self).__init__(lines)
		#The image will be a 16x16 square
		self.image = pygame.Surface((16,16))
		self.image.fill((80, 0, 0))
		#Let's draw lines on top of the image for debugging
		self.draw_lines((255,170,0))
		#Collision box
		self.rect = self.image.get_rect()
		
		#Set position
		self.rect.x = x
		self.rect.y = y

class SimpleRoom(objects.Obstacle):
	def __init__(self):
		#The lines of which this room consists
		lines = [
			objects.Line(array([201, 150]), array([200,400])),
			objects.Line(array([501, 150]), array([500,400])),
			objects.Line(array([201, 150]), array([501,150])),
			objects.Line(array([200, 400]), array([500,400]))
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
		new_movement = self.line_collision()
		if new_movement is not None:
			self.movement = new_movement

		# Can't do +=
		self.pos = self.pos + self.movement

	def line_collision(self):
		""" Check collision with lines.
			returns: The new movement vector, if there was a collision. None else.
		"""
		movement_line = objects.Line( self.center_pos,
			self.center_pos + self.movement)
		intersecting_obstacle = movement_line.closest_intersecting_obstacle(self.pos, obstacles_list)
		intersecting_line = movement_line.closest_intersection_with_obstacle(self.pos, intersecting_obstacle)
		if intersecting_line:
			print "Intersects line at %s" % self.pos
			#http://stackoverflow.com/questions/573084/how-to-calculate-bounce-angle
			normal = intersecting_line.get_normal()
			u = dot( self.movement, normal ) * normal 
			w = self.movement - u
			return w - u
		
		return None 

class Player(Unit):
	def __init__(self, pos, movement):
		super(Player, self).__init__(pygame.Surface((16, 16)), pos, movement)

		#The image will be a 16x16 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, (255,0,0), [8,8], 8)
		pygame.draw.circle(self.image, (0,0,255), [8,8], 1)

		self.bounce_angle = 0.0
		self.bounce_angles = Queue()

	def update(self):
		# Collision with guard
		collision_sprite = pygame.sprite.spritecollideany( self, guard_list )
		if collision_sprite:
			print "Collided with guard"

		# Collision with target
		collision_sprite = pygame.sprite.spritecollideany( self, target_list )
		if collision_sprite:
			print "Collided with target"

		new_movement = self.line_collision()
		if new_movement is not None:
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

class PathCalculator(pygame.sprite.Sprite):
	def __init__(self, unit):
		self.pos = unit.pos
		self.direction = player.movement
		self.angle = 0
		
		self.jump_to_line()
	
	def update(self):
		pass

	def jump_to_line(self):
		direction_line = Line( self.pos, self.pos + 1e10 * self.movement )
		closest_line = direction_line.closest_intersection( self.pos, line_list )
		assert closest_line is not None, "PathCalculator couldn't find a line to jump to." #Truthy

		# Set new position to intersection point.
		intersecting_point = direction_line.intersection_point( closest_line ) 
		self.pos = intersecting_point
		
		# Then figure out the outbound angle.


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

# lines_list = [objects.Line(array([201, 150]), array([200,400])),
# objects.Line(array([501, 150]), array([500,400])),
# objects.Line(array([201, 150]), array([501,150])),
# objects.Line(array([200, 400]), array([500,400]))]

#Add guards
guard_list = pygame.sprite.Group()
guard_list.add( Guard( array([ 5*screen_width/8, screen_height/2 ]), array([ 0.25, 1.0 ])))

all_sprites_list.add( guard_list )

# Add Target
target_list = pygame.sprite.Group()
target_list.add( Target( array([ 3*screen_width/8, screen_height/2 ]), array([ 0.0, 0.0 ])))

all_sprites_list.add( target_list )

#And set the player
player = Player( array([ screen_width/2, screen_height/2 ]), array([ 2.0 ,1.0 ]))
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

# 	pygame.draw.aaline(screen, (0,0,0), [201, 150], [200, 400])
# 	pygame.draw.aaline(screen, (0,0,0), [501, 150], [500, 400])
# 	pygame.draw.aaline(screen, (0,0,0), [201, 150], [501, 150])
# 	pygame.draw.aaline(screen, (0,0,0), [200, 400], [500, 400])

	#FPS limited to 60
	clock.tick(60)
	pygame.display.flip()

pygame.quit()
