import data, pymunk, pygame, sys,os
from pygame.locals import *
from States import Intro, Play, Exit

import Settings

class StateMachine:
    """
    
    """
    

    def __init__ (self):
        settings = Settings.Settings()
        
        print "Welcome to %s, currently in version %f" % (settings.name,settings.version)
        
        
        self.init_pygame(settings)
        self.init_pymunk(settings)
    
        self.states = {
            "intro": Intro,           
            "play": Play,
            "exit": Exit,
            }
        
        self.currentState = self.states["intro"]()
        
        
    def start(self):
        self.currentState.run()
        while True: 
            input(pygame.event.get())
            self.currentState.update()
        
        
    def init_pygame(self,settings):
        print "[StateMachine] initalizing pygame"
        pygame.init()
        screen = pygame.display.set_mode(settings.SCREENSIZE)
        pygame.display.set_caption(settings.name)
        font = pygame.font.Font(None, 16)
        background = pygame.Surface(screen.get_size())
        background = background.convert()
        background.fill((250, 250, 250))

        
    def init_pymunk(self,settings):
        print "[StateMachine] initalizing pymunk"
        pymunk.init_pymunk()
        space = pymunk.Space()
        space.gravity = (0.0, -9.8 * settings.PIX_PER_M)
        space.damping = 0.98
        space.resize_static_hash(dim=10, count=1000)
        space.resize_active_hash(dim=10, count=1000)
       
       
    def input(events): 
       for event in events: 
            if event.type == QUIT: 
                sys.exit(0) 
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.currentState = self.states["exit"]()

            elif event.type == KEYDOWN and event.key == K_SPACE:
                self.currentState = self.states["play"]()                
                
            elif event.type == MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play() #punch
                    chimp.punched()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                fist.unpunch()
            else: 
                print event
        

    
    
    

        
