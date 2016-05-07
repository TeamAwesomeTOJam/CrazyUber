from awesomeengine.component import verify_attrs
from awesomeengine.component import Component
from awesomeengine import engine
from awesomeengine.vec2d import Vec2d
from awesomeengine import rectangle


class GoToPointComponent(Component):

    def add(self, entity):
        verify_attrs(entity, ['target', 'max_forward_speed'])

        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        pos = Vec2d(entity.box2d_car.body.GetWorldPoint((0, 0)))
        facing = Vec2d(entity.box2d_car.body.GetWorldVector((0, 1)))
        target = Vec2d(entity.target)

        pos_to_target = target - pos

        angle = facing.get_angle_between(pos_to_target)

        entity.steering_angle = angle

        entity.desired_speed = entity.max_forward_speed

class FollowCarCompoent(Component):
    def add(self, entity):
        verify_attrs(entity, ['follow'])
        entity.register_handler('update', self.handle_update)

    def remove(self, entity):
        entity.unregister_handler('update', self.handle_update)

    def handle_update(self, entity, dt):
        entity.target = (entity.follow.x, entity.follow.y)

