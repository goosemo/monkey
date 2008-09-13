import pymunk
from pymunk.vec2d import Vec2d

class BaseEntity(object):
    def __init__(self, world_pos, vertices, mass, friction=0.8, moment = None, taggable=True, grabable=False, texture_name=None, dynamic=True, collision_group=0, layers=2**32-1):
        self._world_entity_manager = None

        self._is_dynamic = True

        self._verts = vertices
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
        self._time_passed = 0.0
        self._shape.layers = layers
        self._taggable_attached = None

        self._shape.group = collision_group

        if not self._is_dynamic:
            self._bounding_rect_cache = self.get_bounding_rect(force=True)

        self._tags = {}
        self._attached = False

    def set_texture(self, name):
        self._texture_name = name

    def get_texture_name(self):
        return self._texture_name

    def get_bounding_rect(self, force=False):
        if not force and not self._is_dynamic:
            return self._bounding_rect_cache

        verts = self.get_vertices()
       
        x_s = [x for x,y in verts]
        y_s = [y for x,y in verts]

        min_x = min(x_s)
        max_x = max(x_s)
        min_y = min(y_s)
        max_y = max(y_s)
        
        return ((min_x, min_y), (max_x, max_y))

    def get_texture_origin(self):
        min_v, max_v = self.get_bounding_rect()
        return (min_v[0], max_v[1])

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

    def on_unbind_world(self):
        self.release_tags()
        self.taggable_release()

    def on_tag(self, entity, joint_id):
        self._tags[entity] = joint_id

    def release_tags(self):
        entities = self._tags.keys()
        for entity in entities:
            self.untag(entity)

    def on_taggable_attach(self, tagable):
        self.taggable_release()
        self._taggable_attached = tagable

    def taggable_is_attached(self):
        return self._taggable_attached is not None
        
    def taggable_release(self):
        if self.taggable_is_attached():
            self._taggable_attached.untag(self)

    def untag(self, grabable_ent):
        if grabable_ent in self._tags:
            joint_id = self._tags[grabable_ent]
            self.get_world_entity_manager().unjoin(joint_id)
            grabable_ent._taggable_attached = None
            del self._tags[grabable_ent]

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
        joint_id = grabable_ent.pin_join(self, lc_grabable_pos, lc_taggable_pos)

        grabable_ent.on_taggable_attach(self)
        self.on_tag(grabable_ent, joint_id)

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
        self._time_passed += dt

    def get_time_passed(self):
        return self._time_passed

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
        self._collision = 0

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

    def add_entity(self, entity):
        shape = entity.get_shape()

        self._entities[shape] = entity

        if entity.is_dynamic():
            self._space.add(entity.get_body(), shape)
        else:
            self._space.add_static(shape)

        entity.on_bind_world(self)

    def remove_entity(self, entity):
        shape = entity.get_shape()
        if shape in self._entities:
            del self._entities[shape]
            entity.on_unbind_world()
            self._space.remove(entity.get_body())

    def pin_join_entities(self, ent_a, ent_b, pos_a, pos_b):
        joint = pymunk.PinJoint(ent_a.get_body(), ent_b.get_body(), pos_a, pos_b)
        self._space.add(joint)
        return self._register_joint(EntityManager.PINJOINT, joint, ent_a, ent_b, (pos_a, pos_b))

    def on_collision(self, shapeA, shapeB, contacts, normal_coef, data):
        if not shapeA in self._entities or not shapeB in self._entities:
            return False

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

    def get_time_passed(self):
        time_passed = 0.0
        for entity in self.get_entities():
            time_passed += entity.get_time_passed()

        return time_passed

