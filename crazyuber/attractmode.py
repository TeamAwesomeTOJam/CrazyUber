import awesomeengine


class AttractMode(awesomeengine.mode.Mode):

    def enter(self):
        e = awesomeengine.get()

        welcome_cam_entity = e.add_entity('attract-cam')
        image = e.add_entity('title-image')

        self.entities = [welcome_cam_entity, image]

        camera = awesomeengine.Camera(
            e.renderer,
            welcome_cam_entity,
            layers=[awesomeengine.layer.SolidBackgroundLayer((100,100,100,255)), awesomeengine.layer.SimpleLayer('draw')])

        self.cameras = [camera]

    def leave(self):
        e = awesomeengine.get()

        for ent in self.entities:
            e.remove_entity(ent)

    def handle_event(self, event):
        if event.target == 'GAME':
            if event.action == 'play':
                awesomeengine.get().change_mode('game')

    def update(self, dt):
        pass

    def draw(self):
        for c in self.cameras:
            c.render()
