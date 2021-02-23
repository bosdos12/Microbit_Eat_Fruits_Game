from microbit import *
from random import randint
from time import sleep as tsleep

class GameData:
	def __init__(self, _fruitEx, _fruitLoc, _snakeLocs, _butA_stat, _butB_stat):
		self.fruitExists = _fruitEx
		self.fruitLocation = _fruitLoc
		self.snakeLocations = _snakeLocs
		self.leftButton = _butA_stat
		self.rightButton = _butB_stat

	def clearGame(self):
		self.fruitExists = False
		self.fruitLocation = ["F", "F"]
		self.snakeLocations = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
		self.leftButton = "<"
		self.rightButton = "^"

# Creating the snake class
class Snake:
	def __init__(self, _sn, _sbody, _sPoints):
		self.name = _sn
		self.snakeBody = _sbody
		self.points = _sPoints
	def clearSnake(self):
		self.name = "Mr.Snake"
		self.snakeBody = [[2, 2]]
		self.points = 0


# Creating the snake and game objects
gameData = GameData(False, ["F", "F"], [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], "<", "^")
snake = Snake("Mr.Snake", [[2, 2]], 0)


def main():
	aptS = True
	# asking people to start game
	while aptS:
		display.show("[a]")
		if button_a.is_pressed():
			aptS = False
	# clearing the display
	display.clear()
	# starting a countdown to let people know when the game is starting
	cd = 3
	while cd < 0:
		display.show(str(cd))
		tsleep(1)
		display.clear()

	# creating a reference time point to 
	# be able to end the game after 20seconds of playing
	t_end = running_time() + 30000
	while True:
		if running_time() >= t_end:
			break

		# firstly, setting the head at center via the game grid
		i = 0
		while i < len(snake.snakeBody):
			# the first element of the body array is the head
			display.set_pixel(snake.snakeBody[i][0], snake.snakeBody[i][1], 4)
			i += 1
		# checking if a fruit exists, if it doesnt, rendering one
		if not(gameData.fruitExists):
			createNewFruit()

		# MOVING RELATED FUNCTIONS
		if button_a.is_pressed():
			tsleep(0.5)
			moveSnakeF("horizontal")
		if button_b.is_pressed():
			tsleep(0.5)
			moveSnakeF("vertical")


	# once the 20seconds are over, clearing the screen and ending the game
	display.clear()
	wfNG = True
	# making a simple load animation
	for x in range(5):
		tsleep(0.2)
		display.set_pixel(2, x, 9)
	# showing the people their game score and telling them how to restart
	while wfNG:
		display.show(str(snake.points))
		if button_a.is_pressed():
			# ressetting the game for a fresh one
			wfNG = False
			gameData.clearGame()
			snake.clearSnake()
			# starting a new game
			main()


def moveSnakeF(movingOrientation):
	for i in range(len(snake.snakeBody)):
		# checking for horizontal input
		if movingOrientation == "horizontal":
			# some algorithm to initialise the 
			# player inputs + game state to movements
			if snake.snakeBody[i][0] < 4:
				reRenderScreen(snake.snakeBody[i])
				snake.snakeBody[i][0] += 1
			else:
				reRenderScreen(snake.snakeBody[i])
				snake.snakeBody[i][0] = 0
		elif movingOrientation == "vertical":
			if snake.snakeBody[i][1] > 0:
				reRenderScreen(snake.snakeBody[i])
				snake.snakeBody[i][1] -= 1
			else:
				reRenderScreen(snake.snakeBody[i])
				snake.snakeBody[i][1] = 4


# re rendering the screen after each update for making it fresh
def reRenderScreen(clearLoc):
	# clearing the old user state from the game state array
	gameData.snakeLocations[clearLoc[0]][clearLoc[1]] = 0
	# iterating thru the snake to be able to edit all its elements
	for i in range(len(snake.snakeBody)):
		gameData.snakeLocations[snake.snakeBody[i][0]][snake.snakeBody[i][1]] = 1
	# clearing the old location of the snake
	display.set_pixel(clearLoc[0], clearLoc[1], 0)
	# checking if the old location was the same location as 
	# the game data fruit location, if it was, giving the player +1 points and
	# turning fruitExists to false so a new one can be generated
	if clearLoc == gameData.fruitLocation:
		snake.points += 1
		gameData.fruitExists = False


# creating a fruit, whenever called
def createNewFruit():
	readyToCreate = False
	while not(readyToCreate):
		# generating a randdom number
		rn1 = randint(0, 4)
		rn2 = randint(0, 4)
		# making sure the fruit isnt spawning where the snake is
		if (gameData.snakeLocations[rn1][rn2] != 1):
			# setting the fruit data
			readyToCreate = True
			display.set_pixel(rn1, rn2, 9)
			gameData.fruitLocation = [rn1, rn2]
			gameData.fruitExists = True



# main call	
main()
