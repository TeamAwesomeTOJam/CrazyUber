import random

from awesomeengine.component import verify_attrs
from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d
from awesomeengine import rectangle

import math

class PasangerPickupComponent(Component):

    def add(self, entity):
        verify_attrs(entity, [('pickup_target', None), ('dropoff_target', None)])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):

        if entity.pickup_target is not None:
            targets = engine.get_engine().entity_manager.get_in_area('pickup_zone', rectangle.from_entity(entity))
            for t in targets:
                if t == entity.pickup_target:
                    e = engine.get_engine()
                    e.remove_entity(entity.pickup_target)
                    entity.pickup_target = None
                    road = list(e.entity_manager.get_by_tag('road'))
                    random.shuffle(road)
                    r = road[0]
                    new_target = engine.get_engine().add_entity('dropoff-zone', x=r.x, y=r.y)
                    entity.dropoff_target = new_target
                    break

        elif entity.dropoff_target is not None:
            targets = engine.get_engine().entity_manager.get_in_area('dropoff_zone', rectangle.from_entity(entity))
            for t in targets:
                if t == entity.dropoff_target:
                    e = engine.get_engine()
                    e.remove_entity(entity.dropoff_target)
                    entity.dropoff_target = None
                    road = list(e.entity_manager.get_by_tag('road'))
                    random.shuffle(road)
                    r = road[0]
                    new_target = engine.get_engine().add_entity('pickup-zone', x=r.x, y=r.y)
                    entity.pickup_target = new_target
                    e.entity_manager.get_by_name('score').score += 1
                    break

class DrawPickupArrowComponent(Component):

    def add(self, entity):
        verify_attrs(entity, [('pickup_target', None), ('dropoff_target', None), "x", "y"])

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        if entity.pickup_target is not None:
            target = entity.pickup_target
            c = (0,0,255,255)
        elif entity.dropoff_target is not None:
            target = entity.dropoff_target
            c = (255,0,255,255)
        else:
            return

        pos = Vec2d(entity.x, entity.y)
        t = Vec2d(target.x, target.y)

        pos_to_target = (t - pos).normalized()

        start = pos + 10*pos_to_target
        end = pos + 20*pos_to_target

        camera.draw_line(c, start, end)


class ScoreComponent(Component):

    def add(self, entity):
        verify_attrs(entity, [('score',0)])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.text = 'Trips Made: {}'.format(entity.score)

class TimerComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['time'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.time -= dt
        if entity.time < 0:
            entity.time = 0
        entity.text = '{}:{:05.2f}'.format(int(entity.time)/60, entity.time % 60)

class CarSleepComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height', 'awake_width', 'awake_height'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        to_sleep = engine.get_engine().entity_manager.get_in_area('car', rectangle.from_entity(entity))
        to_wake = engine.get_engine().entity_manager.get_in_area('car', rectangle.Rect(entity.x, entity.y, entity.awake_width, entity.awake_height))

        for e in to_sleep - to_wake:
            e.box2d_car.set_awake(False)

        for e in to_wake:
            e.box2d_car.set_awake(True)