import pymunk, world 
from data import play_sound


class Deliverable(world.BaseEntity):
    _worth = 1

class Banana(Deliverable):
    def __init__(self, pos, mass=2, **kwargs):
        half_w, half_h = (40/2, 40/2)
        verts = [(-half_w, -half_h),(-half_w,half_h),(half_w,half_h),(half_w, -half_h)]
        world.BaseEntity.__init__(self, pos, verts, mass=mass, dynamic=True, texture_name="banana", **kwargs) 

class Bananas(Deliverable):
    def __init__(self, pos, mass=1.5, **kwargs):
        half_w, half_h = (46/2, 46/2)
        verts = [(-half_w, -half_h),(-half_w,half_h),(half_w,half_h),(half_w, -half_h)]
        self._worth = 5
        world.BaseEntity.__init__(self, pos, verts, mass=mass, dynamic=True, texture_name="bananas", **kwargs) 

class GoalBox(world.BaseEntity):
    def __init__(self, pos, **kwargs):
        half_w, half_h = (80/2, 80/2)
        verts = [(-half_w, -half_h),(-half_w,half_h),(half_w,half_h),(half_w, -half_h)]
        world.BaseEntity.__init__(self, pos, verts, 5, dynamic=True, texture_name="bananacrate", **kwargs) 
        self._value = 0

    def get_value(self):
        return self._value

    def on_collision(self, entity, contacts, normal_coef, data):
        if isinstance(entity, Deliverable):
            self._value += entity._worth
            play_sound('goal.wav')
            self.get_world_entity_manager().remove_entity(entity)

ChainLinkLen = 15
class ChainLink(world.BaseEntity):
    LEN = ChainLinkLen 
    POLY = [(-ChainLinkLen/2, -5.00), (-ChainLinkLen/2,5.00), (ChainLinkLen/2, 5.00), (ChainLinkLen/2, -5.00)]
    MAX_SEP = 25*ChainLinkLen

    TICKS_TO_UNTANGLE = 200 

    def __init__(self, pos, previous, friction=0.2, mass=0.25, **kwargs):
        world.BaseEntity.__init__(self, pos, ChainLink.POLY, mass=mass, grabable=True, taggable = False, friction = friction, texture_name="chain", layers=1)

        self._previous = previous
        self._next = None
        self._joint_id = None
        self._untangle_ticks = ChainLink.TICKS_TO_UNTANGLE + 1

    def on_bind_world(self, world_entity_manager):
        world.BaseEntity.on_bind_world(self, world_entity_manager)
        if self._previous:
            self._joint_id = self.get_world_entity_manager().pin_join_entities(self, self._previous, (-ChainLink.LEN/2,0), (ChainLink.LEN/2, 0))

    def is_single(self):
        return self._next is None and self._previous is None

    def chain_untangle(self, grpid):
        self.get_shape().group = grpid
        self._untangle_ticks = 0
        if self._next:
            self._next.chain_untangle(grpid)

    def tick(self, dt):
        world.BaseEntity.tick(self, dt)

        if self._untangle_ticks == ChainLink.TICKS_TO_UNTANGLE:
            self.get_shape().group = 0

        if self._untangle_ticks <= ChainLink.TICKS_TO_UNTANGLE:
            self._untangle_ticks += 1

        if self._previous:
            sep = self._previous.get_body().position - self.get_body().position
            if(sep.length > ChainLink.MAX_SEP):
                self._previous._next = None
                self.get_world_entity_manager().unjoin(self._joint_id)
                self._previous = None

    def register_next(self, chainlink):
        self._next = chainlink

    def get_free_end(self):
        head = self.get_head()
        tail = self.get_tail()

        if not head.taggable_is_attached():
            return head
        elif not tail.taggable_is_attached():
            return tail
        else:
            return None

    def get_head(self):
        if not self._previous:
            return self
        else: 
            return self._previous.get_head()

    def get_tail(self):
        if not self._next:
            return self
        else:
            return self._next.get_tail()
        
class Player(world.BaseEntity):
    STOP = 0
    LEFT = -1
    RIGHT = 1

    MAX_JUMPS = 2

    CollisionGroup = 1231
    
    #STOPPED_TEXTURE = "monkey"
    STOPPED_RIGHT_TEXTURE = "MONKEY_R0"
    STOPPED_LEFT_TEXTURE = "MONKEY_L0"
    LEFT_WALK_CYCLE = ["MONKEY_L0", "MONKEY_L1", "MONKEY_L2", "MONKEY_L3"]
    RIGHT_WALK_CYCLE = ["MONKEY_R0", "MONKEY_R1", "MONKEY_R2", "MONKEY_R3"]
    FRAME_COUNT = 4

    CYCLE_PERIOD = 0.10

    def __init__(self, power = 40000):
        world.BaseEntity.__init__(self, (400,400), [(-25,-50),(-25,50),(25,50),(25,-50)], 
            15, friction=1, moment=pymunk.inf, texture_name="monkey", layers=2)

        self._power = power
        self._direction = Player.STOP
        self._hold_joint = None
        self._held_entity = None
        self._try_grab = False
        self._try_tag = False
        self._try_untag = False

        self.last_dir = 'left'

        self._avail_jumps = Player.MAX_JUMPS
        self._can_begin_jump = False
        
        min_v, max_v = self.get_bounding_rect()
        self.height = max_v[1] - min_v[1]
        self.width = max_v[0] - min_v[0]

        self.half_height = self.height/2
        self.half_width = self.width/2

        self._cycle_position = 0 
        self._cycle_time = 0.0

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
            self.get_body().apply_impulse((0,3000 + 2000 * jump_factor), (0,0))
            play_sound('jump.wav')


    def begin_untagging(self):
        self._try_untag = True

    def end_untagging(self):
        self._try_untag = False

    def begin_grabbing(self):
        self._try_grab = True

    def is_grabbing(self):
        return self._try_grab

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

#        lc_for_entity = entity.get_body().world_to_local(wc_contact_pos)
#        lc_for_player = self.get_body().world_to_local(wc_contact_pos)
        entity.get_body().position = self.get_body().position
        joint_id = self.pin_join(entity, (0,0), (0,0))
        
        self._hold_joint = joint_id
        self._held_entity = entity
        play_sound('chain_up.wav')

    def get_held_entity(self):
        return self._held_entity

    def on_collision(self, entity, contacts, normal_coef, data):
        #handle pick-up and tagging of entities
        if self._try_grab and entity.is_grabable():
            self.end_grabbing()
            self.hold(entity, contacts[0].position)

        elif self._try_tag and entity.is_taggable() and self.get_held_entity() != entity:
            self.end_tagging()
            self.tag(entity, contacts[0].position)

        elif self._try_untag and entity.is_taggable() and self.get_held_entity() != entity:
            self.end_untagging()
            entity.release_tags()

#        self._can_begin_jump = True                 #REMOVE
#        self._avail_jumps = Player.MAX_JUMPS        #REMOVE
#        return                                      #REMOVE

        contact_pos = contacts[0].position

        #collision checking is done in two stages to avoid a
        #potentially costly call to get_bounding_rect
       
        bpos = self._body.position
        if abs(contact_pos[1] - (bpos[1] - self.half_height)) < 0.1:
            min_v, max_v = entity.get_bounding_rect()
            tweak = self.half_width *0.99
            if min_v[0] < bpos[0] + tweak and bpos[0] < max_v[0] + tweak:
                self._avail_jumps = Player.MAX_JUMPS
                self._can_begin_jump = True


    def tick(self, dt):
        #disable the ability to jump each tick
        #jumps are re-enabled in on_collision if on top of a block
        self._can_begin_jump = False

        self._cycle_time += dt
        if self._cycle_time > Player.CYCLE_PERIOD:
            cycle_shift = int(self._cycle_time / Player.CYCLE_PERIOD)
            self._cycle_time -= cycle_shift * Player.CYCLE_PERIOD
            self._cycle_position = (self._cycle_position + cycle_shift) % Player.FRAME_COUNT

            if self._direction == Player.LEFT:
                self.last_dir = 'left'
                self.set_texture(Player.LEFT_WALK_CYCLE[self._cycle_position])
            elif self._direction == Player.RIGHT:
                self.last_dir = 'right'
                self.set_texture(Player.RIGHT_WALK_CYCLE[self._cycle_position])
            else:
                if self.last_dir == 'left':
                    self.set_texture(Player.STOPPED_LEFT_TEXTURE)
                elif self.last_dir == 'right':
                    self.set_texture(Player.STOPPED_RIGHT_TEXTURE)
 
        body = self.get_body()
        if abs(body.velocity[0]) < 250:
            body.apply_impulse((self._direction*self._power*dt, 0),(0,0))

