from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d
from awesomeengine import rectangle

import box2dcar

import math
import random

class InputCarComponent(Component):

    def __init__(self):
        self.required_attrs = (
            'max_steering_angle', 
            ('steering_angle', 0),
            'max_forward_speed', 
            'max_backward_speed', 
            ('desired_speed', 0), 
            ('desired_forward_speed', 0),
            ('desired_backward_speed', 0))
        self.event_handlers = (('input', self.handle_input),)

    def handle_input(self, entity, action, value):
        if action == 'gas':
            entity.desired_forward_speed = entity.max_forward_speed * value
        elif action == 'break':
            entity.desired_backward_speed = entity.max_backward_speed * value
        elif action == 'steer':
            entity.steering_angle = entity.max_steering_angle * -value

        entity.desired_speed = entity.desired_forward_speed + entity.desired_backward_speed


class Box2dCarComponent(Component):

    def __init__(self):
        self.required_attrs = (
            ('angle', 90),
            'x', 
            'y', 
            ('max_lateral_impulse', 3), 
            'max_steering_angle', 
            'engine_force', 
            ('steering_angle', 0), 
            'max_forward_speed', 
            'max_backward_speed', 
            ('desired_speed', 0))
        self.event_handlers = (('update', self.handle_update), ('contact', self.handle_contact))
    
    def add(self, entity):
        Component.add(self, entity)
        entity.box2d_car = box2dcar.TDCar(engine.get().box2d_world,
                                          angle=entity.angle,
                                          entity=entity,
                                          max_drive_force = entity.engine_force,
                                          max_lateral_impulse= entity.max_lateral_impulse,
                                          position=(entity.x, entity.y))
        entity.box2d_car.set_awake(False)
        
    def handle_update(self, entity, dt):
        entity.box2d_car.update(entity.steering_angle, entity.desired_speed, dt)

        entity.x, entity.y = entity.box2d_car.body.GetWorldPoint((0,0))
        entity.angle = math.degrees(entity.box2d_car.body.angle) + 90

        engine.get().entity_manager.update_position(entity)
        
    def handle_contact(self, entity, other, primary):
        crash_sounds = ('crash1', 'crash2')
    
        player = engine.get().entity_manager.get_by_name('player')
        other_is_car = hasattr(other, 'tags') and 'car' in other.tags
        
        if (primary or not other_is_car) and ((player.x - entity.x)**2 + (player.y - entity.y) ** 2) < 10000:
            try:
                if (hasattr(entity, 'name') and entity.name == 'player') or (hasattr(other, 'name') and other.name == 'player'):
                    channel = engine.get().resource_manager.get('sound', random.choice(crash_sounds)).play()
                    channel.volume = 32
                else:
                    channel = engine.get().resource_manager.get('sound', random.choice(crash_sounds)).play()
                    channel.volume = 16
            except:
                pass


class CarDrawComponent(Component):

    def __init__(self):
        self.required_attrs = ('width', 'height', ('colour', (255,255, 0,255)))
        self.event_handlers = (('draw', self.handle_draw),)

    def handle_draw(self, entity, camera):
        x,y = entity.box2d_car.body.GetWorldPoint((0, 0))
        angle = math.degrees(entity.box2d_car.body.angle) + 90

        rect = rectangle.Rect(x,y,entity.width, entity.height, angle)

        camera.draw_rect(entity.colour, rect)
        

class RandomImageChooserComponent(Component):

    def __init__(self):
        self.required_attrs = ('images',)
        self.event_handlers = tuple()
        
    def add(self, entity):
        Component.add(self, entity)
        entity.image = random.choice(entity.images)
        

