from awesomeengine.component import verify_attrs
from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d
from awesomeengine import rectangle

import box2dcar

import math
import random

class InputCarComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['max_steering_angle', ('steering_angle', 0),
                              'max_forward_speed', 'max_backward_speed', ('desired_speed', 0)])
        entity.register_handler('input', self.handle_input)

    def remove(self, entity):
        entity.unregister_handler('input', self.handle_input)

    def handle_input(self, entity, action, value):
        if action == 'gas':
            entity.desired_speed = entity.max_forward_speed * value
        elif action == 'break':
            entity.desired_speed = entity.max_backward_speed * value
        elif action == 'steer':
            entity.steering_angle = entity.max_steering_angle * -value


class Box2dCarComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', ('max_lateral_impulse', 3), 'max_steering_angle', 'engine_force', ('steering_angle', 0), 'max_forward_speed', 'max_backward_speed', ('desired_speed', 0)] )
        entity.box2d_car = box2dcar.TDCar(engine.get_engine().box2d_world,
                                          entity=entity,
                                          max_drive_force = entity.engine_force,
                                          max_lateral_impulse= entity.max_lateral_impulse,
                                          position=(entity.x, entity.y))
        entity.box2d_car.set_awake(False)

        entity.register_handler('update', self.handle_update)
        entity.register_handler('contact', self.handle_contact)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.box2d_car.update(entity.steering_angle, entity.desired_speed, dt)

        entity.x, entity.y = entity.box2d_car.body.GetWorldPoint((0,0))
        entity.angle = math.degrees(entity.box2d_car.body.angle) + 90

        engine.get_engine().entity_manager.update_position(entity)
        
    def handle_contact(self, entity, other, primary):
        crash_sounds = ('crash1', 'crash2')
    
        player = engine.get_engine().entity_manager.get_by_name('player')
        if (player.x - entity.x)**2 + (player.y - entity.y) ** 2 < 10000:
            try:
                engine.get_engine().resource_manager.get('sound', random.choice(crash_sounds)).play()
            except:
                pass       

class CarDrawComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['width', 'height', ('colour', (255,255, 0,255))])

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        x,y = entity.box2d_car.body.GetWorldPoint((0, 0))
        angle = math.degrees(entity.box2d_car.body.angle) + 90

        rect = rectangle.Rect(x,y,entity.width, entity.height, angle)

        camera.draw_rect(entity.colour, rect)

class RandomImageChooserComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['images'])
        entity.image = random.choice(entity.images)
        
    def remove(self, entity):
        pass
        

