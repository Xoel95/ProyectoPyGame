import pygame
import math
import random
from config import *


class Spritesheet:

    def __init__(self, file):
        # funcion main de las hojas de sprites
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite_black(self, x, y, width, height):
        # función que coje el sprite especificado dentro de la hoja de sprites con fondo negro 
        # y lo prepara para el juego
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
    
    def get_sprite_white(self, x, y, width, height):
        # función que coje el sprite especificado dentro de la hoja de sprites con fondo blanco 
        # y lo prepara para el juego
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(WHITE)
        return sprite


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        # función main del jugador
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1
        # self.kills = 0

        # image viene de la clase Sprite
        self.image = self.game.character_spritesheet.get_sprite_black(129, 15, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.character_spritesheet.get_sprite_black(129, 15, self.width, self.height),
                           self.game.character_spritesheet.get_sprite_black(96, 15, self.width, self.height),
                           self.game.character_spritesheet.get_sprite_black(160, 15, self.width, self.height)]

        self.up_animations = [self.game.character_spritesheet.get_sprite_black(129, 159, self.width, self.height),
                         self.game.character_spritesheet.get_sprite_black(96, 159, self.width, self.height),
                         self.game.character_spritesheet.get_sprite_black(160, 159, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite_black(129, 62, self.width, self.height),
                           self.game.character_spritesheet.get_sprite_black(96, 62, self.width, self.height),
                           self.game.character_spritesheet.get_sprite_black(160, 62, self.width, self.height)]

        self.right_animations = [self.game.character_spritesheet.get_sprite_black(129, 110, self.width, self.height),
                            self.game.character_spritesheet.get_sprite_black(96, 110, self.width, self.height),
                            self.game.character_spritesheet.get_sprite_black(160, 110, self.width, self.height)]

    def update(self):
        # función que actualiza el personaje
        self.movement()
        self.animate()
        self.collide_enemies()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        # función que produce el movimiento del personaje
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            # for sprite in self.game.all_sprites:
            #     sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_enemies(self):
        # función que produce las colisiones del personaje con los enemigos
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):
        # función que produce las colisiones del personaje con los muros
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                    # for sprite in self.game.all_sprites:
                    #     sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    # for sprite in self.game.all_sprites:
                    #     sprite.rect.x -= PLAYER_SPEED
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    # for sprite in self.game.all_sprites:
                    #     sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    # for sprite in self.game.all_sprites:
                    #     sprite.rect.y -= PLAYER_SPEED

    def animate(self):
        # función que produce la animación del personaje
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite_black(129, 15, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite_black(129, 159, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite_black(129, 62, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite_black(129, 110, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        # función main de los enemigos
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite_white(32, 0, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.enemy_spritesheet.get_sprite_white(32, 0, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite_white(82, 0, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite_white(136, 0, self.width, self.height)]

        self.up_animations = [self.game.enemy_spritesheet.get_sprite_white(32, 44, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite_white(82, 44, self.width, self.height),
                         self.game.enemy_spritesheet.get_sprite_white(136, 44, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite_white(32, 134, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite_white(82, 134, self.width, self.height),
                           self.game.enemy_spritesheet.get_sprite_white(136, 134, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite_white(32, 89, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite_white(82, 89, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite_white(136, 89, self.width, self.height)]

    def update(self):
        # función que actualiza los enemigos
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        # función que produce el movimiento de los enemigos
        if self.facing == 'left':
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'right'

        if self.facing == 'right':
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left'

        if self.facing == 'up':
            self.y_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = 'down'

        if self.facing == 'down':
            self.y_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'up'

    def animate(self):
        # función que produce las animaciones de los enemigos
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite_white(32, 0, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite_white(32, 44, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite_white(32, 134, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite_white(32, 89, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1

    def collide_blocks(self, direction):
        # función que produce las colisiones de los enemigos con los muros
        if direction == 'x':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == 'y':
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom


class Block(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        # función main de los muros
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite_black(705, 160, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        # función main del suelo
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite_black(805, 510, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:

    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        # función main de los botones
        self.font = pygame.font.Font('fonts/arial.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.bg)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        # función que comprueba si el botón está presionado
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
        return False


class Attack(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        # función main de los ataques
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.animation_loop = 0
        # kills = pygame.sprite.spritecollide(self, self.game.enemies, True)

        self.image = self.game.attack_spritesheet.get_sprite_black(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.attack_spritesheet.get_sprite_black(0, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(32, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(64, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(96, 32, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(128, 32, self.width, self.height)]

        self.up_animations = [self.game.attack_spritesheet.get_sprite_black(0, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(32, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(64, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(96, 0, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(128, 0, self.width, self.height)]

        self.left_animations = [self.game.attack_spritesheet.get_sprite_black(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite_black(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite_black(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite_black(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite_black(128, 96, self.width, self.height)]

        self.right_animations = [self.game.attack_spritesheet.get_sprite_black(0, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(32, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(64, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(96, 64, self.width, self.height),
                            self.game.attack_spritesheet.get_sprite_black(128, 64, self.width, self.height)]

    def update(self):
        # función que actualiza los ataques
        self.animate()
        self.collide()

    def collide(self):
        # función que produce las colisiones del ataque del personaje con los enemigos
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)
        if hits:
            corte = pygame.mixer.Sound("sfx/espada-corta-enemigo.wav")
            corte.set_volume(0.7)
            corte.play(1)

    def animate(self):
        # función que produce las animaciones del ataque del personaje
        direction = self.game.player.facing

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.kill()
