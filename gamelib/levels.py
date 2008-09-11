import world
from game_entities import *
from level_helpers import *

LEVEL_NAME = 0
PLAYER_START = 1
ELEMENTS = 2
FACTORIES = 3

Level1 = {
    LEVEL_NAME: "Monkey on a Boat",

    PLAYER_START: (25, 25),
    
    ELEMENTS: [
        FloorBox((0,0), width=250),
        FloorBox((50, 100), width=100),
        FloorBox((50, 100), width=100),
        FloorBox((-600, -100), width=1200),
        FloorBox((50, 100), height=100, width=20),

        FloorBox((-600, 0), width=200),
        FloorBox((-600, 550), width=20, height=550),
        FloorBox((-500, 450), width=20, height=350),
        FloorBox((-480, 450), width=200)
    ],

    FACTORIES: [],
}

Level3 = {
    LEVEL_NAME: "Alfreds Test Level",
    PLAYER_START: (25,25),

    ELEMENTS: [
        FloorBox((-100,0), width=500),
        FloorBox((0,100), width=300),
        MovableBox((100,200), width=40, height=40, mass = 10)
    ],

    FACTORIES: [
        ChainFactory((0,50), length=20), #length in links
    ]
}

Levels = [Level1]



