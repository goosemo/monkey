import pymunk
from pymunk.vec2d import Vec2d

class BaseEntity(object):
    def __init__(self, world_pos, vertices, mass, friction=5, moment = None, taggable=True, grabable=False, texture_name=None, dynamic=True):
        self._world_entity_manager = None

        self._is_dynamic = True

        pymunk_verts = map(Vec2d, vertices)
        
        if not moment:
            moment = pymunk.moment_for_poly(mass, pymunk_verts, (0,0))

        self._body = pymunk.Body(mass, moment)
        self._body.position = world_pos
  
        self._shape = pymunk.Poly(self._body, pymunk_verts, (0,0) )
        self._shape.friction = friction

        self._is_taggable = taggable
        self._is_grabable = grabable
        self._texture_name = texture_name
        self._is_dynamic = dynamic

    def get_texture_name(self):
        return self._texture_name

    def is_textured(self):
        return self._texture_name is not None

    def is_taggable(self):
        return self._is_taggable

    def is_grabable(self):
        return self._is_grabable

    def is_world_bound(self):
        return self._world_entity_manager is not None

    def is_dynamic(self):
        return self._is_dynamic

    def on_bind_world(self, world_entity_manager):
        self._world_entity_manager = world_entity_manager

    def get_world_entity_manager(self):
        return self._world_entity_manager

    def pin_join(self, entity, self_pos, entity_pos):
        if self.is_world_bound():
            return self._world_entity_manager.pin_join_entities(self, entity, self_pos, entity_pos)

        return False

    def tag(self, grabable_ent, wc_taggable_pos):
        if not self.is_taggable() or not grabable_ent.is_grabable():
            return

        grabable_body = grabable_ent.get_body()

        #move the body to the taggable pos
        grabable_body.position = wc_taggable_pos

        #convert world pin coordinates to local body coords
        lc_grabable_pos = grabable_body.world_to_local(wc_taggable_pos)
        lc_taggable_pos = self.get_body().world_to_local(wc_taggable_pos)

        #turn off collision checking between the combined items
        cgrp = self.get_world_entity_manager().alloc_collision_group()
        self.get_shape().group = cgrp
        grabable_ent.get_shape().group = cgrp
        
        #pin it to the taggable
        grabable_ent.pin_join(self, lc_grabable_pos, lc_taggable_pos)


    def unjoin(self, joint_id):
        if self.is_world_bound():
            return self._world_entity_manager.unjoin(joint_id)

        return False

    def get_shape(self):
        return self._shape

    def get_body(self):
        return self._body

    def get_vertices(self):
        return self._shape.get_points()

    def get_position(self):
        pos = self.get_body().position
        return (pos[0], pos[1])

    def on_collision(self, other_entity, contacts, normal_coef, data):
        pass

    def tick(self, dt):
        pass

class EntityManager(object):
    PINJOINT = 0
    
    JINF_TYPE = 0
    JINF_JOINT = 1
    JINF_ENTA = 2
    JINF_ENTB = 3
    JINF_DATA = 4

    def __init__(self, space):
        self._space = space
        self._entities = {}
        self._group_count = 0
        self._joint_count = 0
        self._joints = {}

    def alloc_collision_group(self):
        self._group_count += 1
        return self._group_count

    def _alloc_joint_id(self):
        self._joint_count += 1
        return self._joint_count

    def _register_joint(self, joint_type, joint, ent_a, ent_b, data):
        joint_id = self._alloc_joint_id()
        self._joints[joint_id] = (joint_type, joint, ent_a, ent_b, data)
        return joint_id
    
    def unjoin(self, joint_id):
        if not joint_id in self._joints:
            return False

        joint_info = self._joints[joint_id]
        self._space.remove(joint_info[EntityManager.JINF_JOINT])
        
        return True

    def add_entity(self, entity, collision_group=0):
        shape = entity.get_shape()
        shape.group = collision_group

        entity.on_bind_world(self)
        self._entities[shape] = entity

        if entity.is_dynamic():
            self._space.add(entity.get_body(), shape)
        else:
            self._space.add_static(shape)

    def pin_join_entities(self, ent_a, ent_b, pos_a, pos_b):
        joint = pymunk.PinJoint(ent_a.get_body(), ent_b.get_body(), pos_a, pos_b)
        self._space.add(joint)
        return self._register_joint(EntityManager.PINJOINT, joint, ent_a, ent_b, (pos_a, pos_b))



    def on_collision(self, shapeA, shapeB, contacts, normal_coef, data):
        ent_a = self._entities[shapeA]
        ent_b = self._entities[shapeB]

        if ent_a and ent_b:
            ent_a.on_collision(ent_b, contacts, normal_coef, data)
            ent_b.on_collision(ent_a, contacts, normal_coef, data)
        
        return True

    def get_entities(self):
        return [ent for (shape, ent) in self._entities.iteritems()]

    def tick(self, dt):
        for entity in self.get_entities():
            entity.tick(dt)

