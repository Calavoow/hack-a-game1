import pygame
import math

from numpy import array, dot, linalg

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
		self.rect.x = x
		self.rect.y = y

		self.movement = movement 
	
	def update(self):
		self.rect.x += self.movement[0]
		self.rect.y += self.movement[1]
		
		# Collision with wall
		collision_sprite = pygame.sprite.spritecollideany( self, block_list )
		if collision_sprite:
			print "collision"
			#http://stackoverflow.com/questions/573084/how-to-calculate-bounce-angle
			normal = collision_sprite.get_normal()
			u = dot( self.movement, normal ) * normal 
			w = self.movement - u
			self.movement = w - u

class Player(Unit):
	def __init__(self, x, y, movement):
		super(Player, self).__init__(pygame.Surface((16, 16)), x, y, movement)

		#The image will be a 16x16 circle 
		self.image.set_colorkey(( 0, 0, 0))		  
		pygame.draw.circle(self.image, (255,0,0), [8,8], 8)
		pygame.draw.circle(self.image, (0,0,255), [8,8], 1)

	def update(self):
		super(Player, self).update()

		# Collision with guard
		collision_sprite = pygame.sprite.spritecollideany( self, block_list )
		if collision_sprite:
			print "Collided with guard"

class Guard(Unit):
	def __init__(self, x, y, movement):
		super(Guard, self).__init__(pygame.Surface((16, 16)), x, y, movement) 

		#The image will be a 16x16 circle 
		self.image.set_colorkey(( 0, 0, 0))		  
		pygame.draw.circle(self.image, (255,255,0), [8,8], 8)

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
for x in range(screen_width/2 - 10*16, screen_width/2 + 10*16, 16):
	new_block = Block(x, screen_height/2 + 8*16)
	block_list.add(new_block)
	new_block = Block(x, screen_height/2 - 8*16)
	block_list.add(new_block)
for y in range(screen_height/2 - 8*16, screen_height/2 + 9*16, 16):
	new_block = Block(screen_width/2 - 10*16, y)
	block_list.add(new_block)
	new_block = Block(screen_width/2 + 10*16, y)
	block_list.add(new_block)
all_sprites_list.add( block_list )
#Add guards
guard_list = pygame.sprite.Group()
guard_list.add( Guard( 5*screen_width/8, screen_height/2, array([ 0, 1 ])))

all_sprites_list.add( guard_list )

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
		if event.type == pygame.KEYDOWN:
			if event.key is pygame.K_ESCAPE: # If user clicked close
				done=True # Flag that we are done so we exit this loop
	
	#Game logic
	all_sprites_list.update()
	
	#Drawing
	screen.fill((255,255,255))
	all_sprites_list.draw(screen)

	#FPS limited to 60
	clock.tick(60)
	pygame.display.flip()

pygame.quit()
