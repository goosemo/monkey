import pymunk, world 

class Player(world.BaseEntity):
    STOP = 0
    LEFT = -1
    RIGHT = 1

    MAX_JUMPS = 2 

    def __init__(self, power = 40000):
        world.BaseEntity.__init__(self, (400,400), [(-21,-48),(-21,48),(21,48),(21,-48)], 
            25, friction=0.4, moment=pymunk.inf, texture_name="monkey")

        self._power = power
        self._direction = Player.STOP
        self._hold_joint = None
        self._held_entity = None
        self._try_grab = False
        self._try_tag = False
        self._avail_jumps = Player.MAX_JUMPS
        self._can_begin_jump = False
        self.stop()

    def left(self):
    	self._direction = Player.LEFT

    def right(self):
        self._direction = Player.RIGHT

    def stop(self):
        self._direction = Player.STOP

    def jump(self):
        if self._avail_jumps == Player.MAX_JUMPS and not self._can_begin_jump:
            return

        if self._avail_jumps > 0:
            self._can_begin_jump = False
            self._avail_jumps -= 1
            jump_factor = 1/(Player.MAX_JUMPS - self._avail_jumps)
            self.get_body().apply_impulse((0,4000 + 4000 * jump_factor), (0,0))

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

        #see if we're standing on something we can jump off of
        min_entity_v, max_entity_v = entity.get_bounding_rect()
        min_player_v, max_player_v = self.get_bounding_rect()
        if abs(max_entity_v[1] - min_player_v[1]) < 0.2:
            self._avail_jumps = Player.MAX_JUMPS
            self._can_begin_jump = True

        #handle pick-up and tagging of entities
        if self._try_grab and entity.is_grabable():
            self.end_grabbing()
            self.hold(entity, contacts[0].position)

        elif self._try_tag and entity.is_taggable() and self.get_held_entity() != entity:
            self.end_tagging()
            self.tag(entity, contacts[0].position)

    def tick(self, dt):
        #disable the ability to jump each tick
        #jumps are re-enabled in on_collision if on top of a block
        self._can_begin_jump = False

        body = self.get_body()
        if abs(body.velocity[0]) < 250:
            body.apply_impulse((self._direction*self._power*dt, 0),(0,0))

