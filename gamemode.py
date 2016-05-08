import random
import awesomeengine


class GameMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get_engine()
        e.add_entities_from_map('map1')
        
        grass = list(e.entity_manager.get_by_tag('grass'))
        random.shuffle(grass)
        for tile in grass[:10000]:
            e.add_entity('building', x=tile.x, y=tile.y)


        road = list(e.entity_manager.get_by_tag('road'))
        random.shuffle(road)

        zone = e.add_entity('pickup-zone', x = road[0].x, y=road[0].y)
        player = e.add_entity('player', pickup_target=zone)
        player_cam_entity = e.add_entity('player-cam', target=player)


        self.entities = [player_cam_entity, player]


        for tile in road[:50]:
            self.entities.append(e.add_entity('taxi', x= tile.x, y = tile.y, follow=player))
        # for y in range(50):
        #     self.entities.append(e.add_entity('civilian-car', x=player.x-20-20*y, y=player.y, follow=player))

        score_display = e.add_entity('score-display')


        e.entity_manager.commit_changes()


        cam = e.create_camera(player_cam_entity,
                              layers=[awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255)),
                                      awesomeengine.layer.SimpleCroppedLayer('terrain'),
                                      awesomeengine.layer.SimpleCroppedLayer('building'),
                                      # awesomeengine.layer.PhysicsLayer(),
                                      awesomeengine.layer.SimpleCroppedLayer('draw')],
                              hud=[score_display])
        self.cams = [cam]
        

    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)
