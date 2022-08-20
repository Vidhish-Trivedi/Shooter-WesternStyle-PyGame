import pygame as pg
import settings as st
import sys
from player import Player

# Create Window class.
class GameWindow:
    def __init__(self):
        pg.init()
        
        self.display_surface = pg.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
        pg.display.set_caption("Western Shooter")
        self.clk = pg.time.Clock()

        # Groups.
        self.all_sprites = pg.sprite.Group()

        self.setup()
        

    def setup(self):
        # Instances.
        my_player = Player((200, 200), self.all_sprites, None, None)  # None for now... 

    def runGame(self):
        while(True):
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    pg.quit()
                    print("Game Closed!")
                    sys.exit()
            
            # Delta time.
            self.dt = self.clk.tick(120)/1000

            # BG.
            self.display_surface.fill("black")


            # Update.
            self.all_sprites.update(self.dt)


            # Draw.
            self.all_sprites.draw(self.display_surface)


            pg.display.update()


if(__name__ == "__main__"):
    my_window = GameWindow()
    my_window.runGame()
