import sys
import pygame as pg
from entity import Entity

class Player(Entity):
    def __init__(self, position, groups, asset_path, coll_sprites, bullet_create):
        super().__init__(position, groups, asset_path, coll_sprites)

        # Overwrites.
        self.health = 10  # TODO: Set to 5 later.

        self.fire_bullet = bullet_create
        self.bullet_shot = False  # To avoid shooting bullets too fast (too close to one another).
        self.bullet_dir = None

    # For Animations (idle and attacking).
    def set_move_dir(self):
        # Idle player.
        if(self.direction.magnitude() == 0):    
            self.move_dir = self.move_dir.split("_")[0] + "_idle"
        
        # Player is attacking.
        if(self.isAttacking):
            self.move_dir = self.move_dir.split("_")[0] + "_attack"

    def input(self):
        keys = pg.key.get_pressed()
        if(not self.isAttacking):  # Player can move only when not attacking.
            if(keys[pg.K_LEFT]):
                self.direction.x = -1
                self.move_dir = 'left'
            elif(keys[pg.K_RIGHT]):
                self.direction.x = 1
                self.move_dir = 'right'
            else:
                self.direction.x = 0

            if(keys[pg.K_UP]):
                self.direction.y = -1
                self.move_dir = 'up'
            elif(keys[pg.K_DOWN]):
                self.direction.y = 1
                self.move_dir = 'down'
            else:
                self.direction.y = 0

        if(keys[pg.K_SPACE]):
            self.isAttacking = True
            self.bullet_shot = False
            self.direction = pg.math.Vector2()  # Stop motion of player.
            self.frame_index = 0
            # Set bullet direction in accordance with the direction in which player is facing.
            if(self.move_dir.split("_")[0] == "left"):
                self.bullet_dir = pg.math.Vector2(-1, 0)
            elif(self.move_dir.split("_")[0] == "right"):
                self.bullet_dir = pg.math.Vector2(1, 0)
            elif(self.move_dir.split("_")[0] == "up"):
                self.bullet_dir = pg.math.Vector2(0, -1)
            elif(self.move_dir.split("_")[0] == "down"):
                self.bullet_dir = pg.math.Vector2(0, 1)

    def animate(self, deltaTime):
        self.frame_index += 7*deltaTime
        
        if(int(self.frame_index) == 2 and self.isAttacking and not self.bullet_shot):  # Check for shooting animation frame.
            self.bullet_shot = True
            self.bullet_pos = self.rect.center + self.bullet_dir*(80)  # Offset so that bullet does not start from center of the player.
            
            if(self.bullet_dir == pg.math.Vector2(0, -1)):  # Facing up.  (Adjusting bullet).
                self.bullet_pos.x += self.rect.width*(0.2)
            elif(self.bullet_dir == pg.math.Vector2(0, 1)):  # Facin down.  (Adjusting bullet).
                self.bullet_pos.x -= self.rect.width*(0.2)
            
            self.fire_bullet(self.bullet_pos, self.bullet_dir)
            self.blt_fire_sound.play()
            
        if(self.frame_index >= len(self.animations[self.move_dir])):
            self.frame_index = 0

            if(self.isAttacking):
                self.isAttacking = False  # Stop attacking once all animations for attack are done.

        self.image = self.animations[self.move_dir][int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)

    # OverWrite.
    def check_alive(self):
        if(self.health <= 0):
            pg.quit()
            print("Game Over!")
            sys.exit()

    def update(self, deltaTime):
        self.input()
        self.set_move_dir()
        self.move_entity(deltaTime)
        self.animate(deltaTime)
        self.blink()
        self.check_alive()
        self.get_vulnerability()
