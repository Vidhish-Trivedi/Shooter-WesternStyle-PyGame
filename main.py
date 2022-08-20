import pygame as pg
import settings as st
import sys
from player import Player
from sprite import MySprite, Bullet
from enemy import Cactus, Coffin
from pytmx.util_pygame import load_pygame

class AllSprites(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        
        self.offset = pg.math.Vector2()
        self.display_surface = pg.display.get_surface()
        self.background = pg.image.load('./graphics/other/background.png').convert()
    
    # Set up camera view.
    def custom_draw(self, player):
        
        self.offset.x = player.rect.centerx - st.WINDOW_WIDTH/2
        self.offset.y = player.rect.centery - st.WINDOW_HEIGHT/2

        self.display_surface.blit(self.background, -self.offset)
        
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

        self.bullet_surf = pg.image.load('./graphics/other/particle.png').convert_alpha()
        self.clk = pg.time.Clock()

        # Groups.
        self.all_sprites = AllSprites()
        self.obstacles = pg.sprite.Group()
        self.bullets_grp = pg.sprite.Group()

        self.setup()
        
    def create_bullet(self, position, dir):
        my_bullet = Bullet(position, dir, self.bullet_surf, [self.all_sprites, self.bullets_grp])

    def setup(self):
        # Importing Tiled data.
        tmx_map = load_pygame('./data/map.tmx')
        
        # Fence.
        for (x, y, surf) in tmx_map.get_layer_by_name('Fence').tiles():
            new_sprite = MySprite((x*64, y*64), surf, [self.all_sprites, self.obstacles])  # (x, y) --> grid cell in Tiled.

        # Objects.
        for obj in tmx_map.get_layer_by_name('Object'):
            new_sprite = MySprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])
        
        # Entities.
        for obj in tmx_map.get_layer_by_name('Entities'):
            if(obj.name == "Player"):
                self.my_player = Player(position=(obj.x, obj.y),
                                        groups=self.all_sprites,
                                        asset_path=st.PATHS['player'],
                                        coll_sprites=self.obstacles,
                                        bullet_create=self.create_bullet)

            elif(obj.name == "Coffin"):
                coffin = Coffin(position=(obj.x, obj.y),
                                groups=[self.all_sprites],
                                asset_path=st.PATHS['coffin'],
                                coll_sprites=self.obstacles,
                                player_par=self.my_player)
            
            elif(obj.name == "Cactus"):
                cactus = Cactus(position=(obj.x, obj.y),
                                groups=[self.all_sprites],
                                asset_path=st.PATHS['cactus'],
                                coll_sprites=self.obstacles,
                                player_par=self.my_player)


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
