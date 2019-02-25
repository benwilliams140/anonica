# imports the libraries needed for the game to function
import pygame
import random
import time

'''
Main 'Object' class that attracts data sprites when left-clicked and changes type when right-clicked

@author: Ben Williams
@date: 02/16/2019
'''
class Gigabyte:
	'''
	Runs when the class is initialized, and initializes all necessary variables

	@params			self	x 	y 	numberOfColours	numberOfTypes	colourID
	@returns		none
	'''
	def __init__(self, x, y, numberOfColours, numberOfTypes, colourID):
		# size of the object
		self.size = 160

		# attracting property
		self.attracting = False

		# initializes all of the different coloured/shaped gigabytes that can be loaded
		self.gigabyte_blue = []
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_square_3.png"))
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_square_2.png"))
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_square_1.png"))
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_circle_3.png"))
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_circle_2.png"))
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_circle_1.png"))
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_triangle_3.png"))
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_triangle_2.png"))
		self.gigabyte_blue.append(pygame.image.load("assets/gigabyte_blue/gigabyte_blue_triangle_1.png"))

		self.gigabyte_green = []
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_square_3.png"))
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_square_2.png"))
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_square_1.png"))
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_circle_3.png"))
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_circle_2.png"))
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_circle_1.png"))
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_triangle_3.png"))
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_triangle_2.png"))
		self.gigabyte_green.append(pygame.image.load("assets/gigabyte_green/gigabyte_green_triangle_1.png"))

		self.gigabyte_orange = []
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_square_3.png"))
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_square_2.png"))
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_square_1.png"))
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_circle_3.png"))
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_circle_2.png"))
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_circle_1.png"))
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_triangle_3.png"))
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_triangle_2.png"))
		self.gigabyte_orange.append(pygame.image.load("assets/gigabyte_orange/gigabyte_orange_triangle_1.png"))

		self.gigabyte_red = []
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_square_3.png"))
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_square_2.png"))
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_square_1.png"))
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_circle_3.png"))
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_circle_2.png"))
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_circle_1.png"))
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_triangle_3.png"))
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_triangle_2.png"))
		self.gigabyte_red.append(pygame.image.load("assets/gigabyte_red/gigabyte_red_triangle_1.png"))

		self.gigabyte_yellow = []
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_square_3.png"))
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_square_2.png"))
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_square_1.png"))
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_circle_3.png"))
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_circle_2.png"))
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_circle_1.png"))
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_triangle_3.png"))
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_triangle_2.png"))
		self.gigabyte_yellow.append(pygame.image.load("assets/gigabyte_yellow/gigabyte_yellow_triangle_1.png"))

		# stores all of the gigabyte sprites in one variable
		self.gigabyteSprites = []
		self.gigabyteSprites.append(self.gigabyte_blue)
		self.gigabyteSprites.append(self.gigabyte_green)
		self.gigabyteSprites.append(self.gigabyte_orange)
		self.gigabyteSprites.append(self.gigabyte_red)
		self.gigabyteSprites.append(self.gigabyte_yellow)
		
		# variables for the total number of colours and types in the current level
		self.numberOfColours = numberOfColours
		self.numberOfTypes = numberOfTypes
		
		# variables for the id and type
		self.colourID = colourID
		self.type = random.randint(1, self.numberOfTypes)

		# number in the animation sequence when attracting
		self.animationNumber = 1
		
		# x and y position
		self.x = x
		self.y = y
	
	'''
	Updates the animation of the gigabyte

	@params			self
	@returns		none
	'''
	def update(self):
		# if the gigabyte is attracting, updates the animation number
		if(self.attracting):
			self.animationNumber += 1
			if self.animationNumber > 3:
				self.animationNumber = 1
		# otherwise, sets the animation number to 1
		else: self.animationNumber = 1
		
	'''
	Renders the gigabyte to the screen, scaling it appropriately

	@params			self	screen
	@returns		none
	'''
	def render(self, screen):
		screen.blit(pygame.transform.scale(self.gigabyteSprites[self.colourID - 1][self.type * 3 - self.animationNumber], (self.size, self.size)), (self.x, self.y))
	
	'''
	Tests if the gigabyte is clicked on by the mouse

	@params			self	mouseX	mouseY	mouseButton
	@returns		boolean if left mouse button is clicked
	'''
	def isClicked(self, mouseX, mouseY, mouseButton):
		# tests if the mouse is within the boundaries of the gigabyte
		if self.x <= mouseX <= self.x + self.size:
			if self.y <= mouseY <= self.y + self.size:

				# if the left mouse button is clicked, calls the updateType function
				if mouseButton == 1:
					self.updateType()

				# if the right mouse button is clicked, calls the updateAttracting function and returns true
				elif mouseButton == 3:
					self.updateAttracting()
					return True

		return False
	
	'''
	Sets the attracting property to the opposite of what it currently is

	@params			self
	@returns		none
	'''
	def updateAttracting(self):
		self.attracting = not self.attracting
	
	'''
	If the gigabyte is not currently attracting, changes the shape of the gigabyte

	@params			self
	@returns		none
	'''
	def updateType(self):
		if not self.attracting:
			self.type += 1
			if self.type > self.numberOfTypes:
				self.type = 1
		
	'''
	Returns the attracting property

	@params			self
	@returns 		attracting
	'''
	def getAttracting(self):
		return self.attracting
	
	'''
	Returns the size of the gigabyte

	@params			self
	@returns 		size
	'''
	def getSize(self):
		return self.size
		
	'''
	Returns the colour id of the gigabyte

	@params			self
	@returns 		colourID
	'''
	def getColourID(self):
		return self.colourID

	'''
	Returns the type of the gigabyte

	@params			self
	@returns 		type
	'''
	def getType(self):
		return self.type
	
	'''
	Returns the x position of the gigabyte

	@params			self
	@returns 		x
	'''
	def getX(self):
		return self.x
	
	'''
	Returns the y position of the gigabyte

	@params			self
	@returns 		y
	'''
	def getY(self):
		return self.y