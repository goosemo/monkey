#! /usr/bin/env python

import pygame, sys, data, game_entities
from pygame.locals import *

import game, util
from ezmenu import *
from data import *


class Menu(object):
 
    def __init__(self, screen):
        self.screen = screen
        self.menu = EzMenu(["New Game", lambda: game.main(self.screen)], ["Quit Game", sys.exit])
        self.menu.set_highlight_color((255, 255, 255))
        self.menu.set_normal_color((10, 10, 10))
        self.menu.center_at(550, 470)
        self.menu.set_font(pygame.font.Font(filepath("pointy.ttf"), 36))

        


        #start music playing forever
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.load(data.filepath('felix8.xm'))
        pygame.mixer.music.play(-1)

        self.main_loop()
  
    def print_directions(self, screen, font):
        
        description = "A 2d side viewed game. In it you play as a monkey that has to use it's chain to grab the bananas and drag them to the goal crate before your time runs out."
        wrapped_description = util.wrapline(description, font, 320)

        directions = [ 
            ' ',
            'Jump - SPACE/UP',
            'Left - LEFT',
            'Right - RIGHT',
            ' ',
            'Attach Chain - Z',
            'Drop Chain - X',
            'Tag Banana - C',
            'Un-Tag Banana - V',
            'Restart Level - R',
        ]
        x_pos = 30
        y_pos = 130
        for line in (wrapped_description):            
            text_surf = font.render("%s" % line, 1, (0,0,0))
            screen.blit(text_surf, (x_pos, y_pos))
            y_pos += 30

        x_pos = 500
        y_pos = 90
        for line in (directions):             
            text_surf = font.render("%s" % line, 1, (0,0,0))
            screen.blit(text_surf, (x_pos, y_pos))
            y_pos += 30

       
    def walking_monkey(self, screen, i=0):
        
        player = game_entities.Player()
        player.tick(1)
        player.get_body().position = (50,50)

        if i < 50:
            player.left()
        elif i < 100:
            player.right()
        elif i < 110:
            player.stop()
            i = 0
        i += i


    def main_loop(self):

        directions_font = pygame.font.Font(data.filepath("oneway.ttf"), 24)
        title_font = pygame.font.Font(filepath("pointy.ttf"), 56)
        title = "Monkey in a Tangle"

        while True:
            events = pygame.event.get()
            self.menu.update(events)
            for e in events:
                if e.type == QUIT:
                    pygame.quit()
                    return
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    pygame.quit()
                    return
        
            self.screen.fill((0x28,0x08b,0xd7))
            bg = load_image("MonkeyWalk001.png")
            self.screen.blit(bg, (80, 500))
            self.menu.draw(self.screen)
              
            text_surf = title_font.render("%s" % title, 1, (255,255,255))
            self.screen.blit(text_surf, (30, 30))
            self.walking_monkey(self.screen)
            self.print_directions(self.screen, directions_font)
            pygame.display.flip()
        
