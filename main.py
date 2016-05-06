import awesomeengine
import attractmode
import gamemode
import attractmodecomponents
import cameracomponets
import playercomponents
import carcomponents

if __name__ == '__main__':

    engine = awesomeengine.Engine('res')
    engine.component_manager.register_module(attractmodecomponents)
    engine.component_manager.register_module(cameracomponets)
    engine.component_manager.register_module(playercomponents)
    engine.component_manager.register_module(carcomponents)

    engine.add_mode('attract', attractmode.AttractMode())
    engine.add_mode('game', gamemode.GameMode())

    engine.create_window((1920, 1080),title='CrazyUber')
    engine.change_mode('attract')

    engine.run()