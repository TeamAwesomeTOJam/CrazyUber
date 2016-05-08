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
        e = engine.get_engine()
        if entity.pickup_target is not None:
            targets = engine.get_engine().entity_manager.get_in_area('pickup_zone', rectangle.from_entity(entity))
            for t in targets:
                if t == entity.pickup_target:

                    fare = e.entity_manager.get_by_name('fare')
                    fare.active = True

                    start = Vec2d(entity.pickup_target.x, entity.pickup_target.y)

                    e.remove_entity(entity.pickup_target)
                    entity.pickup_target = None
                    road = list(e.entity_manager.get_by_tag('road'))
                    random.shuffle(road)
                    r = road[0]
                    new_target = engine.get_engine().add_entity('dropoff-zone', x=r.x, y=r.y)
                    entity.dropoff_target = new_target

                    end = Vec2d(new_target.x, new_target.y)

                    d = start.get_distance(end)

                    timer = e.entity_manager.get_by_name('timer')
                    timer.time = timer.time_per_distatnce * d



                    return

        elif entity.dropoff_target is not None:
            targets = engine.get_engine().entity_manager.get_in_area('dropoff_zone', rectangle.from_entity(entity))
            for t in targets:
                if t == entity.dropoff_target:


                    fare = e.entity_manager.get_by_name('fare')
                    fare.active = False
                    timer = e.entity_manager.get_by_name('timer')
                    cash = e.entity_manager.get_by_name('cash')
                    time_left = timer.time

                    earned = fare.fare + time_left * fare.bonus_rate
                    cash.amount += earned

                    timer.time = 0
                    fare.fare =0


                    e.remove_entity(entity.dropoff_target)
                    entity.dropoff_target = None
                    road = list(e.entity_manager.get_by_tag('road'))
                    random.shuffle(road)
                    r = road[0]
                    new_target = engine.get_engine().add_entity('pickup-zone', x=r.x, y=r.y)
                    entity.pickup_target = new_target
                    e.entity_manager.get_by_name('score').score += 1
                    return

            timer = e.entity_manager.get_by_name('timer')
            if timer.time == 0:
                fare = e.entity_manager.get_by_name('fare')
                fare.fare = 0
                fare.active = False
                timer.time = 0
                e.remove_entity(entity.dropoff_target)
                entity.dropoff_target = None
                road = list(e.entity_manager.get_by_tag('road'))
                random.shuffle(road)
                r = road[0]
                new_target = engine.get_engine().add_entity('pickup-zone', x=r.x, y=r.y)
                entity.pickup_target = new_target
                e.entity_manager.get_by_name('dropped').dropped += 1
                return

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

class DroppedComponent(Component):
    def add(self, entity):
        verify_attrs(entity, [('dropped', 0)])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.text = 'Trips Failed: {}'.format(entity.dropped)

class TimerComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['time', 'time_per_distatnce'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.time -= dt
        if entity.time < 0:
            entity.time = 0
        if entity.time > 0:
            entity.text = '{}:{:05.2f}'.format(int(entity.time)/60, entity.time % 60)
        else:
            entity.text = ''

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


class FareComponent(Component):
    def add(self, entity):
        verify_attrs(entity, [('active', False), ('fare', 0), 'rate'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        if entity.active:
            entity.fare += dt*entity.rate
            entity.text = '${:.2f}'.format(entity.fare)
        else:
            entity.text = ''

class Cash(Component):
    def add(self, entity):
        verify_attrs(entity, ['amount'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.text = 'Cash: ${:.2f}'.format(entity.amount)
