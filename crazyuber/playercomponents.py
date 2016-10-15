from awesomeengine.component import Component
from awesomeengine import engine


class InputVelocityComponent(Component):

    def __init__(self):
        self.required_attrs = (('vx', 0), ('vy', 0))
        self.event_handlers = (('input', self.handle_input),)

    def handle_input(self, entity, action, value):
        if action == 'up' and value == 1:
            entity.vy = 100
        elif action == 'down' and value == 1:
            entity.vy = -100
        elif (action == 'up' or action == 'down') and value == 0:
            entity.vy = 0
        if action == 'left' and value == 1:
            entity.vx = -100
        elif action == 'right' and value == 1:
            entity.vx = 100
        elif (action == 'left' or action == 'right') and value == 0:
            entity.vx = 0
