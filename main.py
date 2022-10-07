import os

# pygame library added
import pygame as pg

# "This module provides access to some variables used or maintained by the interpreter and to functions that interact
# strongly with the interpreter" (https://docs.python.org/3/library/sys.html)
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    def __init__(self):  # Game class object constructor
        pg.init()  # Initializes pygame modules
        pg.mouse.set_visible(False)  # hides cursor
        self.screen = pg.display.set_mode(RES)  # create screen with resolution defined in settings.py
        self.clock = pg.time.Clock()    # instance of clock class for frame of rate
        self.delta_time = 1     # initial delta time used in player movement
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 49)
        self.new_game()

    def new_game(self):     # new game method
        self.map = Map(self) # instance of map created
        self.player = Player(self) # instance of player created
        self.object_renderer = ObjectRenderer(self)  # instance of Object Renderer
        self.raycasting = RayCasting(self) # instance of raycasting
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = Pathfinding(self)
        pg.mixer.music.play(-1)
        # FOLLOWING METHODS TO BE DONE BY OBJECT HANDLER OTHERWISE EVERY SPRITE MUST BE ADDED HERE TO BE INSTANTIATED.
        # self.static_sprite = SpriteObject(self)
        # self.animated_sprite = AnimatedSprite(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        # FOLLOWING 2 METHODS TO BE DONE BY OBJECT HANDLER
        # self.static_sprite.update()
        # self.animated_sprite.update()
        self.weapon.update()
        pg.display.flip()   # update screen. pygame.display.flip(). This will upagte the contents of the entire
        # display. (https://www.pygame.org/docs/ref/display.html#:~:text=flip()%20for%20software%20displays,display.)
        self.delta_time = self.clock.tick(FPS)    # called once per frame
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')  # show current number of FPS

    def draw(self):
        # FILLING SCREEN BLACK NO LONGER NECESSARY AFTER ASSIGNING SKY AND FLOOR BACKGROUND
        # self.screen.fill('black')   # 2D
        self.object_renderer.draw()     # 3D
        self.weapon.draw()      # 3D

        
        # self.map.draw()  # 2D
        # self.player.draw()    # 2D

    def check_events(self):     # Check for following events such at escape + key down and exit. This allows for
        # lexit of application
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):  # runs main loop. update() and draw() methods are called here.
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':  # creates an instance of game.
    game = Game()
    game.run()
