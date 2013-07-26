import pygame
import math
import os
import re
import tiles
import time

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

#Keep track of clicked points, for levelbuilding purposes
clicked = []
clicked_sprites = []

overlay = []

# Keep track of time elapsed, for score
start = time.clock()

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
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# Left mouse button remembers clicked points, for levelbuilding purposes
			if event.button == 1:
				point = Point(event.pos[0] - 3, event.pos[1] - 3)
				clicked.append( event.pos )
				#print "Clicked: array([%f, %f])," % (event.pos)
				clicked_sprites.append(point)
				all_sprites_list.add(point)
			# Right mouse button prints the remembered points (so that no other prints can get inbetween)
			elif event.button == 3:
				print("make_path([")
				for pos in clicked:
					print "array([%f, %f])," % (pos)
				print("])")
				clicked = []
			# Middle mouse button can be used to remove wrongly placed points
			elif event.button == 2:
				clicked.pop()
				
				point = clicked_sprites.pop()
				
				if point != None:
					point.kill()
	
	#Game logic
	all_sprites_list.update(0.0, 0.0)

	
	#Drawing
	screen.fill((255,255,255))
	all_sprites_list.draw(screen)

	# Draw lines
	prev_pos = None
	for pos in clicked:
		if prev_pos != None:
			pygame.draw.aaline(screen, (0,0,0),
				[prev_pos[0], prev_pos[1]],
				[pos[0], pos[1]])
		prev_pos = pos

	prev_pos = None
	for pos in overlay:
		if prev_pos != None:
			pygame.draw.aaline(screen, (0,0,0),
				[prev_pos[0], prev_pos[1]],
				[pos[0], pos[1]])
		prev_pos = pos

	#FPS limited to 60
	clock.tick(60)
	pygame.display.flip()

pygame.quit()
