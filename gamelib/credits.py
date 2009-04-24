import sys
import pygame

from pygame.locals import *

import game
import util
import texture

from ezmenu import *
from data import *


def roll_credits(screen):
    
    title = "\
            Monkey in a tangle:\n\
            \n\
              Devlopers:\n\
                Alfred Rossi\n\
                Morgan Goose\n\
            \n\
              Artist:\n\
                Jane Drozid\n\
            \n\
              Level Designer:\n\
                James Sharpnack\n\
            \n\
              Special thanks to ACCAD\n\
              for letting us use their\n\
              facilaties, and students.\n\
            "
    credit_pos = 400
    font_size = 46
    title_font = pygame.font.Font(filepath("pointy.ttf"), font_size)
    title_size = -(len(title.split('\n')) * (font_size+4))

    text_surf = []
    for line in title.split('\n'):
        text_surf.append(
                title_font.render(
                    line, 1, (255,255,255))
                )

    credits_rolling = True

    while credits_rolling:
        screen.fill((0x28,0x08b,0xd7))

        for event in pygame.event.get():
            if event.type == QUIT:
                credits_rolling = False
                
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    credits_rolling = False
            
        offset = 0  
        for item in text_surf:
            screen.blit(item, (0, credit_pos + offset))
            offset += 50

        
        if credit_pos < title_size:
            return

        credit_pos -= 2
        pygame.display.flip()
        

    return

def main(screen):

    roll_credits(screen)
    pygame.quit()
    sys.exit
