# imports the libraries needed for game to function
import pygame
import random
import sys
import math
import time
import os
import csv

# imports all other classes
from Gigabyte import Gigabyte
from Button import Button
from DataSprite import DataSprite

'''
Main class that has the main functionality of the game within it

@author: Ben Williams
@date: 02/16/2019
'''
class Main:
	'''
	Runs when the class is initialized, and initializes all necessary variables

	@params			self
	@returns 		none
	'''
	def __init__(self):
		# initializes pygame and the font library
		pygame.init()
		pygame.font.init()
		pygame.key.set_repeat(1, 1)
		
		# font for text displayed in the window
		self.youWinLoseFont = pygame.font.SysFont("Times New Roman", 30, True)
		self.tutorialFont = pygame.font.SysFont("Times New Roman", 22)
		self.levelFont = pygame.font.SysFont("Times New Roman", 30, True)
		self.clickFont = pygame.font.SysFont("Times New Roman", 18)
		self.titleFont = pygame.font.SysFont("Times New Roman", 128, True)


		# the resolution of the display window
		self.width = 640
		self.height = 480
		
		# variable for size of the tiles in the game (where objects will spawn)
		self.tileSize = 160
		
		# initializes the display
		self.screen = pygame.display.set_mode((self.width, self.height))
		
		# objects to be rendered into the game
		self.gigabytes = []
		self.dataSprites = []
		
		# font object to be shown before each level
		self.levelMessage = ""

		# objects to be rendered for the tutorial
		self.tutorial = []
		self.tutorial.append(self.tutorialFont.render("Try right clicking on the big blue object!", True, (255, 255, 255)))
		self.tutorial.append(self.tutorialFont.render("Now try left clicking on the object...", True, (255, 255, 255)))
		self.tutorial.append(self.tutorialFont.render("Uh oh... Two colours?", True, (255, 255, 255)))
		self.tutorial.append(self.tutorialFont.render("You're on your own from here... Good Luck!", True, (255, 255, 255)))
		self.tutorial.append(self.clickFont.render("Click to Continue", True, (255, 255, 255)))
		self.tutorialNumber = 0

		# objects to be rendered on the menu
		self.menuObjects = {}
		self.menuObjects["playButton"] = Button(self.width / 2 - 75, self.height - 200, 150, 50, "Play Game")
		self.menuObjects["instructionsButton"] = Button(self.width / 2 - 75, self.height - 145, 150, 50, "Instructions")
		self.menuObjects["background"] = pygame.image.load("assets/background.png")
		self.menuObjects["title"] = self.titleFont.render("Anonica", True, (255, 0, 0))

		self.instructionsObjects = {}
		self.instructionsObjects["backButton"] = Button(5, self.height - 55, 150, 50, "Back")
		self.instructionsObjects["instructions1"] = self.tutorialFont.render("Bits of data have gone missing from the Canadian Government's files,", False, (255, 255, 255))
		self.instructionsObjects["instructions2"] = self.tutorialFont.render("and it is suspected that the American hacker group, Anonica, is", False, (255, 255, 255))
		self.instructionsObjects["instructions3"] = self.tutorialFont.render("responsible. As the expert computer scientist you are, Prime Minister", False, (255, 255, 255))
		self.instructionsObjects["instructions4"] = self.tutorialFont.render("Justin Trudeau is trusting you with the task of protecting the rest", False, (255, 255, 255))
		self.instructionsObjects["instructions5"] = self.tutorialFont.render("of the data. In order to stop the data from going missing, you must", False, (255, 255, 255))
		self.instructionsObjects["instructions6"] = self.tutorialFont.render("return each bit to their respective space in memory, also known as a", False, (255, 255, 255))
		self.instructionsObjects["instructions7"] = self.tutorialFont.render("Gigabyte. Data sprites will be constantly spawning and moving around", False, (255, 255, 255))
		self.instructionsObjects["instructions8"] = self.tutorialFont.render("the map, and will be attracted to the Gigabyte that is currently", False, (255, 255, 255))
		self.instructionsObjects["instructions9"] = self.tutorialFont.render("'turned on'. Be careful though! There are many different types and", False, (255, 255, 255))
		self.instructionsObjects["instructions10"] = self.tutorialFont.render("and colours of Gigabytes. If a piece of data is returned to the wrong", False, (255, 255, 255))
		self.instructionsObjects["instructions11"] = self.tutorialFont.render("colour or type, it will go into the hands of Anonica.  Good Luck!", False, (255, 255, 255))

		# objects to be rendered when the player wins
		self.winLoseObjects = {}
		self.winLoseObjects["youWinLose"] = self.youWinLoseFont.render("", False, (255, 255, 255))
		self.winLoseObjects["playAgainButton"] = Button(self.width / 2 - 155, self.height - 150, 150, 50, "Play Again")
		self.winLoseObjects["quitButton"] = Button(self.width / 2 + 5, self.height - 150, 150, 50, "Quit")

		# variables for the frames per second
		self.frameRate = 30
		self.currentTime = 0
		self.previousTime = 0
		self.delta = 0
		
		# variable to test if game is running or not
		self.running = False
		
		# variable for the state of the game
		self.gameState = "MENU"
		
		# variables to hold information about the level
		self.numLevels = 25
		self.level = 0
		self.levelMap = []
		self.spawnCoordinates = []
		
		# variables for spawning
		self.spawnTime = 250
		self.currentSpawnTime = 0
		self.previousSpawnTime = 0
		self.totalNumberOfData = 0
		self.numberOfDataSpawned = 0
		self.numberOfColours = 0
		self.numberOfGigabytes = 0
		self.attracting = None

		# number of lives the player has
		self.lives = 0
	
	'''
	Gets the user input through mouse/keyboard input

	@params			self
	@returns		none
	'''
	def getInput(self):
		# calls the getButtonInput method
		self.getButtonInput()
		
		# loops through the events in the game
		for event in pygame.event.get():
			# if the user clicks the 'X' button, changes the running property to false
			if event.type == pygame.QUIT:
				self.running = False
			
			# if the user presses the escape key, changes the running property to false
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.running = False
			
			# if the user clicks a button on the mouse
			if event.type == pygame.MOUSEBUTTONDOWN:

				# if the game is running, gets the x, y coordinates of the mouse, as well as the button clicked
				if self.gameState == "PLAYING":

					(mouseX, mouseY) = pygame.mouse.get_pos()
					mouseButton = event.button

					# tests if the gigabyte object is clicked, if it is, updates the attracting variable
					for gigabyte in self.gigabytes:

						if self.attracting == None:
							self.attracting = gigabyte if gigabyte.isClicked(mouseX, mouseY, mouseButton) and gigabyte.getAttracting() else None

						elif gigabyte.getAttracting() and gigabyte.isClicked(mouseX, mouseY, mouseButton):
							self.attracting = None

				# if a tutorial page is being shown, continues the game once the user clicks the left mouse button
				elif self.gameState == "TUTORIAL":

					if event.button == 1:
						self.tutorialNumber += 1
						self.gameState = "PLAYING"

				#if a level number page is being shown, continues to the next screen once the user clicks the left mouse button
				elif self.gameState == "LEVEL_NUMBER":

					if event.button == 1 and self.tutorialNumber < len(self.tutorial) - 1:
						self.gameState = "TUTORIAL"

					elif event.button == 1:
						self.gameState = "PLAYING"

	'''
	Tests if a button is clicked using the Button class

	@params			self
	@returns		none
	'''
	def getButtonInput(self):
		# if the user is on the menu, tests if the play and instructions buttons are clicked
		if self.gameState == "MENU":

			# loads the level and updates the game state when the play button is clicked
			if self.menuObjects["playButton"].isClicked():
				self.gameState = "LEVEL_NUMBER"
				self.level += 1
				self.loadLevel()
			
			# shows the instructions screen when the instructions button is clicked
			if self.menuObjects["instructionsButton"].isClicked():
				self.gameState = "INSTRUCTIONS"

		# if the game is on the instructions screen, tests if the back button is clicked
		elif self.gameState == "INSTRUCTIONS":

			# returns to the main menu when the back button is clicked
			if self.instructionsObjects["backButton"].isClicked():
				self.gameState = "MENU"

		# if the game is on the end screen, tests if the play again and quit buttons are clicked
		elif self.gameState == "END":

			# resets the game if the play again button is clicked
			if self.winLoseObjects["playAgainButton"].isClicked():
				self.reset()

			# changes the running property to false if the quit button is clicked
			if self.winLoseObjects["quitButton"].isClicked():
				self.running = False

	'''
	Resets the game to it's original state

	@params			self
	@returns		none
	'''
	def reset(self):
		self.level = 1
		self.gigabytes = []
		self.dataSprites = []
		self.spawnCoordinates = []
		self.attracting = None
		self.numberOfGigabytes = 0
		self.numberOfDataSpawned = 0
		self.gameState = "LEVEL_NUMBER"
		self.tutorialNumber = 0
		self.loadLevel()
	
	'''
	Updates all of the objects in the game based on the input received

	@params			self
	@returns		none
	'''
	def update(self):
		# updates the time and delta values to keep a specified frame rate
		self.currentTime = time.time()
		self.delta = 1 / self.frameRate - (self.currentTime - self.previousTime)
		self.previousTime = self.currentTime
	
		# if the game is running, spawns a new data sprite every spawnTime milliseconds, until the total number of sprites have been spawned
		if self.gameState == "PLAYING":
			self.currentSpawnTime = int(round(time.time() * 1000))

			if self.currentSpawnTime - self.previousSpawnTime > self.spawnTime:
				self.previousSpawnTime = self.currentSpawnTime

				if self.numberOfDataSpawned < self.totalNumberOfData:

					for coordinate in self.spawnCoordinates:
						self.numberOfDataSpawned += 1
						self.dataSprites.append(DataSprite(coordinate[0], coordinate[1], self.numberOfColours, self.numberOfTypes))
		
			# updates each gigabyte in the level
			for gigabyte in self.gigabytes:
				gigabyte.update()
			
			# updates each data sprite in the level
			for data in self.dataSprites:

				# tests if there is currently a gigabyte that is attracting
				if self.attracting != None:

					# tests if the data is within the boundaries of the attracting gigabyte
					if self.attracting.getX() <= data.getX() <= self.attracting.getX() + self.attracting.getSize():
						if self.attracting.getY() <= data.getY() <= self.attracting.getY() + self.attracting.getSize():

							#removes the data sprite from the dataSprites list
							self.dataSprites.remove(data)

							# if the data sprite is not the same colour and type as the gigabyte, subtracts 1 from the players total lives
							if data.getColourID() != self.attracting.getColourID() or data.getType() != self.attracting.getType():
								self.lives -= 1

							# if the total number of data sprites is zero, moves onto the next level and resets all of the variables
							if len(self.dataSprites) == 0:
								self.level += 1
								# updates the game state to "END" if the user has passed all levels
								if self.level > self.numLevels:
									self.gameState = "END"
								else:
									self.numberOfGigabytes = 0
									self.gigabytes = []
									self.spawnCoordinates = []
									self.loadLevel()
									self.numberOfDataSpawned = 0
									self.attracting = None
									self.gameState = "LEVEL_NUMBER"

							# updates the game state to "END" if the user is out of lives
							if self.lives <= 0:
								self.gameState = "END"

				# updates the data sprite with the attracting gigabyte
				data.update(self.attracting, self.screen)
	
	'''
	Renders all of the objects into the game

	@params			self
	@returns		none
	'''
	def render(self):
		# makes the screen black
		self.screen.fill((0, 0, 0))
		
		# calls the renderMenuObjects function if the gameState is on the menu
		if self.gameState == "MENU":
			self.renderMenuObjects()

		# calls the renderInstructionsObjects function if the gameState is on the instructions
		elif self.gameState == "INSTRUCTIONS":
			self.renderInstructionsObjects()

		# if the game is running, renders all necessary objects onto the screen
		elif self.gameState == "PLAYING":

			# renders all gigabytes onto the screen
			for gigabyte in self.gigabytes:
				gigabyte.render(self.screen)

			# renders all data sprites onto the screen
			for sprite in self.dataSprites:
				sprite.render(self.screen)

			# renders the total number of lives onto the screen
			livesMessage = self.clickFont.render("Lives: " + str(self.lives), True, (255, 255, 255))
			self.screen.blit(livesMessage, (5, 5))

			# renders the current number of data sprites onto the screen
			numberDataMessage = self.clickFont.render("Number of Data: " + str(len(self.dataSprites)), True, (255, 255, 255))
			self.screen.blit(numberDataMessage, (5, self.height - numberDataMessage.get_height() - 5))

			# renders the total number of data sprites onto the screen
			totalDataMessage = self.clickFont.render("Total Number: " + str(self.totalNumberOfData), True, (255, 255, 255))
			self.screen.blit(totalDataMessage, (5, self.height - numberDataMessage.get_height() - totalDataMessage.get_height() - 10))

		# if the gameState is on a tutorial page, renders the current tutorial page
		elif self.gameState == "TUTORIAL":
			self.screen.blit(self.tutorial[self.tutorialNumber], (self.width / 2 - self.tutorial[self.tutorialNumber].get_width() / 2, 50))
			self.screen.blit(self.tutorial[len(self.tutorial) - 1], (self.width / 2 - self.tutorial[len(self.tutorial) - 1].get_width() / 2, self.tutorial[self.tutorialNumber].get_height() + 55))
		
		# if the gameState is on a level number page, renders the current level number
		elif self.gameState == "LEVEL_NUMBER":
			self.levelMessage = self.levelFont.render("Level " + str(self.level), True, (255, 255, 255))
			clickMessage = self.clickFont.render("Click to Continue", True, (255, 255, 255))

			self.screen.blit(self.levelMessage, (self.width / 2 - self.levelMessage.get_width() / 2, 50))
			self.screen.blit(clickMessage, (self.width / 2 - clickMessage.get_width() / 2, self.levelMessage.get_height() + 55))
		
		# calls the renderWinLoseObjects method is the gameState is "END"
		elif self.gameState == "END":
			self.renderWinLoseObjects()
			
		# updates the display
		pygame.display.update()
	
	'''
	Renders all the objects onto the instructions screen

	@params			self
	@returns 		none
	'''
	def renderInstructionsObjects(self):
		self.instructionsObjects["backButton"].render(self.screen)
		self.screen.blit(self.instructionsObjects["instructions1"], (5, 5))
		self.screen.blit(self.instructionsObjects["instructions2"], (5, 28))
		self.screen.blit(self.instructionsObjects["instructions3"], (5, 51))
		self.screen.blit(self.instructionsObjects["instructions4"], (5, 74))
		self.screen.blit(self.instructionsObjects["instructions5"], (5, 97))
		self.screen.blit(self.instructionsObjects["instructions6"], (5, 120))
		self.screen.blit(self.instructionsObjects["instructions7"], (5, 143))
		self.screen.blit(self.instructionsObjects["instructions8"], (5, 166))
		self.screen.blit(self.instructionsObjects["instructions9"], (5, 189))
		self.screen.blit(self.instructionsObjects["instructions10"], (5, 212))
		self.screen.blit(self.instructionsObjects["instructions11"], (5, 235))

	'''
	Renders all the objects when the player wins or loses

	@params			self
	@returns		none
	'''
	def renderWinLoseObjects(self):
		# updates the win/loss message based on if the player wins or loses
		if self.lives <= 0: self.winLoseObjects["youWinLose"] = self.youWinLoseFont.render("You Lose!", False, (255, 255, 255))
		else: self.winLoseObjects["youWinLose"] = self.youWinLoseFont.render("You Win!", False, (255, 255, 255))

		# gets the width of the win/loss message
		youWinLoseWidth = self.winLoseObjects["youWinLose"].get_width()

		# renders the win/loss message, play again button, and quit button onto the screen
		self.screen.blit(self.winLoseObjects["youWinLose"], (self.width / 2 - youWinLoseWidth / 2, 25))
		self.winLoseObjects["playAgainButton"].render(self.screen)
		self.winLoseObjects["quitButton"].render(self.screen)

	'''
	Renders all the objects onto the menu

	@params			self
	@returns		none
	'''
	def renderMenuObjects(self):
		# scales the background image and renders it onto the screen
		background = pygame.transform.scale(self.menuObjects["background"], (self.width, self.height))
		self.screen.blit(background, (0, 0))

		# renders the title onto the screen
		self.screen.blit(self.menuObjects["title"], (self.width / 2 - self.menuObjects["title"].get_width() / 2, 50))

		# renders the play and instructions buttons onto the screen
		self.menuObjects["playButton"].render(self.screen)
		self.menuObjects["instructionsButton"].render(self.screen)
	
	'''
	Loads the level from a csv file into the levelMap list

	@params			self
	@returns		none
	'''
	def loadLevel(self):
		# loads the csv file and resets the levelMap
		levelPath = "assets/levels/level_" + str(self.level) + ".csv"
		file = open(levelPath)
		reader = csv.reader(file)
		self.levelMap = []

		# reads the csv file and adds it to the levelMap list
		for row in reader:
			rowContents = []
			for col in row:
				rowContents.append(col)
			self.levelMap.append(rowContents)
		
		# reads level-specific information from the levelMap list and updates variables
		self.numberOfColours = int(self.levelMap[3][0])
		self.totalNumberOfData = int(self.levelMap[3][1])
		self.lives = int(self.levelMap[3][2])
		self.numberOfTypes = int(self.levelMap[3][3])
		
		# loops through the levelMap and sets locations for level-specific objects
		for i in range(len(self.levelMap)):
			for j in range(len(self.levelMap[i])):

				# gets spawn locations from the levelMap
				if self.levelMap[i][j] == 's':
					spawnX = j * self.tileSize + self.tileSize / 2
					spawnY = i * self.tileSize + self.tileSize / 2
					self.spawnCoordinates.append([spawnX, spawnY])
				
				# gets gigabyte locations from the levelMap and adds them to the gigabytes list
				elif self.levelMap[i][j] == 'g':
					gigabyteX = j * self.tileSize
					gigabyteY = i * self.tileSize
					self.numberOfGigabytes += 1
					self.gigabytes.append(Gigabyte(gigabyteX, gigabyteY, self.numberOfColours, self.numberOfTypes, self.numberOfGigabytes))
	
	'''
	Runs the main game loop

	@params			self
	@returns		none
	'''
	def main(self):
		self.running = True
		while(self.running):
			self.getInput()
			self.update()
			self.render()
			if self.delta > 0:
				time.sleep(self.delta)
			
		pygame.font.quit()
		pygame.quit()
		sys.exit()
		

# creates a new instance of the main class and starts the game
if __name__ == "__main__":
	main = Main()
	main.main()