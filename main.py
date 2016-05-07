import awesomeengine
import attractmode
import gamemode
import attractmodecomponents
import cameracomponets
import playercomponents
import carcomponents
import worldcomponents
import aicomponents

def go():
    engine = awesomeengine.Engine('res')
    engine.component_manager.register_module(attractmodecomponents)
    engine.component_manager.register_module(cameracomponets)
    engine.component_manager.register_module(playercomponents)
    engine.component_manager.register_module(carcomponents)
    engine.component_manager.register_module(worldcomponents)
    engine.component_manager.register_module(aicomponents)

    engine.create_box2d_world((0, 0))

    engine.add_mode('attract', attractmode.AttractMode())
    engine.add_mode('game', gamemode.GameMode())

    engine.create_window((1920, 1080), title='CrazyUber')
    engine.change_mode('attract')

    engine.run()

if __name__ == '__main__':

    go()