import pygame
import math

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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #super(Player, self).__init__(self)
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        #The image will be a 16x16 circle 
        self.image = pygame.Surface((16,16))
        self.image.set_colorkey(( 0, 0, 0))       
        pygame.draw.circle(self.image, (255,0,0), [8,8], 8)
        pygame.draw.circle(self.image, (0,0,255), [8,8], 1)
        #Collision box
        self.rect = self.image.get_rect()

        #Set position
        self.rect.x = x
        self.rect.y = y

        self.direction = 0
        self.speed = 3

    def update(self):
        self.rect.x += math.cos(self.direction) * self.speed
        self.rect.y += math.sin(self.direction) * self.speed


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
        all_sprites_list.add(new_block)
        new_block = Block(x, screen_height/2 - 8*16)
        block_list.add(new_block)
        all_sprites_list.add(new_block)
for y in range(screen_height/2 - 8*16, screen_height/2 + 9*16, 16):
        new_block = Block(screen_width/2 - 10*16, y)
        block_list.add(new_block)
        all_sprites_list.add(new_block)
        new_block = Block(screen_width/2 + 10*16, y)
        block_list.add(new_block)
        all_sprites_list.add(new_block)
#And set the player
player = Player(screen_width/2, screen_height/2)
all_sprites_list.add(player)


# THE GAME LOOP
# Used to manage how fast the screen updates
clock=pygame.time.Clock()
done = False

while not done:
    #Event processing
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
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
    
    
    
        
        
        
        
        
