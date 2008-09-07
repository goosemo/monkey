"""
Remake of the pyramid demo from the box2d testbed.
"""

import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d


class PyramidDemo:
    def flipyv(self, v):
        v = Vec2d(v)
        v.y = -v.y+self.h
        return v
        
    def __init__(self):
        self.running = True
        self.drawing = True
        self.w, self.h = 600,600
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        ### Init pymunk and create space
        pymunk.init_pymunk()
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        
        ### ground
        body = pymunk.Body(pymunk.inf, pymunk.inf)
        shape = pymunk.Segment(body, (50, 100), (550,100), .0)
        shape.friction = 1.0
        self.space.add_static(shape)
        
        ### pyramid
        x=Vec2d(-100, 7.5) + (300,100)
        y=Vec2d(0,0) 
        deltaX=Vec2d(0.5625, 2.0)*10
        deltaY=Vec2d(1.125, 0.0)*10

        for i in range(25):
            y = Vec2d(x)
            for j in range(i, 25):
                size= 5
                points = [(-size, -size), (-size, size), (size,size), (size, -size)]
                mass = 10.0
                moment = pymunk.moment_for_poly(mass, points, (0,0))
                body = pymunk.Body(mass, moment)
                body.position = y
                shape = pymunk.Poly(body, points, (0,0))
                shape.friction = 1
                self.space.add(body,shape)
                
                y += deltaY

            x += deltaX
            
        self.space.resize_active_hash(dim=10, count=3250)
    
    def run(self):
        while self.running:
            self.loop() 
            
            
    def loop(self):  
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_d:
                self.drawing = not self.drawing
        
        steps = 3
        dt = 1.0/120.0/steps            
        for x in range(steps):
            self.space.step(dt)
        if self.drawing:
            self.draw()
        
        ### Tick clock and update fps in title
        self.clock.tick(30)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))
        
    def draw(self):
        ### Clear the screen
        self.screen.fill(THECOLORS["white"])
        
        for shape in self.space.static_shapes:
            body = shape.body
            pv1 = self.flipyv(body.position + shape.a.cpvrotate(body.rotation_vector))
            pv2 = self.flipyv(body.position + shape.b.cpvrotate(body.rotation_vector))
            pygame.draw.lines(self.screen, THECOLORS["lightgray"], False, [pv1,pv2])           
    
        for shape in self.space.shapes:
            body = shape.body
            ps = shape.get_points()
            ps.append(ps[0])
            ps = map(self.flipyv, ps)
            color = THECOLORS["green"]
            #pygame.draw.lines(self.screen, color, False, ps, 1)
            pygame.draw.polygon(self.screen, THECOLORS["lightgray"], ps)
            pygame.draw.polygon(self.screen, THECOLORS["darkgrey"], ps,1)

        ### All done, lets flip the display
        pygame.display.flip()        

def main():
    demo = PyramidDemo()
    demo.run()

if __name__ == '__main__':
    doprof = 0
    if not doprof: 
        main()
    else:
        import cProfile, pstats
        
        prof = cProfile.run("main()", "profile.prof")
        stats = pstats.Stats("profile.prof")
        stats.strip_dirs()
        stats.sort_stats('cumulative', 'time', 'calls')
        stats.print_stats(30)