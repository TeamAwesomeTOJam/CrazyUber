import random
import collections

from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d
from awesomeengine import rectangle


class AiManagerCompoenent(Component):

    def __init__(self):
        self.required_attrs = (('ai_mode', 'wait'), ('ai_mode_timer', 0), ('velocity_queue', collections.deque(maxlen=30)))
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):
        #if ai_mode_timer > 0
        #keep doing what you are doing no interuptions

        #if ai_mode_timer = -1
        #keep doing what you are doing, allow interuptions

        #if ai_mode_timer == 0 return to default mode


        # maintain velocity queue
        entity.velocity_queue.append(entity.box2d_car.body.linearVelocity.length)
        # print entity.ai_mode, entity.ai_mode_timer

        if entity.ai_mode_timer > 0:
            entity.ai_mode_timer -= dt
            if entity.ai_mode_timer < 0:
                if entity.ai_mode == 'backup':
                    entity.ai_mode = 'follow'
                    entity.ai_mode_timer = 2
                elif entity.ai_mode == 'follow':
                    entity.ai_mode_timer = -1
            else:
                return

        if entity.ai_mode_timer == -1:
            if len(entity.velocity_queue) == 30:
                average_velocity = sum(entity.velocity_queue)/len(entity.velocity_queue)
                # print average_velocity
                if average_velocity < 3:
                    entity.ai_mode = 'backup'
                    entity.ai_mode_timer = 1
                    return
        elif entity.ai_mode_timer == 0:
            entity.ai_mode = 'follow'
            entity.ai_mode_timer = -1


class CivilianAiManagerCompoenent(Component):

    def __init__(self):
        self.required_attrs = (('ai_mode', 'wait'), ('ai_mode_timer', 0), ('velocity_queue', collections.deque(maxlen=30)))
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):
        #if ai_mode_timer > 0
        #keep doing what you are doing no interuptions

        #if ai_mode_timer = -1
        #keep doing what you are doing, allow interuptions

        #if ai_mode_timer == 0 return to default mode


        # maintain velocity queue
        entity.velocity_queue.append(entity.box2d_car.body.linearVelocity.length)
        # print entity.ai_mode, entity.ai_mode_timer

        if entity.ai_mode_timer > 0:
            entity.ai_mode_timer -= dt
            if entity.ai_mode_timer < 0:
                if entity.ai_mode == 'backup':
                    entity.ai_mode = 'roam'
                    entity.ai_mode_timer = 2
                elif entity.ai_mode == 'roam':
                    entity.ai_mode_timer = -1
            else:
                return

        if entity.ai_mode_timer == -1:
            if len(entity.velocity_queue) == 30:
                average_velocity = sum(entity.velocity_queue)/len(entity.velocity_queue)
                # print average_velocity
                if average_velocity < 3:
                    entity.ai_mode = 'backup'
                    entity.ai_mode_timer = 1
                    return
        elif entity.ai_mode_timer == 0:
            entity.ai_mode = 'roam'
            entity.ai_mode_timer = -1


class GoToPointComponent(Component):

    def __init__(self):
        self.required_attrs = (('target', None), 'max_forward_speed', ('slow_on_approach', False))
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):

        if entity.target is not None:
            pos = Vec2d(entity.box2d_car.body.GetWorldPoint((0, 0)))
            facing = Vec2d(entity.box2d_car.body.GetWorldVector((0, 1)))
            target = Vec2d(entity.target)

            pos_to_target = target - pos

            angle = facing.get_angle_between(pos_to_target)

            entity.steering_angle = angle

            if entity.slow_on_approach:
                distance = pos_to_target.length
                if distance < 40:
                    entity.desired_speed = entity.max_forward_speed * (distance/80.0)
                else:
                    entity.desired_speed = entity.max_forward_speed
            else:
                entity.desired_speed = entity.max_forward_speed


class FollowCarCompoent(Component):
    
    def __init__(self):
        self.required_attrs = (('ai_mode', 'wait'), ('follow', None))
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):
        if entity.ai_mode == 'follow' and entity.follow is not None:
            entity.target = (entity.follow.x, entity.follow.y)
        else:
            entity.target = None


class BackUpComponent(Component):

    def __init__(self):
        self.required_attrs = (('ai_mode', 'wait'), 'max_backward_speed')
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):
        if entity.ai_mode == 'backup':
            entity.desired_speed = entity.max_backward_speed
            entity.steering_angle = 0


class RoamComponent(Component):
    
    def __init__(self):
        self.required_attrs = (('ai_mode', 'wait'), ('next_corner', None), ('last_corner', None))
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):
        if entity.ai_mode == 'roam' and entity.next_corner is not None:

            e = engine.get_engine()

            corners = e.entity_manager.get_in_area('corner', rectangle.from_entity(entity))

            if entity.next_corner in corners:
                # print entity.next_corner.next_corners

                if entity.last_corner in entity.next_corner.next_corners and len(entity.next_corner.next_corners) > 1:
                    choices = entity.next_corner.next_corners[:]
                    choices.remove(entity.last_corner)
                    # print 'a'
                else:
                    choices = entity.next_corner.next_corners
                    # print 'b'
                # print choices, entity.last_corner, entity.next_corner, entity.next_corner.next_corners
                c = random.choice(choices)
                if c == entity.last_corner:
                    print 'u-turn at', entity.next_corner.x, entity.next_corner.y, 'to', c.x, c.y
                entity.last_corner = entity.next_corner
                entity.next_corner = random.choice(choices)

            entity.target = (entity.next_corner.x, entity.next_corner.y)
        else:
            entity.target = None


class DrawTargetComponent(Component):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'target')
        self.event_handlers = (('draw', self.handle_draw),)

    def handle_draw(self, entity, camera):
        if entity.target is not None:
            camera.draw_line((255, 255, 255, 255), (entity.x, entity.y), entity.target)
            
