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
		for obstacle in self.obstacles:
			sprite_group.add(obstacle)
		
	def add_obstacles_to(self, obstacle_list):
		obstacle_list.extend(self.obstacles)
		obstacle_list.append(self.outline)

# Tile build functions
def make_tile_test1():
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

def make_tile_test2():
	tile = Tile()
	
	# Set the outline
	p1 = make_path([ array([0.0, 200.0]), array([200.0, 0.0]), array([400.0, 0.0])])
	p2 = make_path([ array([0.0, 300.0]), array([200.0, 100.0]), array([400.0, 100.0])])
	tile.outline = Obstacle( array([0.0, 0.0]), array([400.0, 300.0]), p1 + p2)
# 	tile.outline = Obstacle( array([0.0, 0.0]), array([400.0, 300.0]), [
# 		Line( array([0.0, 200.0]), array([200.0, 0.0])),
# 		Line( array([200.0, 0.0]), array([400.0, 0.0])),
# 		Line( array([0.0, 300.0]), array([200.0, 100.0])),
# 		Line( array([200.0, 100.0]), array([400.0, 100.0]))
# 	])
	
	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([0.0, 200.0])
	tile.exit = array([400.0, 0.0])
	
	return tile;

def make_tile_test3():
	tile = Tile()
	
	# Set the outline
	p1 = make_path([ array([0.0, 200.0]), array([200.0, 0.0]), array([400.0, 200.0])])
	p2 = make_path([ array([0.0, 300.0]), array([200.0, 100.0]), array([400.0, 300.0])])
	tile.outline = Obstacle( array([0.0, 0.0]), array([400.0, 300.0]), p1 + p2)
# 	tile.outline = Obstacle( array([0.0, 0.0]), array([400.0, 300.0]), [
# 		Line( array([0.0, 200.0]), array([200.0, 0.0])),
# 		Line( array([200.0, 0.0]), array([400.0, 200.0])),
# 		Line( array([0.0, 300.0]), array([200.0, 100.0])),
# 		Line( array([200.0, 100.0]), array([400.0, 300.0]))
# 	])

	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([0.0, 200.0])
	tile.exit = array([400.0, 200.0])
	
	return tile;

# Real Tile build functions
def make_tile1():
	tile = Tile()
	
	# Set the outline
	p1 = make_path([
		array([22.000000, 292.000000]),
		array([153.000000, 291.000000]),
		array([224.000000, 144.000000]),
		array([387.000000, 46.000000]),
		array([654.000000, 45.000000]),
		array([808.000000, 183.000000]),
		array([717.000000, 369.000000]),
		array([600.000000, 457.000000]),
		array([696.000000, 569.000000]),
		array([801.000000, 636.000000]),
		array([929.000000, 573.000000]),
		array([977.000000, 428.000000]),
		array([1064.000000, 349.000000]),
		array([1207.000000, 355.000000]),
	])
	p2 = make_path([
		array([1207.000000, 455.000000]),
		array([1126.000000, 601.000000]),
		array([1022.000000, 773.000000]),
		array([843.000000, 845.000000]),
		array([645.000000, 785.000000]),
		array([504.000000, 648.000000]),
		array([560.000000, 466.000000]),
		array([468.000000, 397.000000]),
		array([484.000000, 322.000000]),
		array([540.000000, 237.000000]),
		array([504.000000, 189.000000]),
		array([359.000000, 268.000000]),
		array([293.000000, 448.000000]),
		array([158.000000, 457.000000]),
		array([22.000000, 392.000000]),
	])
	tile.outline = Obstacle( array([0.0, 0.0]), array([1210.0, 900.0]), p1 + p2)
	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([22.000000, 292.000000])
	tile.exit = array([1207.000000, 355.000000])
	
	return tile;

def make_tile2():
	tile = Tile()
	
	# Set the outline
	p1 = make_path([
		array([8.000000, 308.000000]),
		array([124.000000, 306.000000]),
		array([123.000000, 166.000000]),
		array([329.000000, 308.000000]),
		array([326.000000, 147.000000]),
		array([470.000000, 305.000000]),
		array([467.000000, 143.000000]),
		array([536.000000, 308.000000]),
		array([570.000000, 140.000000]),
		array([610.000000, 308.000000]),
		array([722.000000, 140.000000]),
		array([730.000000, 307.000000]),
		array([945.000000, 142.000000]),
		array([967.000000, 320.000000]),
		array([1089.000000, 312.000000]),
	])
	p2 = make_path([
		array([1089.000000, 412.000000]),
		array([973.000000, 482.000000]),
		array([979.000000, 666.000000]),
		array([747.000000, 476.000000]),
		array([751.000000, 668.000000]),
		array([614.000000, 470.000000]),
		array([614.000000, 659.000000]),
		array([540.000000, 457.000000]),
		array([471.000000, 645.000000]),
		array([471.000000, 458.000000]),
		array([337.000000, 626.000000]),
		array([327.000000, 461.000000]),
		array([116.000000, 630.000000]),
		array([117.000000, 446.000000]),
		array([8.000000, 408.000000]),
	])
	tile.outline = Obstacle( array([0.0, 0.0]), array([1100.0, 700.0]), p1 + p2)
	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([8.000000, 308.000000])
	tile.exit = array([1089.0, 312.0])
	
	return tile;

def make_tile3():
	tile = Tile()
	
	# Set the outline
	p1 = make_path([
		array([25.000000, 454.000000]),
		array([92.000000, 452.000000]),
		array([242.000000, 355.000000]),
		array([362.000000, 344.000000]),
		array([419.000000, 242.000000]),
		array([548.000000, 186.000000]),
		array([712.000000, 188.000000]),
		array([848.000000, 342.000000]),
		array([925.000000, 293.000000]),
		array([919.000000, 227.000000]),
		array([1073.000000, 143.000000]),
		array([1215.000000, 142.000000]),
	])
	p2 = make_path([
		array([1215.000000, 242.000000]),
		array([1139.000000, 328.000000]),
		array([1135.000000, 502.000000]),
		array([1084.000000, 715.000000]),
		array([958.000000, 840.000000]),
		array([782.000000, 844.000000]),
		array([685.000000, 670.000000]),
		array([645.000000, 614.000000]),
		array([605.000000, 603.000000]),
		array([532.000000, 642.000000]),
		array([518.000000, 675.000000]),
		array([501.000000, 751.000000]),
		array([387.000000, 796.000000]),
		array([251.000000, 797.000000]),
		array([134.000000, 676.000000]),
		array([95.000000, 616.000000]),
		array([25.000000, 554.000000]),
	])
	o1 = make_path([
		array([217.000000, 531.000000]),
		array([260.000000, 411.000000]),
		array([367.000000, 397.000000]),
		array([475.000000, 393.000000]),
		array([580.000000, 354.000000]),
		array([698.000000, 393.000000]),
		array([665.000000, 473.000000]),
		array([602.000000, 544.000000]),
		array([513.000000, 582.000000]),
		array([421.000000, 584.000000]),
		array([355.000000, 601.000000]),
		array([250.000000, 584.000000]),
	], True)
	o2 = make_path([
		array([901.000000, 430.000000]),
		array([926.000000, 384.000000]),
		array([966.000000, 347.000000]),
		array([1011.000000, 475.000000]),
		array([964.000000, 639.000000]),
		array([889.000000, 656.000000]),
		array([857.000000, 507.000000]),
	], True)
	tile.outline = Obstacle( array([0.0, 0.0]), array([1250.0, 1000.0]), p1 + p2 + o1 + o2)
	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([25.0, 454.000000])
	tile.exit = array([1215.000000, 142.000000])
	
	return tile;

def make_tile4():
	tile = Tile()
	
	# Set the outline
	p1 = make_path([
		array([20.000000, 192.000000]),
		array([112.000000, 193.000000]),
		array([246.000000, 102.000000]),
		array([414.000000, 93.000000]),
		array([494.000000, 199.000000]),
		array([578.000000, 443.000000]),
		array([578.000000, 568.000000]),
		array([538.000000, 634.000000]),
		array([556.000000, 671.000000]),
		array([640.000000, 696.000000]),
		array([688.000000, 669.000000]),
		array([703.000000, 578.000000]),
		array([651.000000, 446.000000]),
		array([669.000000, 301.000000]),
		array([591.000000, 217.000000]),
		array([588.000000, 94.000000]),
		array([730.000000, 21.000000]),
		array([910.000000, 52.000000]),
		array([937.000000, 204.000000]),
		array([972.000000, 293.000000]),
		array([907.000000, 349.000000]),
		array([939.000000, 432.000000]),
		array([938.000000, 579.000000]),
		array([1013.000000, 693.000000]),
		array([1140.000000, 697.000000]),
	])
	p2 = make_path([
		array([1140.000000, 797.000000]),
		array([1002.000000, 860.000000]),
		array([938.000000, 858.000000]),
		array([498.000000, 777.000000]),
		array([452.000000, 679.000000]),
		array([338.000000, 732.000000]),
		array([339.000000, 824.000000]),
		array([242.000000, 861.000000]),
		array([159.000000, 819.000000]),
		array([160.000000, 695.000000]),
		array([239.000000, 655.000000]),
		array([308.000000, 675.000000]),
		array([419.000000, 629.000000]),
		array([459.000000, 560.000000]),
		array([478.000000, 453.000000]),
		array([459.000000, 334.000000]),
		array([406.000000, 274.000000]),
		array([311.000000, 270.000000]),
		array([313.000000, 344.000000]),
		array([407.000000, 398.000000]),
		array([309.000000, 515.000000]),
		array([165.000000, 456.000000]),
		array([203.000000, 361.000000]),
		array([169.000000, 296.000000]),
		array([118.000000, 311.000000]),
		array([20.000000, 292.000000]),
	])
	o1 = make_path([
		array([736.000000, 722.000000]),
		array([929.000000, 717.000000]),
		array([876.000000, 587.000000]),
		array([865.000000, 440.000000]),
		array([837.000000, 353.000000]),
		array([871.000000, 273.000000]),
		array([851.000000, 195.000000]),
		array([858.000000, 127.000000]),
		array([794.000000, 100.000000]),
		array([781.000000, 145.000000]),
		array([731.000000, 119.000000]),
		array([750.000000, 164.000000]),
		array([686.000000, 142.000000]),
		array([723.000000, 182.000000]),
		array([686.000000, 199.000000]),
		array([729.000000, 215.000000]),
		array([713.000000, 241.000000]),
		array([758.000000, 263.000000]),
		array([752.000000, 328.000000]),
		array([743.000000, 460.000000]),
		array([779.000000, 577.000000]),
		array([757.000000, 667.000000]),
	], True)
	tile.outline = Obstacle( array([0.0, 0.0]), array([1250.0, 1000.0]), p1 + p2 + o1)
	tile.outline.draw_lines((0,0,0))
	tile.entrance = array([20.000000, 192.000000])
	tile.exit = array([1140.000000, 697.000000])
	
	# Add obstacles
	door1 = Door(array([938.000000, 579.000000]), array([938.000000, 858.000000]))
	tile.obstacles.append(Button(290.0, 350.0, lambda unit: door1.open()))
	tile.obstacles.append(door1)
	
	
	return tile;

# List of all tile builders
tileset = [
	make_tile1,
	make_tile2,
	make_tile3,
	#make_tile4
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
