import pygame
import sys
from config import *
from sprites import *

class Game:

	def __init__(self):
		# función main del juego
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		#self.font = pygame.font.Font('Arial', 32)
		self.running = True

		self.character_spritesheet = Spritesheet('img/character.png')
		self.terrain_spritesheet = Spritesheet('img/terrain.png')

	def create_tilemap(self):
		for i, row in enumerate(TILEMAP):
			for j, column in enumerate(row):
				Ground(self, j, i)
				if column == "B":
					Block(self, j, i)
				if column == "P":
					Player(self, j, i)

	def new(self):
		# función para iniciar una nueva partida
		self.playing = True
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()

		self.create_tilemap()

	def events(self):
		# controla los eventos de la partida
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False

	def update(self):
		# actualiza los datos de la ventana de la partida cuando se ejecuta
		self.all_sprites.update()


	def draw(self):
		# vuelve a dibujar la ventana de la partida con los datos actualizados cuando se ejecuta
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		self.clock.tick(FPS)
		pygame.display.update()

	def main(self):
		# bucle que se ejecuta durante la partida
		while self.playing:
			self.events()
			self.update()
			self.draw()

		self.running = False

	def game_over(self):
		pass

	def intro_screen(self):
		pass

g = Game()
g.intro_screen()
g.new()

while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()