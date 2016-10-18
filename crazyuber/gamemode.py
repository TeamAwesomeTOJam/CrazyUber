import random

import Box2D
import awesomeengine
from awesomeengine.vec2d import Vec2d
from awesomeengine import rectangle
import sdl2hl

import cornergraph



class GameMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get()
        self._create_box2d_world(e)
        e.add_entities_from_map('map1')

        cornergraph.build_corner_graph()

        road = list(e.entity_manager.get_by_tag('road'))
        random.shuffle(road)

        zone = e.add_entity('pickup-zone', x = road[0].x, y=road[0].y)
        player = e.add_entity('player', pickup_target=zone)

        self.entities =[player]

        corners = list(e.entity_manager.get_by_tag('corner'))
        # random.shuffle(corners)

        print len(corners)

        only_road = list(e.entity_manager.get_by_tag('road') - e.entity_manager.get_by_tag('corner'))
        random.shuffle(only_road)
        num_taxi = 65
        for tile in only_road[:num_taxi]:
            self.entities.append(e.add_entity('taxi', x=tile.x, y=tile.y, follow=player))

        for tile in corners:

            target = random.choice(tile.next_corners)

            angle = (Vec2d(target.x, target.y) - Vec2d(tile.x, tile.y)).angle

            self.entities.append(e.add_entity('civilian-car', angle=angle, x=tile.x, y=tile.y, ai_mode='roam', next_corner=target))


        player_cam_entity = e.add_entity('player-cam', target=player)
        update_rect = e.add_entity('update-rect',target=player, name='update-rect')
        awake_rect = e.add_entity('car-sleeper', target=player)

        score_display = e.add_entity('score-display')
        fare = e.add_entity('fare')
        timer = e.add_entity('timer')
        cash = e.add_entity('cash')
        dropped = e.add_entity('pasangers-dropped')

        e.entity_manager.commit_changes()


        cam = awesomeengine.Camera(e.renderer, player_cam_entity,
            layers=[awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255)),
                  awesomeengine.layer.SimpleCroppedLayer('terrain'),
                  awesomeengine.layer.SimpleCroppedLayer('building'),
                  awesomeengine.layer.SimpleCroppedLayer('draw')],
            hud=[score_display, timer, fare, cash, dropped])

        self.cameras = [cam]

        self.music = e.resource_manager.get('sound', 'music')
        self.music.play(loops=-1)
        self.ambient = e.resource_manager.get('sound', 'ambience')
        self.ambient.play(loops=-1)

    def leave(self):
        e = awesomeengine.get()

        for ent in self.entities:
            e.remove_entity(ent)

        sdl2hl.mixer.ALL_CHANNELS.halt()

    def handle_event(self, event):
        if awesomeengine.get().entity_manager.has_by_name(event.target):
            awesomeengine.get().entity_manager.get_by_name(event.target).handle('input', event.action, event.value)

    def update(self, dt):
        engine = awesomeengine.get()

        for e in engine.entity_manager.get_by_tag('always_update'):
            e.handle('update', dt)

        r = rectangle.from_entity(engine.entity_manager.get_by_name('update-rect'))
        for e in engine.entity_manager.get_in_area('update', r):
            e.handle('update', dt)

        velocity_iters = 6
        position_iters = 2
        engine.box2d_world.Step(dt, velocity_iters, position_iters)
        engine.box2d_world.ClearForces()

    def draw(self):
        for c in self.cameras:
            c.render()

    def _create_box2d_world(self, engine):
        class ContactListener(Box2D.b2ContactListener):
            def __init__(self):
                Box2D.b2ContactListener.__init__(self)
            def BeginContact(self, contact):
                if 'entity' in contact.fixtureA.body.userData:
                    contact.fixtureA.body.userData['entity'].handle('contact', contact.fixtureB.body.userData.get('entity', None), True)
                if 'entity' in contact.fixtureB.body.userData:
                    contact.fixtureB.body.userData['entity'].handle('contact', contact.fixtureA.body.userData.get('entity', None), False)
            def EndContact(self, contact):
                pass
            def PreSolve(self, contact, oldManifold):
                pass
            def PostSolve(self, contact, impulse):
                pass

        engine.box2d_world = Box2D.b2World(gravity=(0,0), doSleep=True, contactListener=ContactListener())
