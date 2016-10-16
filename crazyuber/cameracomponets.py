from awesomeengine.component import Component
from awesomeengine import engine


class FollowComponent(Component):

    def __init__(self):
        self.required_attrs = ('angle', 'x', 'y', 'target')
        self.event_handlers = (('update', self.handle_update),)

    def handle_update(self, entity, dt):
        entity.x = entity.target.x
        entity.y = entity.target.y
        # entity.angle = entity.target.angle - 90
        engine.get().entity_manager.update_position(entity)
