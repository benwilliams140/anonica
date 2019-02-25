# imports the libraries needed for the game to function
import pygame

'''
Adds a button functionality to the game, renders a clickable rectangle with text

@author: Ben Williams
@date: 02/16/2019
'''
class Button:
	'''
	Runs when the class is initialized, and initializes all necessary variables

	@params			self	x	y	width	height	text
	@returns		none
	'''
	def __init__(self, x, y, width, height, text):
		# initializes pygame and the font libraries
		pygame.init()
		pygame.font.init()
		
		# sets class variables equal to the variables passed into the function
		self.width = width
		self.height = height
		self.x = x
		self.y = y
		self.text = text

	'''
	Renders the button to the screen

	@params			self	screen
	@returns		none
	'''
	def render(self, screen):
		# draws a white rectangle at (x, y) and of size width x height
		pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))
		
		# initializes a new font
		font = pygame.font.SysFont("Times New Roman", 24)

		#gets the size of the text to be rendered
		(fontWidth, fontHeight) = font.size(self.text)

		# calculates the coordinates where the text should be located
		fontX = self.x + self.width / 2 - fontWidth / 2
		fontY = self.y + self.height / 2 - fontHeight / 2
		
		# creates a new font object to be rendered
		textSurface = font.render(self.text, False, (0, 0, 0))
		
		# renders the text onto the button
		screen.blit(textSurface, (fontX, fontY))
		
	'''
	Tests if the button is clicked

	@params			self
	@returns		mouseClicked
	'''
	def isClicked(self):
		# gets the x and y position of the mouse, and a boolean value for the left mouse button
		(mouseX, mouseY) = pygame.mouse.get_pos()
		(mouseClicked, _, __) = pygame.mouse.get_pressed()
		
		# if the mouse is within the boundaries of the button, returns if the mouse is clicked
		if self.x <= mouseX <= self.x + self.width:
			if self.y <= mouseY <= self.y + self.height:
				return mouseClicked
		
		# otherwise returns false
		return False