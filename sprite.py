import pygame as pg

class MySprite(pg.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -self.rect.height/3)  # For collisions.

class Bullet(pg.sprite.Sprite):
    def __init__(self, position, dir, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(center=position)

        # Float based movement.
        self.pos = pg.math.Vector2(self.rect.center)
        self.direction = dir
        self.speed = 400

    def update(self, deltaTime):
        self.pos += self.direction*self.speed*deltaTime
        self.rect.center = (round(self.pos.x), round(self.pos.y))
