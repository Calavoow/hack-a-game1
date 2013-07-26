from obstacles import *
from numpy import array
from random import randint

# Tile class
class Tile:
	def __init__(self):
		# Obstacle containing the entire outline of the tile
		self.outline = None
		# Own obstacles
		self.obstacles = []
		
		self.entrance = array([0.0, 0.0])
		self.exit = array([0.0, 0.0])
		
		# This should not be set in a make_tile function, but when puzzling the tile to the previous one
		self.pos = array([0.0, 0.0])
	
	# Used to move the tile with the rest of the level
	def update(self, x_offset, y_offset):
		self.pos = self.pos + array([x_offset, y_offset])
	
	# Adjust the position of this tile to fit to the given tile (on the right side)
	def fit_to(self, other_tile):
		if other_tile == None:
			return
		new_pos = other_tile.pos + other_tile.exit - self.entrance
		# Also move the contained elements to the right spot
		self.move_content(new_pos - self.pos)
		self.pos = new_pos
	
	# Place the entrance at this location, an alternative to fit_to
	def place_at(self, loc):
		new_pos = loc - self.entrance
		# Also move the contained elements to the right spot
		self.move_content(new_pos - self.pos)
		self.pos = new_pos
		
	def move_content(self, movement):
		self.outline.pos = self.outline.pos + movement
		for obs in self.obstacles:
			obs.pos = obs.pos + movement
	
	# Add all sprites contained in this tile to the given sprite group
	def add_sprites_to(self, sprite_group):
		sprite_group.add(self.outline)
		
	def add_obstacles_to(self, obstacle_list):
		obstacle_list.extend(self.obstacles)
		obstacle_list.append(self.outline)

# Tile build functions
def make_tile1():
	tile = Tile()
	
	# Set the outline
	tile.outline = Obstacle( array([0.0, 0.0]), array([500.0, 600.0]), [
		Line( array([0.0, 200.0]), array([500, 200.0])),
		Line(array([0.0, 300.0]), array([500, 300.0]))
	])
	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([0.0, 200.0])
	tile.exit = array([500.0, 200.0])
	
	return tile;

# List of all tile builders
tileset = [
	make_tile1
]
def make_tile2():
	tile = Tile()
	
	# Set the outline
	tile.outline = Obstacle( array([0.0, 0.0]), array([400.0, 300.0]), [
		Line( array([0.0, 200.0]), array([200.0, 0.0])),
		Line( array([200.0, 0.0]), array([400.0, 0.0])),
		Line( array([0.0, 300.0]), array([200.0, 100.0])),
		Line( array([200.0, 100.0]), array([400.0, 100.0]))
	])
	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([0.0, 200.0])
	tile.exit = array([400.0, 0.0])
	
	return tile;

def make_tile3():
	tile = Tile()
	
	# Set the outline
	tile.outline = Obstacle( array([0.0, 0.0]), array([400.0, 300.0]), [
		Line( array([0.0, 200.0]), array([200.0, 0.0])),
		Line( array([200.0, 0.0]), array([400.0, 200.0])),
		Line( array([0.0, 300.0]), array([200.0, 100.0])),
		Line( array([200.0, 100.0]), array([400.0, 300.0]))
	])
	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([0.0, 200.0])
	tile.exit = array([400.0, 200.0])
	
	return tile;

# List of all tile builders
tileset = [
	make_tile1,
	make_tile2,
	make_tile3
]

# Function to get a new copy of a specific tile
def get_tile(n):
	return tileset[n]()

def get_random_tile():
	n = randint(0, len(tileset) - 1)
	return get_tile(n)

# Get a new tile, and initialize it
def make_tile(n, prev_tile, sprite_group, obstacle_list):
	tile = get_tile(n)
	tile.add_sprites_to(sprite_group)
	tile.add_obstacles_to(obstacle_list)
	tile.fit_to(prev_tile)
	return tile

def make_random_tile(prev_tile, sprite_group, obstacle_list):
	n = randint(0, len(tileset) - 1)
	return make_tile(n, prev_tile, sprite_group, obstacle_list)
