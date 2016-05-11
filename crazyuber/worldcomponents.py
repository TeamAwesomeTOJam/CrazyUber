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

        r = rectangle.Rect(0,0,entity.width, entity.height)

        body = world.CreateStaticBody(position=(entity.x, entity.y), userData={'entity': entity})
        body.CreatePolygonFixture(vertices=r.corners)

    def remove(self, entity):
        pass
        

class SurfaceComponent(Component):
    
    def add(self, entity):
        verify_attrs(entity, ['x', 'y', 'width', 'height', 'friction'])
        
        world = engine.get_engine().box2d_world
        r = rectangle.Rect(0, 0, entity.width, entity.height)
        body = world.CreateStaticBody(position=(entity.x, entity.y), allowSleep=True, awake=False, userData={'entity': entity})
        fixture = body.CreatePolygonFixture(vertices=r.corners)
        fixture.sensor = True
        
    def remove(self, entity):
        pass
        
        
class DrawCornerGraphComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['x', 'y', ('next_corners', [])])

        entity.register_handler('draw', self.handle_draw)

    def remove(self, entity):
        entity.unregister_handler('draw', self.handle_draw)

    def handle_draw(self, entity, camera):
        for c in entity.next_corners:
            p = (c.x,c.y)
            camera.draw_line((255,255,255,255), (entity.x, entity.y), p)