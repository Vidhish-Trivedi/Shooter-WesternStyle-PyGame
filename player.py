import pygame as pg
from os import walk

class Player(pg.sprite.Sprite):
    def __init__(self, position, groups, asset_path, coll_sprites):
        super().__init__(groups)

        self.import_assets(asset_path)
        self.frame_index = 0
        self.move_dir = 'down_idle'

        self.image = self.animations[self.move_dir][self.frame_index]

        self.rect = self.image.get_rect(center=position)

        # Float based movement.
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2()   # (0, 0) by default.
        self.speed = 200
        

        # Collisions.
        self.hitbox = self.rect.inflate(-self.rect.width/2, -self.rect.height/2)
        self.collision_sprites = coll_sprites

        # Attack.
        self.isAttacking = False

    def import_assets(self, asset_path):
        self.animations = {}  # (k, v): k --> animation 'state', v --> animation frames (list).

        for (index, folder) in enumerate(walk(asset_path)):
            if(index == 0):
                for subfolder in folder[1]:
                    self.animations[subfolder] = []

            else:
                for img in sorted(folder[2], key=lambda string: int(string.split(".")[0])):  # To resolve os.walk() order: [0, 1, 10, 11, 2, 3, ....] is returned by os.walk()
                    subfolder = folder[0].split("\\")[::-1][0]
                    img_path = asset_path + "/" + subfolder + "/" + img
                    surf = pg.image.load(img_path).convert_alpha()
                    self.animations[subfolder].append(surf)
        
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
            self.direction = pg.math.Vector2()  # Stop motion of player.
            self.frame_index = 0


    def move_player(self, deltaTime):
        if(self.direction.magnitude() != 0):
            self.direction = self.direction.normalize()

        # Horizontal movement.
        self.pos.x += self.direction.x*self.speed*deltaTime
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # Vertical movement.
        self.pos.y += self.direction.y*self.speed*deltaTime
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")


    def animate(self, deltaTime):
        self.frame_index += 7*deltaTime
        
        if(self.frame_index >= len(self.animations[self.move_dir])):
            self.frame_index = 0

            if(self.isAttacking):
                self.isAttacking = False  # Stop attacking once all animations for attack are done.

        self.image = self.animations[self.move_dir][int(self.frame_index)]

    # Collisions.
    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if(direction == "horizontal"):
                if(sprite.hitbox.colliderect(self.hitbox)):
                    if(self.direction.x > 0):  # Collision on left side.
                        self.hitbox.right = sprite.hitbox.left

                    if(self.direction.x < 0):  # Collision on right side.
                        self.hitbox.left = sprite.hitbox.right
                    
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
        
            else:  # Direction is vertical.
                if(sprite.hitbox.colliderect(self.hitbox)):
                    if(self.direction.y > 0):  # Collision on top side.
                        self.hitbox.bottom = sprite.hitbox.top

                    if(self.direction.y < 0):  # Collision on bottom side.
                        self.hitbox.top = sprite.hitbox.bottom
                    
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery


    def update(self, deltaTime):
        self.input()
        self.set_move_dir()
        self.move_player(deltaTime)
        self.animate(deltaTime)
