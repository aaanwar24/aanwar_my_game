# File created by Abdullah Anwar

# import libs
import pygame as pg
import os
# import settings 
from setting2 import *
from sprite2 import *
# from pg.sprite import Sprite

# set up assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

# create game class in order to pass properties to the sprites file
# This next big block of code is essentially what the entire game runs on, the different aspects as to
# how the game functions are all defined below
class Game:
    # This first block initializez pygame. The game begins to run and the display is set up. 
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("my game")
        self.clock = pg.time.Clock()
        self.running = True
        print(self.screen)
    # This next part defines the bounds of a new game, in which the score is equal to 0, all the sprites are added to the 
    # screen, both the player and the mobs, and the platforms are also added. It also gives the color and size of the mobs. 
    def new(self):

        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.player = Player(self)
        self.health = 500
        self.plat1 = Platform(WIDTH, 50, 0, HEIGHT-50, (150,150,150), "normal")
        self.all_sprites.add(self.plat1)

        self.platforms.add(self.plat1)
        
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        for i in range(0,10):
            m = Mob(30,30,(255,0,0))
            self.all_sprites.add(m)
            self.enemies.add(m)


        self.run()
    # The run function as shown here with self being the only parameter defines what happens in the game as the values are True
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    # This block defines the keys for jumping and quitting the game. By pressing the X, the game becomes false and shuts down the
    # window. By pressing the space key, the player jumps. 
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
    # This function is the draw_text function, and what it does is it allows the user to draw text on the screen taking a variety 
    # paramters into consideration such as the fint and the placement of the text on the screen. 
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    # This defines the properties for the platforms. As the sprite collides with the platforms, they vary as some are bouncey 
    # and others disappear on impact. This changes depending on whether the author of the code indicates that the player jumps 
    # upon collision or the platform is killed on collision. 
    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hitsplatform = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hitsplatform:
                if hitsplatform[0].variant == "disappearing":
                    hitsplatform[0].kill()
                elif hitsplatform[0].variant == "bouncey":
                    self.player.pos.y = hitsplatform[0].rect.top
                    self.player.vel.y = -PLAYER_JUMP
                else:
                    self.player.pos.y = hitsplatform[0].rect.top
                    self.player.vel.y = 0
        hitsenemy = pg.sprite.spritecollide(self.player, self.enemies, False)
        if hitsenemy:
                if hitsenemy[0]:
                    print("infected!!")
                    print(self.health)
                    self.health -= 5
                if self.health <= 0:
                    print("GAME OVER!!")
        
                    
                
            



    # This draws the background of the screen and utilizes the draw_text function to write "Abdullah's Game" on the screen. 
    def draw(self):
        self.screen.fill(BLUE)
        self.draw_text("DON'T TOUCH THE VIRUS", 24, WHITE, WIDTH/2, HEIGHT/2)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
 
      
    
    def get_mouse_now(self):
        x,y = pg.mouse.get_pos()
        return (x,y)

   

# instantiate the game class...
g = Game()

# kick off the game loop
while g.running:
    g.new()

pg.quit()