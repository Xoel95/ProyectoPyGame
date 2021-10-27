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
		self.font = pygame.font.Font('fonts/arial.ttf', 32)
		self.running = True

		self.character_spritesheet = Spritesheet('img/character.png')
		self.terrain_spritesheet = Spritesheet('img/terrain.png')
		self.enemy_spritesheet = Spritesheet('img/enemy.png')
		self.attack_spritesheet = Spritesheet('img/attack.png')
		self.intro_background = pygame.image.load('img/introbackground.png')
		self.go_background = pygame.image.load('img/gameover.png')

	def create_tilemap(self):
		for i, row in enumerate(TILEMAP):
			for j, column in enumerate(row):
				Ground(self, j, i)
				if column == 'B':
					Block(self, j, i)
				if column == 'E':
					Enemy(self, j, i)
				if column == 'P':
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



	def game_over(self):
		# gestiona el fin del juego
		text = self.font.render('Game Over', True, WHITE)
		text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
		restart_button = Button(10, WIN_HEIGHT - 60, 120, 50, WHITE, BLACK, 'Restart', 32)

		for sprite in self.all_sprites:
			sprite.kill()

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if restart_button.is_pressed(mouse_pos, mouse_pressed):
				self.new()
				self.main()
			self.screen.blit(self.go_background, (0, 0))
			self.screen.blit(text, text_rect)
			self.screen.blit(restart_button.image, restart_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()

	def intro_screen(self):
		# crea la ventana inicial del juego
		intro = True
		title = self.font.render('Awesome Game', True, BLACK)
		title_rect = title.get_rect(x=10, y=10)
		play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)

		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False
			self.screen.blit(self.intro_background, (0, 0))
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()

g = Game()
g.intro_screen()
g.new()

while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()