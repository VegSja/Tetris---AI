import pygame #Importing pygame

#TODO: Split window into game and info

pygame.init()

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

	#Colors tetriminos


class App():

	def __init__(self, width, height, app_title, logo_name):
		self.width = width
		self.height = height
		self.app_title = app_title
		self.logo_name = logo_name

	def create_grid(self, nb_height, nb_width, grid_size):
		grid_color = (UI.black)
		for y in range(nb_height):
			for x in range(nb_width):
				rect = pygame.Rect(x*(grid_size+2), y*(grid_size+2), grid_size, grid_size)
				pygame.draw.rect(self.screen, grid_color, rect)

	def draw_scorebar(self):
		#Draw sidebar
		pygame.draw.rect(self.screen, UI.grey, pygame.Rect(self.width - self.gameboard_width, 0, self.width - self.gameboard_width, self.height))

		#Text
		text_header = UI.h1.render("TETRIS", 1, UI.white)
		text_underHeader = UI.u1.render("A game made by Vegard Sjåvik", 1, UI.white)
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
		self.Update()



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
	def Update(self):
		pygame.display.update()
		
	def start_running(self):
		if self.on_init() == False:
			self.running = False

		while(self.running):
			for event in pygame.event.get():
				self.on_event(event)






if __name__ == "__main__":
	app = App(820, 820, "TETRIS", "jeff.png")
	app.start_running()
