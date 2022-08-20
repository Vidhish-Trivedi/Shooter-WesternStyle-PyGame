import pygame as pg
import settings as st
import sys
from player import Player
from sprite import MySprite
from pytmx.util_pygame import load_pygame  # Module to import Tiled level editor data, to create sprites later.

# AllSprites() class.
class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        
        self.offset = pg.math.Vector2()
        self.display_surface = pg.display.get_surface()
        self.background = pg.image.load('./graphics/other/background.png').convert()
    
    # Set up camera view.
    def custom_draw(self, player):
        # Change offset vector.
        self.offset.x = player.rect.centerx - st.WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - st.WINDOW_HEIGHT/2

        # blit. (For background offset)
        self.display_surface.blit(self.background, -self.offset)
        
        # Offset all sprites (objects).  Sorted() to get overlapping effect.
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)


# Create Window class.
class GameWindow:
    def __init__(self):
        pg.init()
        
        self.display_surface = pg.display.set_mode((st.WINDOW_WIDTH, st.WINDOW_HEIGHT))
        pg.display.set_caption("Western Shooter")
        self.clk = pg.time.Clock()

        # Groups.
        self.all_sprites = AllSprites()

        self.setup()
        

    def setup(self):
        # Importing Tiled data.
        tmx_map = load_pygame('./data/map.tmx')
        
        # Fence.
        for (x, y, surf) in tmx_map.get_layer_by_name('Fence').tiles():
            new_sprite = MySprite((x*64, y*64), surf, self.all_sprites)  # (x, y) --> grid cell in Tiled.

        # Objects.
        for obj in tmx_map.get_layer_by_name('Object'):
            # obj.x    obj.y    obj.image (surface)    obj.name   obj.type (class)
            new_sprite = MySprite((obj.x, obj.y), obj.image, self.all_sprites)
        
        # Entities.
        for obj in tmx_map.get_layer_by_name('Entities'):
            if(obj.name == "Player"):
                self.my_player = Player((obj.x, obj.y), self.all_sprites, st.PATHS['player'], None)  # None for now... 


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
            self.all_sprites.custom_draw(self.my_player)


            pg.display.update()


if(__name__ == "__main__"):
    my_window = GameWindow()
    my_window.runGame()
