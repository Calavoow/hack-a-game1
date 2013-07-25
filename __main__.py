import pygame
import math
import objects

from numpy import array, dot, linalg
from Queue import Queue

class Block(pygame.sprite.Sprite):
	def __init__(self, x, y):
		#super(Block, self).__init__(self)
		# Call the parent class (Sprite) constructor
		pygame.sprite.Sprite.__init__(self) 
		#The image will be a 16x16	
		self.image = pygame.Surface((16,16))
		#Hexadecimal color
		self.image.fill((80, 0, 0))

		#Collision box
		self.rect = self.image.get_rect()
		#Set position
		self.rect.x = x
		self.rect.y = y
	
	def get_normal(self):
		""" Return a fake normal pointing left.
		"""

		return array([-1,0])

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
		# Collision with lines 
		intersecting_line = self.intersects_line()
		if intersecting_line:
			print "Intersects line at %s" % self.pos
			#http://stackoverflow.com/questions/573084/how-to-calculate-bounce-angle
			normal = intersecting_line.get_normal()
			u = dot( self.movement, normal ) * normal 
			w = self.movement - u
			self.movement = w - u
		
		# Can't do +=
		self.pos = self.pos + self.movement

	def intersects_line( self ):
		movement_line = objects.Line( self.center_pos,
			self.center_pos + self.movement )

		closest_line = None
		for line in lines_list:
			# Get all intersecting lines, with movement_line
			lines = []
			if line.intersects( movement_line ):
				lines.append( line )
			smallest_dist = float("inf")
			for line in lines:
				intersection_point = line.intersection_point( movement_line )
				dist = linalg.norm( intersection_point - self.pos )
				if dist < smallest_dist:
					smallest_dist = dist
					closest_line = line
		
		return closest_line 

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

		# Collisiion with lines
		intersecting_line = self.intersects_line()
		if intersecting_line:
			print "Intersects line at %s" % self.pos
			#http://stackoverflow.com/questions/573084/how-to-calculate-bounce-angle
			normal = intersecting_line.get_normal()
			u = dot( self.movement, normal ) * normal 
			w = self.movement - u
			self.movement = w - u
			if not self.bounce_angles.empty():
				angle = self.bounce_angles.get()
				rot_matrix = array([[math.cos(angle), math.sin(angle)],
					[-math.sin(angle), math.cos(angle)]]) 
				self.movement = dot( rot_matrix, self.movement )

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
lines_list = [objects.Line(array([201, 150]), array([200,400])),
objects.Line(array([501, 150]), array([500,400])),
objects.Line(array([201, 150]), array([501,150])),
objects.Line(array([200, 400]), array([500,400]))]

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
	pygame.draw.aaline(screen, (0,0,0), [201, 150], [200, 400])
	pygame.draw.aaline(screen, (0,0,0), [501, 150], [500, 400])
	pygame.draw.aaline(screen, (0,0,0), [201, 150], [501, 150])
	pygame.draw.aaline(screen, (0,0,0), [200, 400], [500, 400])

	#FPS limited to 60
	clock.tick(60)
	pygame.display.flip()

pygame.quit()
