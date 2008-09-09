import data, pymunk, pygame, sys,os
from pygame.locals import *
from gamelib import main
import StateMachine


class Intro:
    def __init__(self):
        print "[States] Into initalizing"
        
    def run(self):
        print "[States] Into run"
        return
    
    def update(self):
        print "[States] Into update"
        return

class Play:        
    def __init__(self):
        pass
    
    def run(self):
        main.main()
         
class Exit:
    pass