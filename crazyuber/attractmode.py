import awesomeengine

class AttractMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get_engine()

        welcome_cam_entity = e.add_entity('attract-cam')
        # welcom_text = e.add_entity('attract-text')
        manager = e.add_entity('attract-manager')
        image = e.add_entity('title-image')

        self.entities = [welcome_cam_entity, image, manager]

        cam = e.create_camera(welcome_cam_entity, layers=[awesomeengine.layer.SolidBackgroundLayer((100,100,100,255)),
                                                          awesomeengine.layer.SimpleLayer('draw')],)

        self.cams = [cam]


    def leave(self):
        e = awesomeengine.get_engine()
        for cam in self.cams:
            e.remove_camera(cam)
        for ent in self.entities:
            e.remove_entity(ent)
