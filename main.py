import sys
import connection
from sprites import *


class Game:

	def __init__(self):
		# función main del juego
		self.attacks = None
		self.enemies = None
		self.blocks = None
		self.all_sprites = None
		self.playing = None
		self.score = 0
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font('fonts/arial.ttf', 32)
		self.running = True

		self.winner_count = 0

		self.character_spritesheet = Spritesheet('img/characters.png')
		self.terrain_spritesheet = Spritesheet('img/terrain.png')
		self.enemy_spritesheet = Spritesheet('img/enemy.png')
		self.attack_spritesheet = Spritesheet('img/attack.png')
		self.intro_background = pygame.image.load('img/intro.jpg')
		self.go_background = pygame.image.load('img/game_over.jpg')
		self.victory_background = pygame.image.load('img/victory.jpg')
		self.icon = pygame.image.load('img/icon.png')

		pygame.display.set_caption("No-Hit No Death")
		pygame.display.set_icon(self.icon)

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
		self.score = 0
		self.winner_count = 0

		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()
		pygame.mixer.music.load("music/the-legend-of-zelda-overworld-theme.mp3")
		pygame.mixer.music.set_volume(0.4)
		pygame.mixer.music.play(20)

		self.create_tilemap(TILEMAP)

	def events(self):
		# controla los eventos de la partida
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				connection.Connection.saveScore(self.score);
				self.playing = False
				self.running = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					corte = pygame.mixer.Sound("sfx/espada-corta-aire.wav")
					corte.set_volume(0.3)
					corte.play()
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
		if not self.enemies:
			self.winner_count += 1
			for sprite in self.all_sprites:
				sprite.kill()

			if self.winner_count == 1:
				self.create_tilemap(TILEMAP2)
				self.score += 50
				print(self.score)
			elif self.winner_count == 2:
				self.create_tilemap(TILEMAP3)
				self.score += 50
				print(self.score)
			elif self.winner_count == 3:
				self.create_tilemap(TILEMAP4)
				self.score += 50
				print(self.score)
			elif self.winner_count == 4:
				self.create_tilemap(TILEMAP5)
				self.score += 50
				print(self.score)
			elif self.winner_count == 5:
				self.create_tilemap(TILEMAP6)
				self.score += 50
				print(self.score)
			elif self.winner_count == 6:
				self.score += 50
				print(self.score)
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

		connection.Connection.saveScore(self.score)
		pygame.mixer.music.load("music/classic-mario-death-tune.mp3")
		pygame.mixer.music.set_volume(0.7)
		pygame.mixer.music.play(1)
		for sprite in self.all_sprites:
			sprite.kill()

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break  # sale del bucle for

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()
			score = self.font.render("Score: " + str(self.score), True, WHITE, BLACK)
			score_rect = score.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 120))
			restart_button = Button(WIN_WIDTH / 2 - 180, WIN_HEIGHT - 90, 120, 50, WHITE, BLACK, 'Restart', 32)
			exit_button = Button(WIN_WIDTH / 2 + 60, WIN_HEIGHT - 90, 120, 50, WHITE, BLACK, 'Exit', 32)

			self.screen.blit(self.go_background, (0, 0))
			self.screen.blit(score, score_rect)
			self.screen.blit(restart_button.image, restart_button.rect)
			self.screen.blit(exit_button.image, exit_button.rect)
			self.clock.tick(FPS)

			if restart_button.is_pressed(mouse_pos, mouse_pressed):
				self.score = 0
				self.winner_count = 0
				self.new()
				break

			if exit_button.is_pressed(mouse_pos, mouse_pressed):
				pygame.quit()
				sys.exit()

			pygame.display.update()

	def win(self):

		# gestiona la victoria del juego

		connection.Connection.saveScore(self.score)
		pygame.mixer.music.load("music/two-steps-from-hell-victory.mp3")
		pygame.mixer.music.set_volume(1)
		pygame.mixer.music.play(1)
		for sprite in self.all_sprites:
			sprite.kill()

		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					break  # sale del bucle for

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()
			score = self.font.render("Score: " + str(self.score), True, WHITE, BLACK)
			score_rect = score.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 150))
			restart_button = Button(WIN_WIDTH / 2 - 180, WIN_HEIGHT - 90, 120, 50, WHITE, BLACK, 'Restart', 32)
			exit_button = Button(WIN_WIDTH / 2 + 60, WIN_HEIGHT - 90, 120, 50, WHITE, BLACK, 'Exit', 32)

			self.screen.blit(self.victory_background, (0, 0))
			self.screen.blit(score, score_rect)
			self.screen.blit(restart_button.image, restart_button.rect)
			self.screen.blit(exit_button.image, exit_button.rect)
			self.clock.tick(FPS)

			if restart_button.is_pressed(mouse_pos, mouse_pressed):
				self.score = 0
				self.winner_count = 0
				self.new()
				break

			if exit_button.is_pressed(mouse_pos, mouse_pressed):
				pygame.quit()
				sys.exit()

			pygame.display.update()

	def intro_screen(self):
		# crea la ventana inicial del juego
		intro = True
		title = self.font.render('No-Hit No Death', True, WHITE, BLACK)
		title_rect = title.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 150))
		play_button = Button(WIN_WIDTH / 2 - 60, WIN_HEIGHT / 2 - 90, 120, 50, WHITE, BLACK, 'Start', 32)
		best_player_button = Button(WIN_WIDTH / 2 - 100, WIN_HEIGHT / 2 - 30, 200, 50,
									WHITE, BLACK, 'Best Player', 32)
		controls_button = Button(WIN_WIDTH / 2 - 100, WIN_HEIGHT / 2 + 30, 200, 50, WHITE, BLACK, 'Controls', 32)
		exit_button = Button(WIN_WIDTH / 2 - 100, WIN_HEIGHT / 2 + 90, 200, 50, WHITE, BLACK, 'Exit', 32)
		pygame.mixer.music.load("music/dragon-quest-overture-orchestral.mp3")
		pygame.mixer.music.set_volume(1)
		pygame.mixer.music.play(20)

		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False

			if best_player_button.is_pressed(mouse_pos, mouse_pressed):
				max_score_show = True
				max_score = connection.Connection.maxScore()
				print(max_score)
				while max_score_show:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pygame.quit()
							sys.exit()
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_RETURN:
								max_score_show = False
							if event.key == pygame.K_BACKSPACE:
								max_score_show = False
					self.screen.fill(BLACK)
					max_score_text = self.font.render('Max Score: ' + max_score, True, WHITE, BLACK)
					max_score_text_rect = max_score_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
					back_text = self.font.render('Press Return Key (Enter) to Exit Menu',
												 True, WHITE, BLACK)
					back_text_rect = back_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT - 90))
					self.screen.blit(max_score_text, max_score_text_rect)
					self.screen.blit(back_text, back_text_rect)
					self.clock.tick(FPS)
					pygame.display.update()

			if controls_button.is_pressed(mouse_pos, mouse_pressed):
				controls_show = True
				while controls_show:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pygame.quit()
							sys.exit()
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_RETURN:
								controls_show = False
							if event.key == pygame.K_BACKSPACE:
								controls_show = False

					self.screen.fill(BLACK)
					controls_text = self.font.render('Controls: ', True, WHITE, BLACK)
					controls_text_rect = controls_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 120))
					movements_text = self.font.render('Arrow Keys: Movement', True, WHITE, BLACK)
					movements_text_rect = movements_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 - 30))
					attack_text = self.font.render('Space Bar: Attack', True, WHITE, BLACK)
					attack_text_rect = attack_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2 + 30))
					back_text = self.font.render('Press Return Key (Enter) to Exit Menu',
												 True, WHITE, BLACK)
					back_text_rect = back_text.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT - 90))
					self.screen.blit(controls_text, controls_text_rect)
					self.screen.blit(movements_text, movements_text_rect)
					self.screen.blit(attack_text, attack_text_rect)
					self.screen.blit(back_text, back_text_rect)
					self.clock.tick(FPS)
					pygame.display.update()

			if exit_button.is_pressed(mouse_pos, mouse_pressed):
				pygame.quit()
				sys.exit()

			self.screen.blit(self.intro_background, (0, 0))
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			self.screen.blit(best_player_button.image, best_player_button.rect)
			self.screen.blit(controls_button.image, controls_button.rect)
			self.screen.blit(exit_button.image, exit_button.rect)
			self.clock.tick(FPS)
			pygame.display.update()

connection.Connection.create_db('scores.sqlite')
connection.Connection.db_connect('scores.sqlite')
g = Game()
g.intro_screen()
g.new()

while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()
