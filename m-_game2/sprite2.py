# file created by Abdullah Anwar
import pygame as pg
from pygame.sprite import Sprite
from setting2 import *
from random import randint
import os

vec = pg.math.Vector2

# player class
# This next chunk of code defines how the player works. There are a variety of things that the player does.
# The block begins by defining the properties of the sprite, such as where it spawns and how fast it moves.
# Following that is the defintions of how the Player moves, which is with the A and D keys on the keyboard. 
# The -PLAYER JUMP keeps the sprite moving on the platform defined by the user rather than jumping whenever 
# the two are touching at all. FOllowing that, the computer indicates where the Player is and whether ot not 
# the player is still on the screen. If the player is off the screen, it prints that out. 
# Although I did not get the collide function to work, I left it in there for the future so that it can work 
# during my final project. 
class Player(Sprite):
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((50,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.cofric = 0.1
        self.canjump = False
    def input(self):
        keystate = pg.key.get_pressed()
        if keystate[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keystate[pg.K_d]:
            self.acc.x = PLAYER_ACC

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    
    def inbounds(self):
        if self.rect.x > WIDTH - 50:
            self.vel.x = -5
        if self.rect.x < 0:
            self.vel.x = 5
        if self.rect.y > HEIGHT:
            self.rect.y = -5 
        if self.rect.y < 0:
            self.rect.y = 5 
    def mob_collide(self):
            hits = pg.sprite.spritecollide(self, self.game.enemies, True)
            if hits:
                print("you collided with an enemy...")
                self.game.score += 1
                print(SCORE)
    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        self.acc.x = self.vel.x * PLAYER_FRICTION
        self.input()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
    

# This next class is the Mob class, or the small red red squares that travel across the screen. 
# Just as were defined for the Player class, the Mob class has the location and velocity defined, although the velocity
# is randomized. The inbounds keeps the Mobs on the screen rather than floating off.
class Mob(Sprite):
    def __init__(self,width,height, color):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(randint(1,5),randint(1,5))
        self.acc = vec(1,1)
        self.cofric = 0.01
    
    def inbounds(self):
        if self.rect.x > WIDTH:
            self.vel.x *= -1
        if self.rect.x < 0:
            self.vel.x *= -1
        if self.rect.y < 0:
            self.vel.y *= -1
        if self.rect.y > HEIGHT:
            self.vel.y *= -1
    def update(self):
        self.inbounds()
        self.pos += self.vel
        self.rect.center = self.pos

# This creates a Platform class so that the user can use the same block of code to create different platforms. 
# All the user has to do is define the given parameters for the platform and it will be made to do so as show in the setting2 file. 

class Platform(Sprite):
    def __init__(self, x, y, width, height, color, variant):
        Sprite.__init__(self)
        self.width = width
        self.height = height
        self.image = pg.Surface((self.width,self.height))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.variant = variant