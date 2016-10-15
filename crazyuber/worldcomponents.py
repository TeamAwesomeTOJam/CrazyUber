from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d

import Box2D

import math

from awesomeengine import rectangle


class StaticBoxComponent(Component):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'width', 'height')
        self.event_handlers = tuple()

    def add(self, entity):
        Component.add(self, entity)

        world = engine.get_engine().box2d_world

        r = rectangle.Rect(0,0,entity.width, entity.height)

        body = world.CreateStaticBody(position=(entity.x, entity.y), userData={'entity': entity})
        body.CreatePolygonFixture(vertices=r.corners)
        

class SurfaceComponent(Component):

    def __init__(self):
        self.required_attrs = ('x', 'y', 'width', 'height', 'friction')
        self.event_handlers = tuple()
    
    def add(self, entity):
        Component.add(self, entity)
        
        world = engine.get_engine().box2d_world
        r = rectangle.Rect(0, 0, entity.width, entity.height)
        body = world.CreateStaticBody(position=(entity.x, entity.y), allowSleep=True, awake=False, userData={'entity': entity})
        fixture = body.CreatePolygonFixture(vertices=r.corners)
        fixture.sensor = True
        
        
class DrawCornerGraphComponent(Component):

    def __init__(self):
        self.required_attrs = ('x', 'y', ('next_corners', []))
        self.event_handlers = (('draw', self.handle_draw),)

    def handle_draw(self, entity, camera):
        for c in entity.next_corners:
            p = (c.x,c.y)
            camera.draw_line((255,255,255,255), (entity.x, entity.y), p)
            
