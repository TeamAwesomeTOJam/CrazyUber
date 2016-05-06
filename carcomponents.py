from awesomeengine.component import verify_attrs
from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d

import math

class CarPhysicsComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['width', ('steering_angle', 0), 'angle', ('breaking_force', 0), ('engine_force',0), ('vx',0), ('vy',0), 'drag_coefficient', 'rolling_coefficient'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):

        facing = Vec2d(1,0)
        facing.angle = entity.angle

        velocity = Vec2d(entity.vx ,entity.vy)

        f_engine = entity.engine_force * facing

        if velocity.dot(facing) > 0:
            f_breaking = - entity.breaking_force * facing
        else:
            f_breaking = Vec2d(0,0)

        f_drag = - entity.drag_coefficient * velocity * velocity.length

        f_rolling = - entity.rolling_coefficient * velocity

        f = f_engine + f_drag + f_rolling + f_breaking

        entity.fx = f.x
        entity.fy = f.y


        if entity.steering_angle:
            corner_radius = entity.width / math.sin(math.radians(entity.steering_angle))
            entity.angle += dt * math.degrees(velocity.length / corner_radius)

class InputEngineComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['max_steering_angle', ('steering_angle', 0), 'base_breaking_force', ('breaking_force', 0),'base_engine_force', ('engine_force', 0)])
        entity.register_handler('input', self.handle_input)

    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)

    def handle_input(self, entity, action, value):
        if action == 'gas' and value == 1:
            entity.engine_force = entity.base_engine_force
        elif action == 'gas' and value == 0:
            entity.engine_force = 0
        elif action == 'break' and value == 1:
            entity.breaking_force = entity.base_breaking_force
        elif action == 'break' and value == 0:
            entity.breaking_force = 0
        elif action == 'left' and value == 1:
            entity.steering_angle = entity.max_steering_angle
        elif action == 'right' and value == 1:
            entity.steering_angle = -entity.max_steering_angle
        elif (action == 'left' or action == 'right') and value == 0:
            entity.steering_angle = 0

