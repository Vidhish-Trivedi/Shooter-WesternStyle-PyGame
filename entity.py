import pygame as pg
from os import walk

# Common parent class for player and monsters.
class Entity(pg.sprite.Sprite):
    def __init__(self, position, groups, asset_path, coll_sprites):
        super().__init__(groups)

        self.import_assets(asset_path)  # Python will call this method from Player() class.
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

        # Health/Damage.
        self.health = 3
        # To avoid multiple calls to damage() in a single attack.
        self.vulnerable = True
        self.hit_time = None

    def damage(self):
        if(self.vulnerable):
            self.health -= 1
            self.vulnerable = False
            self.hit_time = pg.time.get_ticks()

    # Entity would be in-vulnerable for 0.5 seconds after being hit.
    def get_vulnerability(self):
        if(not self.vulnerable):
            if(pg.time.get_ticks() - self.hit_time > 500):
                self.vulnerable = True

    # Methods copied from previously made Player() class.
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


    def move_entity(self, deltaTime):
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

    def check_alive(self):
        if(self.health <= 0):
            self.kill()

