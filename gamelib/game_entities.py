import pymunk, world 

CHAIN_LINK_LEN = 15
CHAIN_LINK_POLY = [(-CHAIN_LINK_LEN/2, -2.5), (-CHAIN_LINK_LEN/2,2.5), (CHAIN_LINK_LEN/2, 2.5), (CHAIN_LINK_LEN/2, -2.5)]

class ChainFactory(world.EntityFactory):
    def __init__(self, pos, length):
        self._pos = pos
        self._length = length

    def create(self, entity_manager):
        x,y = self._pos
        links = []
        for i in range(self._length):
            mass = 1
            entity = world.BaseEntity((x +i*(CHAIN_LINK_LEN+2), y), CHAIN_LINK_POLY, mass, grabable=True, taggable = False, friction=0.1)
            links.append(entity)
            entity_manager.add_entity(entity)

            if i > 0:
                entity_manager.pin_join_entities(links[i], links[i-1], (-CHAIN_LINK_LEN/2,0), (CHAIN_LINK_LEN/2, 0))

class MovableBox(world.BaseEntity):
    def __init__(self, pos, width=100, height = 100, mass=5, friction=3, taggable = True, grabable = True):
        half_w, half_h = (width/2, height/2)
        verts = [(-half_w, -half_h),(-half_w,half_h),(half_w,half_h),(half_w, -half_h)]
        world.BaseEntity.__init__(self, pos, verts, mass, dynamic = True, taggable = taggable, grabable=grabable)

class FloorBox(world.BaseEntity):
    def __init__(self, pos, width=100, height = 20, taggable=False, grabable=False):
        verts = [(0, -height),(0,0),(width,0),(width, -height)]
        world.BaseEntity.__init__(self, pos, verts, pymunk.inf, friction=3, moment=pymunk.inf, dynamic = False, taggable=False, grabable=False)

class Player(world.BaseEntity):
    STOP = 0
    LEFT = -1
    RIGHT = 1

    def __init__(self, power = 50000):
        world.BaseEntity.__init__(self, (400,400), [(-15,-30),(-15,30),(15,30),(15,-30)], 25, friction=0.5, moment=pymunk.inf)
        self._power = power
        self._direction = Player.STOP
        self._hold_joint = None
        self._held_entity = None
        self._try_grab = False
        self._try_tag = False

        self.stop()

    def left(self):
    	self._direction = Player.LEFT

    def right(self):
        self._direction = Player.RIGHT

    def stop(self):
        self._direction = Player.STOP

    def jump(self):
        self.get_body().apply_impulse((0,8000), (0,0))

    def begin_grabbing(self):
        self._try_grab = True

    def end_grabbing(self):
        self._try_grab = False

    def begin_tagging(self):
        self._try_tag = True

    def end_tagging(self):
        self._try_tag = False

    def tag(self, target_entity, wc_contact_pos):
        held_entity = self.get_held_entity()
        if held_entity:
            self.drop()
            target_entity.tag(held_entity, wc_contact_pos)

    def drop(self):
        if self._hold_joint:
            self.unjoin(self._hold_joint)
            self._hold_joint = None
            self._held_entity = None

    def hold(self, entity, wc_contact_pos):
        if not entity.is_grabable():
            return

        self.drop()

        lc_for_entity = entity.get_body().world_to_local(wc_contact_pos)
        lc_for_player = self.get_body().world_to_local(wc_contact_pos)
        joint_id = self.pin_join(entity, lc_for_player, lc_for_entity)
        
        self._hold_joint = joint_id
        self._held_entity = entity

    def get_held_entity(self):
        return self._held_entity

    def on_collision(self, entity, contacts, normal_coef, data):
        if not entity.is_dynamic():
            return

        if self._try_grab and entity.is_grabable():
            self.end_grabbing()
            self.hold(entity, contacts[0].position)
        elif self._try_tag and entity.is_taggable() and self.get_held_entity() != entity:
            self.end_tagging()
            self.tag(entity, contacts[0].position)

    def tick(self, dt):
        body = self.get_body()
        if abs(body.velocity[0]) < 150:
            body.apply_impulse((self._direction*self._power*dt, 0),(0,0))

