import game_entities, pymunk, world

CHAIN_LINK_LEN = 15
CHAIN_LINK_POLY = [(-CHAIN_LINK_LEN/2, -5.00), (-CHAIN_LINK_LEN/2,5.00), (CHAIN_LINK_LEN/2, 5.00), (CHAIN_LINK_LEN/2, -5.00)]

def make_chain(entity_manager, pos, num_links = 10, mass = 1, **kwargs):
    x,y = pos
    links = []
    for i in range(num_links):
        grabable = (i == 0 or i == num_links - 1)
        entity = world.BaseEntity((x +i*(CHAIN_LINK_LEN+3), y), CHAIN_LINK_POLY, mass, grabable=grabable, taggable = False, friction=0.2, texture_name="chain")
        links.append(entity)
        entity_manager.add_entity(entity)

        if i > 0:
            entity_manager.pin_join_entities(links[i], links[i-1], (-CHAIN_LINK_LEN/2,0), (CHAIN_LINK_LEN/2, 0))

def make_mast(entity_manager, pos, height):
    x,y = pos

    if height<=82: height = 83

    entity_manager.add_entity(MastTop((x,y))())
    entity_manager.add_entity(MastBox((x,y-41),height=height-82)())
    entity_manager.add_entity(MastBottom((x,y-(height-41)))())

def make_floor_box(entity_manager, pos, width):
    x,y = pos

    if width<=82: width = 83

    entity_manager.add_entity(FloorBoxLeft((x,y))())
    entity_manager.add_entity(FloorBox((x+40,y),width=width-80)())
    entity_manager.add_entity(FloorBoxRight((x+(width-40),y))())

def MovableBox(pos, width=50, height=50, mass=5, **kwargs):
    half_w, half_h = (width/2, height/2)
    verts = [(-half_w, -half_h),(-half_w,half_h),(half_w,half_h),(half_w, -half_h)]
    
    return (lambda: world.BaseEntity(pos, verts, mass, dynamic=True, texture_name="crate1", **kwargs))

def Banana(pos, **kwargs):
    return (lambda: game_entities.Banana(pos, **kwargs))

def Bananas(pos, **kwargs):
    return (lambda: game_entities.Bananas(pos, **kwargs))

def FloorBox(pos, width=100, height=40, **kwargs):
    verts = [(0, -height),(0,0),(width,0),(width, -height)]
    return (lambda: world.BaseEntity(pos, verts, pymunk.inf, dynamic=False, taggable=False, texture_name="floorBox", **kwargs))

def FloorBoxRight(pos, width=40, height=40, **kwargs):
    verts = [(0, -height),(0,0),(width,0),(width, -height)]
    return (lambda: world.BaseEntity(pos, verts, pymunk.inf, dynamic=False, texture_name="floorBoxRight", **kwargs))

def FloorBoxLeft(pos, width=40, height=40, **kwargs):
    verts = [(0, -height),(0,0),(width,0),(width, -height)]
    return (lambda: world.BaseEntity(pos, verts, pymunk.inf, dynamic=False, texture_name="floorBoxLeft", **kwargs))

def MastBox(pos, width=40, height=200, **kwargs):
    verts = [(0, -height),(0,0),(width,0),(width, -height)]
    return (lambda: world.BaseEntity(pos, verts, pymunk.inf, dynamic=False, texture_name="vertPole", **kwargs))

def MastBottom(pos, width=40, height=41, **kwargs):
    verts = [(0, -height),(0,0),(width,0),(width, -height)]
    return (lambda: world.BaseEntity(pos, verts, pymunk.inf, dynamic=False, texture_name="bottomPole", **kwargs))

def MastTop(pos, width=40, height=41, **kwargs):
    verts = [(0, -height),(0,0),(width,0),(width, -height)]
    return (lambda: world.BaseEntity(pos, verts, pymunk.inf, dynamic=False, texture_name="topPole", **kwargs))

def Hook(pos, **kwargs):
    verts = [(0, -10),(0,0),(15,0),(15, -10)]
    return (lambda: world.BaseEntity(pos, verts, pymunk.inf, dynamic=False, taggable=True, texture_name="chain", **kwargs))


##
# Factories

def ChainFactory(pos, num_links = 10, **kwargs):
    return lambda entity_manager, pos=pos, num_links = num_links, **kwargs: make_chain(entity_manager, pos, num_links = num_links, **kwargs)

def MastFactory(pos, height, **kwargs):
    return lambda entity_manager, pos=pos, height=height, **kwargs: make_mast(entity_manager, pos, height, **kwargs)

def FloorBoxFactory(pos, width, **kwargs):
    return lambda entity_manager, pos=pos, width=width, **kwargs: make_floor_box(entity_manager, pos, width, **kwargs)
