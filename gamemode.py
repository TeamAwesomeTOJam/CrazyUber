import awesomeengine

class GameMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get_engine()

        building = e.add_entity('building')

        player = e.add_entity('player')
        player_cam_entity = e.add_entity('player-cam', target=player)


        self.entities = [player_cam_entity, player, building]

        for x in range(50):
            self.entities.append(e.add_entity('civilian-car', x = 20*x, y = 20, follow=player))

        cam = e.create_camera(player_cam_entity,
                              layers=[awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255)),
                                      awesomeengine.layer.GridLayer((200,200,200,255), 100),
                                      awesomeengine.layer.PhysicsLayer(),
                                      awesomeengine.layer.DepthSortedLayer('draw')],
                              hud=[])

        self.cams = [cam]

    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)