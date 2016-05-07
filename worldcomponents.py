from awesomeengine.component import verify_attrs
from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d

import Box2D

import math

from awesomeengine import rectangle

class StaticBoxComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height'])

        world = engine.get_engine().box2d_world

        r = rectangle.from_entity(entity)

        body = world.CreateStaticBody(position = r.center)
        body.CreatePolygonFixture(vertices=r.corners)

    def remove(self, entity):
        pass
