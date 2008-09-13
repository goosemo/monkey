import world
from game_entities import *
from level_helpers import *

LEVEL_NAME = 0
PLAYER_START = 1
ELEMENTS = 2
FACTORIES = 3

Level1 = {
    LEVEL_NAME: "Monkey on a Boat",

    PLAYER_START: (-150, 1000),
    
    ELEMENTS: [

        # This is where the goods to collect are placed
        
        #   left side
        Banana((-150,550)),
        Bananas((-150,250)),

        #   right side
        Banana((200,800)),
        Bananas((200,500)),

        MovableBox((100,200), width=40, height=40, mass = 10),

    ],

    FACTORIES: [

        # Floor areas

        #   Bottom most floor
        FloorBoxFactory((-310,0), width=700),

        #   left side
        FloorBoxFactory((-280,800), width=250),
        FloorBoxFactory((-280, 500), width=250),
        FloorBoxFactory((-280, 200), width=250),


        #   right side
        #          x    y
        FloorBoxFactory(( 80, 650), width=250),
        FloorBoxFactory(( 80, 350), width=250),

    
        # Uprights

        # Two main masts that hold level together
        MastFactory((-250,900), height=1200),
        MastFactory(( 250,900), height=1200),

        #   left side               
        MastFactory((-130,600), height=200),
        MastFactory((-130,300), height=200),

        #   right side
        MastFactory((140,750), height=200),
        MastFactory((140,450), height=200),
    
    ],
}

Level3 = {
    LEVEL_NAME: "Trickle Down",
    PLAYER_START: (30,1025),

    ELEMENTS: [

        # Items in order on map
        Banana((175,890)),

        Bananas((375,690)),

        #needs to be a goal box
        MovableBox((575,490), width=40, height=40, mass = 10),

        Bananas((775,290)),

    ],

    FACTORIES: [
        ChainFactory((0,50), length=20), #length in links

        # Floor areas
        #                  x    y
        FloorBoxFactory((-50, 850), width=450),
        FloorBoxFactory((250, 650), width=350),
        FloorBoxFactory((450, 450), width=350),
        FloorBoxFactory((650, 250), width=650),

        # Uprights

        # Two main masts that hold level together
        MastFactory(( 100, 1000), height=1200),
        MastFactory((1200, 1000), height=1200),
        
        # Masts inside main two
        MastFactory((300,900), height=300),
        MastFactory((500,700), height=300),
        MastFactory((700,500), height=300),

    ]
}

Level2 = {
    LEVEL_NAME: "Monkey with a Goal",

    PLAYER_START: (50, 30),
    
    ELEMENTS: [
        FloorBox((25,20), width=50),
        FloorBox((50,0), width=1,height=600),
        FloorBox((0,-800), width=500,height=10),
        FloorBox((600,-610), width=40,height=40),
        FloorBox((800,-800), width=200,height=10),
        FloorBox((1000,-760), width=200,height=50),
        FloorBox((1200,-720), width=200,height=90),
        FloorBox((500,-1000), width=300,height=40),
        MovableBox((600,-800), width=10, height=10, mass=1000)
    ],
    
    FACTORIES: [
        ChainFactory((0,50), length=30), #length in links
    ]

}

Levels = [Level1,Level2,Level3]

