import random
import awesomeengine


class GameMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get_engine()

        for i in range(-100, 100):
            for j in range(-100, 100):
                if i%8 == 0 or j%8 == 0:
                    e.add_entity('road', x=i*20, y=j*20)
                else:
                    e.add_entity('grass', x=i*20, y=j*20)

        e.entity_manager.commit_changes()        
        
        grass = list(e.entity_manager.get_by_tag('grass'))
        random.shuffle(grass)
        for tile in grass[:1000]:
            print tile
            e.add_entity('building', x=tile.x, y=tile.y)

        player = e.add_entity('player')
        player_cam_entity = e.add_entity('player-cam', target=player)


        self.entities = [player_cam_entity, player]

        for x in range(50):
            self.entities.append(e.add_entity('civilian-car', x = 20*x, y = 20, follow=player))

        e.entity_manager.commit_changes()        
        
        cam = e.create_camera(player_cam_entity,
                              layers=[awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255)),
                                      awesomeengine.layer.SimpleCroppedLayer('terrain'),
                                      awesomeengine.layer.PhysicsLayer(),
                                      awesomeengine.layer.SimpleCroppedLayer('draw')],
                              hud=[])
        self.cams = [cam]
        

    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)
