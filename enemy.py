import pygame as pg
from entity import Entity


class Coffin(Entity):
    def __init__(self, position, groups, asset_path, coll_sprites):
        super().__init__(position, groups, asset_path, coll_sprites)


class Cactus(Entity):
    def __init__(self, position, groups, asset_path, coll_sprites):
        super().__init__(position, groups, asset_path, coll_sprites)

