import random
import awesomeengine
import cornergraph
from awesomeengine.vec2d import Vec2d


class GameMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get_engine()
        e.add_entities_from_map('map1')

        cornergraph.build_corner_graph()

        road = list(e.entity_manager.get_by_tag('road'))
        random.shuffle(road)

        zone = e.add_entity('pickup-zone', x = road[0].x, y=road[0].y)
        player = e.add_entity('player', pickup_target=zone)


        self.entities =[ player]


        corners = list(e.entity_manager.get_by_tag('corner'))
        # random.shuffle(corners)

        print len(corners)


        only_road = list(e.entity_manager.get_by_tag('road') - e.entity_manager.get_by_tag('corner'))
        random.shuffle(only_road)
        num_taxi = 50
        for tile in only_road[:num_taxi]:
            self.entities.append(e.add_entity('taxi', x=tile.x, y=tile.y, follow=player))

        for tile in corners:

            target = random.choice(tile.next_corners)

            angle = (Vec2d(tile.x, tile.y) - Vec2d(target.x, target.y)).angle

            print 'target', target.x, target.y
            print 'tile', tile.x, tile.y
            print 'tile - target', (Vec2d(tile.x, tile.y) - Vec2d(target.x, target.y))
            print 'angle', angle

            self.entities.append(e.add_entity('civilian-car', angle=angle, x=tile.x, y=tile.y, ai_mode='roam', next_corner=tile))



        player_cam_entity = e.add_entity('player-cam', target=player)
        update_rect = e.add_entity('update-rect',target=player)
        awake_rect = e.add_entity('car-sleeper', target=player)

        e.add_update_layer('always_update')
        e.add_update_layer('update', update_rect)

        score_display = e.add_entity('score-display')
        fare = e.add_entity('fare')
        timer = e.add_entity('timer')
        cash = e.add_entity('cash')
        dropped = e.add_entity('pasangers-dropped')

        e.entity_manager.commit_changes()

        cam = e.create_camera(player_cam_entity,
                              layers=[awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255)),
                                      awesomeengine.layer.SimpleCroppedLayer('terrain'),
                                      awesomeengine.layer.SimpleCroppedLayer('building'),
                                      awesomeengine.layer.SimpleCroppedLayer('draw')],
                              hud=[score_display, timer, fare, cash, dropped])
        self.cams = [cam]

        self.music = e.resource_manager.get('sound', 'music')
        self.music.play(loops=-1)
        self.ambient = e.resource_manager.get('sound', 'ambience')
        self.ambient.play(loops=-1)

    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)
            
        sdl2hl.mixer.ALL_CHANNELS.halt()
