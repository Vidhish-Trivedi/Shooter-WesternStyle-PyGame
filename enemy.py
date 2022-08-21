import pygame as pg
from entity import Entity

# Class for shared methods and attributes between monsters.
class Enemy:
    def get_player_dist_dir(self):
        enemy_pos = pg.math.Vector2(self.rect.center)
        player_pos = pg.math.Vector2(self.player.rect.center)

        dist = (player_pos - enemy_pos).magnitude()
        if(dist != 0):
            dir = (player_pos - enemy_pos).normalize()  # magnitude = 1.
        else:
            dir = pg.math.Vector2(0, 0)

        return (dist, dir)
            
    def face_player(self):
        dist, dir = self.get_player_dist_dir()
        if(dist < self.detect_radius):
            if(dir.y > -0.5  and dir.y < 0.5):  # Detect whether player is above or below AND on left or right side.
                if(dir.x < 0):  # Player is on left side.
                    self.move_dir = "left_idle"
                elif(dir.x > 0):  # Player is on right side.
                    self.move_dir = "right_idle"

            else:
                if(dir.y < 0):  # Player is on top side.
                    self.move_dir = "up_idle"
                elif(dir.y > 0):  # Player is on bottom side.
                    self.move_dir = "down_idle"

    def walk_to_player(self):
        dist, dir = self.get_player_dist_dir()
        if(dist < self.move_to_player_radius and dist > self.attack_radius):
            self.direction = dir  # Overwrite self.direction inside Entity() class.
            self.move_dir = self.move_dir.split("_")[0]
        
        else:
            self.direction = pg.math.Vector2()  # Stop enemy motion.

class Coffin(Entity, Enemy):
    def __init__(self, position, groups, asset_path, coll_sprites, player_par,):
        super().__init__(position, groups, asset_path, coll_sprites)
        
        # Overwrites.
        self.speed = 150

        # Player interactivity.
        self.player = player_par
        self.detect_radius = 550
        self.move_to_player_radius = 400
        self.attack_radius = 50

    def attack(self):
        dist = self.get_player_dist_dir()[0]
        if(dist < self.attack_radius and not self.isAttacking):
            self.isAttacking = True
            self.frame_index = 0

        if(self.isAttacking):
            self.move_dir = self.move_dir.split("_")[0] + "_attack"

    def animate(self, deltaTime):
        self.frame_index += 7*deltaTime

        if(int(self.frame_index) == 4 and self.isAttacking):
            if(self.get_player_dist_dir()[0] < self.attack_radius):
                self.player.damage()

        if(self.frame_index >= len(self.animations[self.move_dir])):
            self.frame_index = 0
            if(self.isAttacking):
                self.isAttacking = False

        self.image = self.animations[self.move_dir][int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)

    def update(self, deltaTime):
        self.face_player()
        self.walk_to_player()
        self.attack()
        self.move_entity(deltaTime)
        self.animate(deltaTime)
        self.blink()
        self.check_alive()
        self.get_vulnerability()

class Cactus(Entity, Enemy):
    def __init__(self, position, groups, asset_path, coll_sprites, player_par, bullet_create):
        super().__init__(position, groups, asset_path, coll_sprites)

        # Overwrites.
        self.speed = 90
        
        # Player interactivity.
        self.player = player_par
        self.detect_radius = 600
        self.move_to_player_radius = 500
        self.attack_radius = 350

        # Bullets.
        self.fire_bullet = bullet_create
        self.bullet_shot = False
        self.bullet_dir = None

    def attack(self):
        dist = self.get_player_dist_dir()[0]
        if(dist < self.attack_radius and not self.isAttacking):
            self.isAttacking = True
            self.frame_index = 0
            self.bullet_shot = False

        if(self.isAttacking):
            self.move_dir = self.move_dir.split("_")[0] + "_attack"

    def animate(self, deltaTime):
        self.frame_index += 7*deltaTime

        if(int(self.frame_index) == 6 and self.isAttacking and not self.bullet_shot):
            
            self.bullet_dir = self.get_player_dist_dir()[1]
            
            self.bullet_pos = self.rect.center + self.bullet_dir*(150)  # Offset so that bullet does not start from center of the player.
            
            if(self.bullet_dir == pg.math.Vector2(0, -1)):  # Facing up.  (Adjusting bullet).
                self.bullet_pos.x += self.rect.width*(0.2)
            elif(self.bullet_dir == pg.math.Vector2(0, 1)):  # Facin down.  (Adjusting bullet).
                self.bullet_pos.x -= self.rect.width*(0.2)

            self.fire_bullet(self.bullet_pos, self.bullet_dir)
            self.bullet_shot = True

        if(self.frame_index >= len(self.animations[self.move_dir])):
            self.frame_index = 0
            if(self.isAttacking):
                self.isAttacking = False

        self.image = self.animations[self.move_dir][int(self.frame_index)]
        self.mask = pg.mask.from_surface(self.image)

    def update(self, deltaTime):
        self.face_player()
        self.walk_to_player()
        self.attack()
        self.move_entity(deltaTime)
        self.animate(deltaTime)
        self.blink()
        self.check_alive()
        self.get_vulnerability()
