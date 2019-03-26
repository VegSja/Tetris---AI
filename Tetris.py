import pygame #Importing pygame
import numpy as np
from pieces import *
from pygame.locals import *
import random

#TODO:

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

	#Colors tetriminos

class Piece():

	def __init__(self, x, y, number, gridArr_x, gridArr_y, screen):
		self.gridArr_x = gridArr_x
		self.gridArr_y = gridArr_y
		self.screen = screen
		self.x = x
		self.y = y
		self.number = number
		self.draw_piece(self.x, self.y, self.number)
		print(gridArr_x, gridArr_y)

	def draw_rect(self, x, y, rect_size, color):
		rect = pygame.Rect(x, y, rect_size, rect_size)
		pygame.draw.rect(self.screen, color, rect)

	def draw_piece(self, board_x, board_y, pieceNb):
		self.board_x = board_x
		self.board_y = board_y
		self.pieceNb = pieceNb
		Piecemap = Pieces.pieces[pieceNb - 1][0]
		for i in range(4):
			for j in range(4):
				if Piecemap[j][i] != 0:
					self.draw_rect(self.gridArr_x[board_x + j], self.gridArr_y[board_y + i], 39, UI.blue)
					#print("Drawing rect at: ",self.gridArr_x[board_x + j], self.gridArr_y[board_y + i])
					#print("Current pos X: ", self.board_x, "Y: ", self.board_y)

	def undraw_piece(self):
		Piecemap = Pieces.pieces[self.pieceNb - 1][0]
		for i in range(4):
			for j in range(4):
				if Piecemap[j][i] != 0:
					self.draw_rect(self.gridArr_x[self.board_x + j], self.gridArr_y[self.board_y + i], 39, UI.black)
					#print("Removing rect at: ",self.gridArr_x[self.board_x + j], self.gridArr_y[self.board_y + i])


	def move(self, new_board_x, new_board_y):
		self.undraw_piece()
		print("##########################trying to draw piece at ", new_board_x, ", ", new_board_y)
		self.draw_piece(new_board_x, new_board_y, self.pieceNb)

	def posX(self):
		#print("Current pos: ", self.board_x)
		return self.board_x

	def posY(self):
		return self.board_y


class App():


	def __init__(self, width, height, app_title, logo_name):
		self.width = width
		self.height = height
		self.app_title = app_title
		self.logo_name = logo_name
		self.currentPiece = False
		self.time_last_action = 0

	def create_grid(self, nb_height, nb_width, grid_size):
		grid_color = (UI.black)
		self.grid_x = [0,41,82,123,164,205,246,287,328,369]
		self.grid_y = [0,41,82,123,164,205,246,287,328,369,410,451,492,533,574,615,656,697,738,779]
		for y in range(nb_height):
			for x in range(nb_width):
				rect = pygame.Rect(x*(grid_size+2), y*(grid_size+2), grid_size, grid_size)
				pygame.draw.rect(self.screen, grid_color, rect)

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
		self.create_grid(20, 10, 39)
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
		print("Should fall", self.time_last_action)
		if self.time_last_action > 250:
			self.currentPiece.move(self.currentPiece.board_x, self.currentPiece.board_y + 1)
			self.time_last_action = 0
			print("FALLING")
			pygame.display.update()


	def Update(self):
		if self.currentPiece != False:
			self.auto_fall()

		#Keyboard events
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					self.currentPiece = Piece(5, 5, 1, self.grid_x, self.grid_y, self.screen)
					pygame.display.update()
				if event.key == K_w:
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
	app = App(820, 820, "TETRIS", "jeff.png")
	app.start_running()
