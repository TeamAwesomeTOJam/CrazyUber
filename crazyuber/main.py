import awesomeengine
import attractmode
import gamemode
import attractmodecomponents
import cameracomponets
import playercomponents
import carcomponents
import worldcomponents
import aicomponents
import gamecomponents

def go():
    engine = awesomeengine.Engine('res')
    engine.component_manager.register_module(attractmodecomponents)
    engine.component_manager.register_module(cameracomponets)
    engine.component_manager.register_module(playercomponents)
    engine.component_manager.register_module(carcomponents)
    engine.component_manager.register_module(worldcomponents)
    engine.component_manager.register_module(aicomponents)
    engine.component_manager.register_module(gamecomponents)

    engine.create_box2d_world((0, 0))

    engine.add_mode('attract', attractmode.AttractMode())
    engine.add_mode('game', gamemode.GameMode())

    engine.create_window(title='CrazyUber')
    engine.change_mode('attract')

    engine.window.set_fullscreen(True)

    engine.run()

if __name__ == '__main__':

    go()
