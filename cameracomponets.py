from awesomeengine.component import verify_attrs
from awesomeengine.component import Component
from awesomeengine import engine


class FollowComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['angle', 'x', 'y', 'target'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.x = entity.target.x
        entity.y = entity.target.y
        # entity.angle = entity.target.angle - 90
