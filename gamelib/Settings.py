import data, pymunk, pygame, sys,os
from pygame.locals import *

class Settings:
    
    def __init__(self):
        self.name = "BalloonKillers" 
        self.tagline = "Ohio State University Game Creation Club presents: Balloon Killer"
        self.version = 1.0
        
        self.SCREENSIZE = (800,600)
        
        self.PIX_PER_M = 40 #pixels per meter
        
        self.chain_link_len = 15
        self.chain_link_poly = [(0,0), (0,5), (self.chain_link_len, 5), (self.chain_link_len, 0)]