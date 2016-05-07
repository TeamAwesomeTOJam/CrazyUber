from awesomeengine.component import verify_attrs
from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d

import math

class CarPhysicsComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['mass', ('velocity', 0),
                              'width', ('steering_angle', 0),
                              'angle', ('breaking_force', 0), ('engine_force',0), ('vx',0), ('vy',0), 'drag_coefficient', 'rolling_coefficient'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):

        # facing = Vec2d(1,0)
        # facing.angle = entity.angle
        #
        # velocity = Vec2d(entity.vx ,entity.vy)
        #
        # f_engine = entity.engine_force * facing
        #
        # if velocity.dot(facing) > 0:
        #     f_breaking = - entity.breaking_force * facing
        # else:
        #     f_breaking = Vec2d(0,0)
        #
        # f_drag = - entity.drag_coefficient * velocity * velocity.length
        #
        # f_rolling = - entity.rolling_coefficient * velocity
        #
        # f = f_engine + f_drag + f_rolling + f_breaking
        #
        # entity.fx = f.x
        # entity.fy = f.y

        f = entity.engine_force

        if entity.velocity > 0:
            f -= entity.breaking_force

        f -= entity.drag_coefficient * entity.velocity * entity.velocity
        f -= entity.rolling_coefficient * entity.velocity

        new_velocity = entity.velocity + dt * f / entity.mass
        if new_velocity < 0:
            new_velocity = 0

        entity.vx = new_velocity * math.cos(math.radians(entity.angle))
        entity.vy = new_velocity * math.sin(math.radians(entity.angle))
        entity.velocity = new_velocity

        if entity.steering_angle:
            corner_radius = entity.width / math.sin(math.radians(entity.steering_angle))
            entity.angle += dt * math.degrees(entity.velocity / corner_radius)

class InputEngineComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['max_steering_angle', ('steering_angle', 0), 'base_breaking_force', ('breaking_force', 0),'base_engine_force', ('engine_force', 0)])
        entity.register_handler('input', self.handle_input)

    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)

    def handle_input(self, entity, action, value):
        if action == 'gas':
            entity.engine_force = entity.base_engine_force * value
        elif action == 'break':
            entity.breaking_force = entity.base_breaking_force * value
        elif action == 'steer':
            entity.steering_angle = entity.max_steering_angle * -value

