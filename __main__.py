from game_manager import GameManager
from levels.pixel_run import PixelRun
from levels.battle import Battle

if __name__ == "__main__":
    gm = GameManager()
    
    gm.add_level(PixelRun(gm.surface))
    gm.add_level(Battle(gm.surface))
        
    gm.main()
