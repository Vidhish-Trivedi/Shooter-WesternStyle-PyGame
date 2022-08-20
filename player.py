import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, position, groups, asset_path, coll_sprites):
        super().__init__(groups)

        self.image = pg.Surface((100, 100))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=position)

        # Float based movement.
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = pg.math.Vector2()   # (0, 0) by default.
        self.speed = 200
        # self.move_dir = 'down'

        # Collisions.
        self.hitbox = self.rect.inflate(0, -self.rect.height/2)
        self.collision_sprites = coll_sprites

    def input(self):
        keys = pg.key.get_pressed()
        
        if(keys[pg.K_LEFT]):
            self.direction.x = -1
            # self.move_dir = 'left'
        elif(keys[pg.K_RIGHT]):
            self.direction.x = 1
            # self.move_dir = 'right'
        else:
            self.direction.x = 0

        if(keys[pg.K_UP]):
            self.direction.y = -1
            # self.move_dir = 'up'
        elif(keys[pg.K_DOWN]):
            self.direction.y = 1
            # self.move_dir = 'down'
        else:
            self.direction.y = 0


    def move_player(self, deltaTime):
        if(self.direction.magnitude() != 0):
            self.direction = self.direction.normalize()

            # Horizontal movement.
            self.pos.x += self.direction.x*self.speed*deltaTime
            self.hitbox.centerx = round(self.pos.x)
            self.rect.centerx = self.hitbox.centerx

            # Vertical movement.
            self.pos.y += self.direction.y*self.speed*deltaTime
            self.hitbox.centery = round(self.pos.y)
            self.rect.centery = self.hitbox.centery

    def update(self, deltaTime):
        self.input()
        self.move_player(deltaTime)
