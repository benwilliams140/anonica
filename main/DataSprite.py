# imports the libraries needed for the game to function
import math
import pygame
import random

'''
Object class that move at random unless being attracted by the larger Gigabytes

@author: Ben Williams
@date: 02/16/2019
'''
class DataSprite:
	'''
	Runs when the class is initialized, and initializes all necessary variables

	@params			self	x	y	numberOfColours	numberOfTypes
	@returns		none
	'''
	def __init__(self, x, y, numberOfColours, numberOfTypes):
		# initializes all of the different coloured/shaped sprites that can be loaded
		self.data_blue = []
		self.data_blue.append(pygame.image.load("assets/data_blue/data_blue_square.png"))
		self.data_blue.append(pygame.image.load("assets/data_blue/data_blue_circle.png"))
		self.data_blue.append(pygame.image.load("assets/data_blue/data_blue_triangle.png"))

		self.data_green = []
		self.data_green.append(pygame.image.load("assets/data_green/data_green_square.png"))
		self.data_green.append(pygame.image.load("assets/data_green/data_green_circle.png"))
		self.data_green.append(pygame.image.load("assets/data_green/data_green_triangle.png"))

		self.data_orange = []
		self.data_orange.append(pygame.image.load("assets/data_orange/data_orange_square.png"))
		self.data_orange.append(pygame.image.load("assets/data_orange/data_orange_circle.png"))
		self.data_orange.append(pygame.image.load("assets/data_orange/data_orange_triangle.png"))

		self.data_red = []
		self.data_red.append(pygame.image.load("assets/data_red/data_red_square.png"))
		self.data_red.append(pygame.image.load("assets/data_red/data_red_circle.png"))
		self.data_red.append(pygame.image.load("assets/data_red/data_red_triangle.png"))
		
		self.data_yellow = []
		self.data_yellow.append(pygame.image.load("assets/data_yellow/data_yellow_square.png"))
		self.data_yellow.append(pygame.image.load("assets/data_yellow/data_yellow_circle.png"))
		self.data_yellow.append(pygame.image.load("assets/data_yellow/data_yellow_triangle.png"))

		# stores all of the data sprites in one variable
		self.dataSprites = []
		self.dataSprites.append(self.data_blue)
		self.dataSprites.append(self.data_green)
		self.dataSprites.append(self.data_orange)
		self.dataSprites.append(self.data_red)
		self.dataSprites.append(self.data_yellow)
		
		# initializes the colour and shape of the sprite
		self.colourID = random.randint(1, numberOfColours)
		self.type =  random.randint(1, numberOfTypes)
		
		# sets the size of the sprite
		self.size = 15
		
		# variable to test if an angle has been generated or not
		self.angleGenerated = False
		
		# variables for position and velocity
		self.x = x
		self.y = y
		self.angle = 0
		self.dx = math.cos(self.angle)
		self.dy = math.sin(self.angle)
		
	'''
	Updates the sprite in relation to the gigabyte that is currently attracting

	@params			self	gigabyte
	@returns		none
	'''
	def update(self, gigabyte, screen):
		# ensures that the gigabyte is not None
		if gigabyte != None:
			# calculates the angle of trajectory towards the attracting gigabyte
			self.angleGenerated = False

			x = gigabyte.getX() + gigabyte.getSize() / 2
			y = gigabyte.getY() + gigabyte.getSize() / 2
			
			distance = math.sqrt(math.pow((x - self.x), 2) + math.pow((y - self.y), 2))
			
			self.angle = math.asin(math.fabs(y - self.y) / distance)
			
			# calculates the velocity of the sprite
			if self.x < x: self.dx = math.cos(self.angle)
			else: self.dx = -math.cos(self.angle)
			
			if self.y < y: self.dy = math.sin(self.angle)
			else: self.dy = -math.sin(self.angle)
			
			# if the colour and type are the same as the gigabyte's colour and type, multiples the speed by 2.5
			if self.colourID == gigabyte.getColourID() and self.type == gigabyte.getType():
				self.dx *= 2.5
				self.dy *= 2.5

		else:
			# if the gigabyte is equal to None, calculates a random angle between 0 and 2pi radians
			if not self.angleGenerated:
				self.angle = random.uniform(0, 2 * math.pi)
				self.angleGenerated = True
				
				# calculates the velocity of the sprite
				self.dx = math.cos(self.angle)
				self.dy = math.sin(self.angle)

		# updates the x and y positions by the velocity
		self.x += self.dx
		self.y += self.dy

		# ensures that the data sprite stays on the screen via screen-wrapping
		if self.x + self.size < 0: self.x = screen.get_width()
		elif self.x > screen.get_width(): self.x = -self.size

		if self.y + self.size < 0: self.y = screen.get_height()
		elif self.y > screen.get_height(): self.y = -self.size
		
	'''
	Renders the sprite to the screen, scaling and rotating it according to its size and angle

	@params			self	screen
	@returns		none
	'''
	def render(self, screen):
		screen.blit(pygame.transform.rotozoom(self.dataSprites[self.colourID - 1][self.type - 1], math.degrees(self.angle), self.size / 160), (self.x, self.y))
		
	'''
	Returns the current x value of the sprite

	@params			self
	@returns 		x
	'''
	def getX(self):
		return self.x
		
	'''
	Returns the current y value of the sprite

	@params			self
	@returns 		y
	'''
	def getY(self):
		return self.y
		
	'''
	Returns the current colour id of the sprite

	@params			self
	@returns 		colourID
	'''
	def getColourID(self):
		return self.colourID

	'''
	Returns the current type of the sprite

	@params			self
	@returns 		type
	'''
	def getType(self):
		return self.type