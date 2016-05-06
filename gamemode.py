import awesomeengine

class GameMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get_engine()

        player = e.add_entity('player')
        player_cam_entity = e.add_entity('player-cam', target=player)

        self.entities = [player_cam_entity, player]

        cam = e.create_camera(player_cam_entity,
                              layers=[awesomeengine.layer.SolidBackgroundLayer((100, 100, 100, 255)),
                                      awesomeengine.layer.GridLayer((200,200,200,255), 100),
                                      awesomeengine.layer.DepthSortedLayer('draw')],
                              hud=[])

        self.cams = [cam]

    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)