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

        player = e.add_entity('player')
        player_cam_entity = e.add_entity('player-cam', target=player)


        self.entities = [player_cam_entity, player]

        # road = list(e.entity_manager.get_by_tag('road'))
        # random.shuffle(road)
        # for tile in road[:50]:
        for y in range(50):
            self.entities.append(e.add_entity('civilian-car', x=0, y=-20-20*y, follow=player))


        e.entity_manager.commit_changes()

        cam = e.create_camera(player_cam_entity,
                              layers=[awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255)),
                                      awesomeengine.layer.SimpleCroppedLayer('terrain'),
                                      awesomeengine.layer.SimpleCroppedLayer('building'),
                                      # awesomeengine.layer.PhysicsLayer(),
                                      awesomeengine.layer.SimpleCroppedLayer('draw')],
                              hud=[])
        self.cams = [cam]
        

    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)
