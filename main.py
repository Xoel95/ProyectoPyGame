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
		self.puntuation = 0
		self.winner_count = 0

		self.character_spritesheet = Spritesheet('img/characters.png')
		self.terrain_spritesheet = Spritesheet('img/terrain.png')
		self.enemy_spritesheet = Spritesheet('img/enemies.png')
		self.attack_spritesheet = Spritesheet('img/attack.png')
		self.intro_background = pygame.image.load('img/introbackground.png')
		self.go_background = pygame.image.load('img/gameover.png')

	def create_tilemap(self, tilemap):
		for i, row in enumerate(tilemap):
			for j, column in enumerate(row):
				Ground(self, j, i)
				if column == 'B':
					Block(self, j, i)
				if column == 'E':
					Enemy(self, j, i)
				if column == 'P':
					self.player = Player(self, j, i)

	def new(self):
		# función para iniciar una nueva partida
		self.playing = True

		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()
		pygame.mixer.music.load("music/legend-of-zelda-the-nes-music-overworld-theme.mp3")
		pygame.mixer.music.set_volume(0.7)
		pygame.mixer.music.play(1)

		self.create_tilemap(TILEMAP)

	def events(self):
		# controla los eventos de la partida
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					if self.player.facing == 'down':
						Attack(self, self.player.rect.x, self.player.rect.y + TILESIZE)
					if self.player.facing == 'up':
						Attack(self, self.player.rect.x, self.player.rect.y - TILESIZE)
					if self.player.facing == 'left':
						Attack(self, self.player.rect.x - TILESIZE, self.player.rect.y)
					if self.player.facing == 'right':
						Attack(self, self.player.rect.x + TILESIZE, self.player.rect.y)

	def update(self):
		# actualiza los datos de la ventana de la partida cuando se ejecuta
		self.all_sprites.update()
		# self.player.kills = self.player.kills
		if not self.enemies:
			for sprite in self.all_sprites:
				sprite.kill()
			self.winner_count += 1
			if self.winner_count == 1:
				self.create_tilemap(TILEMAP2)
			self.puntuation += 50
			print(self.puntuation)
			if self.winner_count == 2:
				self.win()


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
		text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 90))
		puntuation = self.font.render("Puntuación: " + str(self.puntuation), True, WHITE)
		puntuation_rect = puntuation.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 30))
		restart_button = Button(WIN_WIDTH / 2 - 60, WIN_HEIGHT - 120, 120, 50, WHITE, BLACK, 'Restart', 32)
		pygame.mixer.music.load("music/classic-mario-death-tune.mp3")
		pygame.mixer.music.set_volume(0.7)
		pygame.mixer.music.play(1)
		self.winner_count = 0
		self.puntuation = 0

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
			self.screen.blit(puntuation, puntuation_rect)
			self.screen.blit(restart_button.image, restart_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()

	def win(self):
		# gestiona la victoria del juego
		text = self.font.render('Winner', True, WHITE)
		text_rect = text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 90))
		puntuation = self.font.render("Puntuación: " + str(self.puntuation), True, WHITE)
		puntuation_rect = puntuation.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 30))
		restart_button = Button(WIN_WIDTH / 2 - 60, WIN_HEIGHT - 120, 120, 50, WHITE, BLACK, 'Restart', 32)
		pygame.mixer.music.load("music/two-steps-from-hell-victory.mp3")
		pygame.mixer.music.set_volume(0.7)
		pygame.mixer.music.play(1)
		self.winner_count = 0
		self.puntuation = 0

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
			self.screen.blit(puntuation, puntuation_rect)
			self.screen.blit(restart_button.image, restart_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()

	def intro_screen(self):
		# crea la ventana inicial del juego
		intro = True
		title = self.font.render('RPG Brawler', True, BLACK)
		title_rect = title.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 30))
		play_button = Button(WIN_WIDTH / 2 - 60, WIN_HEIGHT / 2 + 30, 120, 50, WHITE, BLACK, 'Start', 32)
		pygame.mixer.music.load("music/dragon-quest-overture-orchestral.mp3")
		pygame.mixer.music.set_volume(0.7)
		pygame.mixer.music.play(1)

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