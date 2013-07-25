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
	def __init__(self, surface, x, y, movement):
		super(Unit, self).__init__()	

		# Set the surface
		self.image = surface

		# Collision box
		self.rect = self.image.get_rect()
		#Set position
		self.x = x 
		self.y = y 

		self.movement = movement 
	
	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		self._x = value
		self.rect.x = self._x

	@property
	def center_x( self ):
		return self.x + self.rect.width/2

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, value):
		self._y = value
		self.rect.y = self._y

	@property
	def center_y( self ):
		return self.y + self.rect.width/2
	
	def update(self):
		# Collision with lines 
		intersecting_line = self.intersects_line()
		if intersecting_line:
			#http://stackoverflow.com/questions/573084/how-to-calculate-bounce-angle
			normal = intersecting_line.get_normal()
			u = dot( self.movement, normal ) * normal 
			w = self.movement - u
			self.movement = w - u

		self.x += self.movement[0]
		self.y += self.movement[1]

	def intersects_line( self ):
		movement_line = objects.Line( array([self.center_x, self.center_y]),
			array([self.center_x + self.movement[0],
			self.center_y + self.movement[1]]) )
		for line in lines_list:
			if line.intersects( movement_line ):
				return line
		return None

class Player(Unit):
	def __init__(self, x, y, movement):
		super(Player, self).__init__(pygame.Surface((16, 16)), x, y, movement)

		#The image will be a 16x16 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, (255,0,0), [8,8], 8)
		pygame.draw.circle(self.image, (0,0,255), [8,8], 1)

		self.bounce_angle = 0
		self.bounce_angles = Queue()

	def update(self):
		super(Player, self).update()

		# Collision with guard
		collision_sprite = pygame.sprite.spritecollideany( self, guard_list )
		if collision_sprite:
			print "Collided with guard"

		collision_sprite = pygame.sprite.spritecollideany( self, target_list )
		if collision_sprite:
			print "Collided with target"
	
	def increase_bounce_angle( self ):
		self.bounce_angle += 1
	
	def decrease_bounce_angle( self ):
		self.bounce_angle -= 1
	
	def confirm_bounce_angle( self ):
		self.bounce_angles.put( self.bounce_angle )

class Guard(Unit):
	def __init__(self, x, y, movement):
		super(Guard, self).__init__(pygame.Surface((16, 16)), x, y, movement) 

		#The image will be a 16x16 circle 
		self.image.set_colorkey(( 0, 0, 0 ))		  
		pygame.draw.circle(self.image, (255,255,0), [8,8], 8)

class Target(Unit):
	def __init__(self, x, y, movement):
		super(Target, self).__init__(pygame.Surface((16, 16)), x, y, movement) 

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
# guard_list.add( Guard( 5*screen_width/8, screen_height/2, array([ 0.25, 1 ])))

all_sprites_list.add( guard_list )

# Add Target
target_list = pygame.sprite.Group()
target_list.add( Target( 3*screen_width/8, screen_height/2, array([ 0, 0 ])))

all_sprites_list.add( target_list )

#And set the player
player = Player(screen_width/2, screen_height/2, array([2,1]))
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
			if event.key is pygame.K_ESCAPE: # If user clicked close
				done=True # Flag that we are done so we exit this loop
			elif event.key is pygame.K_LEFT:
				player.decrease_bounce_angle()
			elif event.key is pygame.K_RIGHT:
				player.increase_bounce_angle()
			elif event.key is pygame.K_SPACE:
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
