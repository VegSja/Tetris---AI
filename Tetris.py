import pygame #Importing pygame
import numpy as np
from pieces import *
from pygame.locals import *
import random

#TODO: Make the collision detection

pygame.init()

clock = pygame.time.Clock()



class UI():

	#Fonts
	font_score = "./Assets/BebasNeue-Regular.ttf"

	h1 = pygame.font.Font(font_score, 50)
	h2 = pygame.font.Font(font_score, 35)
	u1 = pygame.font.Font(font_score, 20)

	#Colors UI
	white = (255,255,255)
	black = (0,0,0)
	grey = (50,50,50)
	blue = (0,0,255)
	red = (255,0,0)

	#Colors tetriminos

class Piece():

	def __init__(self, x, y, number, gridArr_x, gridArr_y, screen, blocked_coordinates):
		self.gridArr_x = gridArr_x
		self.gridArr_y = gridArr_y
		self.screen = screen
		self.x = x
		self.y = y
		self.blocked_coordinates = blocked_coordinates
		self.number = number
		self.falling = True
		self.blocked = False
		self.draw_piece(self.x, self.y, self.number)


	def draw_rect(self, x, y, rect_size, color):
		rect = pygame.Rect(x, y, rect_size, rect_size)
		pygame.draw.rect(self.screen, color, rect)

	def draw_piece(self, board_x, board_y, pieceNb):
		self.squares_pos = [[],[]] #Holds the x values in index 0 and y values in index 1
		self.board_x = board_x
		self.board_y = board_y
		self.pieceNb = pieceNb
		Piecemap = Pieces.pieces[pieceNb - 1][0]
		for i in range(4):
			for j in range(4):
				if Piecemap[j][i] != 0:
					if board_y + i < 20 and board_x + j > 0 and board_x + j < 10: 
						self.draw_rect(self.gridArr_x[board_x + j], self.gridArr_y[board_y + i], 32, UI.blue)
						self.squares_pos[0].append(board_x + j)
						self.squares_pos[1].append(board_y + i)
					#print("Drawing rect at: ",self.gridArr_x[board_x + j], self.gridArr_y[board_y + i])
					#print("Current pos X: ", self.board_x, "Y: ", self.board_y)
		print("Squares on this tetrimino is: ", self.squares_pos)

	def undraw_piece(self):
		Piecemap = Pieces.pieces[self.pieceNb - 1][0]
		for i in range(4):
			for j in range(4):
				if Piecemap[j][i] != 0:
					self.draw_rect(self.gridArr_x[self.board_x + j], self.gridArr_y[self.board_y + i], 32, UI.black)
					#print("Removing rect at: ",self.gridArr_x[self.board_x + j], self.gridArr_y[self.board_y + i])


	def move(self, new_board_x, new_board_y):
		self.undraw_piece()
		#print("##########################trying to draw piece at ", new_board_x, ", ", new_board_y)
		self.draw_piece(new_board_x, new_board_y, self.pieceNb)
		self.collision_detection()


	def collision_detection(self):
		Piecemap = Pieces.pieces[self.pieceNb - 1][0]
		for i in range(4):
			for j in range(4):
				if Piecemap[j][i] != 0:
					if self.board_y + i + 1 == 20:
						self.falling = False
				#Add more actions for what will not be fallable __________________________________________________________________
					if self.board_x + j == 10 or self.board_x - j == 0:
						self.blocked = True

					for x in range(0, len(self.blocked_coordinates[0])):
						for k in range (0, 3):
							if self.squares_pos[0][k] + 1 == self.blocked_coordinates[0][x] and self.squares_pos[1][k] +1 == self.blocked_coordinates[1][x]:
							#if self.board_x + j == self.blocked_coordinates[0][x] and self.board_y + i +1 == self.blocked_coordinates[1][y]:
								print("Blocked by ", self.squares_pos[0][k]+1, self.squares_pos[1][k] + 1, " == ", self.blocked_coordinates[0][x], self.blocked_coordinates[1][x])
								self.blocked = True
								self.falling = False


	def __del__(self):
		print("Deleted object")



class App():


	def __init__(self, width, height, app_title, logo_name):
		self.width = width
		self.height = height
		self.app_title = app_title
		self.logo_name = logo_name
		self.currentPiece_availible = False
		self.time_last_action = 0
		self.blocked_coordinates = [[],[]] #Index 0 = x, Index 1 = y

	def create_grid(self, nb_height, nb_width, grid_size):
		grid_color = (UI.black)
		self.grid_x = [0,34,68,102,136,170,204,238,272,306]
		self.grid_y = [0,34,68,102,136,170,204,238,272,306,340,374,408,442,476,510,544,578,612,646]
		for y in range(nb_height):
			for x in range(nb_width):
				rect = pygame.Rect(x*(grid_size+2), y*(grid_size+2), grid_size, grid_size)
				pygame.draw.rect(self.screen, grid_color, rect)
				#print("X: ", x*(grid_size+2), "Y: ", y*(grid_size+2))

	def draw_scorebar(self):
		#Draw sidebar
		pygame.draw.rect(self.screen, UI.grey, pygame.Rect(self.width - self.gameboard_width, 0, self.width - self.gameboard_width, self.height))

		#Text
		text_header = UI.h1.render("TETRIS", 1, UI.white)
		text_underHeader = UI.u1.render("Made by Vegard Sjåvik", 1, UI.white)
		text_nextpiece = UI.h2.render("NEXT PIECE:", 1, UI.white)
		text_Score = UI.h2.render("SCORE: ", 1, UI.white)
		text_distance = UI.h2.render("Distace: ", 1, UI.white)
		text_linescleared = UI.h2.render("Lines cleared: ", 1, UI.white)
		text_tetrises = UI.h2.render("Tetrises: ", 1, UI.white)

		#Place the text
		self.screen.blit(text_header, (self.width - self.gameboard_width + 10, 14))
		self.screen.blit(text_underHeader, (self.width - self.gameboard_width + 10, 74))
		self.screen.blit(text_nextpiece, (self.width - self.gameboard_width + 10, 200))
		self.screen.blit(text_Score, (self.width - self.gameboard_width + 10, self.height/2))
		self.screen.blit(text_distance, (self.width - self.gameboard_width + 10, self.height/2 + 80))
		self.screen.blit(text_linescleared, (self.width - self.gameboard_width + 10, self.height/2 + 120))
		self.screen.blit(text_tetrises, (self.width - self.gameboard_width + 10, self.height/2 + 160))

	def draw_board(self, gameboard_width, gameboard_height):
		self.gameboard_width = gameboard_width
		self.gameboard_height = gameboard_height
		#Fill background
		self.screen.fill(UI.white)

		#Create grid in game_board
		self.create_grid(20, 10, 32)
		self.draw_scorebar()
		pygame.display.update()

	def on_init(self):
		pygame.init()	#Initialize the pygame module
		#Logo
		logo =	pygame.image.load(self.logo_name)
		pygame.display.set_icon(logo)
		pygame.display.set_caption(self.app_title)
		#Create game surface
		self.canvas = pygame.Surface((self.width, self.height))
		self.screen = pygame.display.set_mode((self.width, self.height))

		self.draw_board(int(self.width/2), self.height)

		self.running = True

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False

	def auto_fall(self):
		dt = clock.tick() #Sets up framerate
		self.time_last_action += dt
		#print("Should fall", self.time_last_action)
		if self.time_last_action > 250 and self.currentPiece.falling == True:
			self.currentPiece.move(self.currentPiece.board_x, self.currentPiece.board_y + 1)
			self.time_last_action = 0
			pygame.display.update()
		#	if self.currentPiece.board_y == 18:
		#		self.currentPiece.falling = False


	def Update(self):
		if self.currentPiece_availible == False:
			print("Spawning new piece")
			self.currentPiece = Piece(5, 5, random.randint(0,7), self.grid_x, self.grid_y, self.screen, self.blocked_coordinates)
			self.currentPiece_availible = True
			print("Not avaliblel")
		elif self.currentPiece_availible != False:
			self.auto_fall()

		if self.currentPiece.blocked == True or self.currentPiece.falling == False:
			for x in range(0, len(self.currentPiece.squares_pos[0])):
				self.blocked_coordinates[0].append(self.currentPiece.squares_pos[0][x])
			for y in range(0, len(self.currentPiece.squares_pos[1])):
				self.blocked_coordinates[1].append(self.currentPiece.squares_pos[1][y])
			print("Blocked Coordinates X: ", self.blocked_coordinates[0], "Y: ", self.blocked_coordinates[1])
			self.currentPiece_availible = False
			#print("Blocked Coordinates X: ", self.blocked_coordinates[0], "Y: ", self.blocked_coordinates[1])

		#Keyboard events
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_SPACE and self.currentPiece_availible == False:
					self.currentPiece = Piece(5, 5, 4, self.grid_x, self.grid_y, self.screen)
					pygame.display.update()
				if event.key == K_BACKSPACE:
					self.currentPiece.undraw_piece()
					del self.currentPiece
					pygame.display.update()
					self.currentPiece_availible = False
				if event.key == K_w and self.currentPiece_availible == True:
					print(self.currentPiece.board_x)
					self.currentPiece.move(self.currentPiece.board_x, self.currentPiece.board_y - 1) 
					pygame.display.update()

		
	def start_running(self):
		if self.on_init() == False:
			self.running = False

		while(self.running):
			self.Update()
			for event in pygame.event.get():
				self.on_event(event)






if __name__ == "__main__":
	app = App(680, 680, "TETRIS", "jeff.png")
	app.start_running()
