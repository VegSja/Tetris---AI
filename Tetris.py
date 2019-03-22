import pygame #Importing pygame

#TODO: Split window into game and info

class App():

	def __init__(self, width, height, app_title, logo_name):
		self.width = width
		self.height = height
		self.app_title = app_title
		self.logo_name = logo_name



	def on_init(self):
		pygame.init()	#Initialize the pygame module
		#Logo
		logo =	pygame.image.load(self.logo_name)
		pygame.display.set_icon(logo)
		pygame.display.set_caption(self.app_title)

		#Create game surface
		self.canvas = pygame.Surface((self.width, self.height))
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.running = True

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False

	def start_game(self):
		game = Game(self.width/2, self.height, self.screen, self.canvas)
		game.render_game_window()

	def start_running(self):
		if self.on_init() == False:
			self.running = False

		while(self.running):
			self.start_game()
			for event in pygame.event.get():
				self.on_event(event)



class Game(object):
	def __init__(self, game_width, game_height, screen, canvas):
		self.game_width = game_width
		self.game_height = game_height
		self.screen = screen
		self.canvas = canvas

	def render_game_window(self):
		tetris_window = pygame.Rect(0,0, self.game_width, self.game_height)
		self.screen.blit(self.canvas, (0,0), tetris_window)



if __name__ == "__main__":
	app = App(640, 400, "TETRIS", "jeff.png")
	app.start_running()
