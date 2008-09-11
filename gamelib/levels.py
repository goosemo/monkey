import world
from game_entities import *

LEVEL_NAME = 0
PLAYER_START = 1
ELEMENTS = 2

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
        FloorBox((-600, 150), width=20, height=100),
    ]
}

Levels = [Level1]
