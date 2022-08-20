import pygame as pg

class MySprite(pg.sprite.Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -self.rect.height/3)  # For collisions.
