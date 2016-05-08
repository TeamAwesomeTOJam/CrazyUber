import random
import awesomeengine
import cornergraph


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


        # for tile in road[:50]:
        #     self.entities.append(e.add_entity('taxi', x= tile.x, y = tile.y, follow=player))
        corners = list(e.entity_manager.get_by_tag('corner'))
        random.shuffle(corners)

        for tile in corners[:25]:
            self.entities.append(e.add_entity('civilian-car', x=tile.x, y=tile.y, ai_mode='roam', next_corner=tile))

        for tile in corners[25:50]:
            self.entities.append(e.add_entity('taxi', x=tile.x, y=tile.y, follow=player))

        player_cam_entity = e.add_entity('player-cam', target=player)
        update_rect = e.add_entity('update-rect',target=player)
        awake_rect = e.add_entity('car-sleeper', target=player)

        e.add_update_layer('always_update')
        e.add_update_layer('update', update_rect)

        score_display = e.add_entity('score-display')
        timer = e.add_entity('timer')

        e.entity_manager.commit_changes()

        cam = e.create_camera(player_cam_entity,
                              layers=[awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255)),
                                      awesomeengine.layer.SimpleCroppedLayer('terrain'),
                                      awesomeengine.layer.SimpleCroppedLayer('building'),
                                      #awesomeengine.layer.PhysicsLayer(),
                                      awesomeengine.layer.SimpleCroppedLayer('draw')],
                              hud=[score_display, timer])
        self.cams = [cam]
        

    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)
