import world
from game_entities import *
from level_helpers import *

LEVEL_NAME = 0
PLAYER_START = 1
MAXTIME = 2
ELEMENTS = 3
FACTORIES = 4
GOALBOX_LOCATION = 5
GOAL_VALUE = 6 

Level0 = {
    LEVEL_NAME: "Welcome to the Jungle",
    PLAYER_START: (820,180),
    MAXTIME: 800,

    GOALBOX_LOCATION: (740, 80),
    GOAL_VALUE: 2,


    ELEMENTS: [

        # Items in order on map
        Banana((200,150)),
        Banana((240,150)),
        MovableBox((300,180), width=80, height=80, mass=5),
        MovableBox((380,180), width=80, height=80, mass=5),
        MovableBox((340,260), width=80, height=80, mass=5),
  
    ],

    FACTORIES: [
        ChainFactory((0,180), length=10), #length in links

        # Floor areas
        #                  x    y
        FloorBoxFactory((-50, 100), width=600),
        FloorBoxFactory((795, 100), width=160),
        FloorBoxFactory((450, 0), width=400),

        # Two main masts that hold level together
        MastFactory((-40, 1140), height=1200),
        MastFactory((900, 1140), height=1200),
        MastFactory((460,80), height=130),
        MastFactory((800,80), height=130)

    ]
}


Level1 = {
    LEVEL_NAME: "Monkey on a Boat",
    PLAYER_START: (-150, 1000),
    MAXTIME: 250,

    GOALBOX_LOCATION: (-70, 100),
    GOAL_VALUE: 12,

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
        ChainFactory((-150, 1050), length=20), #length in links

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
        MastFactory((-90,600), height=180),
        MastFactory((-90,300), height=180),

        #   right side
        MastFactory((100,750), height=180),
        MastFactory((100,450), height=180),
    
    ],
}

Level2 = {
    LEVEL_NAME: "Trickle Down",
    PLAYER_START: (30,1025),
    MAXTIME: 150,

    GOALBOX_LOCATION: (575, 500),
    GOAL_VALUE: 12,


    ELEMENTS: [

        # Items in order on map
        Banana((175,890)),
        Bananas((375,690)),
        Bananas((875,290)),

    ],

    FACTORIES: [
        ChainFactory((20,1050), length=20), #length in links

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


Level3 = {
    LEVEL_NAME: "Semi Golden Ratios",
    PLAYER_START: (100,1025),
    MAXTIME: 200,

    GOALBOX_LOCATION: (100, 100),
    GOAL_VALUE: 12,

    ELEMENTS: [

        # Items on map
        Banana((175,890)),
        Bananas((375,690)),
        Bananas((575,490)),
        Bananas((775,290)),

    ],

    FACTORIES: [
        ChainFactory((150,950), length=20), #length in links

        # Floor areas
        #                  x    y
        FloorBoxFactory((  0, 750), width=675),
        FloorBoxFactory((300, 250), width=375),
        FloorBoxFactory((  0,  70), width=1200),

        # Uprights

        MastFactory(( 400,  400), height= 200),
        MastFactory(( 600,  770), height= 590),
        MastFactory((  50,  900), height= 900),
        MastFactory((1170, 1600), height=1600),

    ]
}

Level4 = {
    LEVEL_NAME: "King of the Forest",
    PLAYER_START: (50, -200),
    MAXTIME: 1000,

    GOALBOX_LOCATION: (300, -1700),
    GOAL_VALUE: 12,

    ELEMENTS: [
        MovableBox((80,-760), width=80, height=80, mass=5),
        MovableBox((80,-680), width=80, height=80, mass=5),
        MovableBox((160,-760), width=80, height=80, mass=5),
        Hook((1195,-795)),

        Banana((760,-960 - 40)),
        Banana((960,-960 - 40)),
        Bananas((980,-1160 - 40)),
        Bananas((780,-1600 - 40)),
        Banana((850,-1450 - 40))

    ],
    
    FACTORIES: [
        ChainFactory((700,-700), num_links=6), 
        ChainFactory((660,-1480 - 40), num_links=6), 
        ChainFactory((800,-900), num_links=15), 
        ChainFactory((1000,-700), num_links=8), 
        FloorBoxFactory((600,-1000 - 40), width = 490),
        FloorBoxFactory((0,-300), width=100), # was y=-300
        FloorBoxFactory((0,-800), width=1200,height=40),
        FloorBoxFactory((1300,-950 - 40), width=200,height=40),
        FloorBoxFactory((700,-1350 - 40), width=200,height=40),
        FloorBoxFactory((640,-1500 - 40), width=450,height=40),
        FloorBoxFactory((940,-1180 - 40), width=120,height=40),
        FloorBoxFactory((700,-1650 - 40), width=200,height=40),
        FloorBoxFactory((200,-1800 - 40), width=440,height=40),


	MastFactory((0,1000), height = 1800),
	MastFactory((210,-1700 - 40), height = 500),
	MastFactory((960,-500), height = 340),
	MastFactory((500,-750), height = 900),
	MastFactory((1400,1000), height = 2000),
	MastFactory((800,-950 - 40), height = 120),
	MastFactory((800,-1190 - 40), height = 800),
        MastFactory((1050,-950 - 40), height = 650)
    ]

}

Levels = [Level0,Level1,Level2,Level3,Level4]

