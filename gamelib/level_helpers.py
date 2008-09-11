import world
from game_entities import *

CHAIN_LINK_LEN = 15
CHAIN_LINK_POLY = [(-CHAIN_LINK_LEN/2, -2.5), (-CHAIN_LINK_LEN/2,2.5), (CHAIN_LINK_LEN/2, 2.5), (CHAIN_LINK_LEN/2, -2.5)]

def make_chain(entity_manager, pos, num_links = 10, mass = 1, **kwargs):
    x,y = pos
    links = []
    for i in range(num_links):
        entity = world.BaseEntity((x +i*(CHAIN_LINK_LEN+2), y), CHAIN_LINK_POLY, mass, grabable=True, taggable = False, friction=0.1)
        links.append(entity)
        entity_manager.add_entity(entity)

        if i > 0:
            entity_manager.pin_join_entities(links[i], links[i-1], (-CHAIN_LINK_LEN/2,0), (CHAIN_LINK_LEN/2, 0))

def MovableBox(pos, width=50, height=50, mass=5, **kwargs):
    half_w, half_h = (width/2, height/2)
    verts = [(-half_w, -half_h),(-half_w,half_h),(half_w,half_h),(half_w, -half_h)]
    
    return world.BaseEntity(pos, verts, mass, dynamic=True, **kwargs)

def FloorBox(pos, width=100, height=20, **kwargs):
    verts = [(0, -height),(0,0),(width,0),(width, -height)]
    return world.BaseEntity(pos, verts, pymunk.inf, dynamic=False, **kwargs)

def ChainFactory(pos, num_links = 10, **kwargs):
    return lambda entity_manager, pos=pos, num_links = num_links, **kwargs: make_chain(entity_manager, pos, num_links = num_links, **kwargs)

