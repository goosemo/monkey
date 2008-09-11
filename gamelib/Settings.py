import data, pymunk, pygame, sys,os
from pygame.locals import *

    
name = "BalloonKillers" 
tagline = "Ohio State University Game Creation Club presents: Balloon Killer"
version = 1.0
        
SCREENSIZE = (800,600)
        
PIX_PER_M = 40 #pixels per meter
        
chain_link_len = 15
chain_link_poly = [(0,0), (0,5), (chain_link_len, 5), (chain_link_len, 0)]
