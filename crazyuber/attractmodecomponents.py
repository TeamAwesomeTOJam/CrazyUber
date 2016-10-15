from awesomeengine.component import verify_attrs
from awesomeengine.component import Component
from awesomeengine import engine


class NextModeComponent(Component):

    def __init__(self):
        self.required_attrs = tuple()
        self.event_handlers = (('input', self.handle_input),)

    def handle_input(self, entity, action, value):
        if action == "play" and value == 1:
            engine.get_engine().change_mode('game')
